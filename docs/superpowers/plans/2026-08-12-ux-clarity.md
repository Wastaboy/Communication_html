# UX Clarity Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rework Parts 2–4 of the live guide series so the app built from them explains Submit before/after and confirms before discarding typed work.

**Architecture:** Edit the scratchpad content fragments, rebuild pages with the existing `build_page.py` (template unchanged), update `tools/verify_pages.py` keys/snippets, QA, push — GitHub Pages redeploys the same URLs.

**Tech Stack:** Existing template/build/verify tooling; Power Fx formulas verbatim in the guide content.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-08-11-ux-clarity-design.md` (as amended: Part 4 d1 OnStart superset; Part 3 = 11 steps).
- No `gate.js`; verify with `grep -c 'gate.js' *.html` = 0.
- Storage keys bump on renumbered pages only: `cbfPart2_v2`, `cbfPart3_v2`. Part 4 keeps `cbfPart4_v1`.
- New step layout: Part 2 = 12 steps (b1–b12), Part 3 = 11 steps (c1–c11).
- Layering rule: no formula may reference a screen or variable that doesn't exist yet at that point in the build order.
- Run `python tools/verify_pages.py` after every rebuild; test over `http://`.

## Canonical new values

- App OnStart (introduced Part 2 b3): `Set(gblEditItem, Blank()); Set(gblShowCancelConfirm, false)`
- Part 4 d1 OnStart (superset, replaces old d1 formula): `Set(gblEditItem, Blank()); Set(gblShowCancelConfirm, false); Set(gblIsCCD, Lower(User().Email) in ["rawan.alqattan@bbkonline.com", "rafa.kaddoura@bbkonline.com", "abdulrahman.danish@bbkonline.com", "samar.qannati@bbkonline.com", "noora.alfaihani@bbkonline.com"]); Set(gblStatusFilter, "All")`
- New controls — scrSubmit: `lblSubmitIntro`, `lblSubmitHint`, `btnCancel`, `recDimmer`, `recDialog`, `lblDialogTitle`, `lblDialogBody`, `btnDialogKeep`, `btnDialogDiscard`; scrDone: `icoDoneCheck`, `lblDoneTitle`, `lblDoneBody`, `btnDoneAnother` (Part 2), `btnDoneMyRequests` (Part 3); scrMyRequests: `lblStatusLegend`.
- Key formulas (verbatim):
  - btnSubmit · Text: `If(IsBlank(gblEditItem), "Submit request", "Save changes")`
  - lblSubmitHint · Text: `If(!frmSubmit.Valid, "Fill the fields marked * to enable Submit.", IsBlank(gblEditItem), "Ready — Submit sends this to the CCD team and you'll see a confirmation.", "Ready — saving updates your request instantly for the CCD team.")`
  - frmSubmit · OnSuccess (Part 2 b9): `ResetForm(frmSubmit); Navigate(scrDone, ScreenTransition.None)`
  - frmSubmit · OnSuccess (Part 3 c7 final): `If(IsBlank(gblEditItem), ResetForm(frmSubmit); Navigate(scrDone, ScreenTransition.None), Notify("Changes saved.", NotificationType.Success); Set(gblEditItem, Blank()); ResetForm(frmSubmit); Navigate(scrMyRequests, ScreenTransition.None))`
  - btnCancel · Text: `If(IsBlank(gblEditItem), "Clear form", "Cancel changes")`
  - btnCancel · OnSelect (Part 2 b10): `If(frmSubmit.Unsaved, Set(gblShowCancelConfirm, true), ResetForm(frmSubmit))`
  - btnCancel · OnSelect (Part 3 c8 final): `If(frmSubmit.Unsaved, Set(gblShowCancelConfirm, true), ResetForm(frmSubmit); If(!IsBlank(gblEditItem), Set(gblEditItem, Blank()); Navigate(scrMyRequests, ScreenTransition.None)))`
  - btnDialogDiscard · OnSelect (Part 2 b10): `Set(gblShowCancelConfirm, false); ResetForm(frmSubmit)`
  - btnDialogDiscard · OnSelect (Part 3 c8 final): `Set(gblShowCancelConfirm, false); ResetForm(frmSubmit); If(!IsBlank(gblEditItem), Set(gblEditItem, Blank()); Navigate(scrMyRequests, ScreenTransition.None))`
  - btnDialogKeep · OnSelect: `Set(gblShowCancelConfirm, false)`
  - lblDetNotes stays as shipped; lblStatusLegend · Text: `"Submitted = waiting for CCD   ·   In Progress = being worked on   ·   Completed = done"`
