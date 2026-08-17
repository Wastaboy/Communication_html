# Real-Schema Rework — Communication Briefing Guides

**Date:** 2026-08-17
**Status:** Approved design, pending implementation
**Source of truth:** `comms.txt` export of the requested list schema (39 columns: 1 Title + 34 custom + 4 system).

## Why

The client supplied the real column list for Communication Requests. The tutorial
currently teaches a 6-column list (Title/Request Subject, Department, RequestDetails,
TargetDate, Status, CCDNotes). All five parts are reworked around the real schema.

## Decisions (settled with the user)

1. **Build from scratch** — Part 1 still teaches creating the list and every column;
   the tutorial stays self-contained.
2. **Choice values are proposed defaults** — flagged *confirm with CCD* in the pages;
   only the 22-division list and the 3 status values are carried over as known-good.
3. **Part 2 uses conditional sections** — Type of Deliverables Required (multi-select)
   and Budget Required drive section visibility; no wizard, no flat 25-field form.
4. **Team stays "CCD"** everywhere; only the column is `CCMNotes` / "CCM Notes",
   matching the real list.
5. **Part 4 gains the full assignment workflow** — assign person (stamps Assigned on),
   Priority, and Completed stamping (Completed on/by).
6. The existing Power Apps build does not survive; Part 2 is a fresh build, not a delta.

## Part 1 — Communication Requests schema

Conventions unchanged: create with **space-free internal name**, rename display label
afterwards; plain text (no rich text) on all multi-line columns; Title keeps its name
(the old "Request Subject" rename is dropped). Site, Audit Log list, versioning,
attachments, and item-level privacy steps are unchanged.

34 custom columns, built in this order (matches comms.txt order):

| # | Internal name | Display label | Type | Options / defaults |
|---|---|---|---|---|
| 1 | `Division` | Division | Choice | The existing 22-division block (was "Department"); no default |
| 2 | `LaunchDate` | Launch Date | Date and time | Include time: No |
| 3 | `TypeOfDeliverables` | Type of Deliverables Required | Choice | **Multi-select: Yes.** Values below; no default |
| 4 | `PurposeObjective` | Purpose Objective | Multiple lines | Plain text |
| 5 | `BackgroundContext` | Background Context | Multiple lines | Plain text |
| 6 | `TargetAudience` | Target Audience | Choice | **Multi-select: Yes.** Values below; no default |
| 7 | `AudienceNotes` | Audience Notes | Multiple lines | Plain text |
| 8 | `DesiredOutcome` | Desired Outcome | Multiple lines | Plain text |
| 9 | `Budget` | Budget | Currency | No default |
| 10 | `BudgetStatus` | Budget Status | Choice | Values below; no default |
| 11 | `PRKeyMessages` | PR - Key Messages | Multiple lines | Plain text |
| 12 | `PRSpokespersons` | PR - Spokespersons | Single line | |
| 13 | `SupportingReferences` | Supporting References | Multiple lines | Plain text |
| 14 | `EventName` | Event Name | Single line | |
| 15 | `EventDescription` | Event Description | Multiple lines | Plain text |
| 16 | `EventStartDate` | Event Start Date | Date and time | Include time: **Yes** |
| 17 | `EventEndDate` | Event End Date | Date and time | Include time: **Yes** |
| 18 | `EventLocation` | Event Location | Single line | |
| 19 | `EventExpectedAttendance` | Event Expected Attendance | Number | No decimals |
| 20 | `EventSpeakers` | Event Speakers | Multiple lines | Plain text |
| 21 | `EventVIPsAttending` | Event VIPs Attending | Yes/No | Default No |
| 22 | `VIPProtocols` | VIPs Dignitaries Attending Protocols | Multiple lines | Plain text |
| 23 | `EventMediaExpected` | Event Media Expected | Yes/No | Default No |
| 24 | `BrandingRequirements` | Branding Requirements | Multiple lines | Plain text |
| 25 | `BrandingDesignExists` | Branding Design Exists | Yes/No | Default No |
| 26 | `BrandingPartnerAssets` | Branding Partner Assets | Yes/No | Default No |
| 27 | `BudgetRequired` | Budget Required | Yes/No | Default No |
| 28 | `Status` | Status | Choice | Submitted / In Progress / Completed; default **Submitted** |
| 29 | `AssignedTo` | Assigned to | Person or Group | Single person |
| 30 | `AssignedOn` | Assigned on | Date and time | Include time: Yes; set by app |
| 31 | `Priority` | Priority | Choice | Low / Medium / High / Urgent; no default (CCD sets at triage) |
| 32 | `CCMNotes` | CCM Notes | Multiple lines | Plain text (replaces CCDNotes) |
| 33 | `CompletedOn` | Completed on | Date and time | Include time: Yes; set by app |
| 34 | `CompletedBy` | Completed by | Person or Group | Single person; set by app |

