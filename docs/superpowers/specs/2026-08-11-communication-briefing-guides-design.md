# Communication Briefing Form — Deployment Guide Series (Design)

**Date:** 2026-08-11
**Source requirements:** `C:\Users\MCPC -902\Downloads\communication-briefing-form-spec.md`
(BBK Corporate Communications — Communication Briefing Form: SharePoint + Power Apps + Power Automate)
**Format reference:** `https://wastaboy.github.io/html_hustle/bloody-2026-08-07-1600.html`

## What this project is

A series of interactive HTML deployment guides that the user follows, step by step,
to build BBK's Communication Briefing Form system. The guides are the deliverable —
not the Power Platform system itself. Same one-repo-per-project pattern as
`IBD_html` and `3rd_party_html`.

## Decisions made during brainstorming

| Decision | Choice |
|---|---|
| Structure | Multi-part series: index + 5 parts, split per screen/layer |
| Password gate | **None.** No `gate.js` anywhere (Zscaler phishing flag lesson from 3rd_party_html, 2026-07-20). Verify: `grep -c 'gate.js' *.html` = 0 per file |
| Spec's open questions | Bake in sensible defaults, each flagged with a "confirm with CCD" callout |
| Deployment | New **public** repo `Wastaboy/Communication_html`, GitHub Pages from `main` root → `https://wastaboy.github.io/Communication_html/` (public approved by user 2026-08-11) |

## Site structure

Six self-contained HTML pages (inline CSS/JS, no external dependencies,
`localStorage` progress per page). Stable filenames — no dates — so cross-links
never churn:

| File | Covers |
|---|---|
| `index.html` | Series hub: what each part builds, links, prerequisites |
| `part1-foundation.html` | SharePoint site, both lists, columns, versioning, item-level permissions, CCD access |
| `part2-submission-form.html` | New canvas app, submission form screen, validation, attachments, first F5 submit test |
| `part3-my-requests.html` | Requester view: own items, status, CCD notes, post-submit editing |
| `part4-ccd-dashboard.html` | Team view: all requests, status filter, update status/notes, Excel export |
| `part5-flows-golive.html` | Notification flow, audit logger, optional status-change email, full acceptance walkthrough |

## Guide page format

Replicate the established interactive format from `bloody-2026-08-07-1600.html`:

- Color-coding legend, prerequisites checklist, numbered steps grouped into stages.
- **Amber pills** = exact names/values, tap to copy. **Navy chips** = UI buttons to
  click. **Dark navy blocks** = formulas/expressions with a Copy button.
  **Grey pills** = reference only.
- "Mark step done" per step, progress counter ("N of M steps done"), reset,
  expand/collapse all.
- Adaptation: steps also cover the SharePoint admin UI and Power Automate designer
  (not just Power Apps studio); the same pill conventions apply there.
- Every part ends with an F5/verify stage before the next part is opened.
- Series footer on each page linking the other parts + index (both layouts, as in
  html_hustle).

## Content defaults (each ⚑ = "confirm with CCD" callout in the guide)

**SharePoint (Part 1)**
- Team site; the site URL is a placeholder pill the user fills from their tenant.
- List **Communication Requests**: Title (Request Subject, required), Department
  (choice), Request Details (multi-line), Target Date (date), Status (choice:
  **Submitted / In Progress / Completed**, default Submitted ⚑), CCD Notes
  (multi-line), attachments enabled, versioning on. Requester = Created By.
- List **Audit Log**: Request ID (number), Action (choice: Created / Edited /
  Status Changed), Modified By (person), Modified DateTime (date & time),
  Change Summary (multi-line).
- Item-level permissions on Communication Requests: Read/Create/Edit **own items
  only** for general staff. Full access for the 5 named CCD members (Rawan
  AlQattan, Rafa Kaddoura, Abdulrahman Danish, Samar Qannati, Noora AlFaihani)
  via the site Members/Owners group. IT administers.
- Never hard-delete: status/archival only.

**Canvas app (Parts 2–4)**
- App name **Communication Briefing Form**; control prefixes `txt…`, `dd…`,
  `gal…`, `btn…`, `lbl…` per existing convention.
- Requester form fields ⚑: Request Subject, Department, Request Details,
  Target Date, attachments. Status and CCD Notes hidden from the requester form
  (CCD-managed). Required-field validation before submit. Experience must stay
  Google-Form simple — no approval steps anywhere (Phase-1 rule stated up front).
- My Requests: own submissions only, live status + CCD notes, edit capability.
- CCD Dashboard: all requests, filter by status, edit status/notes, Excel export
  step (native SharePoint export).

**Flows (Part 5)**
- **CBF – New Request Notification**: item created → email to
  `Corporate.Communications@bbkonline.com` ⚑ with request summary + link.
- **CBF – Audit Logger**: item created/modified → row in Audit Log (user,
  timestamp, action).
- **CBF – Status Change Notification** (explicitly optional stage): status
  change → email requester ⚑.
- No edit-lock after Completed ⚑ (Phase 1).
- Known-gotcha callouts carried from earlier guides: first-run SharePoint
  connection sign-in, lookalike-trigger warnings, delegation notes.

## Verification

**In-guide:** each part ends with an F5/verify checklist; Part 5 closes with a
go-live walkthrough mapped 1:1 to the spec's 10 acceptance criteria (submit with
attachment, CCD email, audit-logged edit, live status visible, item isolation
between requesters, Excel export, versioning on, no approval step, etc.).

**Guide QA before deploy:** serve over `http://` with `python -m http.server`
(never `file://`); click through copy buttons, progress persistence,
expand/collapse; verify cross-links and footers; `grep -c 'gate.js' *.html`
returns 0 for every page. Then commit, push, and spot-check the live Pages URLs.

## Out of scope

- Approval/rejection workflow (business decision, Phase 1).
- Building the Power Platform system itself in this repo — the guides are the
  deliverable.
- Password gating.
