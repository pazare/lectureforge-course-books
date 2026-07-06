# Workflow

Latest local workflow material reviewed: July 2, 2026.

## Principle

A course-book workflow should preserve the instructor's judgment and make every
generated artifact inspectable. The machine can stage, draft, render, and check.
It should not decide that private material is public, that a missing review has
happened, or that a skipped check has passed.

## Pipeline

### 1. Intake

Accept only authorized teaching materials:

- instructor notes;
- slide decks;
- reading lists;
- notebooks and lab files;
- de-identified transcripts, when allowed by policy and consent.

Do not ingest student submissions, grades, rosters, identifying class discussion,
recording passcodes, LMS snapshots, or raw video.

### 2. Staging

Create a source manifest with:

- stable file names;
- source type;
- rights status;
- hash;
- owner or reviewer;
- exclusion notes.

The manifest is part of the book's evidence, not paperwork after the fact.

### 3. Drafting

Generate a structured intermediate representation before rendering. A useful IR
contains:

- course and unit metadata;
- sections and learning objectives;
- tiered explanation blocks;
- exercises and answer keys;
- source citations;
- concept links;
- known gaps.

Persist the IR so rendering can be repeated without another model call.

### 4. Rendering

Render PDFs, HTML, or other formats from the same IR. Keep generated outputs out
of the public workflow repository unless the source rights and release approval
are explicit.

### 5. Verification

Record deterministic checks separately from model review and human review:

- `V_det`: executable checks, source-link checks, render checks, hashes;
- `V_LLM`: optional critique by a model;
- `V_human`: instructor, editor, or domain-review signoff.

Never upgrade a missing review into a pass. Skipped checks should stay visible.

### 6. Release

Release only what has passed the right gate:

- workflow: safe to publish when it contains no private course material;
- private instructor draft: share only with authorized reviewers;
- public course book: publish only after rights, privacy, instructor approval,
  and final human review are explicit.

## Public-Release Rule

The public artifact is the workflow. The books remain private unless the
professor or rights holder chooses to publish them.
