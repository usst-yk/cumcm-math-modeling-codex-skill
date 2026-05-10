# HTML Presentation

Use this reference when the user asks for a report deck, training summary,
defense brief, or full-project handoff beside the paper.

## Purpose

Generate `presentation/index.html` as a local, static, slide-like brief that
helps teammates, teachers, or training groups understand the solution. It is
not the paper and must not introduce facts absent from the result registry,
tables, figures, or problem statement.

## Default Structure

Use 8-10 slides:

1. title and core task;
2. problem decomposition;
3. data and preprocessing;
4. overall technical route;
5. Q1 model and result;
6. Q2/Q3 model and result;
7. validation, errors, feasibility, or sensitivity;
8. selling points and limitations;
9. final conclusions;
10. appendix or traceability notes when needed.

## Content Rules

- Reuse existing figures from `figures/`; do not create decorative filler.
- Put one sentence under each figure: what the figure proves or explains.
- Show registry id, source file, or table path for headline numbers.
- AI-generated images may be used only as conceptual or presentation visuals
  and must be marked as illustrative.
- Keep text compact. The brief is for explanation and review, not for replacing
  the paper.

## Script

Generate a minimal static brief with:

```bash
python scripts/build_presentation.py --plan problem/task_plan.json --registry results/result_registry.csv --figures figures
```

Review the generated page for missing figures, stale numbers, and unsupported
claims before using it in a defense or training session.
