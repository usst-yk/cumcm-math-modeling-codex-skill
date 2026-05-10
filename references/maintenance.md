# Maintenance

Use this reference only when editing or publishing the skill itself.

## Editing Rules

- Keep `SKILL.md` short and navigational.
- Put detailed procedures in `references/`.
- Put deterministic repeated work in `scripts/`.
- Put reusable output skeletons in `templates/`.
- Avoid duplicating the same instruction in both `SKILL.md` and a reference file.
- Preserve beginner-facing natural language in `README.md`.

## Publish Checklist

Before pushing:

1. Check that `SKILL.md` front matter is valid YAML.
2. Confirm changed Markdown, Python, JSON, and TeX files are normally formatted.
3. Verify only relevant skill files are staged.
4. Commit with a concise message.
5. Push `main` to the configured GitHub remote.

