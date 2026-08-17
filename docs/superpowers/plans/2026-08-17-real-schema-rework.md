# Real-Schema Rework Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rework all six guide pages around the real 34-custom-column Communication Requests schema, with conditional form sections and the CCD assignment workflow.

**Architecture:** Six static HTML guide pages generated from `template.html` conventions, verified by `tools/verify_pages.py` (step-ID sequences, localStorage keys, verbatim formula snippets). Each page task first updates the verifier's expectations (the failing test), then reworks the page until the verifier passes, then commits.

**Tech Stack:** Static HTML/CSS/JS (no build), Python verifier, GitHub Pages deploy.

**Spec:** `docs/superpowers/specs/2026-08-17-real-schema-rework-design.md` — the 34-column table, choice values, and per-part scope live there; this plan references them as **[SPEC §Part 1 table]** etc. Executors read both.

## Global Constraints

- No page may reference `gate.js` (verifier enforces).
- Pages follow `template.html` conventions: `details.step` blocks with sequential ids, `fxgroup`/`fx` copy blocks, `dl.props` tables, `note check` + `done` button per step, "of N steps" progress label matching step count.
- Column creation convention: space-free internal name first, display rename after (spec table is authoritative for both names).
- All multi-line columns: plain text, never rich text.
- Team name is **CCD** everywhere; the notes column alone is `CCMNotes` / "CCM Notes".
- Choice-value blocks that are proposed defaults carry a *confirm with CCD* warn note.
- New-designer Power Automate wording (⊕ / "Add an action", ⚡ chips, fx expressions) with classic fallbacks, as in the current Part 5.
- Verify after every page edit: `python tools/verify_pages.py`. Test over `http://`, never `file://`.
- Commit + push per task (git autopilot).

---

### Task 1: Part 1 — schema build (part1-foundation.html)

**Files:**
- Modify: `part1-foundation.html`
- Modify: `tools/verify_pages.py` (part1 entry + key)
- Test: `python tools/verify_pages.py`

**Interfaces:**
- Produces: internal column names per [SPEC §Part 1 table] — every later task references columns by exactly those names. Step ids `a1`–`a15`. localStorage key `cbfPart1_v3`.

New step map (a1, a2 keep current content; old a4–a9 become a10–a15 with content carried over and column names updated):

| id | Title | Content |
|---|---|---|
| a1 | Create the site | unchanged |
| a2 | Create the Communication Requests list | unchanged |
| a3 | Basics columns (1–3 of 34) | `Division` (Choice, existing 22-division block, no default), `LaunchDate` (Date, include time No), `TypeOfDeliverables` (Choice, **Allow multiple selections: Yes**, values below) |
| a4 | Request-detail columns (4–8) | `PurposeObjective`, `BackgroundContext` (MLOT); `TargetAudience` (Choice, multi-select Yes, values below); `AudienceNotes`, `DesiredOutcome` (MLOT) |
| a5 | Budget columns (9–11) | `BudgetRequired` (Yes/No, default No), `Budget` (Currency), `BudgetStatus` (Choice, values below) |
| a6 | PR & references columns (12–14) | `PRKeyMessages` (MLOT), `PRSpokespersons` (single line), `SupportingReferences` (MLOT) |
| a7 | Event columns (15–24) | `EventName`, `EventDescription`, `EventStartDate`/`EventEndDate` (Date, include time **Yes**), `EventLocation`, `EventExpectedAttendance` (Number, 0 decimals), `EventSpeakers`, `EventVIPsAttending` (Yes/No No), `VIPProtocols` (MLOT), `EventMediaExpected` (Yes/No No) |
| a8 | Branding columns (25–27) | `BrandingRequirements` (MLOT), `BrandingDesignExists`, `BrandingPartnerAssets` (Yes/No, default No) |
| a9 | CCD workflow columns (28–34) | `Status` (Choice Submitted/In Progress/Completed, default **Submitted**), `AssignedTo` (Person, single), `AssignedOn` (Date+time Yes), `Priority` (Choice Low/Medium/High/Urgent, no default), `CCMNotes` (MLOT), `CompletedOn` (Date+time Yes), `CompletedBy` (Person, single) |
| a10 | Rename the display labels | one table, every internal→display rename from [SPEC §Part 1 table] (18 renames; Division, Budget, Status, Priority need none; Title keeps its name — note explicitly that the old "Request Subject" rename is gone) |
| a11 | Versioning and attachments | old a5 unchanged |
| a12 | Item-level privacy | old a6 unchanged |
| a13 | Create the Audit Log list | old a7 unchanged |
| a14 | Permissions & members | old a8 unchanged |
| a15 | Final check | old a9, checklist updated to new column headers |

