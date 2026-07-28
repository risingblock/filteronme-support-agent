---
topic: tech-issue
volume: 340 of 1957 (17%)
status: draft-for-eddy-review
---

# App malfunctions: camera not found, black/blank screen, crashes, and specific-app failures

## When this applies

- Customer can't get the Filteronme virtual camera to appear or work inside another app
  - "Can't find Filteronme camera" in Zoom/Meet/Teams/Discord/OBS/FaceTime/Skype video source list
  - Camera appears but shows black, white, blank, purple, or green screen
  - Works in one app but not another (e.g. fine in FaceTime, missing in Discord/OBS)
- App itself misbehaves
  - Crashes on launch or shows a BugSplat crash-report dialog
  - Loads then immediately closes
  - Filter flickers / turns on and off / app goes "Not Responding" mid-call
  - Sliders/filters have no visible effect ("no effect", filters not applying)
- Performance complaints: laggy video, high CPU/energy use, slow filter response, worse when a specific setting (e.g. "mirror camera") is toggled
- Resolution/quality complaints: image looks blurry, low-res, or capped below the customer's source camera's real resolution; "why no 4K"
- Hardware/peripheral-specific failures: Elgato Cam Link / capture cards, DSLRs via capture card, discolored (green/purple) image tied to a specific camera
- Post-update or post-OS-upgrade regressions: worked before a Filteronme update or a macOS/Windows update, broke after

## What to check first

