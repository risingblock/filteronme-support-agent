---
id: 106
slug: there-is-a-problem-with-this-windows-installer-package
legacy_url: https://help.filteronme.com/article/106-there-is-a-problem-with-this-windows-installer-package
title: "There's a problem with this Windows installer package"
category: install-setup
verdict: rewrite
related: [how-to-install-and-setup-filteronme-on-windows, error-installing-another-installation-is-in-progress, how-to-uninstall-filteronme]
---

Seeing "There is a problem with this Windows Installer package," or the install just won't complete? Work through these in order — most people are fixed by the first two.

![screenshot](images/106-there-is-a-problem-with-this-windows-installer-package/1.png)

## 1. Install the required libraries

Missing one of these is the single most common cause of this error. Most Windows computers already have them:

- [Microsoft WebView2 Runtime](https://developer.microsoft.com/en-us/microsoft-edge/webview2/consumer/)
- [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)
- [Microsoft .NET Framework 4](https://dotnet.microsoft.com/en-us/download/dotnet-framework)

## 2. Run the installer as administrator

Right-click the installer file and choose "Run as administrator."

## 3. Restart your computer

Then try the installer again.

## 4. Temporarily disable your antivirus

Security software sometimes blocks the installer. Turn it back on once the install finishes.

## 5. Do a fresh download

Delete the installer you already have, then download a new copy from [filteronme.com/downloads](https://filteronme.com/downloads). Let it finish downloading fully before running it.

## 6. Clear your temp folder

Press Windows key + R, type `%temp%`, press Enter, select all the files, and delete them. Try installing again.

## Still failing? Send us an install log

1. Open Command Prompt as administrator, in the folder where FilterOnMe.msi is.
2. Run:
   ```
   msiexec /i "FilterOnMe.msi" /L*v "install_log.txt"
   ```
3. Email `install_log.txt`, your Windows version, and a screenshot of the error to support@filteronme.com.

Still stuck? Email support@filteronme.com
