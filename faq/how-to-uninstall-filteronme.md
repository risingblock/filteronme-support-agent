---
id: null
slug: how-to-uninstall-filteronme
legacy_url: null
title: How to uninstall FilterOnMe (Mac and Windows)
category: install-setup
verdict: new
absorbs: [93]
related: [how-to-install-and-setup-filteronme-on-windows, there-is-a-problem-with-this-windows-installer-package]
---

## Mac

1. Delete FilterOnMe from your Applications folder.
2. A pop-up appears asking to remove the camera extension too — confirm it.
3. Reboot.

If the pop-up doesn't appear, open FilterOnMe → Settings tab and remove the camera extension manually from there, then delete the app and reboot.

### Extension still won't go away (advanced, Terminal)

This involves disabling System Integrity Protection — only do this if you're comfortable with the risk. We can't take responsibility for problems it causes; email us first if you're unsure.

1. Reboot into recovery mode (hold ⌘+R while restarting).
2. Open Terminal from the Utilities menu, run `csrutil disable`, then reboot again.
3. Open Terminal and run `systemextensionsctl list` to find the FilterOnMe camera extension's team ID and bundle ID.
4. Run `sudo systemextensionsctl uninstall <teamID> <bundleID>`.
5. In Finder, drag any leftover extension files from `/Library/SystemExtensions` to the trash.
6. Reboot into recovery mode again, run `csrutil enable`, then reboot once more.

![screenshot](images/93-how-can-i-uninstall-it-on-mac-computer/1.png)

## Windows

1. Open Windows Settings → Apps → **Add or remove programs**.
2. Find FilterOnMe, click it, and choose **Uninstall**.
3. Reboot.

<!-- TODO screenshot: Windows Settings > Apps > Add or remove programs, with FilterOnMe selected -->

### Uninstaller fails, or FilterOnMe won't fully remove

We don't have a dedicated fix for this yet. Your best bet is the fresh-install steps in [There's a problem with this Windows installer package](https://help.filteronme.com/article/106-there-is-a-problem-with-this-windows-installer-package) — the library installs, running as administrator, and clearing the temp folder can unstick a broken uninstall too, even if you're not trying to reinstall. Still stuck after that? Email us — this is a known gap and we'll help directly.

Still stuck? Email support@filteronme.com
