---
topic: install-setup
volume: 84 of 1957 (4%)
status: approved 2026-07-27
---

# Install, setup, and update problems (Mac + Windows)

## When this applies

Customer can't finish installing, can't open the app after installing, can't
find/enable the Mac camera extension, is stuck on a setup screen, can't
uninstall, can't find a download link, or hit trouble after an update/upgrade.
Covers both the Windows installer (.msi/.exe) and the Mac app + system camera
extension.

## What to check first

**Mac or Windows — ask immediately if not stated.** The fixes are completely
different; don't send Windows steps to a Mac user or vice versa. Most vague
first messages ("it doesn't work", "check it pls") give neither the OS nor an
error message — the single most useful next question is usually "What's the
exact error message you're seeing? A screenshot helps" (conv 3208334774,
2782785669, 2609747347). Jona's habit of skipping this and pasting a generic
"reset the app / unplug your camera" reply regardless of what was reported is
the single biggest source of frustrated follow-ups in this topic (see conv
2914288204, where a customer explicitly complaining about a broken download
link got a "try resetting the camera" reply and escalated to "useless AI").
Don't repeat that pattern.

Once you know the OS, match the **exact error text** to a policy below —
don't guess.

## Policy

### Windows

- **"There is a problem with this Windows installer package" / install
  won't complete / DLL registration failure (e.g. softcam.dll HRESULT
  -2147024770)** — canonical doc: (docs/106). Order of operations Eddy
  actually uses: install the 3 required libraries (WebView2 Runtime, VC++
  Redistributable, .NET Framework v4) → run installer as administrator →
  restart → temporarily disable antivirus → fresh download from
  filteronme.com (delete the old installer first) → clear `%temp%` folder.
  If none of that works, ask for an install log: run
  `msiexec /i "FilterOnMe.msi" /L*v "install_log.txt"` from an admin Command
  Prompt in the installer's folder, and get the OS version + screenshot too
  (conv 2664033213, 2754566719, 2755642030, 3271155896). This is the
  workhorse doc — it also covers reports that look unrelated at first (DLL
  errors, "can't uninstall" loops) because the root cause is usually the same
  Windows Installer service.
- **"Another installation is in progress. You must complete that
  installation before continuing this one."** — (docs/111): restart the
  computer, wait a minute after logging in, open Task Manager and kill any
  `msiexec.exe` process, then retry.
- **"The feature you are trying to use is on a network resource that is
  unavailable" / "The older version of FilterOnMeWindows cannot be removed.
  Contact your technical support group"** — (docs/95): this happens after a
  bad/incomplete uninstall (deleting the app folder instead of using the
  uninstaller) followed by trying to reinstall or update. Point to the
  external fix guide linked in the doc. **Era note:** every example we have
  of this (conv 2605280074, 2663983767, 2664033213) is from 2024 on the
  legacy 1.0.x/early-2.x installer; it's rare in 2025–2026 conversations.
  Still the right doc if the exact message matches.
- **Can't uninstall at all / MSI source missing / orphaned Windows Installer
  registration with no reinstall desired** — we don't have a real uninstall
  doc for this; current policy (per Eddy, conv 2991825847) is "delete it
  normally like any other Windows app," and when that's not possible we fall
  back to (docs/106)'s clean-install steps even though the customer doesn't
  want to reinstall (conv 3372447162, 3367153536). This is a known gap — flag
  rather than confidently promising a fix (see Escalate section).
