---
name: legacy-project-ai-init
description: Initialize AI-agent and GitHub Copilot development foundations for existing legacy projects. Use this skill whenever the user asks to set up, improve, or generate README.md, AGENTS.md, Copilot instructions, contribution docs, architecture notes, PR templates, .env examples, or other AI-assisted development guidance for an existing repository, especially when they emphasize "old project", "legacy project", "existing codebase", "do not use generic templates", "agent rules", or "Copilot setup".
---

# Legacy Project AI Init

Use this skill to add practical AI-agent development documentation to an existing repository. The core principle is evidence first: understand the repository that is actually present, then write only documentation and configuration that the repository can justify.

This skill is for maintained projects, not greenfield scaffolding. Do not invent missing stacks, commands, architecture, services, deployment steps, or conventions.

## Default behavior

- If the session is allowed to edit files, directly create or update the appropriate documentation files.
- If the session is in Plan Mode, the user asks for drafts only, or file writes are not available, produce a complete implementation plan or full file drafts instead of editing.
- Match the user's language for prose. Keep commands, paths, package names, environment variable names, and code identifiers unchanged.
- Prefer small, accurate documentation over broad generic documentation.

## Repository discovery

Before writing, inspect the repository. Read only what is needed to understand the project shape.

Start with:

- Top-level files and directories.
- Existing `README*`, `AGENTS.md`, `.github/copilot-instructions.md`, `.github/instructions/*`, `CONTRIBUTING*`, `docs/*`, and PR templates.
- Build and dependency manifests such as `package.json`, `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`, `.sln`, `.csproj`, `pom.xml`, `build.gradle`, `pyproject.toml`, `requirements.txt`, `go.mod`, `Cargo.toml`, Dockerfiles, compose files, CI configs, and task scripts.
- Source and test directories only far enough to identify entry points, architecture boundaries, naming conventions, test style, and important modules.
- Environment/config examples such as `.env.example`, appsettings files, config templates, sample YAML/JSON, or documented secret names.

Capture:

- Project purpose, as far as the repository proves it.
- Technology stack and package/build tools.
- Important directories and ownership boundaries.
- Local run, build, test, lint, and deployment commands.
- Existing documentation worth preserving.
- Constraints, generated files, vendored code, or areas that agents should avoid.
- Unknowns that cannot be reliably determined.

If a fact is not discoverable, write `待确认`, `需要人工补充`, or the equivalent in the user's language. Do not fill gaps with likely defaults.

## File strategy

Always prioritize:

- `README.md`
- `AGENTS.md`

Create or update optional files only when they add concrete value based on repository evidence:

- `.github/copilot-instructions.md` for concise global Copilot guidance when GitHub/Copilot usage is relevant.
- `.github/instructions/*.instructions.md` for scoped instructions only when there are clear subsystems, languages, or domains that need different rules.
- `CONTRIBUTING.md` when the repository has observable contribution, test, branch, review, or local setup conventions to document.
- `docs/architecture.md` when the architecture can be inferred from code, manifests, existing docs, or module boundaries.
- `.env.example` only when environment variables are discoverable from code or existing config. Never invent secrets.
- `pull_request_template.md` when review expectations, tests, or risk notes can be made concrete.

If an optional file is not created, explain why. A good reason is usually "the repository does not yet provide enough evidence".

## README.md guidance

If `README.md` exists, preserve useful content and improve it in place. Do not replace it wholesale unless it is empty or clearly obsolete.

README content should include, when supported by repository evidence:

- Project summary.
- Technology stack.
- Directory structure.
- Local development setup.
- Run/start commands.
- Build commands.
- Test commands.
- Lint/format commands.
- Key development notes.
- Deployment notes, if discoverable.
- Environment variables or config notes, if discoverable.
- Known unknowns or items needing human confirmation.

Avoid marketing copy and generic filler. Make the README useful to a maintainer opening the project today.

## AGENTS.md guidance

Create or update `AGENTS.md` for repository-specific agent behavior.

Include a short repository-specific section before the core rules. Base it only on discovered facts:

- Which directories to inspect first.
- Critical modules or boundaries.
- Commands for build, test, lint, and local run.
- Generated, vendored, binary, migration, or config areas to avoid or treat carefully.
- Existing patterns agents should follow.
- Unknown commands or conventions marked clearly as unconfirmed.

The file must include this core rule block exactly in meaning. Do not remove or weaken it:

```markdown
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
```

## Copilot and GitHub instructions

Add Copilot-specific instructions only when useful. Keep them short and operational.

Good Copilot guidance includes:

- Repository purpose and stack.
- Preferred commands.
- Where tests live.
- Where not to make broad changes.
- How to treat generated files, migrations, or public APIs.
- How to document uncertainty.

Do not duplicate all of `AGENTS.md` into Copilot instructions. Copilot files should be concise reminders, not another full handbook.

## Engineering constraints

- Do not modify business logic unless the user explicitly asks.
- Do not reformat unrelated files.
- Do not introduce dependencies for documentation-only work.
- Do not create empty placeholder directories.
- Do not create files only to satisfy a checklist.
- Do not expose secrets or copy real secret values into examples.
- Do not assume a missing test command means no tests exist; say it was not discoverable.
- Prefer existing project names and terminology over renaming or rebranding.

## Recommended workflow

1. Inspect the repository and existing docs.
2. Identify real project facts and unknowns.
3. Decide the minimum useful file set.
4. Draft or edit documentation using repository-specific details.
5. Verify generated docs for internal consistency.
6. If commands are known and safe, run non-mutating checks where appropriate.
7. Report:
   - Current project understanding.
   - Files created or changed.
   - Files intentionally not created and why.
   - Commands run and results.
   - Remaining human-confirmation items.

## Final response shape

When edits were made, respond in the user's language with:

1. A concise summary of the current project understanding.
2. The files changed.
3. What changed and why.
4. Verification performed.
5. Remaining items needing human confirmation.

When only drafting, include the full file drafts and clearly state that no files were changed.