From the ticket itself:
- OS and OS version (Mac vs Windows, and which version — many fixes are Mac-only or Windows-only)
- Filteronme app version (Settings tab shows it) — recent regressions are version-specific (2.1.5 flicker bug, fixed in 2.1.6)
- Which app they're using Filteronme with (Zoom/OBS/Discord/etc.) and whether it fails in *only* that app or everywhere
- Was it working before? What changed (an update, a new webcam, a Mac/Windows OS upgrade)?
- Exact symptom: black vs white vs purple vs green screen are different bugs — don't treat them as the same thing
- Screenshot/video if the customer offers one — ask for one if the description is ambiguous (e.g., resolution complaints are frequently a misread of OBS's on-screen position/size numbers, not actual resolution — conv 3023640356)

From Help Scout history (live API search by customer email):
- Has this customer already tried the standard reinstall ladder in a prior ticket? Don't repeat the same first-line fix if a previous conversation shows they exhausted it.
- Look for a `Note` from Eddy on a similar case — several tech-issue notes contain his real diagnosis (e.g. Elgato/CamLink dongle suspicion, "ask if it worked before during trial") that never made it into a doc article.

Once Phase 3 (Stripe) lands:
- Subscription status/plan — a customer threatening to cancel over an unresolved bug is a signal to prioritize/escalate, not a reason to change the technical answer.
- Do NOT use Stripe status to decide refund eligibility yourself — refunds are always human-executed (CLAUDE.md hard rule); flag for Eddy instead of promising one.

## Policy

- **Standard fix ladder, cheapest step first** (evidenced across dozens of Eddy replies, and formalized in help.filteronme.com/article/105): confirm Filteronme is open *before* the main app (Windows only — Mac 2.1+ no longer requires the main app to stay open, conv 3125342687) → change camera selection and change it back, or unplug/replug the camera → reboot the app → Mac-only: toggle camera permission off/on, then toggle camera extension off/on in System Settings → reinstall the camera extension from Filteronme's Advanced menu → reboot computer → full uninstall/reinstall (conv 2386659864, 2397252852, article 123).
- **Always ask 1-2 isolating questions before prescribing fixes** when the ticket doesn't already answer them — OS/version, does it happen in other apps, did it work before (conv 2809512589, 2822592771, 2757491615, 3131216372). Eddy essentially never fires the full fix ladder on the first reply without at least confirming OS/version first.
- **4K is explicitly not supported, by design** — resource cost is too high for most customers' machines, and call apps like Zoom recompress video anyway so the gain is marginal (conv 2923620793, note from Eddy 2025-05-02/05). This is stated as durable policy, not "not yet" — don't imply a 4K roadmap unless Eddy has said so elsewhere.
- **1080p support has been improving** — as of the Aug/Sep 2025 Mac release "fully supports 1080p" (note in conv 3023640356); earlier in 2024 a customer was told Mac 1080p output wasn't confirmed (conv 2695090226). Confirm current version before promising 1080p works — don't assume it's true for older installs.
- **Resolution complaints need visual proof before being treated as a bug.** The OBS position/size numbers (e.g. "640x360") are frequently mistaken by customers for the resolution — that is not a Filteronme bug (conv 3023640356). Ask for a webcamtests.com screenshot of the Filteronme camera output, and a screenshot of the same camera without Filteronme, before concluding it's a real regression.
- **Elgato/Cam Link and other capture-card issues are acknowledged, real, and unresolved** — Eddy's honest answer is that these are "technically difficult problems" with no timeline, not a promise of an imminent fix (conv 2657432637). Don't imply Elgato support is coming unless told otherwise.
- **Green/purple/discolored screen tied to one specific camera is usually a camera-input problem, not Filteronme** — but verify with a different webcam and a cable/USB-direct connection check before concluding that, and don't accuse the customer of anything (conv 3253230468 — this became a long, frustrating thread partly because "try a different camera" was pushed repeatedly without ever getting a clean isolation test; ask for the webcamtests.com screenshot early instead of iterating one variable at a time over days).
- **No refunds for confirmed non-Filteronme (hardware) issues**, and refunds are never decided or executed by this agent regardless of cause — always escalate refund requests to Eddy/human (conv 3253230468 — "no refunds you can share no refund policy and close follow ups" was Eddy's explicit call, made by him, not inferred by support).
- **When a real regression is suspected (a version made things worse for multiple people), acknowledge it as a known/investigating issue rather than denying or re-running the generic fix ladder** — see the 2.1.5 flicker cluster (conv 3125342687, 3132888293, 3134539353): Eddy's fix was pointing to the 2.1.6 update, and offering the old-version download (article 124) as a fallback if 2.1.6 didn't help. If multiple recent tickets show the same new symptom right after a release, treat it as a known issue, not a one-off.
- **Honesty over a firm fix when there isn't one** — for hardware/compatibility-limited cases (old/underpowered computers, exotic hardware) Eddy says plainly that he'll look into it with no promised timeline, rather than guessing at a fix (conv 2657432637, 2757491615).

## How to respond

Default shape: one diagnostic question, or one concrete next step — never both, and never the full fix ladder in one message unless the ticket already ruled out the earlier rungs.

Camera not showing up in another app (first contact, info missing):
> Hi <Name>,
>
> What version of Mac/Windows do you have, and which app are you trying to use Filteronme with?
>
> Best

Black screen, standard case (Windows, app-ordering suspected):
> Hi <Name>,
>
> Black screen usually means the app isn't open. Can you confirm you've opened the Filteronme app before opening <their app>?
>
> Best

Mac camera-extension stuck after an OS/app update (specific fix, not the full ladder):
> Hi <Name>,
>
> Sorry you're running into this. Please try:
>
> With Filteronme open, go to the top-left menu → Advanced → Uninstall Extension.
> Reboot your computer, then reopen Filteronme.
>
> Let me know if that gets it working.
>
> Best

Known-regression case, pointing at the fix release with a fallback offered:
> Hi <Name>,
>
> We just released version 2.1.6, which should fix this. You'll need to do a full reinstall — steps here: <help.filteronme.com/article/123>
>
> Let me know if that resolves it. If not, the previous version is still available here: <help.filteronme.com/article/124>
>
> Best

Resolution/quality complaint needing verification before assuming a bug:
> Hi <Name>,
>
> Could you send a screenshot of the Filteronme camera on https://webcamtests.com, and one of your regular camera on the same site? That'll tell us whether this is an actual resolution drop.
>
> Best

Hardware-limited / no fix available, honest close:
> Hi <Name>,
>
> Thanks for the detailed info. This looks like a hardware compatibility issue I can't fix quickly — I'll look into it but can't give a timeline right now. I'll follow up if we get it resolved.
>
> Thanks for trying us out.

## Escalate instead (tag needs-human) when

- Customer requests or implies a refund, chargeback, or "cancel and refund me" — refund decisions and execution are always human (see conv 3253230468, 3113873715).
- A likely new regression that doesn't match any known pattern in this playbook or the docs (possible new bug — needs Eddy's engineering judgment, not a guess).
- Repeated back-and-forth (3+ rounds) where the standard fix ladder hasn't worked and the next step isn't obvious — don't keep iterating alone; loop in Eddy the way notes show him doing internally (e.g. conv 3253230468's long thread).
- Angry/escalated tone combined with a technical claim you can't verify (e.g. accusations the app is "robbing people", threats of chargebacks) — these tickets tend to also carry a refund ask; escalate rather than drafting a technical-only reply.
- Anything involving a payment failure ("we weren't able to charge your card") tangled up with a tech complaint (conv 3113873715) — this crosses into billing and needs a human to sort out the account state.
- A ticket in a language other than English where you're not confident about the technical accuracy of a translated fix.

## Doc links to use in replies