- **Virus/malware warning on download** — get a screenshot + OS version.
  This has been a real false positive before; Eddy fixed it upstream once by
  re-signing/updating the hosted installer (conv 3170125467: "I updated it,
  try [the download link] again"). Don't tell the customer their antivirus is
  wrong on your own authority — get the screenshot to Eddy/needs-human if it's
  a new pattern.
- **App opens then instantly closes / white flash / crashes** — first ask for
  the exact error text or screen recording. Known generic fix: unplug all
  cameras except one basic webcam, uninstall any other virtual cameras, then
  retry (conv 2839321880, 3212222583 — this came from Eddy, not Jona's
  boilerplate). If a video is attached but doesn't load on our end, ask them
  to re-upload or send a link (conv 2909452755).
- **FilterOnMe Camera doesn't show up as a device in OBS/Discord/Zoom/etc.**
  — FilterOnMe must be **open first**, before the target app is opened; the
  virtual camera only registers as available while the app is running.

### Mac

- **Stuck on the setup screen (grayed-out "Done" button, camera extension
  won't finish installing, "Camera Extensions" item missing from Login Items
  & Extensions)** — (docs/121) for finding the toggle on different macOS
  versions (older macOS 12.x: General tab of Security & Privacy; betas: under
  "Others"), and (docs/126) for the actual unstick sequence: run
  `tccutil reset Camera com.filtersoftware.filteronme.CameraExtension` in
  Terminal, open FilterOnMe → Advanced → Uninstall Extension, reboot, retry,
  click Allow when the permission prompt appears. Toggling the camera
  permission or the extension off/on in System Settings also frequently
  clears it (conv 2492098805, 2426149458, 2711224189, 3122825597).
  Oddity worth knowing: one customer's stuck extension only installed after
  they moved the app off the Desktop into a synced folder (Google Drive) —
  not a documented step, but real (conv 3122825597).
- **App must be dragged into /Applications, not run from the installer/
  Desktop** — macOS requires this for the camera driver to register. If a
  customer says the setup screen never progresses and they haven't mentioned
  the Applications folder, ask/check this before anything else (conv
  2492098805 — this alone fixed it twice in that thread).
- **"You can't use this version… requires macOS 13.0 or later"** — be
  straight with them: FilterOnMe 2.x needs macOS 13+. Offer the last version
  that supported older macOS: v2.0.15
  (https://github.com/risingblock/FilterOnMeSparkleUpdate/releases/download/v2.0.15/FilterOnMe.dmg,
  also linked from docs/124 "download old mac version"), and recommend they
  still follow the full-reinstall steps to avoid version conflicts
  (docs/123). No fix exists to run 2.x on macOS 12 or lower (conv 3126132273,
  3243086784).
- **Upgrading to 2.1.6 / general "trouble after update"** — (docs/127) says
  plainly: a full reinstall is required for most Mac upgrades, and if the
  customer is happy on their current version, they can just stay on it.
  Reinstall = (docs/123): Advanced → Uninstall Extension (2.1+ only) → delete
  from Applications → reboot → confirm the virtual camera is gone from
  Zoom/Discord/FaceTime → download latest from filteronme.com/download-mac →
  reinstall.
- **2.1.6 infinite "Check for updates automatically?" loop on Apple
  Silicon (M1/M2), app exits either way you answer** — this was a real,
  version-specific bug reported January 2026 (conv 3199324023). Interim
  workaround Eddy gave: fully quit the app (not just close the window) and
  reopen. **It's fixed as of 2.1.7** — if anyone still reports this exact
  symptom, just point them to the latest download; if it persists on 2.1.7+,
  that's new and should go to Eddy.

### Full-reinstall / escalation ladder (both platforms)

1. Get the OS + exact error text/screenshot if not already given.
2. Apply the specific doc above for that exact error.
3. If the error is vague or none of the specific docs match, the generic
   fallback (what most closes tickets when nothing else fits): reset the app
   or reinstall it, try changing the selected camera and back (or
   unplug/replug the physical camera), make sure FilterOnMe is open and
   showing your preview *before* opening the target app, restart the
   computer. On Mac, also try toggling camera + extension permissions off
   and back on.
4. Still stuck → full reinstall: (docs/123) on Mac; on Windows, a fresh
   download plus the (docs/106) steps in order.
5. Still stuck and it's Mac-only + old hardware/OS → offer the older
   compatible build (docs/124) rather than a dead end.
6. Still stuck after all of the above → **needs-human**. Don't invent a fix.
   Eddy has occasionally hand-built a patched installer for one customer
   (e.g. an MSI with the WebView2 requirement stripped out, conv 2755642030)
   — that's a founder-level move outside what this agent should attempt or
   promise.

## How to respond

Ask for the OS + exact error before troubleshooting anything, if unknown:

> Hi,
>
> Are you on Mac or Windows, and what's the exact error message (a
> screenshot helps)?
>
> Best

Known Windows installer error, first touch:

> Hi Kade,
>
> Sorry about the trouble. Can you try the steps here, especially the
> library installs and clearing the temp folder:
> https://help.filteronme.com/article/106-there-is-a-problem-with-this-windows-installer-package
>
> If it still fails, could you send the install log? The guide above shows
> how to generate one.
>
> Best

Mac stuck-on-setup:

> Hi,
>
> Try this — open Terminal and run:
> `tccutil reset Camera com.filtersoftware.filteronme.CameraExtension`
>
> Then reopen FilterOnMe and go through setup again, clicking Allow when it
> asks for permission.
>
> Best