Modified, Created, Created By, Modified By are built-in — no steps.

### Proposed choice values (each carries a *confirm with CCD* note in the page)

- **TypeOfDeliverables:** Event Support · Media & PR · Branding & Design ·
  Digital & Social Media · Internal Communication · Print & Publications ·
  Video & Photography
- **TargetAudience:** Internal Staff · External Public · Media · Customers ·
  Partners & Stakeholders · VIPs & Dignitaries
- **BudgetStatus:** Approved · Pending Approval · Not Yet Requested

## Part 2 — Requester form (fresh build)

Existing conventions carry over: typed globals in App.OnStart (`gblEditItem`
seeded with `LookUp('Communication Requests', false)`), dialog overlays with
explicit Visible on every control, Patch-based save, red FIX-tag styling where
the old build differs.

**Always visible:** Title, Division, Launch Date, Type of Deliverables Required,
Purpose Objective, Background Context, Target Audience, Audience Notes,
Desired Outcome, Supporting References, Budget Required (toggle).

**Conditional sections** (one `Visible` pattern taught once, then reused):

| Section | Fields | Visible when |
|---|---|---|
| Budget | Budget, Budget Status | `tglBudgetRequired.Value` |
| PR | PR - Key Messages, PR - Spokespersons | `"Media & PR" in cmbDeliverables.SelectedItems.Value` |
| Event | Event Name … Event Media Expected (9 fields) | `"Event Support" in cmbDeliverables.SelectedItems.Value` |
| — VIP protocols | VIPs Dignitaries Attending Protocols | Event section visible **and** `tglVIPs.Value` |
| Branding | Branding Requirements, Design Exists, Partner Assets | `"Branding & Design" in cmbDeliverables.SelectedItems.Value` |

Multi-select choice columns bind combo boxes to `Choices()`; Patch passes
`SelectedItems` directly. Hidden sections Patch blank/default values — the page
teaches this explicitly so stale values from a deselected deliverable type
don't linger on edit.

Required-field validation lives in the app (list-level Required is all off in
the real schema): Title, Division, Launch Date, Type of Deliverables, Purpose
Objective at minimum.

## Part 3 — My Requests (light touch)

- Gallery/labels updated to new names (Launch Date replaces Target Date, etc.).
- Detail view gains the conditional blocks read-only, using the same Visible
  logic driven by the record's stored values (show a block only if it has data
  or its deliverable type is selected).
- Status logic unchanged.

## Part 4 — CCD Dashboard (assignment workflow)

Existing dashboard (status change + notes) is extended, not rebuilt:

- **Assign:** person picker combo backed by `Office365Users.SearchUserV2`
  (connector added in this part). Saving an assignment patches `AssignedTo`
  (person record built from the selected user) and stamps `AssignedOn: Now()`
  only when the assignee actually changed.
- **Priority:** dropdown over `Choices('Communication Requests'.Priority)`.
- **Complete:** when Status is saved as Completed, the same Patch stamps
  `CompletedOn: Now()` and `CompletedBy` (current user via `User()`); moving
  out of Completed clears both.
- **CCM Notes** replaces CCD Notes in the notes panel.
- Dashboard list view gains Priority and Assigned to columns.

## Part 5 — Flows

Flow structure unchanged (new-designer wording kept). Changes:

- **Email bodies** (new-request notification to CCD, status-change email to
  requester) gain: Division, Launch Date, Type of Deliverables Required,
  Priority (status email only), and link fields as today.
- **Audit flow:** unchanged shape; ChangeSummary wording updated to new
  column names.
- **New, optional (flagged cut-if-unwanted):** assignment notification —
  on item modified, use *Get changes for an item or file (properties only)*
  to detect `AssignedTo` changed, then email the assignee. One flow, one
  condition, one Send an email (V2).

## Execution

1. In-place rework of the five part pages + `index.html`, preserving template
   conventions (fxgroups, copy chips, props tables, step IDs, localStorage keys —
   keys bumped where a page's step list changes shape).
2. `tools/verify_pages.py` updated to the new snippets/columns.
3. Commit per part (git autopilot: push after each), `verify_pages.py` green +
   browser QA over `http://`, then deploy to GitHub Pages and verify live.
4. No gate.js anywhere (standing rule).

## Out of scope

- Migrating data or the existing half-built Power App (declared dead).
- Building the SharePoint list or flows ourselves — this repo ships guides only.
- Wizard/multi-screen form UX.
