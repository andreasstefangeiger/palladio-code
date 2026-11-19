// Palladio-Code design engine (browser + node). Mirrors src/palladio_code/design.py;
// tests/test_app_engine.py checks both against the same cases.

export const FORMS = {
  "1:1": 1, "4:3": 4 / 3, "sqrt2:1": Math.SQRT2, "3:2": 1.5, "5:3": 5 / 3, "2:1": 2,
};
export const TOL = 0.01;

const snap = (v, step = 0.5) => Math.round(v / step) * step;
const relDev = (v, t) => Math.abs(v - t) / t;

export const MEANS = {
  I23_first: (l, b) => (l + b) / 2,
  I23_second: (l, b) => Math.sqrt(l * b),
  I23_third: (l, b) => (2 * l * b) / (l + b),
};
const MEAN_RULE = { I23_first: "A-HT-VAULT-002", I23_second: "A-HT-VAULT-003", I23_third: "A-HT-VAULT-004" };

export const DEFAULTS = {
  module: 16,
  wall: 1.5,
  sala_form: "5:3",
  rooms: [
    { size: "grande", form: "5:3", ceiling: "vault" },
    { size: "mediocre", form: "1:1", ceiling: "vault" },
    { size: "picciola", form: "4:3", ceiling: "vault" },
  ],
  upper_factor: 5 / 6,
  window_ratio: 1 / 4.5,
};

// nearest of the seven forms to a ratio, with its relative deviation
export function nearestForm(ratio) {
  let best = null;
  for (const [name, v] of Object.entries(FORMS)) {
    const dev = relDev(ratio, v);
    if (!best || dev < best.dev) best = { name, value: v, dev };
  }
  return best;
}