Each column gets a full `fxgroup` ("Division — column 1 of 34" numbering runs across steps) with props `dl` and copy chips, same pattern as the current a3. Choice blocks to embed verbatim:

```
Event Support
Media & PR
Branding & Design
Digital & Social Media
Internal Communication
Print & Publications
Video & Photography
```

```
Internal Staff
External Public
Media
Customers
Partners & Stakeholders
VIPs & Dignitaries
```

```
Approved
Pending Approval
Not Yet Requested
```

Division block: reuse the existing 22-division `fx` block unchanged. Status block: existing three values unchanged. Multi-select columns need the extra prop row: **Allow multiple selections → Yes** (under More options). The *confirm with CCD* warn note (current a3 has one) moves to cover TypeOfDeliverables/TargetAudience/BudgetStatus + divisions + status.

- [ ] **Step 1: Update verifier (failing test).** In `tools/verify_pages.py`: part1 key → `cbfPart1_v2` becomes `cbfPart1_v3`; part1 snippets become:

```python
    "part1-foundation.html": [
        "Everyone except external users",
        "Create items and edit items that were created by the user",
        "TypeOfDeliverables",
        "Event Support\nMedia & PR\nBranding & Design\nDigital & Social Media\nInternal Communication\nPrint & Publications\nVideo & Photography",
        "Approved\nPending Approval\nNot Yet Requested",
        "VIPs Dignitaries Attending Protocols",
        "CCMNotes",
    ],
```

