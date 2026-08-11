# Communication Briefing Form Guide Series — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and deploy six interactive HTML guide pages (index + 5 parts) that walk the user through deploying BBK's Communication Briefing Form (SharePoint + Power Apps + Power Automate), live on GitHub Pages.

**Architecture:** Static, self-contained HTML pages generated from the proven template at `C:\Users\MCPC -902\Projects\3rd_party_html\template.html` (gate-free, inline CSS/JS, localStorage progress, tap-to-copy chips). Content per page comes verbatim from this plan. A small Python verify script gates every page edit.

**Tech Stack:** Plain HTML/CSS/JS (IBM Plex fonts via Google Fonts), Python 3 for verification, GitHub Pages for hosting.

## Global Constraints

- **No `gate.js` anywhere.** `grep -c 'gate.js' *.html` must return 0 for every page (Zscaler phishing-flag lesson, 3rd_party_html 2026-07-20).
- Template source of truth: `template.html` (copied into this repo by Task 1). Follow its canonical step block comment exactly: `<code class="cc">` = amber tap-to-copy value; `<kbd class="ui">` = navy click-target; `<kbd class="key">` = keyboard press; `.note.why/.warn/.tip` callouts; every step ends with `.note.check` then `button.done`.
- HTML-escape all formulas inside `.fx` blocks (`&amp; &lt; &gt;`) — copied text must be the exact formula.
- Stable filenames, no dates: `index.html`, `part1-foundation.html`, `part2-submission-form.html`, `part3-my-requests.html`, `part4-ccd-dashboard.html`, `part5-flows-golive.html`.
- Step-id prefixes / localStorage keys: part1 `a`/`cbfPart1_v1`, part2 `b`/`cbfPart2_v1`, part3 `c`/`cbfPart3_v1`, part4 `d`/`cbfPart4_v1`, part5 `e`/`cbfPart5_v1`. Index has no steps, no sticky progress bar.
- Every part page footer links the index and the other four parts.
- "Confirm with CCD" items render as `.note.warn` callouts with `<b>Confirm with CCD</b>`.
- Phase-1 rule stated on index and part1: **no approval/rejection workflow anywhere**.
- Test over `http://` (`python -m http.server`), never `file://`.
- Commit after every task; push after every commit.

## Canonical build values (used across tasks — keep identical everywhere)

- SharePoint site: **Communication Briefing** (user records their tenant URL into a placeholder; every later reference uses "your site").
- List 1: **Communication Requests** — columns created with space-free names, then display-renamed:
  | Create as | Rename display to | Type | Details |
  |---|---|---|---|
  | Title (built-in) | Request Subject | Single line | Required |
  | `Department` | Department | Choice | 22 BBK divisions (list below) |
  | `RequestDetails` | Request Details | Multiple lines, plain text | |
  | `TargetDate` | Target Date | Date only | |
  | `Status` | Status | Choice | Submitted / In Progress / Completed; default **Submitted** |
  | `CCDNotes` | CCD Notes | Multiple lines, plain text | |
- Department choice values (verbatim, from BBK division list): CE Office; Operations & Administration; Information Technology; Financial Planning & Control; Human Resources; Strategy & Transformation; Marketing & Communications; Corporate & Business Development; Remedial; In - Business Risk; Treasury & Investment; Private Banking & Wealth Management; International Banking; Wholesale Banking; Retail Banking; Corporate Secretariat; Information Security; Risk Management; Credit & Overseas Risk; Compliance & AML; Internal Audit; Legal. (⚑ confirm list current with CCD.)
- List 2: **Audit Log** — `RequestID` (Number), `Action` (Choice: Created / Edited / Status Changed), `ModifiedBy` (Single line), `ModifiedDateTime` (Date and time, include time), `ChangeSummary` (Multiple lines).
- Canvas app: **Communication Briefing Form**, tablet format. Screens `scrSubmit`, `scrMyRequests`, `scrDashboard`.
- Control names (complete roster — reuse exactly):
  - scrSubmit: `recSubmitHeader`, `lblSubmitTitle`, `btnGoMyRequests`, `frmSubmit`, `btnSubmit`
  - scrMyRequests: `recMyHeader`, `lblMyTitle`, `btnGoSubmit`, `btnMyRefresh`, `galMyRequests` (inside: `lblReqTitle`, `lblReqStatus`, `lblReqDate`), `lblMyEmpty`, `lblDetNotes`, `btnEditRequest`
  - scrDashboard: `recDashHeader`, `lblDashTitle`, `btnGoDashboard` (lives on scrMyRequests), `txtDashSearch`, `btnChipAll`, `btnChipSubmitted`, `btnChipProgress`, `btnChipCompleted`, `galAllRequests` (inside: `lblDashReqTitle`, `lblDashReqStatus`, `lblDashReqDept`), `ddStatus`, `txtCCDNotes`, `btnSaveUpdate`, `lblDashEmpty`
- Globals: `gblEditItem`, `gblIsCCD`, `gblStatusFilter` (text: "All"/"Submitted"/"In Progress"/"Completed").
- Colors in-app: navy `RGBA(31, 59, 110, 1)`, amber `RGBA(224, 138, 30, 1)`, green `RGBA(31, 138, 82, 1)`.
- Flows: `CBF - New Request Notification`, `CBF - Audit Logger`, `CBF - Status Change Notification` (optional). Recipient default `Corporate.Communications@bbkonline.com` ⚑.

---

### Task 1: Repo scaffold — template, verify script, CLAUDE.md

**Files:**
- Create: `template.html` (copy of `C:\Users\MCPC -902\Projects\3rd_party_html\template.html`, verbatim)
- Create: `tools/verify_pages.py`
- Create: `CLAUDE.md`

**Interfaces:**
- Produces: `template.html` placeholder tokens (`__PAGE_TITLE__`, `__PAGE_KICKER__`, `__PAGE_H1__`, `__PAGE_SUB__`, `__PAGE_META_PILLS__`, `__STEP_COUNT__`, `__PAGE_CONTENT__`, `__PAGE_FOOTER_LINE__`, `__SERIES_LINKS__`, `__STORAGE_KEY__`) that Tasks 2–7 fill; `tools/verify_pages.py` runnable as `python tools/verify_pages.py` exiting 0 on pass, 1 with messages on fail.

- [ ] **Step 1: Copy the template**

