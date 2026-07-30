---
id: 81
slug: how-to-use-with-obs-or-streamlabs
legacy_url: https://help.filteronme.com/article/81-how-to-use-with-obs-or-streamlabs
title: How to use FilterOnMe with OBS or Streamlabs
category: using-with-apps
verdict: rewrite
related: [how-to-use-with-discord, which-apps-does-filteronme-work-with]
---

Open FilterOnMe first — it needs to already be running before OBS or Streamlabs starts looking for cameras.

In OBS or Streamlabs, add a **Video Capture Device** source and select **FilterOnMe Camera**.

![screenshot](images/81-how-to-use-with-obs-or-streamlabs/2.jpg)

- **Windows:** keep FilterOnMe open the whole time you're using OBS.
- **Mac (latest version):** once the FilterOnMe camera is selected in OBS, you can close FilterOnMe to save resources.

## Running OBS as Administrator?

If OBS runs in Administrator mode, the FilterOnMe camera may not show up. Try running OBS as a normal user first.

If you need OBS in admin mode specifically, this is an admin/non-admin mismatch — the fix is reinstalling FilterOnMe so it's registered for all users:

1. Uninstall FilterOnMe.
2. Open Command Prompt as Administrator.
3. Run this (replace `YOURUSERNAME`, and assumes the installer is in your Downloads folder):
   ```
   msiexec /i "C:\Users\YOURUSERNAME\Downloads\Filteronme.msi" ALLUSERS=1
   ```
4. Open FilterOnMe — it should now work with OBS in admin mode.

Still stuck? Email support@filteronme.com
