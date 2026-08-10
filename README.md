# Aura — companion site

The marketing, privacy and support site for the Aura iPhone app, served by GitHub Pages from
`main` at the repo root. Four hand-written files — `index.html`, `privacy.html`, `support.html`,
`style.css` — plus generated screenshots in `shots/`. No build step, no framework, no JavaScript,
no dependencies. `.nojekyll` disables Jekyll processing; pushing to `main` publishes.

```sh
python3 -m http.server 8000   # local preview
./tools/process-shots.py      # regenerate shots/ from the app's captures (needs Pillow)
```

Verifying a change means loading the three pages at both widths (narrow and >860px) and in both
colour schemes.

## The app repo is the source of truth

The sibling checkout `../aura-ios` owns everything this site describes.

- **Privacy policy.** App Store Connect points at `privacy.html`. It must keep describing what the
  app actually does — local-only storage, HealthKit read-only, coarse location to Open-Meteo,
  fixed-term NCBI queries, and no research collection running.
- **Accent colour.** `--accent` in `style.css` is the app's teal from `Core/Design/AuraTheme.swift`,
  darkened enough to clear 4.5:1 as link text.
- **Screenshots.** Captured by `aura-ios/Tools/screenshots.sh`, which drives the real app through a
  UI test against a fixed fixture. `tools/process-shots.py` only resizes and re-encodes. Nothing is
  retouched: if a number in a screenshot looks wrong, it is wrong in the app.

Claims on `index.html` and `support.html` are product claims. Check them against the app before
writing new ones — this app was rejected twice under guideline 5.1.1, and the copy here has to stay
consistent with the privacy label and the in-app wording.