```bash
cp "/c/Users/MCPC -902/Projects/3rd_party_html/template.html" "/c/Users/MCPC -902/Projects/Communication_html/template.html"
```

- [ ] **Step 2: Write `CLAUDE.md`**

```markdown
# Project rules

- **No password gate:** pages in this repo must NOT load `gate.js` (Zscaler
  phishing flag hit 3rd_party_html on 2026-07-20 for gate + bank vocabulary).
  Verify with: `grep -c 'gate.js' *.html` (exactly 0 per file).
- Pages are generated from `template.html`; follow its canonical step block.
- Run `python tools/verify_pages.py` after any page edit.
- Test over `http://` (`python -m http.server`), never `file://`.
- Design spec: `docs/superpowers/specs/2026-08-11-communication-briefing-guides-design.md`.
```

- [ ] **Step 3: Write `tools/verify_pages.py`** — checks every registered page for: zero `gate.js` mentions; storage key present; expected sequential step ids with matching uppercase `.num`; a `button.done` and `.note.check` per step; footer links to the other five pages; `__`-style unfilled template tokens absent; required formula snippets present (decoded from HTML entities). Registry starts empty of snippets; Tasks 2–6 append theirs.

```python
"""Scripted verification of the Communication Briefing guide series."""
import html, re, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ALL = ["index.html", "part1-foundation.html", "part2-submission-form.html",
       "part3-my-requests.html", "part4-ccd-dashboard.html", "part5-flows-golive.html"]
PAGES = {
    "part1-foundation.html": {"prefix": "a", "key": "cbfPart1_v1"},
    "part2-submission-form.html": {"prefix": "b", "key": "cbfPart2_v1"},
    "part3-my-requests.html": {"prefix": "c", "key": "cbfPart3_v1"},
    "part4-ccd-dashboard.html": {"prefix": "d", "key": "cbfPart4_v1"},
    "part5-flows-golive.html": {"prefix": "e", "key": "cbfPart5_v1"},
}
SNIPPETS = {}  # filename -> [verbatim decoded formula strings]; filled by later tasks

def fail(msgs, m): msgs.append(m)

def check(name, cfg, msgs):
    p = REPO / name
    if not p.exists(): return fail(msgs, f"{name}: MISSING")
    t = p.read_text(encoding="utf-8")
    if "gate.js" in t: fail(msgs, f"{name}: references gate.js")
    if re.search(r"__[A-Z_]+__", t): fail(msgs, f"{name}: unfilled template token")
    if cfg:
        if cfg["key"] not in t: fail(msgs, f"{name}: storage key {cfg['key']} missing")
        ids = re.findall(r'<details class="step[^"]*" id="([a-z]+\d+)"', t)
        want = [f"{cfg['prefix']}{i}" for i in range(1, len(ids) + 1)]
        if ids != want: fail(msgs, f"{name}: step ids {ids} != {want}")
        if not ids: fail(msgs, f"{name}: no steps found")
        for sid in ids:
            m = re.search(rf'id="{sid}".*?</details>', t, re.S)
            body = m.group(0) if m else ""
            if 'class="done"' not in body: fail(msgs, f"{name}#{sid}: no done button")
            if "note check" not in body: fail(msgs, f"{name}#{sid}: no check note")
        n = len(ids)
        if f"of {n} steps" not in t: fail(msgs, f"{name}: progress label != {n} steps")
    others = [o for o in ALL if o != name]
    for o in others:
        if o not in t: fail(msgs, f"{name}: footer/link missing {o}")
    decoded = html.unescape(t)
    for snip in SNIPPETS.get(name, []):
        if snip not in decoded: fail(msgs, f"{name}: missing formula: {snip[:60]}...")

def main():
    msgs = []
    for name in ALL:
        check(name, PAGES.get(name), msgs)
    if msgs:
        print("\n".join("FAIL " + m for m in msgs)); return 1
    print(f"OK — {len(ALL)} pages verified"); return 0

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run it to verify it fails correctly** — `python tools/verify_pages.py` → expect FAIL lines: all six pages MISSING. That proves the harness works before any page exists.

- [ ] **Step 5: Commit**

```bash
git add template.html tools/verify_pages.py CLAUDE.md
git commit -m "Scaffold: template, verify script, project rules (no gate.js)"
git push
```

---

### Task 2: `part1-foundation.html` — SharePoint Foundation (steps a1–a9)

**Files:**
- Create: `part1-foundation.html` (from `template.html`)

**Interfaces:**
- Consumes: template tokens from Task 1.
- Produces: the site/list/column names in "Canonical build values" — every later part references them verbatim.

**Page header:** kicker `BBK · CCD · Part 1 of 5`; H1 `SharePoint Foundation`; sub: "Two lists, versioning, and item-level privacy — the data layer the whole Communication Briefing system stands on."; meta pills: `<span><b>~40 min</b> hands-on</span> <span><b>SharePoint</b> only</span> <span><b>No code</b> yet</span>`. Storage key `cbfPart1_v1`.

