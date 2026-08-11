# Project rules

- **No password gate:** pages in this repo must NOT load `gate.js` (Zscaler
  phishing flag hit 3rd_party_html on 2026-07-20 for gate + bank vocabulary).
  Verify with: `grep -c 'gate.js' *.html` (exactly 0 per file).
- Pages are generated from `template.html`; follow its canonical step block.
- Run `python tools/verify_pages.py` after any page edit.
- Test over `http://` (`python -m http.server`), never `file://`.
- Design spec: `docs/superpowers/specs/2026-08-11-communication-briefing-guides-design.md`.
