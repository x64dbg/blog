---
layout: post
title: Weekly digest 6
author: mrexodia
website: http://mrexodia.cf
contents: ["Remove all breakpoints before detaching", "Warnings when trying to set CIP to a non-executable page", "Fixed event filter plugin callbacks with Qt5", "Refactor command-related code", "Import multiple patches", "Adjust width of status label for translations", "Active view API", "Highlight ud2 and ud2b as unusual instructions", "Optimized menu order in the register view", "Lots of code improvements", "Allow debugging of AnyCPU .NET files", "Clarified SetMemoryBPX command", "Improved follow in memory map", "Highlight active view in CPU", "Print symbolic name on expression command", "Performance improvement of disasm command", "Corrected width of the Hex short dump", "Fixed bug with endianness in the float register editor", "Performance improvement in plugin loader", "Type system", "Fail assembling short jumps that don't fit in 2 bytes", "Added plugin callback to filter symbols", "Show comments/labels in the bookmark list", "Use reference view for varlist", "Allow allocation at a specified address", "Use CIP per default in imageinfo", "Final words"]

---

This is the sixth of (hopefully) many weekly digests. Basically it will highlight the things that happened to x64dbg and related projects during the week before.

## Remove all breakpoints before detaching

When detaching x64dbg all breakpoints will be removed to prevent the debuggee from crashing when reaching breakpointed code.

## Warnings when trying to set CIP to a non-executable page

When using the 'Set New Origin Here' option in the disassembler it will prompt you with a warning if the code there is not executable.