**Intro blocks (before steps):** a `.tldr` (what Part 1 builds); a `.pane` prerequisites list (M365 account with permission to create SharePoint team sites — otherwise ask IT; the 5 CCD member names; Phase-1 rule: **no approval/rejection workflow anywhere in this build** as a `.note.why`); the color-legend section explaining chips (copy the legend wording style from the template's comment: amber = tap-to-copy value, navy = click it, key = press it).

**Steps (each `details.step`, sub-steps as `ol.steps2`, ends with `.note.check` + done button):**

- **a1 — Create the team site.** office.com → app launcher → <kbd class="ui">SharePoint</kbd> → <kbd class="ui">+ Create site</kbd> → <kbd class="ui">Team site</kbd> → <kbd class="ui">Standard team</kbd>. Name <code class="cc">Communication Briefing</code>, privacy <kbd class="ui">Private</kbd>, language English → <kbd class="ui">Finish</kbd>. `.note.tip`: if site creation is disabled in the tenant, ask IT to create it and grant you Owner. Check: the new site opens and its URL ends in `/sites/CommunicationBriefing` (record your URL — every later part calls it "your site").
- **a2 — Create the Communication Requests list.** On the site: <kbd class="ui">+ New</kbd> → <kbd class="ui">List</kbd> → <kbd class="ui">Blank list</kbd> → name <code class="cc">Communication Requests</code> → <kbd class="ui">Create</kbd>. Check: empty list with a Title column.
- **a3 — Add the columns.** For each: <kbd class="ui">+ Add column</kbd> → type → <kbd class="ui">Next</kbd> → name → save. Create `Department` (Choice; paste the 22 BBK divisions — render the full list as one `.fx` copy block, one value per line, plus a `.note.warn` **Confirm with CCD** that the division list is current), `RequestDetails` (Multiple lines of text, plain text), `TargetDate` (Date and time → date only), `Status` (Choice: <code class="cc">Submitted</code>, <code class="cc">In Progress</code>, <code class="cc">Completed</code>; default value <code class="cc">Submitted</code>; `.note.warn` **Confirm with CCD** on exact status names), `CCDNotes` (Multiple lines, plain text). Check: five new columns visible.
- **a4 — Rename display names.** Column header → <kbd class="ui">Column settings</kbd> → <kbd class="ui">Rename</kbd>: Title → <code class="cc">Request Subject</code>, RequestDetails → <code class="cc">Request Details</code>, TargetDate → <code class="cc">Target Date</code>, CCDNotes → <code class="cc">CCD Notes</code>. `.note.why`: creating space-free names first keeps internal names clean for flows; renaming after only changes the label. Check: headers read Request Subject / Department / Request Details / Target Date / Status / CCD Notes.
- **a5 — Versioning and attachments.** Gear → <kbd class="ui">List settings</kbd> → <kbd class="ui">Versioning settings</kbd> → "Create a version each time…" <kbd class="ui">Yes</kbd> → <kbd class="ui">OK</kbd>. Then <kbd class="ui">Advanced settings</kbd> → Attachments <kbd class="ui">Enabled</kbd> (usually already). Check: both confirmed in settings.
- **a6 — Item-level permissions.** List settings → <kbd class="ui">Advanced settings</kbd> → Item-level Permissions: Read access <kbd class="ui">Read items that were created by the user</kbd>; Create and Edit access <kbd class="ui">Create items and edit items that were created by the user</kbd> → <kbd class="ui">OK</kbd>. `.note.why`: this is what hides other people's requests; users with **Manage Lists / Full Control** (the CCD owners you add in a8) bypass it and see everything. Check: settings saved.
- **a7 — Create the Audit Log list.** <kbd class="ui">+ New</kbd> → <kbd class="ui">List</kbd> → <kbd class="ui">Blank list</kbd> → <code class="cc">Audit Log</code>. Add columns: `RequestID` (Number), `Action` (Choice: <code class="cc">Created</code> / <code class="cc">Edited</code> / <code class="cc">Status Changed</code>), `ModifiedBy` (Single line of text), `ModifiedDateTime` (Date and time, include time <kbd class="ui">Yes</kbd>), `ChangeSummary` (Multiple lines of text). `.note.why`: text ModifiedBy keeps the Part-5 flow simple and export-friendly. Check: list with five columns.
- **a8 — Grant access.** Site home → gear → <kbd class="ui">Site permissions</kbd> → <kbd class="ui">Add members</kbd> → add the five CCD members (Rawan AlQattan, Rafa Kaddoura, Abdulrahman Danish, Samar Qannati, Noora AlFaihani) as <kbd class="ui">Owner</kbd>; add staff as Members — for all-staff access add <code class="cc">Everyone except external users</code> as <kbd class="ui">Member</kbd>. `.note.warn` **Confirm with CCD/IT**: whether all staff or a pilot group get access first. Check: permissions panel lists CCD as owners.
- **a9 — Verify the foundation (F5 stage).** Create a test item in Communication Requests (Request Subject <code class="cc">TEST - delete me later</code>), edit it once, then <kbd class="ui">Version history</kbd> on the item — expect version 2.0 with your name and timestamps. Confirm Status default shows Submitted. `.note.check` list: two lists exist; six display columns correct; versioning on; item-level permissions set; CCD owners added; test item shows version history. `.note.tip`: keep the test item — Part 2's first F5 test edits it and Part 5's flow tests delete it.

**Footer:** `Part 1 of 5 — the Communication Briefing Form build.` + series links to all other pages.

- [ ] **Step 1: Write the page** from `template.html`, filling every `__TOKEN__`, with the 9 steps above (step count 9 in the progress label).
- [ ] **Step 2: Register formulas in verify script.** Append to `SNIPPETS` in `tools/verify_pages.py`: `"part1-foundation.html": ["Everyone except external users", "Create items and edit items that were created by the user"]`.
- [ ] **Step 3: Run verification** — `python tools/verify_pages.py`. Expect: part1 passes all checks except cross-links to not-yet-existing pages will FAIL for the five missing files — confirm part1's own FAIL lines are only "MISSING" entries for other pages, none about part1 content.
- [ ] **Step 4: Visual check** — `python -m http.server 8000` in the repo, open `http://localhost:8000/part1-foundation.html`: legend renders, chips copy on tap, done buttons update the counter, reset works, reload keeps progress.
- [ ] **Step 5: Commit**

```bash
git add part1-foundation.html tools/verify_pages.py
git commit -m "Part 1: SharePoint foundation guide (two lists, versioning, item-level privacy)"
git push
```

---

### Task 3: `part2-submission-form.html` — App Shell + Submission Form (steps b1–b10)

**Files:**
- Create: `part2-submission-form.html`

**Interfaces:**
- Consumes: site/list names from Part 1; template tokens.
- Produces: app name, `scrSubmit` control roster, `frmSubmit`/`btnSubmit` behavior that Part 3 extends (`gblEditItem` hooks are added in Part 3, not here).

**Page header:** kicker `BBK · CCD · Part 2 of 5`; H1 `App Shell + Submission Form`; sub: "A canvas app whose submit screen feels like a Google Form — fields, validation, attachments, done."; meta pills `~45 min`, `Power Apps`, `First F5 test`. Storage key `cbfPart2_v1`. `.tldr` + prerequisites `.pane` (Part 1 finished; make.powerapps.com access in the BBK environment).

**Steps:**

- **b1 — Create the app.** make.powerapps.com → check environment (top-right) → <kbd class="ui">+ Create</kbd> → <kbd class="ui">Blank app</kbd> → <kbd class="ui">Blank canvas app</kbd> → name <code class="cc">Communication Briefing Form</code> → format <kbd class="ui">Tablet</kbd> → <kbd class="ui">Create</kbd>. Check: empty Screen1 in the studio.
- **b2 — Connect the data.** Left rail <kbd class="ui">Data</kbd> → <kbd class="ui">Add data</kbd> → search <code class="cc">SharePoint</code> → pick the SharePoint connector → sign in if prompted (`.note.warn`: first-run connection sign-in is normal — pick your BBK account) → paste your site URL → check <kbd class="ui">Communication Requests</kbd> → <kbd class="ui">Connect</kbd>. Check: 'Communication Requests' appears under Data.
- **b3 — Name the screen, add the header.** Tree view: rename Screen1 → <code class="cc">scrSubmit</code>. Insert <kbd class="ui">Rectangle</kbd> → <code class="cc">recSubmitHeader</code>: X `0`, Y `0`, Width `Parent.Width`, Height `88`, Fill `RGBA(31, 59, 110, 1)`. Insert <kbd class="ui">Text label</kbd> → <code class="cc">lblSubmitTitle</code>: Text `"Communication Briefing Form"`, X `24`, Y `0`, Height `88`, Color `White`, Size `22`, FontWeight `Semibold`. Check: navy band with white title.
- **b4 — Insert the form.** <kbd class="ui">Insert</kbd> → <kbd class="ui">Edit form</kbd> → <code class="cc">frmSubmit</code>: X `24`, Y `112`, Width `Parent.Width - 48`, Height `Parent.Height - 200`. Properties pane: Data source <kbd class="ui">Communication Requests</kbd>. DefaultMode formula `FormMode.New`. Check: form shows fields.
- **b5 — Pick and order the fields.** Properties → <kbd class="ui">Edit fields</kbd>: keep, in order, <kbd class="ui">Request Subject</kbd>, <kbd class="ui">Department</kbd>, <kbd class="ui">Request Details</kbd>, <kbd class="ui">Target Date</kbd>, <kbd class="ui">Attachments</kbd>; remove <kbd class="ui">Status</kbd> and <kbd class="ui">CCD Notes</kbd> (`.note.why`: those two are CCD-managed; requesters never set them — Status lands as its list default, Submitted). `.note.warn`: the Attachments card only works inside a form bound to SharePoint — don't try to move the control out of the form. Check: five cards, in order.
- **b6 — Make the fields friendly.** Unlock cards where needed (card → <kbd class="ui">Advanced</kbd> → <kbd class="ui">Unlock</kbd>). Request Subject card: Required `true`. Request Details data card value: Mode `TextMode.MultiLine`, Height `120`, HintText `"What is this communication about, audience, key messages…"`. Target Date: leave the date picker default. Department: default combobox is fine. Check: F-key nothing yet — visual only.
- **b7 — The submit button.** Insert <kbd class="ui">Button</kbd> → <code class="cc">btnSubmit</code>: Text `"Submit request"`, X `24`, Y `frmSubmit.Y + frmSubmit.Height + 8`, Width `220`, Height `48`, Fill `RGBA(224, 138, 30, 1)`, Color `RGBA(20, 20, 20, 1)`. OnSelect:
  `SubmitForm(frmSubmit)`
  DisplayMode:
  `If(frmSubmit.Valid, DisplayMode.Edit, DisplayMode.Disabled)`
  Check: button disabled until Request Subject has text.
- **b8 — Success and failure behavior.** frmSubmit OnSuccess:
  `Notify("Request submitted — the CCD team has been notified.", NotificationType.Success); ResetForm(frmSubmit)`
  frmSubmit OnFailure:
  `Notify("Something went wrong — your request was not saved. " & frmSubmit.Error, NotificationType.Error)`
  `.note.why`: OnFailure surfaces SharePoint rejections (lost connection, missing required) instead of failing silently. Check: formulas accepted, no red underlines.
- **b9 — First F5 test.** <kbd class="key">F5</kbd> (or ▷): fill Request Subject <code class="cc">TEST from app - delete me later</code>, pick a Department, details, a target date, attach any small file → <kbd class="ui">Submit request</kbd> → expect the green success toast and a cleared form. Then open the SharePoint list: the item exists, attachment paper-clip visible, Status = Submitted. `.note.warn`: if submit fails with a permissions error, re-check Part 1 a6/a8. Check list per above.
- **b10 — Save and publish.** <kbd class="key">Ctrl+S</kbd> (first save names it — keep <code class="cc">Communication Briefing Form</code>) → <kbd class="ui">Publish</kbd> → <kbd class="ui">Publish this version</kbd>. `.note.tip`: publish after every part so testers always see the latest. Check: "All changes saved" + published.

**Footer:** series links.

- [ ] **Step 1: Write the page** (10 steps, counter = 10).
- [ ] **Step 2: Register snippets:** `"part2-submission-form.html": ["SubmitForm(frmSubmit)", "If(frmSubmit.Valid, DisplayMode.Edit, DisplayMode.Disabled)", "Notify(\"Request submitted — the CCD team has been notified.\", NotificationType.Success); ResetForm(frmSubmit)"]`.
- [ ] **Step 3: Run `python tools/verify_pages.py`** — part1+part2 content checks pass (missing-file FAILs shrink to four).
- [ ] **Step 4: Serve and click-test** the page as in Task 2 Step 4.
- [ ] **Step 5: Commit** — `git add`, `git commit -m "Part 2: app shell + submission form guide (form, validation, attachments, first F5)"`, `git push`.

---

### Task 4: `part3-my-requests.html` — My Requests (steps c1–c10)

**Files:**
- Create: `part3-my-requests.html`

**Interfaces:**
- Consumes: `scrSubmit`, `frmSubmit`, `btnSubmit` from Part 2.
- Produces: `scrMyRequests` roster; `gblEditItem` edit pattern (Part 2's form gains Item/DefaultMode formulas here); nav buttons Part 4 extends.

**Page header:** kicker `BBK · CCD · Part 3 of 5`; H1 `My Requests`; sub: "Requesters see their own submissions, live status, CCD notes — and can edit after submitting."; meta pills `~45 min`, `Power Apps`, `Edit-after-submit`. Storage key `cbfPart3_v1`. Prereq pane: Parts 1–2 done.

**Steps:**

- **c1 — New screen.** <kbd class="ui">New screen</kbd> → <kbd class="ui">Blank</kbd> → rename <code class="cc">scrMyRequests</code>. Copy header pattern: `recMyHeader` (same X/Y/W/H/Fill as recSubmitHeader), `lblMyTitle` Text `"My Requests"` (same styling as lblSubmitTitle). Check: matching navy header.
- **c2 — Navigation both ways.** On scrSubmit insert Button `btnGoMyRequests`: Text `"My requests"`, X `Parent.Width - 244`, Y `20`, Width `220`, Height `48`, OnSelect:
  `Navigate(scrMyRequests, ScreenTransition.None)`
  On scrMyRequests insert Button `btnGoSubmit`: Text `"+ New request"`, X `Parent.Width - 244`, Y `20`, Width `220`, Height `48`, OnSelect:
  `Set(gblEditItem, Blank()); Navigate(scrSubmit, ScreenTransition.None)`
  `.note.why`: clearing `gblEditItem` here is what makes the shared form open in New mode (wired in c6). Check: both buttons navigate.
- **c3 — The gallery.** Insert <kbd class="ui">Vertical gallery</kbd> → <code class="cc">galMyRequests</code>: X `24`, Y `112`, Width `Parent.Width * 0.45`, Height `Parent.Height - 136`. Items:
  `SortByColumns(Filter('Communication Requests', 'Created By'.Email = User().Email), "Created", SortOrder.Descending)`
  `.note.warn` (delegation): filtering on 'Created By'.Email is not delegable to SharePoint — fine at CCD's volumes (< 500 items in practice, < 2000 delegation limit); for regular staff the Part 1 item-level permissions already restrict server-side, the filter mainly matters for CCD members who can see everything. Check: blue delegation underline may appear — expected; gallery shows your test items.
- **c4 — Gallery fields.** In the gallery template: `lblReqTitle` Text `ThisItem.'Request Subject'` (Semibold, Size 16); `lblReqStatus` Text `ThisItem.Status.Value`, Color:
  `Switch(ThisItem.Status.Value, "Submitted", RGBA(224, 138, 30, 1), "In Progress", RGBA(31, 59, 110, 1), "Completed", RGBA(31, 138, 82, 1), RGBA(120, 130, 145, 1))`
  ; `lblReqDate` Text `"Target: " & Text(ThisItem.'Target Date', ShortDate)`. Check: rows show subject, colored status, date.
- **c5 — Detail panel.** Right of the gallery add `lblDetNotes` (multiline label): X `galMyRequests.X + galMyRequests.Width + 24`, Y `112`, Width `Parent.Width - Self.X - 24`, Height `240`, Text:
  `If(IsBlank(galMyRequests.Selected), "Select a request on the left.", "Status: " & galMyRequests.Selected.Status.Value & Char(10) & Char(10) & "CCD notes:" & Char(10) & If(IsBlank(galMyRequests.Selected.'CCD Notes'), "— none yet —", galMyRequests.Selected.'CCD Notes'))`
  Check: selecting a row shows status + notes.
- **c6 — Wire edit-after-submit (touches Part 2's form).** On scrMyRequests insert Button `btnEditRequest`: Text `"Edit this request"`, X `lblDetNotes.X`, Y `368`, Width `220`, Height `48`, DisplayMode `If(IsBlank(galMyRequests.Selected), DisplayMode.Disabled, DisplayMode.Edit)`, OnSelect:
  `Set(gblEditItem, galMyRequests.Selected); Navigate(scrSubmit, ScreenTransition.None)`
  Then on **frmSubmit** set Item:
  `gblEditItem`
  and DefaultMode:
  `If(IsBlank(gblEditItem), FormMode.New, FormMode.Edit)`
  and lblSubmitTitle Text:
  `If(IsBlank(gblEditItem), "Communication Briefing Form", "Edit request")`
  Check: no formula errors.
- **c7 — Return after edit.** frmSubmit OnSuccess becomes:
  `Notify(If(IsBlank(gblEditItem), "Request submitted — the CCD team has been notified.", "Changes saved."), NotificationType.Success); If(IsBlank(gblEditItem), ResetForm(frmSubmit), Set(gblEditItem, Blank()); Navigate(scrMyRequests, ScreenTransition.None))`
  `.note.why`: new submissions clear for the next entry; edits bounce you back to the list. Check: formula accepted.
- **c8 — Refresh + empty state.** `btnMyRefresh` (icon button, refresh icon) top of gallery, OnSelect `Refresh('Communication Requests')`. `lblMyEmpty`: same X/Y as gallery, Text `"No requests yet — tap + New request to submit your first."`, Visible `IsEmpty(galMyRequests.AllItems)`. Check: empty state hidden while test items exist.
- **c9 — F5 test.** <kbd class="key">F5</kbd>: My requests → select the b9 test item → Edit this request → change Request Details → submit → back on My Requests with "Changes saved." Open SharePoint version history: new version logged with your name/time (the audit trail requirement working end-to-end, before flows even exist). Check list.
- **c10 — Save and publish.** <kbd class="key">Ctrl+S</kbd> → <kbd class="ui">Publish</kbd>. Check: published.

- [ ] **Step 1: Write the page** (10 steps).
- [ ] **Step 2: Register snippets:** `"part3-my-requests.html": ["SortByColumns(Filter('Communication Requests', 'Created By'.Email = User().Email), \"Created\", SortOrder.Descending)", "Set(gblEditItem, galMyRequests.Selected); Navigate(scrSubmit, ScreenTransition.None)", "If(IsBlank(gblEditItem), FormMode.New, FormMode.Edit)"]`.
- [ ] **Step 3: Run verify script** (three missing-file FAILs remain).
- [ ] **Step 4: Serve and click-test.**
- [ ] **Step 5: Commit** — `"Part 3: My Requests guide (own items, status, CCD notes, edit-after-submit)"`, push.

---

### Task 5: `part4-ccd-dashboard.html` — CCD Dashboard (steps d1–d10)

**Files:**
- Create: `part4-ccd-dashboard.html`

**Interfaces:**
- Consumes: screens/globals from Parts 2–3.
- Produces: `scrDashboard` roster; `gblIsCCD`; `gblStatusFilter`.

**Page header:** kicker `BBK · CCD · Part 4 of 5`; H1 `CCD Dashboard`; sub: "The team view: every request, status filters, search, updates that requesters see instantly, and Excel export."; meta pills `~45 min`, `Power Apps`, `CCD only`. Storage key `cbfPart4_v1`.

**Steps:**

- **d1 — Screen + CCD gate.** New blank screen → <code class="cc">scrDashboard</code>; header `recDashHeader`/`lblDashTitle` Text `"CCD Dashboard"` (same pattern as before). App OnStart (App object in tree view):
  `Set(gblIsCCD, Lower(User().Email) in ["rawan.alqattan@bbkonline.com", "rafa.kaddoura@bbkonline.com", "abdulrahman.danish@bbkonline.com", "samar.qannati@bbkonline.com", "noora.alfaihani@bbkonline.com"])`
  `.note.warn` **Confirm with CCD/IT**: replace all five with the real addresses from Outlook — the format here is a guess; wrong addresses lock the team out of the dashboard (data itself stays safe: SharePoint owners see everything regardless). On scrMyRequests add Button `btnGoDashboard`: Text `"CCD dashboard"`, X `Parent.Width - 488`, Y `20`, Width `220`, Height `48`, Visible `gblIsCCD`, OnSelect `Navigate(scrDashboard, ScreenTransition.None)`. Check: button visible for you only if your email is in the list (add yourself while building, remove at go-live — `.note.tip`).
- **d2 — Filter chips.** Four buttons across the top, Y `112`, Width `170`, Height `40`, X `24` / `210` / `396` / `582`: `btnChipAll` Text `"All"` OnSelect `Set(gblStatusFilter, "All")`; `btnChipSubmitted` Text `"Submitted"` OnSelect `Set(gblStatusFilter, "Submitted")`; `btnChipProgress` Text `"In Progress"` OnSelect `Set(gblStatusFilter, "In Progress")`; `btnChipCompleted` Text `"Completed"` OnSelect `Set(gblStatusFilter, "Completed")`. Each chip Fill:
  `If(gblStatusFilter = Self.Text, RGBA(31, 59, 110, 1), RGBA(238, 240, 246, 1))`
  and Color `If(gblStatusFilter = Self.Text, White, RGBA(31, 59, 110, 1))`. App OnStart append `; Set(gblStatusFilter, "All")` — full OnStart shown as one `.fx` block. Check: chips toggle highlight.
- **d3 — Search box.** <code class="cc">txtDashSearch</code> Text input: X `24`, Y `168`, Width `540`, Height `44`, HintText `"Search by request subject…"`. Check: renders.
- **d4 — The all-requests gallery.** `galAllRequests` vertical gallery: X `24`, Y `228`, Width `Parent.Width * 0.5`, Height `Parent.Height - 252`. Items:
  `SortByColumns(Filter('Communication Requests', (gblStatusFilter = "All" || Status.Value = gblStatusFilter) && (IsBlank(txtDashSearch.Text) || StartsWith(Title, txtDashSearch.Text))), "Created", SortOrder.Descending)`
  `.note.warn` delegation: StartsWith on Title delegates; the Status/choice comparison does not — same volumes argument as c3. Template fields: `lblDashReqTitle` `ThisItem.'Request Subject'`; `lblDashReqStatus` `ThisItem.Status.Value` (Switch color from c4, repeated verbatim); `lblDashReqDept` `ThisItem.Department.Value & " · " & Text(ThisItem.Created, ShortDate)`. `lblDashEmpty` Visible `IsEmpty(galAllRequests.AllItems)`, Text `"No requests match this filter."`. Check: chips + search narrow the list live.
- **d5 — Update panel: status dropdown.** Right side, `ddStatus` (classic dropdown): X `galAllRequests.X + galAllRequests.Width + 24`, Y `228`, Width `300`, Items:
  `Choices('Communication Requests'.Status)`
  Default `galAllRequests.Selected.Status.Value` — wrapped in the DefaultSelectedItems note: for the modern dropdown use DefaultSelectedItems `[galAllRequests.Selected.Status]` (`.note.tip` covers both control generations). Check: selecting a request preloads its status.
- **d6 — Update panel: notes + save.** `txtCCDNotes` Text input, Mode `TextMode.MultiLine`: X `ddStatus.X`, Y `296`, Width `Parent.Width - Self.X - 24`, Height `160`, Default `galAllRequests.Selected.'CCD Notes'`, HintText `"Notes the requester will see…"`. `btnSaveUpdate` Button: Text `"Save update"`, X `ddStatus.X`, Y `472`, Width `220`, Height `48`, DisplayMode `If(IsBlank(galAllRequests.Selected), DisplayMode.Disabled, DisplayMode.Edit)`, OnSelect:
  `Patch('Communication Requests', galAllRequests.Selected, {Status: ddStatus.Selected, 'CCD Notes': txtCCDNotes.Text}); Notify("Request updated.", NotificationType.Success)`
  `.note.why`: Patch writes only these two columns — the requester's own fields are untouched, and the requester sees the change on their My Requests screen at next refresh. Check: no formula errors.
- **d7 — F5 test: the CCD loop.** <kbd class="key">F5</kbd> → dashboard → pick the test item → status <kbd class="ui">In Progress</kbd>, notes <code class="cc">Reviewing — expect a draft by Thursday</code> → <kbd class="ui">Save update</kbd> → toast → My requests screen → the requester view shows the new status color and note. Check list.
- **d8 — Excel export.** In the SharePoint list (not the app): <kbd class="ui">Export</kbd> → <kbd class="ui">Export to Excel</kbd> → open the downloaded query — all columns land in an Excel table that refreshes on open. `.note.tip`: CCD can filter the list view first; the export honors the current view's filter. Check: xlsx opens with the requests.
- **d9 — Status names sanity check.** `.note.warn` **Confirm with CCD**: if CCD wants different status names (spec left this open), change them in ONE place — the Status column choices in SharePoint — and re-check d2's chip Texts match exactly; everything else reads values dynamically. Single sub-step + check.
- **d10 — Save and publish.** As before. Check: published.

- [ ] **Step 1: Write the page** (10 steps).
- [ ] **Step 2: Register snippets:** `"part4-ccd-dashboard.html": ["Set(gblIsCCD, Lower(User().Email) in [", "Choices('Communication Requests'.Status)", "Patch('Communication Requests', galAllRequests.Selected, {Status: ddStatus.Selected, 'CCD Notes': txtCCDNotes.Text}); Notify(\"Request updated.\", NotificationType.Success)"]`.
- [ ] **Step 3: Run verify script.**
- [ ] **Step 4: Serve and click-test.**
- [ ] **Step 5: Commit** — `"Part 4: CCD dashboard guide (filters, search, status/notes updates, Excel export)"`, push.

---

### Task 6: `part5-flows-golive.html` — Flows + Go-Live (steps e1–e12)

**Files:**
- Create: `part5-flows-golive.html`

**Interfaces:**
- Consumes: both lists (Part 1), the app (Parts 2–4).
- Produces: the three flow definitions; the go-live acceptance walkthrough.

**Page header:** kicker `BBK · CCD · Part 5 of 5`; H1 `Flows + Go-Live`; sub: "Email the team on every new request, log every edit, and walk the full acceptance checklist."; meta pills `~50 min`, `Power Automate`, `Go-live`. Storage key `cbfPart5_v1`.

**Steps:**

- **e1 — Notification flow: trigger.** make.powerautomate.com → same environment → <kbd class="ui">+ Create</kbd> → <kbd class="ui">Automated cloud flow</kbd> → name <code class="cc">CBF - New Request Notification</code> → search triggers for <code class="cc">When an item is created</code> → pick **SharePoint · When an item is created** (`.note.warn` lookalike triggers: NOT "…created or modified", NOT the "(properties only)" file trigger, NOT Dataverse "When a row is added") → <kbd class="ui">Create</kbd>. Configure Site Address = your site, List Name = <kbd class="ui">Communication Requests</kbd>. Check: trigger card filled.
- **e2 — Notification flow: the email.** <kbd class="ui">+ New step</kbd> → search <code class="cc">Send an email (V2)</code> → **Office 365 Outlook · Send an email (V2)** (first-run sign-in `.note.warn`). To: <code class="cc">Corporate.Communications@bbkonline.com</code> (`.note.warn` **Confirm with CCD**: shared mailbox vs the five individuals — for individuals list all five addresses separated by `;`). Subject: `New Communication Briefing Request: ` + dynamic content <kbd class="ui">Request Subject</kbd>. Body (one `.fx` block to copy, then swap the bracketed parts for dynamic content chips):
  `A new communication briefing request has been submitted.` / `Subject: [Request Subject]` / `Department: [Department Value]` / `Target date: [Target Date]` / `Details: [Request Details]` / `Open the request: [Link to item]`
  Check: no unfilled required fields; <kbd class="ui">Save</kbd> succeeds.
- **e3 — Test the notification.** In the app (published version or F5): submit a fresh test request. Within ~1 minute the CCD address receives the email with working item link. `.note.warn`: emails send from **your** account (the flow owner's connection); for a service-account sender ask IT — future enhancement, not Phase 1. Check: email received.
- **e4 — Audit flow: trigger.** New automated flow, name <code class="cc">CBF - Audit Logger</code>, trigger **SharePoint · When an item is created or modified** (this time the "or modified" one — mirror-image lookalike warning), Site = your site, List = <kbd class="ui">Communication Requests</kbd>. Check: trigger set.
- **e5 — Audit flow: created-or-edited branch.** Add <kbd class="ui">Condition</kbd>: left = dynamic <kbd class="ui">Created</kbd>, operator <kbd class="ui">is equal to</kbd>, right = dynamic <kbd class="ui">Modified</kbd> (`.note.why`: on a brand-new item both timestamps are identical — that's how we tell a create from an edit without extra queries). **If yes** → <kbd class="ui">Create item</kbd> (SharePoint) → Site, List = <kbd class="ui">Audit Log</kbd>; Title = dynamic <kbd class="ui">Request Subject</kbd>; RequestID = dynamic <kbd class="ui">ID</kbd>; Action Value = <code class="cc">Created</code>; ModifiedBy = dynamic <kbd class="ui">Modified By DisplayName</kbd>; ModifiedDateTime = dynamic <kbd class="ui">Modified</kbd>; ChangeSummary = <code class="cc">New request submitted</code>. Check: yes-branch complete.
- **e6 — Audit flow: was it a status change?** **If no** branch → <kbd class="ui">Get changes for an item or a file (properties only)</kbd> (SharePoint): Site, List = Communication Requests, Id = dynamic <kbd class="ui">ID</kbd>, Since = expression:
  `triggerOutputs()?['body/{TriggerWindowStartToken}']`
  Until = expression:
  `triggerOutputs()?['body/{TriggerWindowEndToken}']`
  Then a nested <kbd class="ui">Condition</kbd>: dynamic <kbd class="ui">Has Column Changed: Status</kbd> <kbd class="ui">is equal to</kbd> expression `true`. Nested-yes → Create item in Audit Log with Action Value = <code class="cc">Status Changed</code>, ChangeSummary = concat expression:
  `concat('Status is now: ', triggerOutputs()?['body/Status/Value'])`
  ; nested-no → Create item with Action Value = <code class="cc">Edited</code>, ChangeSummary = <code class="cc">Fields updated by requester or CCD</code>; both rows carry the same Title/RequestID/ModifiedBy/ModifiedDateTime mappings as e5. Check: three Create-item cards total, all mapped.
- **e7 — Test the audit trail.** Save the flow. Submit a new test request; edit it from My Requests; change its status from the dashboard. Open Audit Log: three rows — Created, Edited, Status Changed — each with name + timestamp. `.note.check` includes: the FR-4 acceptance line (every edit logged with editor name + date/time) is now met and Excel-exportable. Check: three rows verified.
- **e8 — Optional: status-change email to requester.** `.note.tip` marks the whole step optional (spec's open question 3 — **Confirm with CCD** first). New automated flow <code class="cc">CBF - Status Change Notification</code>, trigger **When an item is created or modified** on Communication Requests → Get changes (same Since/Until expressions as e6) → Condition Has Column Changed: Status = `true` AND Created **is not equal to** Modified → yes → Send an email (V2): To = dynamic <kbd class="ui">Created By Email</kbd>; Subject `Your communication request status: ` + dynamic <kbd class="ui">Status Value</kbd>; Body: status + CCD Notes dynamic content + item link. Check (if built): requester email arrives on status change.
- **e9 — Go-live: clean the test data.** Delete every `TEST` item from Communication Requests (recycle-bin note: they persist 93 days in the site recycle bin — that's fine) and the matching Audit Log rows. `.note.warn`: from Part 1 a9 onward the guide seeded test items — sweep them all. Check: both lists clean.
- **e10 — Go-live: acceptance walkthrough, requester half.** With a colleague's account (or IT test account): they open the published app link (studio → <kbd class="ui">Share</kbd> → copy link; share the app with <code class="cc">Everyone except external users</code> plus grant the SharePoint connection). They: submit with attachment (✓ AC-1); CCD inbox gets the email (✓ AC-2); they edit their submission (✓ AC-3); Audit Log rows appear (✓ AC-4); they see live status (✓ AC-5); they can NOT see your items on My Requests (✓ AC-7). Rendered as a `table.cols` mapping each check to its acceptance criterion. Check: six ticks.
- **e11 — Go-live: CCD half.** From your (owner) account: dashboard shows all items incl. the colleague's (✓ AC-6); Export to Excel from the list (✓ AC-8); confirm nowhere in the flow is an approve/reject step (✓ AC-9); list settings show versioning on (✓ AC-10). Check: four ticks — all ten green.
- **e12 — Hand over.** Share the app link + this guide series URL with the five CCD members; tell IT the two lists, the app, and the three flows exist (maintenance owner per the requirements). `.note.tip`: future enhancements parked by the spec — approval workflow, edit-lock after Completed, service-account mailbox. Check: handover message sent.

- [ ] **Step 1: Write the page** (12 steps).
- [ ] **Step 2: Register snippets:** `"part5-flows-golive.html": ["triggerOutputs()?['body/{TriggerWindowStartToken}']", "triggerOutputs()?['body/{TriggerWindowEndToken}']", "concat('Status is now: ', triggerOutputs()?['body/Status/Value'])"]`.
- [ ] **Step 3: Run verify script.**
- [ ] **Step 4: Serve and click-test.**
- [ ] **Step 5: Commit** — `"Part 5: flows + go-live guide (notification, audit logger, acceptance walkthrough)"`, push.

---

### Task 7: `index.html` — Series hub

**Files:**
- Create: `index.html` (from `template.html`, minus the sticky progress block and step machinery)

**Interfaces:**
- Consumes: all five part pages (links + their step counts).

**Content:** mast (kicker `BBK · Corporate Communications`, H1 `Communication Briefing Form`, sub "Five guided parts that take a blank SharePoint tenant to a working briefing-request system — form, tracking, audit trail, notifications.", meta pills `5 parts`, `~3.5 hours`, `SharePoint · Power Apps · Power Automate`). A `.tldr` describing the system. A `.note.why` with the Phase-1 rule (no approval workflow). A prerequisites `.pane` (M365 account, site-creation rights or IT help, the CCD member list). Then five link cards — reuse `details.step` styling as always-open `<div class="step-card">`s or simple `section.block` entries, each: part number, title, one-line summary, step count, `<a>` to the page. Footer: same series links (self-link plain text). Remove the `<div class="sticky">` block and the progress/step JS can stay (it no-ops with zero steps) — simplest is to keep the script untouched and delete only the sticky HTML. No storage key needed but leave `__STORAGE_KEY__` filled with `cbfIndex_v1` so no token survives.

- [ ] **Step 1: Write the page.**
- [ ] **Step 2: Run `python tools/verify_pages.py`** — expect `OK — 6 pages verified` (first fully green run).
- [ ] **Step 3: Serve and click every link** on index + every footer link on all five parts (30 links total) over `http://localhost:8000`.
- [ ] **Step 4: Commit** — `"Index: series hub wiring all five parts"`, push.

---

### Task 8: Full QA pass

**Files:**
- Modify: any page that fails a check.

- [ ] **Step 1: Gate check** — `grep -c 'gate.js' *.html` → every line ends `:0` (template.html included).
- [ ] **Step 2: Verify script** — `python tools/verify_pages.py` → `OK — 6 pages verified`.
- [ ] **Step 3: Browser pass over http://localhost:8000, all six pages** — for each: fonts load, legend/pills render, tap-to-copy works (amber chip and dark-block Copy button), mark-done updates counter + survives reload, Reset clears, expand/collapse chevrons work, no horizontal scroll at 390px width (mobile emulation).
- [ ] **Step 4: Formula spot-check** — copy each registered snippet from the rendered page via its Copy button and diff against this plan's text (escaping bugs show up here).
- [ ] **Step 5: Fix anything found, re-run Steps 1–4, commit** — `"QA pass: six pages verified (script + browser + copy-path)"`, push.

---

### Task 9: Deploy to GitHub Pages + live verification

- [ ] **Step 1: Enable Pages**

```bash
gh api repos/Wastaboy/Communication_html/pages -X POST -f build_type=legacy -f "source[branch]=main" -f "source[path]=/"
```

(409 means already enabled — then verify with `gh api repos/Wastaboy/Communication_html/pages`.)

- [ ] **Step 2: Wait for the first build** — poll `gh api repos/Wastaboy/Communication_html/pages --jq .status` until `built` (typically < 2 min).
- [ ] **Step 3: Verify all six live URLs return 200 and real content**

```bash
for p in index part1-foundation part2-submission-form part3-my-requests part4-ccd-dashboard part5-flows-golive; do
  curl -s -o /dev/null -w "%{http_code} $p\n" "https://wastaboy.github.io/Communication_html/$p.html"; done
```

- [ ] **Step 4: Open the live index in a browser** and click through to one part page; mark a step done to confirm localStorage works on the live origin.
- [ ] **Step 5: Final commit if anything changed; report the live URL set to the user.**

---

## Self-review notes (completed)

- **Spec coverage:** FR-1 → Task 3 (b4–b9); FR-2 → b5/b9; FR-3 → Task 4 (c6–c7); FR-4 → Task 6 (e4–e7) + version history (a5, c9); FR-5 → e1–e3; FR-6 → Status column (a3) + c4/c5 + d5–d7; FR-7 → d8; FR-8 → a5 + e9 recycle-bin note (no hard-delete guidance); access list → a8 + d1; out-of-scope rule → index + part1 + e11 AC-9. All ten acceptance criteria are individually walked in e10–e11.
- **Type/name consistency:** control roster, globals, storage keys, and filenames are defined once in "Canonical build values" and referenced verbatim in Tasks 2–6.
- **Placeholder scan:** the only intentionally-open values are real-world unknowns the user must supply (site URL, CCD emails, division-list currency, status names, recipient mailbox) — each is rendered as a **Confirm with CCD** warn note, per the approved design, not left as plan TBDs.
