# CUMCM Project Structure

- `problem/`: problem statement, problem parse, assumptions, task plan, and model cards.
- `data/raw/`: untouched attachments.
- `data/processed/`: cleaned or reconstructed data.
- `src/`: deterministic scripts, named by subquestion when possible.
- `notebooks/`: optional exploration notebooks.
- `results/`: result registry, validation report, and sensitivity outputs.
- `figures/`: code-generated paper figures and editable roadmap outputs.
- `figures/ai_briefs/`: AI figure briefs that require human review.
- `presentation/`: optional HTML/PPT-style presentation assets for final sharing.
- `presentation/figures/`: presentation-specific figure copies or exports.
- `tables/`: generated result tables and data audit tables.
- `paper/`: TeX/Markdown paper, sections, references, and compiled PDF.
- `appendix/`: appendix code and supplemental material.
- `logs/`: run log and error recovery log.

All headline values must be registered in `results/result_registry.csv` before final writing.
