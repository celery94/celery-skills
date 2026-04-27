# celery-skills

This repository is for managing user-created Codex/Claude-style skills.

Current repository evidence:

- Skills live under `skills/`.
- Each skill is expected to have a required `SKILL.md`.
- The current checked-in skill is `skills/legacy-project-ai-init`.
- `skills/legacy-project-ai-init/evals/evals.json` shows the local convention for skill evaluation prompts and assertions.

## Directory Layout

```text
.
├── readme.md
└── skills/
    └── legacy-project-ai-init/
        ├── SKILL.md
        └── evals/
            └── evals.json
```

Recommended layout for new skills:

```text
skills/
└── skill-name/
    ├── SKILL.md
    ├── evals/
    │   └── evals.json
    ├── scripts/
    ├── references/
    └── assets/
```

Only `SKILL.md` is required. Add `evals/`, `scripts/`, `references/`, and `assets/` when the skill actually needs them.

## Skill Authoring Notes

`SKILL.md` should include YAML frontmatter with at least:

```markdown
---
name: skill-name
description: Use this skill when...
---
```

Guidelines:

- Keep the `description` specific and trigger-oriented. It should say when to use the skill and what it helps accomplish.
- Keep the main `SKILL.md` focused enough to load into context easily.
- Put reusable deterministic work in `scripts/`.
- Put long domain references in `references/` and load only the relevant reference when working.
- Put templates, images, or other reusable files in `assets/`.
- Add `evals/evals.json` for skills that benefit from repeatable test prompts.

## Evaluation Convention

The existing `legacy-project-ai-init` skill uses this shape:

```json
{
  "skill_name": "skill-name",
  "evals": [
    {
      "id": 1,
      "prompt": "Task prompt",
      "expected_output": "Expected behavior",
      "files": [],
      "assertions": [
        {
          "text": "Objective assertion to check"
        }
      ]
    }
  ]
}
```

Use realistic prompts that resemble actual user requests. Prefer assertions that can be checked objectively.

## Local Commands

No build, test, lint, packaging, or install commands are currently discoverable from this repository.

Known unknowns needing confirmation:

- How these skills are installed from this repository into the active Codex/Claude environment.
- Whether packaged `.skill` artifacts should be committed.
- Whether evaluation workspaces and generated benchmark outputs should be committed or ignored.
- Whether this repository should enforce formatting for Markdown or JSON files.

## Maintenance Checklist

When adding or updating a skill:

1. Create or edit `skills/<skill-name>/SKILL.md`.
2. Confirm the frontmatter `name` matches the intended skill identifier.
3. Make the `description` strong enough for reliable triggering.
4. Add bundled resources only when they reduce repeated work or keep the main instructions lean.
5. Add or update `evals/evals.json` when the skill has repeatable behavior to verify.
6. Run any known validation or packaging steps once they are defined.
