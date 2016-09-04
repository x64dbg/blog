---
layout: post
title: Weekly digest 2
author: mrexodia
website: http://mrexodia.cf

---

This is the second of (hopefully) many weekly digests. Basically it will highlight the things that happened to x64dbg and related projects during the week before.

## Font in the command completion dialog

The command completion dialog and the command edit now use the same font as the log view.

![completion font](https://i.imgur.com/Z6rWVG4.png)

## Added memdump option to savedata

The [savedata](http://x64dbg.readthedocs.io/en/latest/commands/data/savedata.html) command now allows you to use `:memdump:` as a filename to create a file `memdump_pid_addr_size.bin` in the x64dbg directory. This is useful for scripting purposes.

## Fixed various general purpose instructions

The commands [inc](http://x64dbg.readthedocs.io/en/latest/commands/general-purpose/inc.html) and [dec](http://x64dbg.readthedocs.io/en/latest/commands/general-purpose/dec.html) work again and the [bswap](http://x64dbg.readthedocs.io/en/latest/commands/general-purpose/bswap.html) command can now also be used when not debugging.

Also the operators `<<<` and `>>>` ([rol](http://x64dbg.readthedocs.io/en/latest/commands/general-purpose/rol.html) and [ror](http://x64dbg.readthedocs.io/en/latest/commands/general-purpose/ror.html)) have been added to the expression parser.

## More usable disassembly popup

The disassembly popup menu now also works on instruction tokens directly (such as immediate or memory addresses).

![popup](https://i.imgur.com/FjQc43L.png)

## Fixed empty watchdog menu

The watchdog menu was bugged and would always be empty, this has been resolved.

![non-empty](https://i.imgur.com/j6LP7wL.png)

## Trace record tracing works again

The [TraceIntoIntoTraceRecord](http://help.x64dbg.com/en/latest/commands/debug-control/TraceIntoIntoTraceRecord.html) command and various other trace record based tracing command had incorrect behavior because of a typo, everything works again now!

## Animation into has been implemented!

[torusrxxx](https://github.com/torusrxxx) added animate into/over in pull request [#1020](https://github.com/x64dbg/x64dbg/pull/1020)!

![animate into](https://i.imgur.com/nWSfnfV.gif)

## Better unicode support

The dump window now uses the local code page per default instead of only displaying `latin1` characters, there has also been a menu added for displaying the last code page which is convenient for non-English speaking users. See pull request [#1023](https://github.com/x64dbg/x64dbg/pull/1023) for more details.

![ascii](https://i.imgur.com/khkHtNz.png)

## Execute a script on attach or initialize

A global or per-debuggee script can now be executed on initialization. See pull request [#1026](https://github.com/x64dbg/x64dbg/pull/1026) for more details.

## Create a thread in the debuggee

The [createthread](http://x64dbg.readthedocs.io/en/latest/commands/debug-control/createthread.html) command has been added and you can also right click a location in the disassembly and directly spawn a new thread from that location. See pull request [#1028](https://github.com/x64dbg/x64dbg/pull/1028).

## Performance improvements in TitanEngine

For every (single) register query TitanEngine would read the entire context (including the time-demanding AVX registers). This has been fixed and stepping can be observed to be much faster in some cases.

## Auto scrolling when moving the mouse out of views

The oldest unresolved issue [#22](https://github.com/x64dbg/x64dbg/issues/22) has been resolved in pull request [#1029](https://github.com/x64dbg/x64dbg/pull/1029) and the disassembly (and other views) will now scroll if you move your mouse outside of the view.

![auto scroll](https://i.imgur.com/ezkjlNp.gif)

## Expression functions

The (currently) undocumented feature of expression functions has been extended with various new functions, see [expressionfunctions.cpp](https://github.com/x64dbg/x64dbg/blob/development/src/dbg/expressionfunctions.cpp#L41) if you want to know more.

Hint: you can simulate branch tracing with the command `TraceIntoConditional dis.isbranch(cip) || dis.isret(cip)`

Expect a blog post on this somewhere this month.

## Allow modification of the singleshoot flag

Previously it was impossible to change a singleshoot breakpoint to a persistent one, this has now been implemented in the breakpoint editor and the [SetBreakpointSingleshoot](http://x64dbg.readthedocs.io/en/latest/commands/breakpoints-conditional/SetBreakpointSingleshoot.html) command.

## Added NTSTATUS codes

The [NTSTATUS](https://msdn.microsoft.com/en-us/library/cc704588.aspx) code names have been added to the exception handling, this should cover pretty much all exception names that are hardcoded in Windows.

## Updated color schemes

Many people are probably unaware of the x64dbg [wiki](http://wiki.x64dbg.com). I slightly adapted some of the [color schemes](https://github.com/x64dbg/x64dbg/wiki/Color-Schemes) to support trace record and graphs better. You can now also customize the background of the graph view. Feel free to add your schemes or ping me if you have an improvement for an existing one.

![color scheme](https://i.imgur.com/1Jf38zh.png)

Also, Storm Shadow updated some of his [stylesheets](https://github.com/x64dbg/x64dbg/wiki/Stylesheets), check it out!

![stylesheet](https://cloud.githubusercontent.com/assets/3592375/15633822/abd605c8-25b6-11e6-97af-d3202cc3f90c.png)

## Final words

That has been about it for this week again. If you have any questions, contact us on [Telegram](http://telegram.x64dbg.com), [Gitter](http://gitter.x64dbg.com) or [IRC](http://webchat.freenode.net/?channels=x64dbg). If you want to see the changes in more detail, check the [commit log](https://github.com/x64dbg/x64dbg/commits).

You can always get the latest release of x64dbg [here](http://releases.x64dbg.com). If you are interested in contributing, check out [this page](http://contribute.x64dbg.com).

Finally, if someone is interested in hiring me to work on x64dbg more, please contact me!