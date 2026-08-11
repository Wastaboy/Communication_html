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
SNIPPETS = {  # filename -> [verbatim decoded formula strings]
    "part1-foundation.html": [
        "Everyone except external users",
        "Create items and edit items that were created by the user",
    ],
    "part2-submission-form.html": [
        "SubmitForm(frmSubmit)",
        "If(frmSubmit.Valid, DisplayMode.Edit, DisplayMode.Disabled)",
        'Notify("Request submitted — the CCD team has been notified.", NotificationType.Success); ResetForm(frmSubmit)',
    ],
    "part3-my-requests.html": [
        "SortByColumns(Filter('Communication Requests', 'Created By'.Email = User().Email), \"Created\", SortOrder.Descending)",
        "Set(gblEditItem, galMyRequests.Selected); Navigate(scrSubmit, ScreenTransition.None)",
        "If(IsBlank(gblEditItem), FormMode.New, FormMode.Edit)",
    ],
    "part4-ccd-dashboard.html": [
        "Set(gblIsCCD, Lower(User().Email) in [",
        "Choices('Communication Requests'.Status)",
        "Patch('Communication Requests', galAllRequests.Selected, {Status: ddStatus.Selected, 'CCD Notes': txtCCDNotes.Text}); Notify(\"Request updated.\", NotificationType.Success)",
    ],
}

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
