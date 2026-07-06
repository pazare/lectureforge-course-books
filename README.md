# LectureForge Course-Book Workflow

Latest local workflow material reviewed: July 2, 2026.

This repository documents a public-safe workflow for turning authorized teaching
materials into private, inspectable course-book drafts. It publishes the method,
not the books.

The workflow was distilled from an internal instructor-facing pilot. The pilot
artifacts, source materials, Canvas exports, transcripts, recordings, student
submissions, generated PDFs, and professor-owned course content are excluded.
Professors may decide independently whether any book they receive should be
published.

## What This Is

LectureForge treats a course-book draft package as a verification record:

1. Stage only materials the instructor or teaching team is authorized to use.
2. Convert source materials into a structured manifest.
3. Generate a stable JSON intermediate representation.
4. Render book drafts from that intermediate representation.
5. Record deterministic checks, skipped checks, and known gaps.
6. Keep publication, licensing, and human review as separate approval gates.

The goal is not to make AI sound fluent. The goal is to make educational
material show its work.

## What This Is Not

This repository is not:

- a public release of any course book;
- a dump of course materials;
- a Canvas, Zoom, or LMS export;
- an official university, instructor, or platform publication;
- a legal, FERPA, copyright, or institutional-policy clearance.

Generated outputs belong in private release packages, not this repository.

## Workflow

See [docs/WORKFLOW.md](docs/WORKFLOW.md) for the end-to-end process.

See [docs/PROVENANCE_POLICY.md](docs/PROVENANCE_POLICY.md) for the public-release
and privacy boundary.

See [docs/RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md) before publishing any
derived artifact.

## Synthetic Example

The files under [examples/synthetic-course](examples/synthetic-course) show the
shape of a source manifest, generation spec, and verification record. They are
synthetic. They do not contain real course material.

## Local Release Scan

Run the scanner before committing any release candidate:

```sh
python3 scripts/scan_release_candidate.py .
```

The scanner blocks common leakage patterns: Canvas and Zoom markers, transcript
or media extensions, secret-shaped strings, course IDs, student/grading terms,
and private local paths.

## License

Code and documentation are released under the Apache License 2.0. The license
does not grant permission to publish any instructor-owned course materials or
student records.