- New copy (verbatim):
  - lblSubmitIntro: "This form goes straight to the Corporate Communications team. Fields marked * are required — and you can still edit your request after submitting."
  - lblDialogTitle: "Discard this request?" / lblDialogBody: "Anything you've entered here will be lost. Your already-submitted requests are not affected."
  - lblDoneTitle: "Request submitted" / lblDoneBody: "The CCD team has just been emailed your request. Track it anytime in My Requests — Submitted → In Progress → Completed. You can still edit it after submitting."

---

### Task 1: Rework Part 2 (b1–b12, key v2)

**Files:**
- Modify: scratchpad `part2-content.html`; `build_page.py` META (count 12, key `cbfPart2_v2`); `tools/verify_pages.py` (key + snippets)
- Rebuild: `part2-submission-form.html`

**Step layout:** b1 create app · b2 connect data · b3 screen, header, **App OnStart, intro label** · b4 insert form · b5 fields · b6 friendly fields · b7 submit button **+ hint label** · b8 **NEW: confirmation screen scrDone** · b9 success/failure behavior (OnSuccess → scrDone) · b10 **NEW: cancel + discard dialog** · b11 F5 test (extended) · b12 save & publish.

- [ ] **Step 1: Edit the fragment.** b3 gains two sub-steps + fx blocks: App OnStart (formula above; then tree view → App → ⋮ → Run OnStart) and `lblSubmitIntro` (X `24`, Y `92`, Width `Parent.Width - 48`, Size `14`, Color `RGBA(91, 102, 120, 1)`, copy above) with a `.note.why` "users should know where this goes and that submitting isn't final-final". b7 keeps position/fill sub-steps but Text becomes the If formula, and adds `lblSubmitHint` (X `24`, Y `btnSubmit.Y + 56`, Width `Parent.Width - 48`, Size `13`, Color `RGBA(91, 102, 120, 1)`) with its three-arm Text formula and a check "type/clear Request Subject and watch the hint change". New b8 builds scrDone: blank screen, `icoDoneCheck` (Insert → Icons → Check; Color `RGBA(31, 138, 82, 1)`, X `(Parent.Width - 120) / 2`, Y `160`, Width `120`, Height `120`), `lblDoneTitle` (Y `300`, Width `Parent.Width`, Align `Align.Center`, Size `28`, Semibold), `lblDoneBody` (X `(Parent.Width - 640) / 2`, Y `360`, Width `640`, Height `120`, Align `Align.Center`), `btnDoneAnother` (Text `"Submit another request"`, X `(Parent.Width - 220) / 2`, Y `500`, Width `220`, Height `48`, OnSelect `Navigate(scrSubmit, ScreenTransition.None)`); `.note.tip`: Part 3 adds a "View my requests" button here once that screen exists. b9 = old b8 with OnSuccess replaced by `ResetForm(frmSubmit); Navigate(scrDone, ScreenTransition.None)` (OnFailure unchanged) + `.note.why` "a full confirmation screen beats a toast — the user reads what happened and chooses what's next". New b10 builds `btnCancel` (Text If-formula, X `268`, Y `frmSubmit.Y + frmSubmit.Height + 8`, Width `180`, Height `48`, Fill `RGBA(238, 240, 246, 1)`, Color `RGBA(31, 59, 110, 1)`, OnSelect Part-2 version) and the dialog overlay, inserted in this order so it stacks on top: `recDimmer` (X `0`, Y `0`, Width `Parent.Width`, Height `Parent.Height`, Fill `RGBA(15, 31, 61, 0.6)`), `recDialog` (X `(Parent.Width - 520) / 2`, Y `(Parent.Height - 260) / 2`, Width `520`, Height `260`, Fill `White`), `lblDialogTitle` (X `recDialog.X + 24`, Y `recDialog.Y + 20`, Width `472`, Size `20`, Semibold), `lblDialogBody` (X `recDialog.X + 24`, Y `recDialog.Y + 64`, Width `472`, Height `90`), `btnDialogKeep` (Text `"Keep editing"`, X `recDialog.X + 24`, Y `recDialog.Y + 188`, Width `220`, Height `48`, Fill `RGBA(31, 59, 110, 1)`), `btnDialogDiscard` (Text `"Discard"`, X `recDialog.X + 276`, Y `recDialog.Y + 188`, Width `220`, Height `48`, Fill `White`, Color `RGBA(200, 55, 55, 1)`) — every one of the six gets Visible `gblShowCancelConfirm`; OnSelects per Global Constraints; `.note.why` "never lose typed work silently; never nag when nothing was typed". b11 = old b9 F5 test extended: after submit expect the **confirmation screen** (not a toast), tap "Submit another request" → empty form; then type something, tap "Clear form" → dialog appears → "Keep editing" preserves, reopen → "Discard" clears; check list covers hint-label states, confirmation screen, both dialog exits. b12 = old b10 unchanged.
- [ ] **Step 2: Update META + verify script.** `build_page.py`: part2 count `12`, key `cbfPart2_v2`. `verify_pages.py`: part2 key `cbfPart2_v2`; snippets become: the OnSuccess `ResetForm(frmSubmit); Navigate(scrDone, ScreenTransition.None)`, the three-arm lblSubmitHint formula (match on `Fill the fields marked * to enable Submit.`), `If(frmSubmit.Unsaved, Set(gblShowCancelConfirm, true), ResetForm(frmSubmit))`, and `Discard this request?`.
- [ ] **Step 3: Rebuild + verify.** Run build for part2; `python tools/verify_pages.py` → part2 clean (index count mismatch expected until Task 4).
- [ ] **Step 4: Commit** — `"Part 2 v2: submit transparency, confirmation screen, cancel safety net (12 steps)"`.

