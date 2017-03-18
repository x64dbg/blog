---
layout: post
title: Weekly digest 1
author: x64dbg
website: http://x64dbg.com

---

This is the first of (hopefully) many weekly digests. Basically it will highlight the things that happened to x64dbg and related projects during the week before.

## Improvements to the attach dialog

[Forsari0](https://github.com/Forsari0) contributed this in pull request [#994](https://github.com/x64dbg/x64dbg/pull/994), the attach dialog will now also show the command line arguments for every process:

![attach dialog](https://i.imgur.com/UTo7MUy.png)

## Disable debuggee notes when debugging

Previously it was possible to edit notes in the 'Debuggee' tab, even when you were not debugging anything. These notes would be forever lost so now you can no longer see that tab when not debugging. 

## Translation of the DBG

In addition to the Qt interface translation, [torusrxxx](https://github.com/torusrxxx) added the infrastructure in the DBG to translate log strings. See pull request [#998](https://github.com/x64dbg/x64dbg/pull/998) for more details.

![translated](http://i.imgur.com/m6pbWzU.png)

## Search box locking in symbol view

Yet another contribution by [Forsari0](https://github.com/Forsari0), in pull request [#1003](https://github.com/x64dbg/x64dbg/pull/1003). He added a checkbox in the symbol view that allows you to save your search query when switching to other modules, allowing you to repeat the same query in various different modules:

![symbol lock](https://i.imgur.com/hCJV7Lv.png)

## Various GUI improvements

[torusrxxx](https://github.com/torusrxxx) added various useful interface improvements in pull request [#1004](https://github.com/x64dbg/x64dbg/pull/1004):

-  Forward and Backward mouse buttons found in some models of mice.
-  No confirmation when adding functions.
-  Allocate memory from the dump menu.
-  Placeholder tips for learners.
-  Disable/Cancel log redirect (issue [#939](https://github.com/x64dbg/x64dbg/issues/939))
-  Use Windows configuration for the singe step scroll size (issue [#1000](https://github.com/x64dbg/x64dbg/issues/1000))

Here is an example of those placeholder tips:

![placeholder](http://i.imgur.com/NixhO4s.png)

## Don't freeze when the debuggee doesn't close properly

In certain (rare) cases, the debuggee cannot be terminated correctly. TitanEngine will wait for `EXIT_PROCESS_DEBUG_EVENT`, but in some cases this event is not received and there will be an infinite debug loop, thus freezing x64dbg when trying to terminate the process. This has been worked around by setting the maximum wait time to 10 seconds. 

## Warn when setting a software breakpoint in non-executable memory

If you attempt to set a breakpoint in a data location, x64dbg will warn you and ask if you are certain about this. Usually the only thing that comes out of it is data corruption:

![warning](https://i.imgur.com/IGV06Ht.png)

## Signed and unsigned bytes in the dump

The dump views now include signed and unsigned byte views:

![signed bytes](https://i.imgur.com/T0as8JI.png)

## Fixed WOW64 redirection issues

See [the dedicated blog post](/blog/2016/08/27/supporting-wow64-debugging.html) for more information.

## Fixed invalid save to file sizes

When using the `Binary -> Save to file` option the `savedata` command would be executed but with the decimal size as argument, thus saving far too much data. This has been fixed.

![save data](https://i.imgur.com/bS6RVC5.png)

## Added imageinfo command

During a discussion in the [Telegram channel](http://telegram.x64dbg.com), someone mentioned [OllySEH](https://tuts4you.com/download.php?view.3390) and I decided to implement a similar command in x64dbg. The command `imageinfo modbase` will show you a summary of the `FileHeader.Characteristics` and `OptionalHeader.DllCharacteristics` fields:

```
Image information for ntdll.dll
Characteristics (0x2022):
  IMAGE_FILE_EXECUTABLE_IMAGE: File is executable (i.e. no unresolved externel references).
  IMAGE_FILE_LARGE_ADDRESS_AWARE: App can handle >2gb addresses
  IMAGE_FILE_DLL: File is a DLL.
DLL Characteristics (0x4160):
  IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE: DLL can move.
  IMAGE_DLLCHARACTERISTICS_NX_COMPAT: Image is NX compatible
```

Adding this command required a small change in [TitanEngine](bitbucket.org/titanengineupdate/titanengine-update) (the `DllCharacteristics` field was not supported).

## Updated Yara to 3.5.0

Quite recently the latest version of Yara (3.5.0) was released. This version is now also updated in x64dbg!

![yara scan](https://i.imgur.com/V64mRwf.png)

## Work on GleeBug

[GleeBug](https://github.com/x64dbg/GleeBug) is the planned new debug engine for x64dbg. During the holidays there has been quite a bit of work with regards to memory breakpoints. See the [commit log](https://github.com/x64dbg/GleeBug/commits/membp) for in-depth information.

GleeBug has been in development for about 1.5 years now. It can currently replace TitanEngine for x64dbg (giving massive performance improvements), but not all features are implemented yet. The main blockers are currently:

- Memory breakpoints
- Extended (XMM, YMM) register support
- Breakpoint memory transparency

For reference, when tracing with TitanEngine, the events/s counter is around 250. When tracing with GleeBug, this counter comes near 30000 events/s in some cases!

![performance](https://i.imgur.com/TAfH2Qg.png)

## Final words

That has been about it for this week. If you have any questions, contact us on Telegram/Gitter/IRC. If you want to see the changes in more detail, check the [commit log](https://github.com/x64dbg/x64dbg/commits).

You can always get the latest release of x64dbg [here](http://releases.x64dbg.com). If you are interested in contributing, check out [this page](http://contribute.x64dbg.com).