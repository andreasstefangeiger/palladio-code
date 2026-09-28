PYTHON ?= python3
export PYTHONPATH := src

.PHONY: pilot local-review overnight-review test clean

pilot:
	$(PYTHON) -m palladio_code.cli all

local-review:
	$(PYTHON) -m palladio_code.local_review --model gemma4:12b --batch-size 4

overnight-review:
	$(PYTHON) -m palladio_code.local_review --model gemma4:12b --batch-size 1
	$(PYTHON) -m palladio_code.local_review --model gemma4:12b --batch-size 4 --output-stem local_llm_review_pass2 --second-pass

test:
	$(PYTHON) -m unittest discover -s tests -v

clean:
	rm -rf output/analysis output/qc output/palladio_code.sqlite output/csv output/pilot_summary.json output/full_corpus_summary.json output/automatic_rule_candidates.json output/automatic_review_queue.csv output/topic_index.json output/design_phase_index.json output/automatic_ratio_candidates.json output/local_llm_review.jsonl output/local_llm_review_summary.json output/local_llm_review_pass2.jsonl output/local_llm_review_pass2_summary.json
