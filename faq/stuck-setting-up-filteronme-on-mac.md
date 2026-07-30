---
id: 126
slug: stuck-setting-up-filteronme-on-mac
legacy_url: https://help.filteronme.com/article/126-stuck-setting-up-filteronme-on-mac
title: Stuck setting up FilterOnMe on Mac
category: install-setup
verdict: keep
related: [how-to-do-a-full-reinstall-of-filteronme-for-mac, where-is-camera-extension-in-mac-settings]
---

If the camera extension doesn't install properly, setup can get stuck. Try this:

1. Open Terminal (search for it in Spotlight) and run:

```
tccutil reset Camera com.filtersoftware.filteronme.CameraExtension
```

You should see a message saying "Successfully reset...".

2. Open FilterOnMe.
3. Click **Advanced** in the top-left menu, then **Uninstall Extension**.

![screenshot](images/126-stuck-setting-up-filteronme-on-mac/2.jpg)

4. Reboot your computer and go through setup again. Click **Allow** when the camera extension asks for permission.

![screenshot](images/126-stuck-setting-up-filteronme-on-mac/3.jpg)

5. Still not working? Try switching the selected camera in the app, then switching back.

![screenshot](images/126-stuck-setting-up-filteronme-on-mac/4.jpg)

Changing cameras and changing back can "reset" a stuck extension.

Still stuck after all of that? Do a [full reinstall](how-to-do-a-full-reinstall-of-filteronme-for-mac).

Still stuck? Email support@filteronme.com