![new origin warning](https://i.imgur.com/xLgh0dV.png)

## Fixed event filter plugin callbacks with Qt5

The [PLUG_CB_WINEVENT](http://help.x64dbg.com/en/latest/developers/plugins/Callbacks/plugcbwinevent.html) callback is now working as intended again. This allows plugins to intercept and handle native window events that are usually handled by Qt. [Multiline Ultimate Assembler](http://rammichael.com/multimate-assembler) uses this to handle hotkeys registered by the plugin. You can also use it to intercept mouse clicks and paint events for example.

## Refactor command-related code

All [commands](https://github.com/x64dbg/x64dbg/tree/development/src/dbg/commands) have been cleanly organized in separate source files (matching the categories in the [documentation](http://help.x64dbg.com/en/latest/commands/index.html)). This should help new contributers to find the code they are looking for more easily.

## Import multiple patches

You can now import multiple patch files from the patch manager. Just select multiple files in the browse dialog and enjoy patching!

## Adjust width of status label for translations

The debug status label will now scale to the biggest translation width.

![translation label](https://i.imgur.com/j96WFN9.png)

## Active view API

Issue [#917](https://github.com/x64dbg/x64dbg/issues/917) has been partially addresses with this. The following code allows you to query the active view. The titles are subject to change, but the class names shouldn't change.

```c++
ACTIVEVIEW activeView;
GuiGetActiveView(&activeView);
printf("activeTitle: %s, activeClass: %s\n", activeView.title, activeView.className);
```

## Highlight ud2 and ud2b as unusual instructions

The `ud2` in addition to various other [unusual instructions](https://github.com/x64dbg/capstone_wrapper/blob/master/capstone_wrapper.cpp#L394) are marked in red to draw attention when encountered.

![ud2 unusual](https://i.imgur.com/PqyqCak.png)

## Optimized menu order in the register view

In his [blog post](http://lifeinhex.com/why-im-not-using-x64dbg), kao mentioned that the context menu in the register view was bloated. This has now been addresses and menu options are roughly ordered to how often they are used in practice. If you see more issues like this, please let us know [here](http://issues.x64dbg.com).

Before:

![reg before](http://lifeinhex.com/wp-content/uploads/2016/09/values_menu.png)

After:

![reg after](https://i.imgur.com/yspjo0R.png)

## Lots of code improvements

Various static analysis runs with [Coverity](https://scan.coverity.com), [ReSharper](https://www.jetbrains.com/resharper-cpp) and [Visual Studio](https://msdn.microsoft.com/en-us/library/ms182025.aspx) provided lots of small bugs or anomalies and these have been fixed.

## Allow debugging of AnyCPU .NET files

Pull request [#1124](https://github.com/x64dbg/x64dbg/pull/1124) addressed a bug where .NET files with AnyCPU would not load in x64dbg because their headers had the wrong PE architecture.

## Clarified SetMemoryBPX command

The [SetMemoryBPX](http://help.x64dbg.com/en/latest/commands/breakpoint-control/SetMemoryBPX.html) command has been slightly changed. There was confusion in issue [#1123](https://github.com/x64dbg/x64dbg/issues/1123) what read, write and access mean exactly. This has been clarified in the documentation and the correct type of memory breakpoint is now set for 'Access' when using the GUI.

## Improved follow in memory map

When using the follow in memory map option it will now scroll to the entry requested, it will also show the memory map if you weren't looking at it already.

## Highlight active view in CPU

The view that is currently active will be highlighted with a thin black border.

![highlight active view](https://i.imgur.com/XlAU2qL.png)

## Print symbolic name on expression command

When typing an unknown command in the command bar your text will be evaluated as an expression and the result will be printed. When the expression resolves to a symbolic address it will now also display the symbol name.

![symbolic expression address](https://i.imgur.com/ufUlv01.png)

## Performance improvement of disasm command

The [disasm](http://help.x64dbg.com/en/latest/commands/gui/disasm.html) command is now more responsive.

## Corrected width of the Hex short dump

The default width of the 'hex short' dump view didn't show all values, this has now been corrected.

![hex short dump](https://i.imgur.com/MLtWHNg.png)

## Fixed bug with endianness in the float register editor

Issue [#1127](https://github.com/x64dbg/x64dbg/issues/1127) has been fixed. When showing FPU registers as big endian the editor would interpret the values incorrectly.

![issue 1127](https://i.imgur.com/9YO9VTw.png)

## Performance improvement in plugin loader

The plugin callback system didn't have a separation on type, which meant that performance-critical locations that used plugin callbacks would pay for thing like menu callbacks. Every callback now has a separate list which solves the problem. 

## Type system

Issue [#1108](https://github.com/x64dbg/x64dbg/issues/1108) that requests displaying types has been partially addressed. The basics of a [type system](https://github.com/x64dbg/x64dbg/blob/development/src/dbg/types.h) have been implemented and you can now create and view types.

There is an [example script](https://gist.github.com/mrexodia/e949ab26d5986a5fc1fa4944ac68147a) available and the documentation is [here](http://help.x64dbg.com/en/latest/commands/types/index.html). There will be a blog post later explaining the type system in more detail.

[![stack struct](https://i.imgur.com/dkMDoE7.png)](https://i.imgur.com/dkMDoE7.png)

## Fail assembling short jumps that don't fit in 2 bytes

When assembling short jumps with [keystone](http://www.keystone-engine.org) you could assemble short jumps that are not actually show. [RaMMicHaeL](https://github.com/RaMMicHaeL) has addressed this in pull request [#1134](https://github.com/x64dbg/x64dbg/pull/1134).

## Added plugin callback to filter symbols

Various symbols have no real meaning and these are filtered from view. Plugins can now register custom filter callbacks. This has been implemented by [shamanas](https://github.com/shamanas) in pull request [#1135](https://github.com/x64dbg/x64dbg/pull/1135).

## Show comments/labels in the bookmark list

When listing bookmarks your comments/labels will now be shown in the list. This was implemented by [Atvaark](https://github.com/Atvaark) in pull request [#1136](https://github.com/x64dbg/x64dbg/pull/1136).

## Use reference view for varlist

The [varlist](http://x64dbg.readthedocs.io/en/latest/commands/variables/varlist.html) command will now show variables in the reference view instead of the console.

![varlist reference](https://i.imgur.com/SkFoGvA.png)

## Allow allocation at a specified address

The [alloc](http://x64dbg.readthedocs.io/en/latest/commands/memory-operations/alloc.html) command now has an optional second parameter that allows you to specify an address to allocate memory at (similar to VirtualAlloc).

## Use CIP per default in imageinfo

The [imageinfo](http://x64dbg.readthedocs.io/en/latest/commands/analysis/imageinfo.html) command now uses CIP when no address is specified.

## Final words

That has been about it for this week again. If you have any questions, contact us on [Telegram](http://telegram.x64dbg.com), [Gitter](http://gitter.x64dbg.com) or [IRC](http://webchat.freenode.net/?channels=x64dbg). If you want to see the changes in more detail, check the [commit log](https://github.com/x64dbg/x64dbg/commits).

You can always get the latest release of x64dbg [here](http://releases.x64dbg.com). If you are interested in contributing, check out [this page](http://contribute.x64dbg.com).

Finally, if someone is interested in hiring me to work on x64dbg more, please contact me!