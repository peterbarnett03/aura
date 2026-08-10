# Aura — companion site

The marketing, privacy and support site for the Aura iPhone app, served by GitHub Pages from
`main` at the repo root. Four hand-written files — `index.html`, `privacy.html`, `support.html`,
`style.css` — plus generated screenshots in `shots/`. No build step, no framework, no JavaScript,
no dependencies. `.nojekyll` disables Jekyll processing; pushing to `main` publishes.

```sh
python3 -m http.server 8000   # local preview
./tools/process-shots.py      # regenerate shots/ from the app's captures (needs Pillow)
```

Verifying a change means loading the three pages at 390px, ~900px and desktop, in both colour
schemes, and confirming `document.documentElement.scrollWidth` still equals `clientWidth` at the
narrowest width. The hero glow bleeds past the hero on purpose and is clipped by its own wrapper;
widen it carelessly and the page starts scrolling sideways on a phone.

## The iPhone is drawn, not photographed

`.phone` in `style.css` builds the device out of CSS 3D: a rail, three stacked plates behind the
front face so the body has a side wall when it turns, the screen, the Dynamic Island, and one soft
band of glare. Proportions are the iPhone 16 Pro Max's, which is the device `shots/` was captured
on, so the screenshot inside it is the app's own pixels with nothing done to them.

Rotation is per instance through `--ry` / `--rx` / `--rz`, and drops toward flat at the two
breakpoints. `tools/process-shots.py` must keep emitting bare screens: a baked-in bezel or corner
radius would double up on the frame the page draws.

## The app icon

`assets/` holds renders of the shipping icon, not a redraw of it. They come from
`aura-ios/Aura/Resources/AppIcon.icon` compiled by `actool` for macOS, whose 1024px intermediate is
the same glass composition iOS renders. The opaque shape is cropped out of that, recomposited over
the gradient from `icon.json`, and masked with the iOS superellipse. Checked against `actool`'s own
iOS render at 120px: mean absolute difference 2.4/255. Regenerate it the same way if the icon
changes, rather than screenshotting a device.

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