- https://help.filteronme.com/article/105-how-to-fix-most-problems — last updated Feb 24, 2026. Freshest, most-used generic fix ladder. Good primary link for ambiguous "it just stopped working" tickets.
- https://help.filteronme.com/article/82-how-to-fix-black-screen-on-filteronme-camera — last updated Nov 9, 2025. Current.
- https://help.filteronme.com/article/97-cant-find-filteronme-camera-in-app-settings — last updated Nov 9, 2025. Current.
- https://help.filteronme.com/article/110-filters-are-not-working — last updated Jan 20, 2026. Current, but thin (just "check the toggle is on") — fine for sliders-have-no-effect tickets.
- https://help.filteronme.com/article/121-where-is-camera-extension-in-mac-settings — last updated Jan 20, 2026. Says minimum supported macOS is 13.
- https://help.filteronme.com/article/141-change-camera-selection — last updated Jun 26, 2026. Current.
- https://help.filteronme.com/article/123-how-to-do-a-full-reinstall-of-filteronme-for-mac — last updated Jan 20, 2026. Current; this is the doc-ified version of the "full reinstall" step.
- https://help.filteronme.com/article/96-minimum-computer-requirements-to-run-filteronme — last updated Jul 23, 2025. **CONFLICTS with article 121**: this one says macOS 12.4+ is sufficient, article 121 says minimum supported is macOS 13. Don't cite both in the same reply; flagged below for Eddy.
- https://help.filteronme.com/article/89-riverside-audio-and-video-of-out-sync — last updated Jul 26, 2024. Stale (2+ years) and just links out to Riverside's own blog/a Reddit thread — low-value link, treat as last resort only.
- https://help.filteronme.com/article/106-there-is-a-problem-with-this-windows-installer-package — last updated Nov 9, 2024. Use for Windows "purple screen"/missing-libraries installer errors specifically (conv 2822227440); not re-verified for this pass.

## Notes from history

- **Volume shape**: this is the single largest cluster (340 convs). Sub-clusters roughly by frequency of keyword hits across all 340: OBS-related (63), webcam-general (56), Zoom (58), Discord/FaceTime (33/26 respectively), crash (33), black screen (23), lag (21), Elgato/Cam Link (13 + 6), resolution/quality (~15-20 with overlap). No single sub-topic dominates enough to warrant its own playbook yet.
- **Jona vs Eddy, biggest divergence**: Jona's default reply is a near-identical canned paragraph ("Most issues can be solved by resetting the app or reinstalling... Make sure the FilterOnMe app is open... You can also try restarting your computer.") sent almost verbatim regardless of whether the symptom is a crash, a BugSplat error, a color glitch, lag, or an install failure (conv 2963031323, 3113873715, 3202136260, 3120685684, 3132888293, 3134539353). It reads as scripted, skips the diagnostic question Eddy nearly always asks first, and doesn't adapt to the specific symptom. Eddy's replies are shorter and lead with one targeted question (OS? version? other apps? worked before?) before prescribing a fix. Do not have the agent default to Jona's canned block — model the "ask first" pattern instead.
- **Jona escalation pattern**: on judgment calls (is this eligible for refund? did the new version fix this? should I offer the old version?) Jona reliably pings Eddy via an internal Note rather than deciding — this is the *right* instinct and matches this playbook's escalation policy, but in practice it produced multi-day gaps and frustrated customers (conv 3253230468 ran ~3 weeks with repeated "please follow up" pings). If the agent escalates, it should still tag `needs-human` promptly rather than let a thread go stale, and shouldn't attempt Jona's workaround of quoting Eddy's internal note back to the customer nearly verbatim (occasionally stilted, e.g. "This isn't something we support as we speak").
- **Known past bug, now fixed (probably)**: version 2.1.5 introduced a filter flicker / "Not Responding" regression on Mac for at least 3 separate customers in Oct-Nov 2025 (conv 3125342687, 3132888293, 3134539353). Fix shipped as 2.1.6 with a full-reinstall requirement; old-version download offered as fallback. No confirmation in the data whether 2.1.6 fully resolved it for everyone (one customer, Mona Lee, reported "same problem" on 2.1.6 and was told to revert to old version) — treat 2.1.6 as "likely fixed, offer old version if not" rather than a guaranteed fix.
- **Mirror-camera-off lag**: one customer (conv 2822592771) reported the camera becomes laggy specifically when the "Mirror camera" setting is turned off, and needs it off because call apps already mirror by default. Thread ended without resolution or a note from Eddy — unclear if this is a known/reproduced bug. Worth checking with Eddy before including in the fix ladder as a known issue.

**Open questions for Eddy:**
- Article 96 (macOS 12.4+) and article 121 (macOS 13 minimum) directly contradict each other on minimum macOS version. Which is current?
- Is 1080p output now fully supported on both Mac and Windows, or only the newer Mac releases? A 2024 ticket (conv 2695090226) went unanswered on this exact question.
- Is the 2.1.5 flicker bug considered fully resolved by 2.1.6, or still open for some hardware (per Mona Lee's follow-up)?
- Is there any plan (even directional, no date) for Elgato/Cam Link/capture-card support, so the agent can give a slightly warmer "on our radar" answer instead of "technically difficult, no timeline"?
- The mirror-off lag report (conv 2822592771) — reproduced/known, or a one-off environmental issue?
