# Maintenance

Use this reference only when editing or publishing the skill itself.

## Editing Rules

- Keep `SKILL.md` short and navigational.
- Put detailed procedures in `references/`.
- Put deterministic repeated work in `scripts/`.
- Put reusable output skeletons in `templates/`.
- Avoid duplicating the same instruction in both `SKILL.md` and a reference file.
- Preserve beginner-facing natural language in `README.md`.
- When fixing a failure found in a real run, do not patch only that named
  example. First identify the failure class, then update the general routing,
  modeling, validation, paper, or review rule that would catch the same mistake
  in a variant of the problem.

## Failure Feedback Loop

When a user reports that a solved problem missed key conditions or produced a
weak paper:

1. Read the problem statement, modeling ideas, code outputs, validation report,
   and paper.
2. Separate symptoms from root causes: missed wording, wrong unit/object
   granularity, hidden assumption, weak model route, weak validation, or weak
   paper explanation.
3. Add or revise a general guardrail, not a one-off rule tied to the exact
   contest problem.
4. Update templates or validator checks when the mistake should be caught
   every time.
5. Run the structure/eval checks before reporting back.

## Publish Checklist

Before pushing:

1. Check that `SKILL.md` front matter is valid YAML.
2. Confirm changed Markdown, Python, JSON, and TeX files are normally formatted.
3. Verify only relevant skill files are staged.
4. Commit with a concise message.
5. Push `main` to the configured GitHub remote.
