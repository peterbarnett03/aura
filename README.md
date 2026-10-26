# Aura — companion site

The marketing, privacy and support site for the Aura iPhone app, served by GitHub Pages from
`main` at the repo root. Hand-written pages — `index.html`, `privacy.html`, `support.html`, and
the guides (`guides.html` plus four articles) — share one `style.css`, alongside `robots.txt`,
`sitemap.xml`, `llms.txt` and generated screenshots in `shots/`. No build step, no framework, no
JavaScript, no dependencies. `.nojekyll` disables Jekyll processing; pushing to `main` publishes.

The app is live: <https://apps.apple.com/us/app/aura-palindromic-rheumatism/id6749520199>.

```sh
python3 -m http.server 8000   # local preview
./tools/process-shots.py      # regenerate shots/ from the app's dark captures (needs Pillow)
```

Verifying a change means loading the three pages at 390px, ~900px and desktop, in both colour
schemes, and confirming `document.documentElement.scrollWidth` still equals `clientWidth` at the
narrowest width. The hero glow bleeds past the hero on purpose and is clipped by its own wrapper;
widen it carelessly and the page starts scrolling sideways on a phone.

## The iPhone is drawn, not photographed

`.phone` in `style.css` builds the device out of CSS 3D: a rail, three stacked plates behind the
front face so the body has a side wall when it turns, the screen, the Dynamic Island, and one soft
band of glare. Proportions are the 6.9" iPhone's — the 1320 × 2868 screen `shots/` is captured at,
whichever simulator of that size the capture script picks — so the screenshot inside it is the
app's own pixels with nothing done to them.

Rotation is per instance through `--ry` / `--rx` / `--rz`, and drops toward flat at the two
breakpoints. `tools/process-shots.py` must keep emitting bare screens: a baked-in bezel or corner
radius would double up on the frame the page draws.

The frames are dark, which is what the graphite body was drawn for: a lit screen in a dark frame
reads as a phone that is on, where a light one reads as a bright rectangle with a border around
it. See `tools/process-shots.py` for the rest of that argument.

## The app icon

`assets/` holds renders of the shipping icon, not a redraw of it. Compiling
`aura-ios/Aura/Resources/AppIcon.icon` with `actool` for `iphoneos` leaves both 1024px appearance
renders in a temporary directory on the way to `Assets.car`; catch them while it runs, mask each
with the iOS superellipse, and that is the whole set. Do it that way rather than screenshotting a
device or redrawing anything.

```sh
xcrun actool ../aura-ios/Aura/Resources/AppIcon.icon --compile /tmp/out --platform iphoneos \
  --minimum-deployment-target 26.0 --app-icon AppIcon --output-partial-info-plist /tmp/out/p.plist &
# then copy AppIcon1024x1024_UIAppearance{Any,Dark}*.png out of $TMPDIR/*/ before it finishes
```

The header icon, the apple-touch icon and the social card use the light appearance. **The favicon
uses the dark one**, which is deliberate: at 16px the light icon's pale glass body dissolves into a
light tab bar and all that survives is a small orange dot. The dark appearance is the same logo and
holds on either chrome. A `media="(prefers-color-scheme: dark)"` pair would be nicer still, except
that browsers ignoring `media` on `rel=icon` fall back to document order, and no ordering leaves
the light icon out of the light-tab-bar case.

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

  The fixture is fixed to the *day*, not to the minute, so three things in the alt text move with
  when the capture ran rather than with the app, and have to be re-read every time: the flare's age
  on `today` (it starts at 07:30 local, so it reads however far past that the run was), the dose
  times on `medications`, and the report period start on `doctor` (90 days back from the capture
  date). The featured paper on `research` and `today` comes from a live PubMed query and can change
  outright.

## Anything about the listing is a claim too

The App Store link, the price, the platform and the minimum iOS version appear in the hero copy,
in the `MobileApplication` structured data on `index.html`, and in the smart-app-banner `app-id`
on all three pages. Every one of those was read off the live listing rather than assumed, and
every one of them can change without this repo hearing about it — a paid tier, a raised
deployment target, a renamed app. Re-read the listing before editing any of them, and do not add
an `aggregateRating`: inventing one is the sort of thing the product itself refuses to do.

`sitemap.xml` and `llms.txt` are written by hand because there is no build step; add every new
page to both. Move `lastmod`
when a page's content changes, not when a typo is fixed.

Claims on `index.html` and `support.html` are product claims. Check them against the app before
writing new ones — this app was rejected twice under guideline 5.1.1, and the copy here has to stay
consistent with the privacy label and the in-app wording.

## The guides are for people who have not heard of the app

`palindromic-rheumatism.html`, `palindromic-rheumatism-vs-rheumatoid-arthritis.html`,
`flare-diary.html` and `rheumatology-appointment.html` exist to be found by someone searching for
the condition, and `guides.html` indexes them. They are the site's search surface: the landing
page can only rank for "palindromic rheumatism app", and almost nobody searches for that.

Every figure on them is cited, by number, to a source at the foot of the page, and every source
is a paper a rheumatologist would recognise. Keep it that way. A health page is judged on whether
it can be trusted, and a number that cannot be traced is a reason not to. Each page carries an
`Article` and `BreadcrumbList` in JSON-LD; bump `dateModified` there, the "Updated" line and the
sitemap's `lastmod` together when the substance changes. The app panel on each page uses claims
already made on `index.html`, so the rule above about product claims applies to it too.

`flare-diary.html` has `class="print-sheet"` on `body`: printed, only the log sheet comes out, on
a landscape page where the browser supports named `@page`s. Check a print preview after touching
the print rules at the end of the guides section of `style.css`.

`.github/workflows/lighthouse.yml` audits every page on each push (config in `lighthouserc.json`)
and fails below 95 on SEO or accessibility. New pages go in its URL list.
