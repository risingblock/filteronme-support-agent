---
topic: how-to-use
volume: 85 of 1957 (4%)
status: draft-for-eddy-review
---

# Using FilterOnMe with other apps

## When this applies

Customer is asking how to *do* something — connect FilterOnMe to a specific
video app, find a setting, or remove the app — with no indication anything is
actually broken. Covers: per-app camera setup (Zoom/Meet/Teams/OBS/Streamlabs/
Discord/Webex/Skype/FaceTime/Messenger/Riverside.fm), phone-as-webcam chains
(DroidCam etc.), mirror video, minimize to tray, change camera/language,
uninstall (Mac/Windows), watermark removal, username setup.

## What to check first

Usually nothing — these are one-shot answers. The only thing worth confirming
if it's ambiguous: **which app** they mean (a bare "it's not working" with no
app named needs one clarifying question) and **Mac or Windows** (uninstall and
tray-minimize answers differ by OS).

## Policy

**The universal pattern** (state this whenever the question is "how do I use
FilterOnMe with X"):

> Open FilterOnMe first, select your real webcam inside it, then select the
> "FilterOnMe" camera inside X's video/camera settings. FilterOnMe needs to be
> open when X starts looking for cameras — open FilterOnMe before X.

On Mac (latest app version), FilterOnMe can be closed after the camera is
selected in the target app, to save resources. On Windows it must stay open
the whole time. (docs 81, 88)

**Per-app notes:**

- **Zoom / Google Meet / Teams / Webex / Messenger / Skype / FaceTime /
  Riverside.fm** — select "FilterOnMe" as the camera in that app's video
  settings, FilterOnMe must be open. (convs 2536444506, 2299718402, 2484253372,
  2341705382, 2573643900, 2556990995, 2524998992)
- **OBS / Streamlabs** — add/edit the "Video Capture Device" source, pick
  FilterOnMe. If OBS is running as Administrator, the FilterOnMe camera may not
  show up — try running OBS as a normal user; if admin mode is required, the
  fix is reinstalling FilterOnMe via `msiexec /i "...\Filteronme.msi"
  ALLUSERS=1` from an admin command prompt (doc 81 has exact steps — just link
  it, don't retype the command manually to the customer unless they need
  hand-holding). (convs 2472093336, 2541793380, 2567668898, 2528147213,
  2517731178) (doc 81)
- **Discord** — same pattern; on some Discord versions the camera won't list
  directly and the working chain is FilterOnMe → OBS → Discord. (convs
  2537266550, 2556807646) (doc 88)
- **Phone-as-webcam chains (DroidCam, etc.)** — select DroidCam (or whatever
  phone-cam app) as the input *inside FilterOnMe*, then select FilterOnMe
  inside the target app: `Phone/DroidCam → FilterOnMe → OBS/Discord/etc. →
  final app`. (conv 2480067625)
- **Pre-recorded video / TikTok-style filtering** — not natively supported.
  Workaround: start the OBS virtual camera with the video looping as a source,
  select the OBS virtual camera inside FilterOnMe, apply filters, then screen
  record FilterOnMe. Frame as a workaround, not a real feature. (conv
  2751615480)
- **Mirror video** — Settings tab → toggle "Mirror". (conv 2956199142) (doc
  107)
- **Minimize to tray** — Mac (latest version): app doesn't need to stay open,
  just close it. Windows: no native tray-minimize; only option is a
  third-party tool (RBTray) — disclaim we don't support/guarantee third-party
  software. (doc 130)
- **Change camera selection** — dropdown near the top of the app. (conv
  3366512676) (doc 141)
- **Change language** — Settings → pick a language. (doc 139)
- **Uninstall Mac** — delete the app from Applications; a pop-up appears to
  remove the camera extension too. If that pop-up doesn't fire, the extension
  can be removed manually from the Settings tab, or the app deleted + reboot.
  A terminal-based manual removal exists for stuck cases (advanced users
  only, disable SIP, `systemextensionsctl uninstall`) — link doc 93 rather
  than walking them through it live. (convs 2499272936, 2612826463, 2382469364,
  3069206277-style "extension won't go away") (doc 93)
- **Uninstall Windows** — Add/Remove Programs (Windows Settings) → uninstall
  FilterOnMe. **Do not** reuse the Mac "delete from Applications folder"
  answer for a Windows question — one historical Jona reply (conv 2904723262)
  did exactly that and it's wrong for Windows; use the Windows-specific
  answer. (conv 2510210958 has the correct Windows answer)
- **Remove watermark / go premium** — click "Remove Watermark" inside the
  app (top-left of controls) after upgrading to premium, then reboot the app.
  If they're asking generally, point to upgrading at filteronme.com. (convs
  2469494323, 2484280847, 2372762756)