export function run(input = {}) {
  const p = { ...DEFAULTS, ...input, rooms: (input.rooms || DEFAULTS.rooms).map((r) => ({ ...r })) };
  const w = p.module, wall = p.wall;
  const decisions = [];
  const log = (step, topic, decision, rules, status = "follows", note = "") =>
    decisions.push({ step, topic, decision, rules, status, note });

  log(1, "module", `${w}`, ["B-SYS-MOD-001"], "follows");
  log(1, "wall", `${wall}`, [], "assumption");

  // step 4: wing rooms (grande extends the module, picciola shortens it)
  let y = wall;
  const rooms = p.rooms.map((r) => {
    const ratio = FORMS[r.form] ?? 1;
    let depth = r.depth ?? (ratio === 1 ? w : snap(r.size === "picciola" ? w / ratio : w * ratio));
    const room = { ...r, width: w, depth, y };
    room.length = Math.max(w, depth);
    room.breadth = Math.min(w, depth);
    room.ratio = room.length / room.breadth;
    const near = nearestForm(room.ratio);
    room.nearest = near.name;
    room.status = near.dev < 1e-9 ? "follows" : near.dev <= TOL ? "approx" : "deviation";
    y += depth + wall;
    log(4, "form", `${room.size}: ${room.length} x ${room.breadth}`, ["A-PROP-ROOM-001", "B2-CAP2-1"],
      room.status, room.status === "follows" ? "" : `${room.ratio.toFixed(4)} ~ ${near.name}`);
    return room;
  });
  const areas = rooms.map((r) => r.width * r.depth);
  const descending = areas.every((a, i) => i === 0 || areas[i - 1] >= a);
  log(4, "sequence", descending ? "grande-mediocre-picciola" : "not descending", ["B2-CAP2-1"],
    descending ? "follows" : "deviation");
  const wingDepth = y;

  // step 2: centre
  const salaDepth = wingDepth - 2 * wall;
  const salaWidth = p.sala_width ?? snap(salaDepth / (FORMS[p.sala_form] ?? 5 / 3));
  const sala = { width: salaWidth, depth: salaDepth, x: wall + w + wall, y: wall };
  sala.length = Math.max(salaWidth, salaDepth);
  sala.breadth = Math.min(salaWidth, salaDepth);
  sala.ratio = sala.length / sala.breadth;
  log(2, "centre", `${sala.length} x ${sala.breadth}`, ["A-ORG-CEN-001", "A-DIM-HALL-001"],
    sala.ratio <= 2 + 1e-9 ? "follows" : "deviation");

  // step 3: symmetry
  log(3, "symmetry", "mirror", ["A-ORG-SYM-001"], p.asymmetric ? "deviation" : "follows");

  // step 5: heights
  const square = rooms.find((r) => r.length === r.breadth && r.ceiling === "vault");
  const target = square ? (square.breadth * 4) / 3 : null;
  for (const r of rooms) {
    if (r.ceiling === "flat") {
      r.height = r.breadth; r.heightRule = "flat_h_eq_w"; r.rules = ["A-HT-ROOM-001"];
    } else if (r.length === r.breadth) {
      r.height = (r.breadth * 4) / 3; r.heightRule = "I23_square_4_3"; r.rules = ["A-HT-VAULT-001"];
    } else {
      r.means = Object.fromEntries(Object.entries(MEANS).map(([k, f]) => [k, f(r.length, r.breadth)]));
      let method = r.method;
      if (!method) {
        method = target === null ? "I23_first"
          : Object.keys(MEANS).reduce((a, b) => (relDev(r.means[a], target) <= relDev(r.means[b], target) ? a : b));
      }
      r.height = r.means[method]; r.heightRule = method; r.rules = [MEAN_RULE[method]];
    }
    log(5, "height", `${r.size}: ${r.height.toFixed(2)} (${r.heightRule})`, r.rules);
  }
  const rowHeights = rooms.filter((r) => r.ceiling === "vault" && r.size !== "picciola").map((r) => r.height);
  let spread = null;
  if (rowHeights.length > 1) {
    spread = (Math.max(...rowHeights) - Math.min(...rowHeights)) / Math.max(...rowHeights);
    log(5, "equal_heights", `${(spread * 100).toFixed(1)} %`, ["A-HT-VAULT-005", "B-SYS-VAULT-001"],
      spread <= TOL ? "follows" : "deviation");
  }

  // step 6: upper floor
  const mainH = rowHeights.length ? Math.max(...rowHeights) : w;
  const upper = mainH * p.upper_factor;
  log(6, "upper", upper.toFixed(2), ["A-HT-STORY-001"],
    Math.abs(p.upper_factor - 5 / 6) < 1e-9 ? "follows" : "deviation");

  // step 7: openings
  const winW = snap(w * p.window_ratio, 0.25);
  const winH = (winW * 13) / 6;
  const winOk = winW >= w / 5 - 1e-9 && winW <= w / 4 + 1e-9;
  log(7, "window", `${winW} x ${winH.toFixed(2)}`, ["A-DIM-WIN-001", "A-DIM-WIN-002"], winOk ? "follows" : "deviation");
  log(7, "window_upper", ((winH * 5) / 6).toFixed(2), ["A-DIM-WIN-003"]);
  log(7, "axes", "aligned", ["A-ORG-OPEN-001", "A-LOC-WIN-001"]);
  log(7, "door", "3 x 6.5", ["A-DIM-DOOR-001"]);

  return {
    params: p, rooms, sala, spread, target, mainHeight: mainH, upperHeight: upper,
    window: { width: winW, height: winH, upperHeight: (winH * 5) / 6 }, decisions,
    total: { width: wall + w + wall + salaWidth + wall + w + wall, depth: wingDepth },
  };
}

export function nearestPalladio(design, readings) {
  const by = {};
  for (const r of readings) if (r.length && r.confidence !== "low") (by[r.building] ||= []).push([r.length, r.width]);
  let best = null;
  for (const [b, rooms] of Object.entries(by)) {
    let cost = 0;
    for (const r of design.rooms) cost += Math.min(...rooms.map(([l, w]) => Math.abs(r.length - l) + Math.abs(r.breadth - w)));
    if (!best || cost < best.cost) best = { building: b, cost, rooms };
  }
  return best;
}
