# Metronome — website

Marketing, support and legal pages for **Metronome That Listens To You** (iOS). Static HTML served by GitHub Pages at https://alexriakhin.com/Metronome/. This repository is the `MetronomeWebsite` submodule of the app repository (`Metronome-App`).

```
src/<page>.html        page bodies; first line is a <!-- {json} --> comment (title, description, nav)
tools/build_site.py    wraps each body in the shared header/footer → <page>.html, writes sitemap.xml
assets/css/site.css    styles (navy stage, orchid purple accent, teal support; dark + light)
assets/img/            app icon and framed simulator screenshots
favicons/              generated from the app icon (ictool export of AppIcon.icon)
```

```bash
python3 tools/build_site.py          # rebuild every page after editing src/
python3 -m http.server 8765          # preview at http://localhost:8765
```

The App Store listing links to `support.html` and `privacy.html`. Keep those paths stable. Replace the "Coming soon" buttons in `src/index.html` with the App Store link once the app is live. Update `privacy.html` before shipping microphone timing feedback.

## Screenshots

Capture the app in the iPhone simulator (status bar at 9:41: `xcrun simctl status_bar <device> override --time 9:41 …`) into `tools/raw/<name>.png` (gitignored), then:

```bash
python3 tools/frame_screenshots.py tools/raw/*.png   # → assets/img/<name>.webp inside tools/iphone-frame.webp
```