### Task 2: Rework Part 3 (c1–c11, key v2)

**Files:**
- Modify: scratchpad `part3-content.html`; `build_page.py` META (count 11, key `cbfPart3_v2`); `tools/verify_pages.py`
- Rebuild: `part3-my-requests.html`

**Step layout:** c1–c4 unchanged · c5 detail panel **+ status legend** · c6 edit wiring (unchanged content; b-references renumbered) · c7 return-after-edit (final OnSuccess above) · c8 **NEW: edit-aware cancel + "View my requests" on scrDone** · c9 = old c8 refresh/empty · c10 = old c9 F5 test extended · c11 = old c10 publish.

- [ ] **Step 1: Edit the fragment.** c5 gains `lblStatusLegend` (X `24`, Y `90`, Width `Parent.Width - 48`, Size `12`, Color `RGBA(91, 102, 120, 1)`, Text per Global Constraints) with `.note.why` "colored words must decode themselves". c7's fx block becomes the final OnSuccess (replaces the b9 version; note says exactly that). New c8: replace `btnCancel` OnSelect and `btnDialogDiscard` OnSelect with their edit-aware finals (both fx blocks), then on `scrDone` add `btnDoneMyRequests` (Text `"View my requests"`, X `(Parent.Width - 452) / 2`, Y `500`, Width `220`, Height `48`, Fill `RGBA(31, 59, 110, 1)`, OnSelect `Navigate(scrMyRequests, ScreenTransition.None)`) and move `btnDoneAnother` to X `(Parent.Width - 452) / 2 + 232` so the pair centers; `.note.why` "cancelling an edit returns you to your list, and the confirmation screen now offers both next moves". c10 F5 test adds: edit an item, Cancel changes → dialog → Discard → lands on My Requests with values reverted; submit new → confirmation screen → View my requests. Fix all stale references: b8→b9 (OnSuccess step), b9→b11 (TEST item), old text "b9 test item" → "b11 test item".
- [ ] **Step 2: Update META + verify script.** part3 count `11`, key `cbfPart3_v2`; part3 snippets: keep the three shipped ones, add the final OnSuccess (match on `Notify("Changes saved.", NotificationType.Success); Set(gblEditItem, Blank()); ResetForm(frmSubmit); Navigate(scrMyRequests, ScreenTransition.None)`) and `btnDoneMyRequests`.
- [ ] **Step 3: Rebuild + verify** (part3 clean).
- [ ] **Step 4: Commit** — `"Part 3 v2: status legend, edit-aware cancel, dual next-steps on confirmation (11 steps)"`.