- [ ] **Step 2: Run `python tools/verify_pages.py`** — expect FAIL on part1 (missing key + snippets).
- [ ] **Step 3: Rework part1-foundation.html** per the step map above: retitle steps, replace a3/a4, insert a5–a9, renumber old steps to a10–a15, update the progress label to `of 15 steps`, set localStorage key to `cbfPart1_v3`, update the page intro ("what Part 1 builds" — 34 columns, 8 groups) and any TL;DR.
- [ ] **Step 4: Run `python tools/verify_pages.py`** — expect OK (other pages' expectations untouched).
- [ ] **Step 5: Commit** `git add -A; git commit -m "Part 1: real 34-column schema build (a1-a15)"; git push`

---

### Task 2: Part 2 — requester form rebuild (part2-submission-form.html)

**Files:**
- Modify: `part2-submission-form.html`
- Modify: `tools/verify_pages.py` (part2 entry)
- Test: `python tools/verify_pages.py`

**Interfaces:**
- Consumes: column internal/display names from Task 1.
- Produces: control names later tasks rely on — `frmSubmit`, `cmbDeliverables`, `tglBudgetRequired`, `tglVIPs`, `gblEditItem`, `gblShowCancelConfirm`, screens `scrSubmit`, `scrDone`. Step ids `b1`–`b14`, key `cbfPart2_v4`.

Step map (b1–b3 largely carried over from current page; the form steps are fresh):

| id | Title |
|---|---|
| b1 | Create the app |
| b2 | Connect the data (SharePoint V2 connector, both lists) |
| b3 | App.OnStart — typed globals (formula unchanged from current page: `Set(gblEditItem, LookUp('Communication Requests', false)); Set(gblShowCancelConfirm, false)`) |
| b4 | scrSubmit — header + Edit form shell (`frmSubmit`: DataSource `'Communication Requests'`, Item `gblEditItem`, DefaultMode `If(IsBlank(gblEditItem), FormMode.New, FormMode.Edit)`, snap-to-column layout, 1 column) |
| b5 | Always-on cards I — Title, Division, Launch Date, Type of Deliverables (unlock card, rename inner combo to `cmbDeliverables`) |
| b6 | Always-on cards II — Purpose Objective, Background Context, Target Audience, Audience Notes, Desired Outcome, Supporting References, Budget Required (unlock, rename toggle `tglBudgetRequired`) |
| b7 | Conditional section pattern + Budget cards |
| b8 | Conditional PR cards |
| b9 | Conditional Event cards (rename VIP toggle `tglVIPs`) |
| b10 | Conditional Branding cards |
| b11 | Required fields + Submit button |
| b12 | Cancel-confirm dialog (carried over: `If(frmSubmit.Unsaved, Set(gblShowCancelConfirm, true), ResetForm(frmSubmit))`, dialog controls each with `Visible: gblShowCancelConfirm`, "Discard this request?") |
| b13 | scrDone — confirmation screen (`ResetForm(frmSubmit); Navigate(scrDone, ScreenTransition.None)` lives in the form's OnSuccess) |
| b14 | Test the form end-to-end |

b7 teaches the pattern once, in three parts, then b8–b10 repeat it per section:

1. **Card Visible** (on every card in the section):
   - Budget cards: `tglBudgetRequired.Value`
   - PR cards: `"Media & PR" in cmbDeliverables.SelectedItems.Value`
   - Event cards: `"Event Support" in cmbDeliverables.SelectedItems.Value`
   - VIP Protocols card: `"Event Support" in cmbDeliverables.SelectedItems.Value && tglVIPs.Value`
   - Branding cards: `"Branding & Design" in cmbDeliverables.SelectedItems.Value`
2. **Card Update** (so a hidden section saves blank instead of a stale value; example for the Budget card, adapted per card): `If(tglBudgetRequired.Value, DataCardValue_Budget.Value)` — the pattern is `If(<section visible>, <inner control value>)`; the missing else saves blank.
3. **Why note:** hidden ≠ cleared; without the Update guard an edited request keeps event fields after Event Support is deselected.

b11 content: required at app level (list-level Required is all off): Title, Division, Launch Date, Type of Deliverables, Purpose Objective — set each card's Required to `true` and its star visible; Submit button `DisplayMode: If(frmSubmit.Valid, DisplayMode.Edit, DisplayMode.Disabled)`, `OnSelect: SubmitForm(frmSubmit)`, helper label "Fill the fields marked * to enable Submit."; form `OnSuccess: Notify("Request submitted.", NotificationType.Success); Set(gblEditItem, Blank()); ResetForm(frmSubmit); Navigate(scrDone, ScreenTransition.None)`.

- [ ] **Step 1: Update verifier (failing test).** part2 key → `cbfPart2_v4`; part2 snippets become:

```python
    "part2-submission-form.html": [
        "SubmitForm(frmSubmit)",
        "If(frmSubmit.Valid, DisplayMode.Edit, DisplayMode.Disabled)",
        "Fill the fields marked * to enable Submit.",
        "If(frmSubmit.Unsaved, Set(gblShowCancelConfirm, true), ResetForm(frmSubmit))",
        "Discard this request?",
        "Set(gblEditItem, LookUp('Communication Requests', false)); Set(gblShowCancelConfirm, false)",
        "gblShowCancelConfirm</code></dd></div>",
        '"Event Support" in cmbDeliverables.SelectedItems.Value',
        '"Media & PR" in cmbDeliverables.SelectedItems.Value',
        '"Branding & Design" in cmbDeliverables.SelectedItems.Value',
        '"Event Support" in cmbDeliverables.SelectedItems.Value && tglVIPs.Value',
        "tglBudgetRequired.Value",
    ],
```

(The old `ResetForm(frmSubmit); Navigate(scrDone…` snippet is superseded by the OnSuccess above — keep whichever exact string the page ships; the snippet list is the contract.)

- [ ] **Step 2: Run verifier** — expect FAIL on part2.
- [ ] **Step 3: Rework part2-submission-form.html** per step map: 14 steps, `of 14 steps` label, key `cbfPart2_v4`, intro rewritten (conditional-sections diagram in prose: always-on core + 4 conditional blocks), FIX-tag styling dropped (fresh build — nothing to "fix", the old app is dead; note this in the intro).
- [ ] **Step 4: Run verifier** — expect OK.
- [ ] **Step 5: Commit** `git commit -m "Part 2: fresh form build with conditional sections (b1-b14)"; git push`

---

### Task 3: Part 3 — My Requests light touch (part3-my-requests.html)

**Files:**
- Modify: `part3-my-requests.html`
- Modify: `tools/verify_pages.py` (part3 entry only if a listed snippet's text changes)
- Test: `python tools/verify_pages.py`

**Interfaces:**
- Consumes: `gblEditItem`, `frmSubmit`, `scrSubmit` from Task 2; column names from Task 1.
- Produces: step ids stay `c1`–`c11`, key stays `cbfPart3_v3` unless a step is added/removed (then bump to v4 and update verifier).

Scope (edits within existing steps — read each step, change only what the schema touches):

- Gallery labels/fields: `TargetDate` → `'Launch Date'`, subtitle text updates; Status pills unchanged.
- Detail/edit flow unchanged (`Set(gblEditItem, galMyRequests.Selected); Navigate(scrSubmit, ScreenTransition.None)` still the contract — form mode formula unchanged).
- Detail view gains read-only conditional blocks mirroring b7–b10: labels with `Visible: "Event Support" in galMyRequests.Selected.'Type of Deliverables Required'.Value` pattern (record-driven, not control-driven — one why-note on the difference).
- OnSuccess/notify snippet: keep `Notify("Changes saved.", …)` string identical (verifier).
- Any "CCD Notes" mention → "CCM Notes".

- [ ] **Step 1: Update verifier if needed** — expected: part3 snippets keep their exact strings except any that name TargetDate/CCD Notes; adjust those strings to the new names.
- [ ] **Step 2: Run verifier** — FAIL only if Step 1 changed strings.
- [ ] **Step 3: Edit part3-my-requests.html** per scope list.
- [ ] **Step 4: Run verifier** — expect OK.
- [ ] **Step 5: Commit** `git commit -m "Part 3: Launch Date + conditional read-only blocks"; git push`

---

### Task 4: Part 4 — CCD assignment workflow (part4-ccd-dashboard.html)

**Files:**
- Modify: `part4-ccd-dashboard.html`
- Modify: `tools/verify_pages.py` (part4 entry + key)
- Test: `python tools/verify_pages.py`

**Interfaces:**
- Consumes: `gblIsCCD`, `galAllRequests`, `ddStatus` from the current page; columns from Task 1.
- Produces: controls `cmbAssign`, `ddPriority`, `txtCCMNotes`; step ids `d1`–`d12`, key `cbfPart4_v3`.

Step map: d1–d4 carried over (gate check `gblIsCCD`, gallery, filters) with label updates (gallery rows gain Priority pill + Assigned-to name); new/reworked steps:

| id | Title |
|---|---|
| d5 | Connect Office365Users (add connector — Data → Add data → Office 365 Users) |
| d6 | Assign picker — `cmbAssign`: `Items: Office365Users.SearchUserV2({searchTerm: cmbAssign.SearchText, top: 15}).value`, `IsSearchable: true`, display field `DisplayName`, `DefaultSelectedItems` seeded from `galAllRequests.Selected.'Assigned to'` |
| d7 | Priority dropdown — `ddPriority.Items: Choices('Communication Requests'.Priority)`, `Default: galAllRequests.Selected.Priority` |
| d8 | Notes panel — `txtCCMNotes` (was txtCCDNotes), Default `galAllRequests.Selected.'CCM Notes'` |
| d9 | The Save patch (below) |
| d10–d12 | carried over: dialogs / reset / test steps from current d5–d10, renumbered and updated |

d9's Patch — the page's centerpiece `fx` block, verbatim:

```
Patch('Communication Requests', galAllRequests.Selected, {
    Status: ddStatus.Selected,
    Priority: ddPriority.Selected,
    'CCM Notes': txtCCMNotes.Text,
    'Assigned to': If(IsBlank(cmbAssign.Selected), Blank(), {
        Claims: "i:0#.f|membership|" & Lower(cmbAssign.Selected.Mail),
        DisplayName: cmbAssign.Selected.DisplayName,
        Email: cmbAssign.Selected.Mail,
        Department: "", JobTitle: "", Picture: ""
    }),
    'Assigned on': If(
        Lower(cmbAssign.Selected.Mail) <> Lower(galAllRequests.Selected.'Assigned to'.Email),
        Now(),
        galAllRequests.Selected.'Assigned on'
    ),
    'Completed on': If(ddStatus.Selected.Value = "Completed",
        Coalesce(galAllRequests.Selected.'Completed on', Now())
    ),
    'Completed by': If(ddStatus.Selected.Value = "Completed",
        Coalesce(galAllRequests.Selected.'Completed by', {
            Claims: "i:0#.f|membership|" & Lower(User().Email),
            DisplayName: User().FullName,
            Email: User().Email,
            Department: "", JobTitle: "", Picture: ""
        })
    )
});
Notify("Request updated.", NotificationType.Success)
```

Why-notes to include: Assigned-on stamps only when the assignee changes; Completed-on/by use Coalesce so re-saving a completed item keeps the first stamp; the If-without-else clears both when a request moves out of Completed.

- [ ] **Step 1: Update verifier (failing test).** part4 key → `cbfPart4_v3`; part4 snippets: keep the two OnStart/gblIsCCD strings and `Choices('Communication Requests'.Status)`, replace the old Patch snippet with these:

```python
        "Office365Users.SearchUserV2({searchTerm: cmbAssign.SearchText, top: 15}).value",
        "Choices('Communication Requests'.Priority)",
        "'CCM Notes': txtCCMNotes.Text",
        "Coalesce(galAllRequests.Selected.'Completed on', Now())",
        '"i:0#.f|membership|" & Lower(User().Email)',
```

- [ ] **Step 2: Run verifier** — expect FAIL on part4.
- [ ] **Step 3: Rework part4-ccd-dashboard.html** per step map: 12 steps, `of 12 steps`, key `cbfPart4_v3`, intro updated (dashboard now assigns, prioritizes, completes).
- [ ] **Step 4: Run verifier** — expect OK.
- [ ] **Step 5: Commit** `git commit -m "Part 4: assignment workflow (assign/priority/complete stamps)"; git push`

---

### Task 5: Part 5 — flows (part5-flows-golive.html)

**Files:**
- Modify: `part5-flows-golive.html`
- Modify: `tools/verify_pages.py` (part5 entry + key)
- Test: `python tools/verify_pages.py`

**Interfaces:**
- Consumes: column internal names from Task 1 (flow tokens are internal names: `LaunchDate`, `TypeOfDeliverables`, `AssignedTo`, …).
- Produces: step ids `e1`–`e14`, key `cbfPart5_v3`.

Scope:

1. **Existing email bodies** (new-request → CCD; status-change → requester): insert rows for Division (`body/Division/Value`), Launch Date (`formatDateTime(triggerOutputs()?['body/LaunchDate'], 'dd MMM yyyy')`), Deliverables, and Priority (status email only, `body/Priority/Value` with `coalesce(…, 'Not set')`). Multi-choice Deliverables needs the two-action pattern, taught once as its own sub-block in the relevant step:
   - **Select — Deliverables**: From `triggerOutputs()?['body/TypeOfDeliverables']`, Map (switch to text mode) `item()?['Value']`
   - In the email body: `join(body('Select_-_Deliverables'), ', ')`
2. **Audit flow**: ChangeSummary wording updated to new column names; structure untouched.
3. **New steps e-13/e-14 (numbers per final layout): assignment-notification flow** (flagged optional in an intro note — "cut this flow if CCD doesn't want assignment emails"):
   - Trigger: When an item is created **or modified** (Communication Requests), trigger condition left off; first action **Get changes for an item or file (properties only)** with `Since: triggerOutputs()?['body/{TriggerWindowStartToken}']`, `Until: triggerOutputs()?['body/{TriggerWindowEndToken}']`
   - Condition: `outputs('Get_changes_for_an_item_or_file_(properties_only)')?['body/ColumnHasChanged/AssignedTo']` is equal to `true` **and** `AssignedTo` is not blank (expression `empty(triggerOutputs()?['body/AssignedTo'])` is equal to `false`)
   - Yes branch: **Send an email (V2)** — To: `triggerOutputs()?['body/AssignedTo/Email']`; Subject: `New assignment: ` + Title token. Body, verbatim (tokens in ⚡ chips as elsewhere):

     ```
     Hi,

     A communication request has been assigned to you.

     Request: [Title]
     Division: [Division Value]
     Launch date: [formatDateTime(triggerOutputs()?['body/LaunchDate'], 'dd MMM yyyy')]
     Priority: [coalesce(triggerOutputs()?['body/Priority/Value'], 'Not set')]

     Open it in the CCD dashboard to review the details and update the status:
     [Link to item]

     — Communication Briefing (automated)
     ```
   - Test step: assign someone in the Part 4 dashboard, confirm the email.
4. Step renumbering to `e1`–`e14`, progress label `of 14 steps`, key `cbfPart5_v3`, go-live checklist updated (new columns spot-check, optional flow noted).

- [ ] **Step 1: Update verifier (failing test).** part5 key → `cbfPart5_v3`; part5 snippets: keep the three existing strings, add:

```python
        "join(body('Select_-_Deliverables'), ', ')",
        "formatDateTime(triggerOutputs()?['body/LaunchDate'], 'dd MMM yyyy')",
        "ColumnHasChanged/AssignedTo",
        "triggerOutputs()?['body/AssignedTo/Email']",
```

- [ ] **Step 2: Run verifier** — expect FAIL on part5.
- [ ] **Step 3: Rework part5-flows-golive.html** per scope; keep new-designer wording with classic fallbacks throughout.
- [ ] **Step 4: Run verifier** — expect OK.
- [ ] **Step 5: Commit** `git commit -m "Part 5: email fields for new schema + optional assignment flow (e1-e14)"; git push`

---

### Task 6: index.html + cross-page consistency

**Files:**
- Modify: `index.html`
- Test: `python tools/verify_pages.py`

**Interfaces:**
- Consumes: final step counts from Tasks 1–5 (15/14/11/12/14).

- [ ] **Step 1: Update index.html** — part cards' descriptions and step counts (Part 1 "the full 34-column schema", Part 2 "conditional sections", Part 4 "assign, prioritise, complete", Part 5 "3 flows + optional assignment email"); any schema mentions in the hero/TL;DR; keep the simple-requester-experience framing note.
- [ ] **Step 2: Grep sweep for stragglers** — `grep -niE "TargetDate|Target Date|RequestDetails|Request Details|Request Subject|CCDNotes|CCD Notes|Department" *.html` must return only intentional hits (e.g. Part 1's note that Division replaced Department, if written); fix the rest. `grep -c 'gate.js' *.html` = 0 per file.
- [ ] **Step 3: Run verifier** — expect `OK — 6 pages verified`.
- [ ] **Step 4: Commit** `git commit -m "Index + cross-page cleanup for real schema"; git push`

---

### Task 7: Browser QA

**Files:** none (verification only)

- [ ] **Step 1:** `python -m http.server 8000` (background) and open `http://localhost:8000/` via the Chrome tools.
- [ ] **Step 2:** On each of the 6 pages: no console errors; progress label matches step count; mark-done + copy buttons work on one step; new sections render (Part 1 a3–a9 fxgroups, Part 2 b7–b10 Visible formulas, Part 4 d9 Patch block, Part 5 assignment flow step).
- [ ] **Step 3:** Fix anything found, re-run verifier, commit fixes.

---

### Task 8: Deploy + live verification

**Files:** none

- [ ] **Step 1:** Confirm clean tree (`git status`), push already done per-task; confirm GitHub Pages workflow/branch picked up the last commit.
- [ ] **Step 2:** Open the live Pages URL, spot-check index + Part 1 a3 + Part 2 b7 + Part 4 d9 render with the new content.
- [ ] **Step 3:** Update memory (`communication-html-guide-site.md`: new schema, step counts, keys) and the Obsidian project note's log + next steps.
