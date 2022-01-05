---
layout: post
title: Weekly digest 4
author: mrexodia
website: https://mrexodia.github.io
contents: ["Fixed goto dialog for reserved memory pages", "Different trace record + selection color in the graph", "No foreground window per default", "Disassembly preview is now theme aware", "Search pattern in module", "Fixed intermodular calls in module", "Added various memory-related expression functions", "Script DLL template for Visual Studio", "UpxUnpacker for x64dbgpy", "Register view enhancements", "University", "Final words"]

---

This is the fourth of (hopefully) many weekly digests. Basically it will highlight the things that happened to x64dbg and related projects during the week before.

## Fixed goto dialog for reserved memory pages

You can now no longer disassemble in reserved memory pages, but the goto dialog would still mark them as 'valid address' which has now been fixed.

## Different trace record + selection color in the graph

The color for trace record + selection is now the mix of both colors:

![trace selection](https://i.imgur.com/y92GlyY.png)

## No foreground window per default

The option to not call `SetForegroundWindow` when the debugger pauses is now enabled per default, this fixed lots of annoyances with scripting.

## Disassembly preview is now theme aware

Previously the disassembly preview would look horrible if you used a darker theme, it will now adjust to that theme properly:

![disassembly preview](https://i.imgur.com/5aIf5FT.png)

## Search pattern in module

You can now search a pattern in the whole module from the disassembly context menu:

![find pattern](https://i.imgur.com/59xcOck.png)

## Fixed intermodular calls in module

Issue [#509](https://github.com/x64dbg/x64dbg/issues/509) has been resolved and you can now properly search (all) modules.

## Added various memory-related expression functions

The functions `mem.base`, `mem.size`, `mem.iscode`, and `mem.decodepointer` have been added. See the [documentation](http://help.x64dbg.com/en/latest/introduction/Expression-functions.html) for more information.

## Script DLL template for Visual Studio

The [scriptdll](http://x64dbg.readthedocs.io/en/latest/commands/script/scriptdll.html) command has been documented and there is an example [UpxUnpacker](https://github.com/x64dbg/Scripts/blob/master/UpxUnpacker.cpp) available, but the barrier of entry was still too high. [ScriptDllTemplate](https://github.com/x64dbg/ScriptDllTemplate) is a template project for Visual Studio so you don't have to worry about setting up and you can start natively scripting x64dbg.

![Script DLL Template](https://i.imgur.com/y216Nr2.png)

A Visual Studio template for regular plugins is on the way.

## UpxUnpacker for x64dbgpy

There has been a Python scripting plugin available for quite some time ([x64dbgpy](https://github.com/x64dbg/x64dbgpy)), now there is a very simple [UpxUnpacker.py](https://github.com/x64dbg/Scripts/blob/master/UpxUnpacker.py) available. We are in need of contributers for x64dbgpy, so please come in contact if you want more powerful Python scripting in x64dbg.

## Register view enhancements

In pull request [#1098](https://github.com/x64dbg/x64dbg/pull/1098) torusrxxx added various enhancements to the registers view. The configured endianness is now respected in the edit dialog and there are tooltips for various uncommon registers and flags:

![registers enhancement](https://i.imgur.com/7XMb2O5.png)

## University

For me the university started again, which means I will have less time to work on x64dbg. Probably I will have more time to work on x64dbg during the Christmas break again. If you have an hour of free time, please try to solve a few [easy issues](http://easy.x64dbg.com)!

## Final words

That has been about it for this week again. If you have any questions, contact us on [Telegram](http://telegram.x64dbg.com), [Gitter](http://gitter.x64dbg.com) or [IRC](http://webchat.freenode.net/?channels=x64dbg). If you want to see the changes in more detail, check the [commit log](https://github.com/x64dbg/x64dbg/commits).

You can always get the latest release of x64dbg [here](http://releases.x64dbg.com). If you are interested in contributing, check out [this page](http://contribute.x64dbg.com).

Finally, if someone is interested in hiring me to work on x64dbg more, please contact me!