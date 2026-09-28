from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from .ratios import normalized_ratio, rank_targets


@dataclass(frozen=True)
class ROI:
    x0: float
    y0: float
    x1: float
    y1: float

    def pixels(self, width: int, height: int) -> tuple[int, int, int, int]:
        return (
            int(self.x0 * width), int(self.y0 * height),
            int(self.x1 * width), int(self.y1 * height),
        )


def _background_normalize(gray: np.ndarray) -> np.ndarray:
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))
    background = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    return cv2.divide(gray, background, scale=255)


def _deskew(binary: np.ndarray) -> tuple[np.ndarray, float]:
    edges = cv2.Canny(binary, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 1800, threshold=max(100, binary.shape[1] // 5))
    if lines is None:
        return binary, 0.0
    deviations = []
    for rho_theta in lines[:100]:
        theta = float(rho_theta[0][1])
        degrees = np.degrees(theta)
        nearest = min((0, 90, 180), key=lambda axis: abs(degrees - axis))
        deviation = degrees - nearest
        if abs(deviation) <= 3:
            deviations.append(deviation)
    if not deviations:
        return binary, 0.0
    angle = float(np.median(deviations))
    center = (binary.shape[1] / 2, binary.shape[0] / 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(binary, matrix, (binary.shape[1], binary.shape[0]), borderValue=255)
    return rotated, angle


def _line_segments(binary: np.ndarray) -> list[dict]:
    ink = 255 - binary
    edges = cv2.Canny(ink, 50, 150)
    threshold = max(45, min(binary.shape[:2]) // 18)
    min_length = max(35, min(binary.shape[:2]) // 16)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 720, threshold=threshold,
                            minLineLength=min_length, maxLineGap=12)
    result = []
    if lines is None:
        return result
    # OpenCV 4 commonly returns (N, 1, 4); OpenCV 5 may return (N, 4).
    # Reshaping keeps the analysis stable across both representations.
    for raw in np.asarray(lines).reshape(-1, 4):
        x1, y1, x2, y2 = map(int, raw)
        dx, dy = x2 - x1, y2 - y1
        length = float(np.hypot(dx, dy))
        angle = float(np.degrees(np.arctan2(dy, dx)))
        orientation = "horizontal" if min(abs(angle), abs(abs(angle) - 180)) <= 3 else (
            "vertical" if abs(abs(angle) - 90) <= 3 else "diagonal"
        )
        result.append({
            "x1": x1, "y1": y1, "x2": x2, "y2": y2,
            "length": length, "angle_degrees": angle, "orientation": orientation,
        })
    return sorted(result, key=lambda line: line["length"], reverse=True)


def _ink_bbox(binary: np.ndarray) -> tuple[int, int, int, int] | None:
    ink = 255 - binary
    count, _, stats, _ = cv2.connectedComponentsWithStats((ink > 0).astype(np.uint8), 8)
    candidates = []
    for index in range(1, count):
        x, y, w, h, area = map(int, stats[index])
        if area >= max(40, binary.size * 0.00002):
            candidates.append((x, y, w, h, area))
    if not candidates:
        return None
    x0 = min(item[0] for item in candidates)
    y0 = min(item[1] for item in candidates)
    x1 = max(item[0] + item[2] for item in candidates)
    y1 = max(item[1] + item[3] for item in candidates)
    return x0, y0, x1 - x0, y1 - y0


def _symmetry_score(binary: np.ndarray, axis: str) -> float:
    ink = (binary < 128).astype(np.uint8)
    # Historical strokes seldom land on identical pixels after printing, scanning
    # and deskewing. A small, fixed tolerance makes this a stroke-overlap measure
    # rather than an unrealistically exact pixel-identity test.
    ink = cv2.dilate(ink, np.ones((5, 5), np.uint8), iterations=1).astype(np.float32)
    flipped = np.fliplr(ink) if axis == "vertical" else np.flipud(ink)
    union = np.maximum(ink, flipped).sum()
    if union == 0:
        return 0.0
    overlap = np.minimum(ink, flipped).sum()
    return float(overlap / union)


def analyze_drawing(spec: dict, root: str | Path, output_dir: str | Path,
                    tolerance_percent: float = 4.0) -> Path:
    root = Path(root)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    image_path = root / spec["image_path"]
    color = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if color is None:
        raise FileNotFoundError(image_path)
    gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
    normalized = _background_normalize(gray)
    _, binary = cv2.threshold(normalized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    binary, skew = _deskew(binary)

    height, width = binary.shape
    roi = ROI(**spec["roi"])
    x0, y0, x1, y1 = roi.pixels(width, height)
    crop = binary[y0:y1, x0:x1]
    lines = _line_segments(crop)
    bbox = _ink_bbox(crop)
    measurements: list[dict] = []

    if bbox:
        bx, by, bw, bh = bbox
        measured = normalized_ratio(bw, bh)
        measurements.append({
            "region_id": f"{spec['drawing_id']}-roi-main",
            "measurement_method": "ink_component_extent",
            "reference_line": "outer extent of retained connected ink components",
            "quantity": "width_height_ratio",
            "raw_value": measured,
            "measured_ratio": measured,
            "endpoints": {"x": bx, "y": by, "width": bw, "height": bh},
            "ratio_hypotheses": rank_targets(measured)[:4],
            "confidence": 0.45,
            "human_review_required": True,
            "notes": "Page furniture and labels may influence this extent; it is not an architectural clear dimension.",
        })

    horizontal = [line for line in lines if line["orientation"] == "horizontal"][:12]
    vertical = [line for line in lines if line["orientation"] == "vertical"][:12]
    if horizontal and vertical:
        h_med = float(np.median([line["length"] for line in horizontal]))
        v_med = float(np.median([line["length"] for line in vertical]))
        measured = normalized_ratio(h_med, v_med)
        measurements.append({
            "region_id": f"{spec['drawing_id']}-roi-main",
            "measurement_method": "dominant_line_median",
            "reference_line": "median of 12 longest near-horizontal versus near-vertical segments",
            "quantity": "line_span_ratio",
            "raw_value": measured,
            "measured_ratio": measured,
            "endpoints": {"horizontal_median_px": h_med, "vertical_median_px": v_med},
            "ratio_hypotheses": rank_targets(measured)[:4],
            "confidence": 0.35,
            "human_review_required": True,
            "notes": "Exploratory segmentation statistic, not yet a room or bay measurement.",
        })

    for axis in ("vertical", "horizontal"):
        measurements.append({
            "region_id": f"{spec['drawing_id']}-roi-main",
            "measurement_method": "binary_reflection_overlap",
            "reference_line": f"geometric centre, {axis} reflection axis",
            "quantity": f"{axis}_symmetry_iou",
            "raw_value": _symmetry_score(crop, axis),
            "confidence": 0.55,
            "human_review_required": True,
            "notes": "Sensitive to labels, stains, cropping and line loss; useful for comparison, not attribution.",
        })

    overlay = color.copy()
    cv2.rectangle(overlay, (x0, y0), (x1, y1), (20, 150, 20), 4)
    for line in lines[:80]:
        color_value = (20, 20, 220) if line["orientation"] == "horizontal" else (
            (220, 80, 20) if line["orientation"] == "vertical" else (160, 30, 160)
        )
        cv2.line(overlay, (x0 + line["x1"], y0 + line["y1"]),
                 (x0 + line["x2"], y0 + line["y2"]), color_value, 2)
    overlay_path = output_dir / f"{spec['drawing_id']}_overlay.png"
    cv2.imwrite(str(overlay_path), overlay)
    binary_path = output_dir / f"{spec['drawing_id']}_binary.png"
    cv2.imwrite(str(binary_path), crop)

    result = {
        "drawing_id": spec["drawing_id"],
        "algorithm": "deterministic_opencv_pilot",
        "algorithm_version": "0.1.0",
        "tolerance_percent": tolerance_percent,
        "source_image": str(image_path),
        "source_pixel_dimensions": {"width": width, "height": height},
        "configured_roi_normalized": spec["roi"],
        "configured_roi_pixels": {"x0": x0, "y0": y0, "x1": x1, "y1": y1},
        "estimated_skew_degrees": skew,
        "detected_lines": {
            "total": len(lines),
            "horizontal": sum(line["orientation"] == "horizontal" for line in lines),
            "vertical": sum(line["orientation"] == "vertical" for line in lines),
            "diagonal": sum(line["orientation"] == "diagonal" for line in lines),
        },
        "measurements": measurements,
        "artifacts": {"overlay": str(overlay_path), "binary_roi": str(binary_path)},
        "interpretive_status": "measurement_only_no_c1_rule_claimed",
    }
    result_path = output_dir / f"{spec['drawing_id']}_analysis.json"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result_path
