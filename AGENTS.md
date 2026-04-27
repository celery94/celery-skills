# Repository Instructions

This repository manages user-created skills. The current structure is small and documentation-focused.

## Repository Shape

- Inspect `readme.md` first for the repository overview and skill management conventions.
- Inspect `skills/<skill-name>/SKILL.md` before changing any skill.
- Keep each skill self-contained under `skills/<skill-name>/`.
- The only currently discoverable skill is `skills/legacy-project-ai-init`.
- The only currently discoverable eval convention is `skills/<skill-name>/evals/evals.json`.

## Skill Conventions

- Each skill must include `SKILL.md`.
- `SKILL.md` frontmatter must include at least `name` and `description`.
- The `description` should be specific about when the skill should trigger.
- Keep `SKILL.md` concise; move large supporting material into `references/`.
- Use `scripts/` for reusable deterministic helpers.
- Use `assets/` for templates or reusable media.
- Use `evals/evals.json` for repeatable skill tests when the skill's output can be meaningfully checked.

## Commands

No repository-level build, test, lint, packaging, or install commands are currently discoverable.

If you need to validate a skill, inspect that skill's own files first and state any command uncertainty plainly. Do not invent commands.

## Areas To Treat Carefully

- Do not rewrite a whole skill when a focused edit is enough.
- Do not change a skill's `name` unless the user explicitly asks.
- Do not add generated benchmark outputs, packaged artifacts, or evaluation workspaces unless the repository later documents that they should be committed.
- Do not introduce new dependencies for documentation-only changes.
- Preserve existing eval prompts and assertions unless the task is to update them.

## Approach

- Think before acting.
- Read existing files before writing code.
- Do not re-read files you have already read unless they may have changed.
- Prefer the smallest necessary change over broad rewrites.
- Prefer editing existing code over rewriting whole files.
- Keep solutions simple, direct, and consistent with the existing codebase.
- Understand the current implementation before making changes.
- Do not change public behavior, function names, interfaces, or project structure unless the task requires it.
- Do not introduce new dependencies unless they are clearly needed.
- When fixing bugs, change only the code directly related to the issue.
- Add or update tests when needed, especially for bug fixes and edge cases.
- Test your code before declaring the task done.
- Be concise in output but thorough in reasoning.
- Clearly state what changed, why it changed, and which files were affected.
- If something is uncertain, say so plainly.
- No sycophantic openers or closing fluff.
- User instructions always override this file.
