---
topic: feature-request
volume: 42 of 1957 (2%)
status: approved 2026-07-27
---

# Feature requests & suggestions

## When this applies

Customer is asking for a feature that doesn't exist today — a new filter/slider,
a platform (mobile, Linux), a resolution/quality bump, a pricing model change, a
UI convenience (tray, changelog, zoom/pan), or "will you ever add X." Distinct
from a **bug report** (something that used to work / should work and doesn't)
and from a **how-do-I** question (feature already exists, they haven't found it).

## What to check first

1. **Is this a known standing answer?** Check the table below (4K, mobile, Linux,
   lifetime purchase, camera zoom/rotate, background replace, color temperature,
   filter-editor/Snap Camera import, face-tracking-requires-a-face). If yes,
   answer directly and honestly — don't reopen it as if it were new news.
2. **Has it already shipped?** Several past requests are now live: mirror
   (Settings tab), lip height/width and eyebrow thickness (Lips/Eyebrows tabs),
   minimize-to-tray (help.filteronme.com/article/130), language selection
   including Turkish (article/139). Check current app/docs before saying no.
3. **Is it novel?** Not covered by a standing answer and not shipped — this is
   the case the agent should be most careful with. Never invent a roadmap
   status. Draft an honest "not currently, thanks for the suggestion" reply
   and flag it for Eddy (see Escalate below) so it becomes real product signal
   instead of disappearing.

## Policy

- **The agent never invents a roadmap.** Only say a feature is planned/"on the
  roadmap" if a standing doc or a recent Eddy note in this ticket says so.
  Default honest line when unsure: *"This is not on the roadmap currently, not
  sure if it's possible with our current technology :( Maybe one day!"*
  (conv 2648210443).
- **Never promise a ship date.** Eddy's actual language when he does want to
  build something: "I will add this to our feature suggestion list, however I
  cannot promise a timeline" (conv 2797097722); "Will look into those
  improvements but cannot promise a timeline" (conv 2830480924).
- **Thank genuinely, don't template-thank.** Eddy's replies are short and
  specific to the request, not "we value your feedback" boilerplate. When a
  request is interesting he asks a clarifying question before answering
  (what do you mean by zoom — the app or face zoom? conv 2767738997; any
  particular fun filters you miss? conv 2524600023; what app are you using
  Filteronme for? conv 2322459543).
- **All feature requests get logged for Eddy**, even ones the agent answers
  correctly as "not currently possible." Post a private Note tagging Eddy
  (`@eddy`) with a one-line summary of the ask, same pattern Jona/Rajan already
  use ("forwarding you a feature request").

### Known standing answers (do not treat as novel)

| Ask | Answer | Source |
|---|---|---|
| 4K / higher resolution | Not supported — too resource-intensive for most computers; app auto-downscales 4K cameras; quality gain is minimal once video-call apps compress anyway | doc 94, conv 3199474253 |
| Mobile app (iOS/Android) | Desktop only — Mac & Windows | doc 85 |
| Linux support | No plans currently | conv 2652767589 |
| Lifetime / one-time purchase | Not offered — monthly or yearly subscription only | conv 3240382280 |
| Vertical camera / flip / rotate | Not supported directly; suggest combining with OBS | conv 2671073589 |
| Camera zoom / pan / crop | Not built into Filteronme; point to OBS crop+enlarge, webcam software's own PTZ, or macOS Continuity Camera pan/zoom | conv 2767738997, 2632509312, 3365596607 |
| Color temperature / white balance | Filteronme has no temp/color control; check webcam software (Logitech, Microsoft) or OBS color settings | conv 3158996742 |
| Filters disable when face isn't detected | Expected — filters need a tracked face; not adjustable | conv 2801958696 |
| Import Snap Camera lenses | Not feasible — technically and legally unclear who owns lens copyright | conv 2517237772 |
| Custom filter editor / Lens-Studio-style creator tool | No ETA — big lift; may happen eventually as a creator-tools initiative | conv 2344820531, conv 2517237772 |
| Background replace (not just blur) | No native replace; use the meeting app's own background replacement (Google Meet/Teams) alongside Filteronme | conv 2322459543 |

## How to respond

**Standing "no," novel-ish ask, light disappointment expected:**
> Hi [Name],
>
> Thanks for reaching out! [Feature] isn't something we support today — [one-line honest reason if there is one, e.g. "it's too resource-intensive for most people's setups"]. Not ruling it out for the future, just nothing planned right now.
>
> Best

**Genuine, specific suggestion worth encouraging (matches Eddy's real pattern):**
> Hi [Name],
>
> Thanks for the suggestion! This isn't on the roadmap currently, not sure if it's possible with our current technology :( Maybe one day!
>
> Best

**Interesting/novel request where a clarifying question helps before drafting anything final:**
> Hi,
>
> Thanks for the idea! Just to make sure I understand — do you mean [restate the two plausible interpretations]?
>
> Best

Do not draft a reply that says "I'll add this" or "this is on the roadmap" unless
the ticket, a doc, or an Eddy note already confirms it — that line is Eddy's
call to make, not the agent's.

## Escalate instead (tag needs-human) when

- **Any request not in the standing-answer table** — log it as a Note to Eddy
  regardless of whether the drafted reply is otherwise fine to send. The goal
  is Eddy sees the raw ask, not just the agent's paraphrase.
- **Specific face-sculpting/slider requests** (chin reshaping, eye tilt,
  almond eyes, saggy-jaw lift, brow/beard for male faces, under-eye-only skin
  cleanup) — these are recurring, plausible, and Eddy has shipped similar
  asks fast before (lip slider, eyebrow thickness). Worth his eyes even
  though the honest answer today is "not available."
- **Power/business users** — streamers, agencies, cam studios, telehealth
  practices, anyone mentioning a paid production use case (DSLR/CamLink rigs,
  professional recording, business Google Meet use). They're higher-value
  signal and sometimes worth a different tone (Eddy personally offered to
  build a custom filter and meet for coffee with one such user, conv
  2558957600).
- **Requests that are actually complaints in disguise** — e.g. "have all the
  fun filters been removed?" (conv 2524600023) is a regression complaint, not
  a pure suggestion; verify current state before answering and loop in Eddy
  if filters really did disappear.
- **Nonsensical, personal, or off-brand asks** (e.g. a request to build and
  name a filter after a specific private individual's body) — do not draft a
  reply implying this could ever be built; escalate and let Eddy decide
  whether to respond at all.

## Doc links to use in replies

- Do you have a mobile app? — https://help.filteronme.com/article/85-do-you-have-a-mobile-app
- Do you offer 4K or higher quality resolution? — https://help.filteronme.com/article/94-do-you-offer-4k-or-higher-quality-resolution
- How to minimize Filteronme to the tray — https://help.filteronme.com/article/130-how-to-minimize-filteronme-to-the-tray
- Change language of the app — https://help.filteronme.com/article/139-change-language-of-the-app

## Notes from history

Ranked by frequency in this 42-conversation sample — useful product signal for Eddy:

1. **Camera zoom / pan / move-with-mouse** (3 tickets) — recurring ask from
   streamers whose webcam is physically far from their face.
2. **Face-sculpting sliders beyond current set** — chin V-shape/projection, eye
   tilt ("foxy eyes"), almond eye shape, saggy-jaw lift, brow/beard for male
   faces, under-eye-only skin cleanup (7 tickets combined). Eddy has shipped
   this category fast before (lip slider, eyebrow thickness) — likely the
   highest-leverage bucket to mine for the next release.
3. **Background blur/replace improvements** — adjustable blur intensity,
   portrait-lighting-style background dimming, true background replacement
   (3 tickets).
4. **Fun/Snap-Camera-style filters** — anime filter, "fun filters" that
   disappeared in an update, custom/community filter requests, makeup
   realism (4 tickets). Signal that the fun-filter library is under-invested
   relative to demand.
5. **4K / resolution ceiling** (2 tickets) — mostly professional
   streamers/recorders willing to pay extra; standing answer holds but this
   segment keeps re-asking.
6. **Creator tools / custom filter editor** (2 tickets) — small but vocal;
   Eddy has floated this as a future direction (conv 2517237772).
7. One-off asks worth noting but low volume: lifetime purchase, Linux
   support, vertical camera flip, color temperature control, changelog
   (Eddy liked this idea and shipped one informally, conv 2516139875),
   teeth/mouth fix, hair color change, eye-contact correction.
