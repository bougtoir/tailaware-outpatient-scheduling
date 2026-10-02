PY = python3

.PHONY: all sim figs tables manuscript qc test clean

all: sim figs tables manuscript qc

sim:
	$(PY) scripts/exp01_descriptors.py
	$(PY) scripts/exp02_policies.py
	$(PY) scripts/exp03_misspec.py
	$(PY) scripts/exp04_pareto.py
	$(PY) scripts/exp05_decision_map.py
	$(PY) scripts/exp06_cascade.py

figs:
	$(PY) scripts/make_figures.py

tables:
	$(PY) scripts/make_tables.py

manuscript:
	$(PY) scripts/build_manuscript.py
	$(PY) scripts/make_supplement.py
	$(PY) scripts/make_inline_docx.py
	$(PY) scripts/revision_audits.py

qc:
	$(PY) -m pytest tests -q
	$(PY) scripts/audit_integrity.py
	$(PY) scripts/verify_docx.py

literature:
	$(PY) scripts/build_literature.py

test:
	$(PY) -m pytest tests -q

clean:
	rm -f results/processed/*.csv figures/*.pdf figures/*.png manuscript/*.docx manuscript/manuscript.md
