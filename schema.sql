PRAGMA foreign_keys = ON;

CREATE TABLE rules (
    rule_id TEXT PRIMARY KEY,
    evidence_class TEXT NOT NULL CHECK (evidence_class IN ('A','B','C1','C2')),
    status TEXT NOT NULL,
    building_type TEXT,
    design_phase TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT,
    rule_text_de TEXT NOT NULL,
    condition_text_de TEXT,
    exception_text_de TEXT,
    purpose_text_de TEXT,
    reasoning_de TEXT,
    confidence REAL CHECK (confidence IS NULL OR confidence BETWEEN 0 AND 1),
    ratio_json TEXT,
    dimension_json TEXT,
    unit TEXT,
    notes TEXT,
    CHECK ((evidence_class = 'A' AND confidence IS NULL) OR evidence_class <> 'A')
);

CREATE TABLE rule_sources (
    rule_source_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_id TEXT NOT NULL REFERENCES rules(rule_id) ON DELETE CASCADE,
    source_work TEXT NOT NULL,
    book INTEGER NOT NULL,
    chapter TEXT NOT NULL,
    printed_page TEXT,
    pdf_page INTEGER,
    quotation_original TEXT NOT NULL,
    translation_de TEXT,
    transcription_status TEXT NOT NULL
);

CREATE TABLE rule_derivations (
    rule_id TEXT NOT NULL REFERENCES rules(rule_id) ON DELETE CASCADE,
    source_rule_id TEXT NOT NULL REFERENCES rules(rule_id),
    PRIMARY KEY (rule_id, source_rule_id)
);

CREATE TABLE drawings (
    drawing_id TEXT PRIMARY KEY,
    source_work TEXT NOT NULL,
    book INTEGER NOT NULL,
    chapter TEXT,
    printed_page TEXT,
    pdf_page INTEGER NOT NULL,
    drawing_type TEXT NOT NULL,
    building_name TEXT,
    image_path TEXT NOT NULL,
    roi_json TEXT,
    selection_reason TEXT NOT NULL,
    attribution_status TEXT NOT NULL
);

CREATE TABLE drawing_regions (
    region_id TEXT PRIMARY KEY,
    drawing_id TEXT NOT NULL REFERENCES drawings(drawing_id) ON DELETE CASCADE,
    semantic_type TEXT,
    geometry_json TEXT NOT NULL,
    detection_method TEXT NOT NULL,
    confidence REAL CHECK (confidence BETWEEN 0 AND 1),
    review_status TEXT NOT NULL
);

CREATE TABLE measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    drawing_id TEXT NOT NULL REFERENCES drawings(drawing_id) ON DELETE CASCADE,
    region_id TEXT,
    measurement_method TEXT NOT NULL,
    reference_line TEXT,
    quantity TEXT NOT NULL,
    raw_value REAL NOT NULL,
    unit TEXT NOT NULL,
    endpoint_json TEXT,
    algorithm TEXT NOT NULL,
    algorithm_version TEXT NOT NULL,
    confidence REAL CHECK (confidence BETWEEN 0 AND 1),
    human_review_required INTEGER NOT NULL CHECK (human_review_required IN (0,1)),
    notes TEXT
);

CREATE TABLE ratio_hypotheses (
    ratio_hypothesis_id INTEGER PRIMARY KEY AUTOINCREMENT,
    measurement_id INTEGER NOT NULL REFERENCES measurements(measurement_id) ON DELETE CASCADE,
    rank INTEGER NOT NULL,
    measured_ratio REAL,
    target_label TEXT NOT NULL,
    target_value REAL NOT NULL,
    deviation_percent REAL NOT NULL,
    target_origin TEXT NOT NULL,
    within_pilot_tolerance INTEGER NOT NULL CHECK (within_pilot_tolerance IN (0,1)),
    UNIQUE (measurement_id, rank)
);

CREATE TABLE c1_rule_candidates (
    candidate_id TEXT PRIMARY KEY,
    rule_text_de TEXT NOT NULL,
    population_definition TEXT NOT NULL,
    n_examined INTEGER NOT NULL,
    n_matches INTEGER NOT NULL,
    mean_value REAL,
    median_value REAL,
    standard_deviation REAL,
    mean_deviation_percent REAL,
    outliers_json TEXT,
    alternative_explanations TEXT,
    confidence REAL CHECK (confidence BETWEEN 0 AND 1),
    status TEXT NOT NULL
);

CREATE TABLE c1_candidate_support (
    candidate_id TEXT NOT NULL REFERENCES c1_rule_candidates(candidate_id) ON DELETE CASCADE,
    measurement_id INTEGER NOT NULL REFERENCES measurements(measurement_id),
    PRIMARY KEY (candidate_id, measurement_id)
);

CREATE TABLE corpus_pages (
    page_id TEXT PRIMARY KEY,
    physical_image_number INTEGER NOT NULL UNIQUE,
    pdf_page INTEGER NOT NULL UNIQUE,
    book INTEGER,
    printed_page_candidate TEXT,
    alto_page_id TEXT,
    ocr_word_count INTEGER NOT NULL,
    ocr_character_count INTEGER NOT NULL,
    ink_coverage REAL,
    edge_density REAL,
    long_horizontal_lines INTEGER,
    long_vertical_lines INTEGER,
    illustration_score REAL,
    page_class_candidate TEXT,
    review_status TEXT NOT NULL
);

CREATE TABLE automatic_rule_candidates (
    candidate_id TEXT PRIMARY KEY,
    page_id TEXT NOT NULL REFERENCES corpus_pages(page_id) ON DELETE CASCADE,
    source_work TEXT NOT NULL,
    book INTEGER NOT NULL,
    chapter_candidate TEXT,
    printed_page_candidate TEXT,
    pdf_page INTEGER NOT NULL,
    passage_ocr TEXT NOT NULL,
    normalized_passage TEXT NOT NULL,
    marker_types_json TEXT NOT NULL,
    category_candidate TEXT,
    design_phase_candidate TEXT,
    extraction_score REAL NOT NULL,
    contains_quantity INTEGER NOT NULL CHECK (contains_quantity IN (0,1)),
    status TEXT NOT NULL,
    notes TEXT
);

CREATE TABLE automatic_drawing_candidates (
    page_id TEXT PRIMARY KEY REFERENCES corpus_pages(page_id) ON DELETE CASCADE,
    drawing_type_candidate TEXT,
    reason_json TEXT NOT NULL,
    rank_within_book INTEGER,
    status TEXT NOT NULL
);

CREATE VIEW rules_flat AS
SELECT r.*, s.source_work, s.book, s.chapter, s.printed_page, s.pdf_page,
       s.quotation_original, s.translation_de, s.transcription_status
FROM rules r
LEFT JOIN rule_sources s ON s.rule_id = r.rule_id;