### Task 3: Part 4 d1 OnStart superset (text-only, key stays v1)

**Files:**
- Modify: scratchpad `part4-content.html`; `tools/verify_pages.py`
- Rebuild: `part4-ccd-dashboard.html`

- [ ] **Step 1: Edit d1.** Replace the OnStart fx block with the four-Set superset (Canonical new values) and drop the now-redundant "App OnStart append ; Set(gblStatusFilter, "All")" wording in d2 (the superset already includes it; d2 keeps its chips content). Add one `.note.warn` line to d1: "This replaces the whole OnStart — the two Set lines from b3 must stay in it."
- [ ] **Step 2: Verify script:** add part4 snippet `Set(gblEditItem, Blank()); Set(gblShowCancelConfirm, false); Set(gblIsCCD` .
- [ ] **Step 3: Rebuild + verify; commit** — `"Part 4: d1 OnStart carries the b3 globals (wholesale-replace safety)"`.

### Task 4: Index counts + full QA + deploy

**Files:**
- Modify: scratchpad `index-content.html` (Part 2 card "10 steps · ~45 min" → "12 steps · ~50 min"; Part 3 card → "11 steps · ~50 min")
- Rebuild: `index.html`

- [ ] **Step 1: Edit + rebuild index; `python tools/verify_pages.py`** → `OK — 6 pages verified`.
- [ ] **Step 2: QA.** `grep -c 'gate.js' *.html` all 0. Serve `http://localhost:8000`; browser-check part2/part3/part4/index: step counts (12/11/10), new storage keys `cbfPart2_v2`/`cbfPart3_v2` written on tick, no console errors, no horizontal overflow, copy-path spot-check of the new formulas (dialog OnSelects, final OnSuccess, hint three-arm).
- [ ] **Step 3: Commit + push** — `"Index: updated step counts for Parts 2–3"` (push triggers Pages).
- [ ] **Step 4: Live verify.** Poll `gh api repos/Wastaboy/Communication_html/pages --jq .status` → `built`; curl all six URLs → 200; live-load part2, confirm 12 steps and `cbfPart2_v2`.

## Self-review notes (completed)

- Spec coverage: intro/hint/dynamic labels → T1 b3/b7; confirmation screen → T1 b8/b9 + T2 c8 button; cancel dialog → T1 b10 + T2 c8 finals; legend → T2 c5; OnStart layering → T1 b3 + T3; keys/counts/index → T1/T2/T4. Out-of-scope items untouched.
- Layering check: every formula in Part 2 references only Part 1–2 artifacts (gblEditItem/gblShowCancelConfirm exist via b3 OnStart; scrDone built b8 before b9 uses it; no scrMyRequests references until Part 3).
- Name consistency: control names match the spec's roster; b/c renumbering cross-references fixed in T2 Step 1.