- **Username not set** — press "Share" on any preset; you'll be prompted to
  set a username there. (conv 2597611456)
- **Resolution / zoom / frame rate control** — not currently configurable
  (locked at 1080p, fixed FOV) due to performance/lag constraints. Give the
  honest "not possible right now" answer per TONE.md, no fake timeline. (convs
  2872701503, 2805764762, 2322334526, 3366512676)

## How to respond

> Hi,
> Once installed you should be able to select the FilterOnMe camera inside
> OBS.
> Best

> Hey you should be able to select Droidcam in FilterOnMe, then select
> FilterOnMe in OBS.
> So it's Droidcam → FilterOnMe → OBS → final app.
> Let me know if you need more help!
> Best

> Hi, make sure the FilterOnMe app is open, then select the FilterOnMe camera
> inside of Discord.

> Hi,
> At this time we're unable to change the resolution due to
> performance/lag constraints.
> Best

Most of these are legitimately 1–2 lines with a link (per TONE.md) — resist
the urge to pre-emptively dump every troubleshooting step. If they come back
saying they don't see the camera option, that's when it becomes a
tech-issue/no-camera-detected conversation.

## Escalate instead (tag needs-human) when

- They followed the standard steps (FilterOnMe open, correct order) and the
  camera still doesn't show up in the target app, is blank, or crashes — this
  is now a malfunction, not a how-to question. Route to the tech-issue
  playbook.
- Lag/freezing that persists after confirming app order and isn't the known
  Google-Meet-fullscreen quirk (conv 2322334526) — likely a performance bug,
  needs investigation, not a how-to answer.
- Angry/refund-threatening tone (e.g. "give me the money back") layered on top
  of a how-to question — still answer the technical question if you can, but
  tag `needs-human` so Eddy can also address the refund/tone.
- A feature request disguised as "how do I..." (e.g. "how do I zoom out",
  "how do I use a pre-recorded video natively") where the honest answer is
  "you can't, it's not built" — fine to answer per Policy above, but if they
  push back or it's a purchase-decision blocker, tag `needs-human`.

## Doc links to use in replies

- https://help.filteronme.com/article/81-how-to-use-with-obs-or-streamlabs
- https://help.filteronme.com/article/88-how-to-use-with-discord
- https://help.filteronme.com/article/107-how-to-mirror-the-video
- https://help.filteronme.com/article/130-how-to-minimize-filteronme-to-the-tray
- https://help.filteronme.com/article/139-change-language-of-the-app
- https://help.filteronme.com/article/141-change-camera-selection
- https://help.filteronme.com/article/93-how-can-i-uninstall-it-on-mac-computer
- https://www.filteronme.com/downloads (pushing an update / fresh install)
- https://www.filteronme.com/ (homepage "Simple Setup" section has a live
  setup demo video, useful for Google Meet questions specifically)

## Notes from history

- Docs are fresh: 141 (change camera) updated June 26 2026, 139 (language)
  April 23 2026, 107/130 (mirror/tray) January 20 2026, 81/88 (OBS/Discord)
  November 9 2025 — all recent, safe to link as-is. 93 (Mac uninstall) is
  oldest at July 26 2024; the top-level answer (delete app, pop-up removes
  extension) still matches what Eddy says in 2024–2025 conversations, so
  no evidence it's stale, just hasn't needed a recent edit.
  There's no separate Windows-uninstall doc — only the Mac one exists in
  history/docs. Worth flagging to Eddy as a possible doc gap since Windows
  uninstall questions do recur and at least one raw reply (2904723262)
  answered the Windows question with Mac instructions.
- The 85-conversation set skews heavily pre-2025 (most Eddy-authored samples
  are 2023–2024); volume of "how do I connect to app X" appears to have
  dropped in 2025–2026 as the docs above matured — recent tickets in this
  bucket lean more toward OBS performance/admin-mode edge cases (e.g. conv
  3226566124) than basic "how do I select the camera."
  Recommend Eddy double check whether that's real or just export sampling.
- No malfunction language should sneak into this playbook's example replies —
  anything with "freezes", "crashes", "not detected" that survives past one
  retry belongs in tech-issue, not here.