Old macOS, no fix available — honesty over a dead end (per TONE):

> Hi,
>
> FilterOnMe 2.x needs macOS 13 or later, so it won't run on 12.7.6. You can
> use our last version that supports older Macs here:
> https://github.com/risingblock/FilterOnMeSparkleUpdate/releases/download/v2.0.15/FilterOnMe.dmg
>
> We'd recommend the reinstall steps here to avoid version conflicts:
> https://help.filteronme.com/article/123-how-to-do-a-full-reinstall-of-filteronme-for-mac
>
> Best

## Escalate instead (tag needs-human) when

- The exact error doesn't match any doc above and the generic reset/reinstall
  fallback has already failed once.
- A full reinstall (or the old-version offer, if OS-incompatible) has been
  tried and it's still broken.
- Customer explicitly wants to uninstall/remove the app and can't, and
  (docs/106)'s steps don't resolve it — we don't have a real fix for orphaned
  MSI registrations yet (conv 3372447162, 3367153536).
- Anything that smells like a new version-specific bug (multiple reports of
  the same new symptom right after an update) — Eddy has fixed several of
  these upstream (2.1.6 loop, virus-flagged installer, client-side exception
  crash) once he's aware; don't have the agent troubleshoot a bug that needs
  a code fix.
- Angry/escalated customers who've already gotten (and rejected) canned
  troubleshooting — repeating the same steps a third time reads as not
  listening (conv 2914288204).
- Any request for a discount/promo code tied to install frustration — no
  discounts since early 2025 per TONE.md; don't offer one even though one
  Eddy reply from Aug 2024 did (that was before the policy).

## Doc links to use in replies

- https://help.filteronme.com/article/98-how-to-install-and-setup-filteronme-on-windows
- https://help.filteronme.com/article/99-how-to-install-and-setup-filteronme-on-mac
- https://help.filteronme.com/article/106-there-is-a-problem-with-this-windows-installer-package
- https://help.filteronme.com/article/111-error-installing-another-installation-is-in-progress
- https://help.filteronme.com/article/95-the-feature-you-are-trying-to-use-is-on-a-network-resource-that-is-unavailble
- https://help.filteronme.com/article/121-where-is-camera-extension-in-mac-settings
- https://help.filteronme.com/article/123-how-to-do-a-full-reinstall-of-filteronme-for-mac
- https://help.filteronme.com/article/126-stuck-setting-up-filteronme-on-mac
- https://help.filteronme.com/article/127-upgrading-to-2-1-6
- Also useful for this topic (all already exported in history/docs/):
  article 124 ("download old mac version"), article 97 ("can't find
  FilterOnMe camera in app settings"), article 105 ("how to fix most
  problems"). Article 125 ("upgrading to Mac version 2.1.5") appears in old
  replies but is no longer in the live sitemap — treat links to it as dead.

## Notes from history

- **Doc freshness:** 121, 123, 126, 111 were all updated January 20, 2026 —
  a coordinated refresh, likely tied to the 2.1.6 upgrade wave. 106 (Nov 9,
  2024) is older but still matches current error messages (used
  successfully as recently as March 2026, conv 3271155896). 95 (Aug 2, 2024)
  is the stalest and describes a mostly-legacy 1.0.x uninstall bug — keep it
  for exact-string matches but don't lead with it for new customers.
- **Version-specific bugs already fixed, don't re-litigate:** the 2.1.6
  "Check for updates" exit loop on M1/M2 (fixed in 2.1.7, Jan 2026); a
  virus-flagged Windows installer (fixed by Eddy re-uploading, Dec 2025).
  If a customer describes either of these on current versions, something new
  is going on — escalate rather than assuming the old fix applies.
- **Jona-vs-Eddy divergence:** Jona's default reply is a one-size-fits-all
  "reset the app / unplug your camera / make sure it's open before your main
  app" paragraph, sent regardless of what error was actually reported. It
  works often enough as a first-touch reply when no error has been given
  yet, but sending it *after* a customer has already stated a specific error
  or already tried it reads as not listening and has caused visible
  escalations (conv 2914288204, 3208334774 pattern). Eddy's replies
  consistently read the actual error/screenshot first and ask one pointed
  diagnostic question. Model replies on Eddy's pattern, not Jona's default.
- **Open question:** no documented clean path exists for "customer wants to
  fully remove FilterOnMe from Windows and can't" when normal uninstall
  fails — current guidance just reuses the install-repair doc. Worth a real
  uninstall article; flagging for Eddy rather than inventing steps.
