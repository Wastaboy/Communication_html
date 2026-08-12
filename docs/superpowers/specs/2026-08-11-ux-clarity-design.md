# UX Clarity Enhancement — Design

**Date:** 2026-08-11 (same-day follow-up to the shipped series)
**Goal:** The app built from these guides must make it obvious what happens
before and after Submit, and never lose typed work without asking.

## App behavior (built via Parts 2–3 edits)

**Before Submit (scrSubmit)**
- `lblSubmitIntro` under the header: "This form goes straight to the Corporate
  Communications team. Fields marked * are required — and you can still edit
  your request after submitting."
- `btnSubmit` Text: `If(IsBlank(gblEditItem), "Submit request", "Save changes")`.
- `lblSubmitHint` under the button, live:
  - form invalid → "Fill the fields marked * to enable Submit."
  - valid + new → "Ready — Submit sends this to the CCD team and you'll see a confirmation."
  - valid + edit → "Ready — saving updates your request instantly for the CCD team."

**Cancel safety net (scrSubmit)**
- `btnCancel` beside Submit: Text `If(IsBlank(gblEditItem), "Clear form", "Cancel changes")`.
- If `frmSubmit.Unsaved` → show confirm dialog (`gblShowCancelConfirm`):
  dim overlay `recDimmer`, card `recDialog`, `lblDialogTitle` "Discard this
  request?", `lblDialogBody` "Anything you've entered here will be lost. Your
  already-submitted requests are not affected.", buttons `btnDialogKeep`
  "Keep editing" (primary) and `btnDialogDiscard` "Discard".
- If nothing typed → cancel acts quietly (reset; in edit mode also navigate back).
- Discard: `ResetForm(frmSubmit)`; in edit mode also
  `Set(gblEditItem, Blank())` + `Navigate(scrMyRequests)`.

**After Submit (new screen scrDone, Part 2)**
- New submissions: `frmSubmit.OnSuccess` navigates to `scrDone` — green check
  icon `icoDoneCheck`, `lblDoneTitle` "Request submitted", `lblDoneBody`
  "The CCD team has just been emailed your request. Track it anytime in
  My Requests — Submitted → In Progress → Completed. You can still edit it
  after submitting.", buttons `btnDoneMyRequests` "View my requests",
  `btnDoneAnother` "Submit another request".
- Edits keep the existing behavior: "Changes saved." toast + Navigate back to
  My Requests (no scrDone detour).

**Status clarity (scrMyRequests, Part 3)**
- `lblStatusLegend` one-liner: "Submitted = waiting for CCD · In Progress =
  being worked on · Completed = done".

## Guide mechanics

- Edit in place (user has not started building). Part 2: 10 → 12 steps
  (intro/labels/hint folded into b3/b7/b8; new steps for the cancel dialog and
  scrDone). Part 3: legend added, c7 return-flow text adjusted.
- Storage keys bump: `cbfPart2_v2`, `cbfPart3_v2` (renumbered steps must not
  inherit old tick-marks). Index step counts updated (Part 2 = 12).
- Part 2 introduces `App.OnStart = Set(gblEditItem, Blank()); Set(gblShowCancelConfirm, false)`
  so its formulas can reference the globals before Part 3 exists. Part 4's d1
  (which replaces App.OnStart wholesale) therefore gains those two Sets in its
  formula — text-only change, step ids and storage key unchanged.
- scrDone is built in Part 2 with only "Submit another request"; Part 3 adds the
  "View my requests" button (that screen doesn't exist during Part 2) and
  upgrades Cancel/Discard to their edit-aware versions. Part 3 becomes 11 steps.
- Parts 1 and 5 unchanged. Verify script: update part2/part3 snippet lists and
  key names; full QA + redeploy to the same URLs.

## Out of scope (YAGNI)

- Nav-away guard on btnGoMyRequests mid-entry (Cancel covers the ask).
- Spinners/loading states (SubmitForm latency is sub-second here).
- Any change to flows, dashboard, or SharePoint.
