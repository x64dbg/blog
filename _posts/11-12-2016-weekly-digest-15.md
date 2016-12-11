---
layout: post
title: Weekly digest 15
author: mrexodia
website: http://mrexodia.cf

---

This is number fifteen of the weekly digests. This time it will highlight the things that happened in the last two weeks, since last week wasn't so busy.

## Log redirection encoding

Previously the default log redirect option was UTF-16 with BOM, but this has been changed to support [UTF-8 Everywhere](http://utf8everywhere.org). You can get the old behaviour back in the settings dialog if you favor UTF-16.

![UTF-16 log redirect option](https://i.imgur.com/DmKBJec.png)

## Properly enforce size limits for comments and labels

The sizes of labels and comments are limited to ~256 characters and this is now properly enforced in the GUI to avoid nasty surprises. You will now also be warned if you set a duplicate label.

## Large address awareness

The 32 bit version of x64dbg previously wasn't 'Large address aware'. It now is, which means that you can consume more than 2GB of memory if you feel like it.

## Optimized logging speed

The logging should be somewhat faster now, especially when redirecting it to a file and disabling the GUI log. You can find more details [here](https://github.com/x64dbg/x64dbg/pull/1354), but the numbers might be off since additional changes were not made and no benchmarks were done.

## Fixed a crash when clicking out of range in the side bar

Issue [#1299](https://github.com/x64dbg/x64dbg/issues/1299) described a crash and a dump was provided but I did not have debug symbols for that particular build. To figure out what was happening I used x64dbg to debug x64dbg and then some pattern searching to find the crash location in a build for which I did have symbols. The person who opened the issue and a video is available [here](https://youtu.be/zhoSpXnsWMI).

## Updated Scylla

Recently a tool called [pe_unmapper](https://github.com/hasherezade/malware_analysis/tree/master/pe_unmapper) by malware analyst [hasherezade](https://twitter.com/hasherezade) was released and I thought it would be a nice thing to have in x64dbg so I added it to Scylla since it already had a framework to do exactly that. You can find a simple video demonstration [here](https://youtu.be/PFNG-keJ74k).

## Plugin API to get useful information about the current debuggee

There are some new functions available for plugins that help with querying the `PROCESS_INFORMATION` of the debuggee. These functions are:

```c++
BRIDGE_IMPEXP HANDLE DbgGetProcessHandle();BRIDGE_IMPEXP HANDLE DbgGetThreadHandle();BRIDGE_IMPEXP DWORD DbgGetProcessId();BRIDGE_IMPEXP DWORD DbgGetThreadId();
```

## Various improvements to the type system

Issue [#1305](https://github.com/x64dbg/x64dbg/issues/1305) highlights some issues with the type system, various have been addressed and hopefully everything is a bit more stable now...

## More styles

Various additional styles have been added on the [wiki](https://github.com/x64dbg/x64dbg/wiki/Stylesheets). Check them out below!

![Color Show](https://i.imgur.com/NudqRft.png)

![Visual Studio Dark](http://i.imgur.com/0vdWCvN.png)

![Visual Studio Light](http://i.imgur.com/x8GM3Ci.png)

## Case-insensitive regex search in symbol view

It is now possible to use both case sensitive and insensitive searching in the symbol view.

![regex](https://i.imgur.com/O4R9hTa.png)

## GUI speed improvements

A bad locking mechanism has been replaced by [Event Objects](goo.gl/Wc4BoS), resulting in a noticeable performance improvement, mostly when visiting types.

## Intercept more functions for crashdumps

Some crash dumps were missing information and Nukem addressed this in pull request [#1338](https://github.com/x64dbg/x64dbg/pull/1338). This might help on some Windows 10 installations.

## Don't change selection when the search text changes

Thanks to lynnux' pull request [#1340](https://github.com/x64dbg/x64dbg/pull/1340) the last cursor position will now be remembered when removing the search string in the search list view. This is very useful if you want to for example find string references in close proximity to one you are looking for. Below is a GIF demonstrating this new feature.

![keep selection](https://i.imgur.com/kDGHLka.gif)

## Make x64dbg run on Wine again

There is a branch called [wine](https://github.com/x64dbg/x64dbg/tree/wine) that runs under Wine. The reason that x64dbg is not running under Wine is that the [Concurrency::unbounded_buffer](https://msdn.microsoft.com/en-us/library/dd492602.aspx) is not implemented. The branch is not very well-tested but feedback is appreciated!

## Added more advanced plugin callbacks

In pull request [#1314](https://github.com/x64dbg/x64dbg/pull/1343) torusrxxx added automatic detection of PEB fields as labels. This functionality has instead been moved to the [LabelPEB](https://github.com/x64dbg/LabelPEB) plugin and the plugin callbacks `CB_VALFROMSTRING` and `CB_VALTOSTRING` have been added to allow plugins to add additional behavior to the expression resolver.

![PEB labels](https://i.imgur.com/8cvdK4X.png)

## Print additional information on access violations

An interesting piece of [documentation](https://goo.gl/tylmvr) on access violation exceptions is now represented in x64dbg with pull request [#1361](https://github.com/x64dbg/x64dbg/pull/1361) by [changeofpace](https://github.com/changeofpace).

> The first element of the array contains a read-write flag that indicates the type of operation that caused the access violation. If this value is zero, the thread attempted to read the inaccessible data. If this value is 1, the thread attempted to write to an inaccessible address. If this value is 8, the thread causes a user-mode data execution prevention (DEP) violation.
> 
> The second array element specifies the virtual address of the inaccessible data.

![exception information](https://i.imgur.com/0h3Xe7v.png)

## Fixed incorrect detection of unary operators

The expression `(1<<5)+4` would be interpreted as incorrect because the `+` was treated as a unary operator. This has now been fixed!

## Remove breakpoints when clearing the database

The [dbclear](http://x64dbg.readthedocs.io/en/latest/commands/user-database/dbclear.html) command didn't remove breakpoints from the process, causing some weird behavior if you hit a breakpoint anyway. This should now be fixed.

## Fixed bug with searching in the memory map

A bug has been fixed in the [findallmem](http://x64dbg.readthedocs.io/en/latest/commands/searching/findallmem.html) command where the size argument was interpreted incorrectly and thus causing searching the entire process memory to fail.

## Improvements to the breakpoint view

Pull requests [#1359](https://github.com/x64dbg/x64dbg/pull/1359) by [ThunderCls](https://github.com/ThunderCls) and [#1346](https://github.com/x64dbg/x64dbg/pull/1346) by [ner0x652](https://github.com/ner0x652) have added some improvements to the breakpoint view. You can now see if CIP is on the current breakpoint and the edit dialog will show the full symbolic address in the title.

![breakpoint view](https://i.imgur.com/EjyRlQq.png)

## Find window in the attach dialog

You can now find a window by title in the attach dialog to attach to a process without knowing the PID. There is also a new [config](http://help.x64dbg.com/en/latest/commands/misc/config.html) command that can be used by scripts to get/set configuration values. More details in pull request [#1355](https://github.com/x64dbg/x64dbg/pull/1355).

![attach dialog](https://i.imgur.com/3p2ajK6.png)

## Usual stuff

*Thanks a lot to all the contributors!*

That has been about it for this time again. If you have any questions, contact us on [Telegram](http://telegram.x64dbg.com), [Gitter](http://gitter.x64dbg.com) or [IRC](http://webchat.freenode.net/?channels=x64dbg). If you want to see the changes in more detail, check the [commit log](https://github.com/x64dbg/x64dbg/commits).

You can always get the latest release of x64dbg [here](http://releases.x64dbg.com). If you are interested in contributing, check out [this page](http://contribute.x64dbg.com).

Finally, if someone is interested in hiring me to work on x64dbg more, please contact me!