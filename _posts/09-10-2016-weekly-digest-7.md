---
layout: post
title: Weekly digest 7
author: mrexodia
website: http://mrexodia.cf

---

This is the seventh of (hopefully) many weekly digests. Basically it will highlight the things that happened to x64dbg and related projects during the week before.

## Plugin page

There is now a [wiki page](http://plugins.x64dbg.com) available dedicated to x64dbg plugins. It contains various templates and also a list of plugins. If you wrote a plugin yourself, feel free to add it to the list!

## Variable list will now be shown in the reference view

The command [varlist](http://x64dbg.readthedocs.io/en/latest/commands/variables/varlist.html) will now show the available variables in the reference view instead of in the log.

![variable references](https://i.imgur.com/LbNSLcZ.png)

## Fixed a crash in the pluginload command

Previously the [pluginload](http://x64dbg.readthedocs.io/en/latest/commands/plugins/plugload.html) commands would not check the number of arguments and it would read in bad memory. See issue [#1141](https://github.com/x64dbg/x64dbg/issues/1141) for more details.

## Added undo in registers view

[Atvaark](https://github.com/Atvaark) added an 'Undo' option to revert register changes in pull request [#1142](https://github.com/x64dbg/x64dbg/pull/1142).

![undo register](https://i.imgur.com/tVpXtjI.png)

## Hide actions in a submenu

Think there are too many entries in the disassembly context menu? You can now move menu entries you don't use to the 'More commands' section to make your life less complicated. This also works for some other menus but [some](https://github.com/x64dbg/x64dbg/issues/1154) more [work](https://github.com/x64dbg/x64dbg/issues/1155) is required to make it possible everywhere.

![more commands](https://i.imgur.com/Nn2Go1o.png) 

## Better character recognition in the info box

The info box will now recognize escaped characters in addition to printable characters.

## Character recognition in comments

Pull request [#1145](https://github.com/x64dbg/x64dbg/pull/1145) added character recognition requested in issue [#1128](https://github.com/x64dbg/x64dbg/issues/1128).

![character comments](https://i.imgur.com/prSMBuD.png)

## Goto origin in memory map

[Atvaark](https://github.com/Atvaark) has added the Goto -> Origin option in the memory map in pull request [#1146](https://github.com/x64dbg/x64dbg/pull/1146). This will show you the memory page that EIP/RIP is currently in.

![goto origin](https://i.imgur.com/KTJrtbB.png)

## Highlight jump lines in the sidebar if the destination is selected

The branch lines in the sidebar are now highlighted when selecting the branch destination. This is in addition to the xref feature that was implemented some time ago. If you want xref analysis use the command [analx](http://x64dbg.readthedocs.io/en/latest/commands/analysis/analxrefs.html), analyze a single function with the 'A' button or use the [analr](http://x64dbg.readthedocs.io/en/latest/commands/analysis/analrecur.html) command. For more analysis commands, see the [analysis](http://x64dbg.readthedocs.io/en/latest/commands/analysis/index.html) section of the documentation.

![highlight destination](https://i.imgur.com/d5IH0vi.png)

## Various updates to the mnemonic database

If you are looking for a quick description of every instruction you can use the 'Show mnemonic brief' (Ctrl+Alt+F1) option to get a brief description of every opcode. The [mnemonic database](https://github.com/x64dbg/idaref) used for this has been slightly updated and should give better results in some cases.  

![mnemonicbrief](https://i.imgur.com/xJbRByS.png)

## Open file/directory options for the source view

You can now open the file/directory of the source file you are currently debugging in to view the file in your favorite editor.

![open source file](https://i.imgur.com/ydB5tvl.png)

## Next/Previous/Hide tab

The third and fourth(!!!) pull request by [Atvaark](https://github.com/Atvaark) this week ([#1152](https://github.com/x64dbg/x64dbg/pull/1152) and [#1153](https://github.com/x64dbg/x64dbg/pull/1153)) added more flexibility with tabs. You can now easily hide tabs and switch between them.

## Import/export database

It is now possible to use the [dbload](http://x64dbg.readthedocs.io/en/latest/commands/user-database/dbload.html) and [dbsave](http://x64dbg.readthedocs.io/en/latest/commands/user-database/dbsave.html) commands to import/export databases to an arbitrary location. Once you have an exported the database you can import it in IDA with the [x64dbgida](https://github.com/x64dbg/x64dbgida) plugin. This also works the other way around!

![export database](https://i.imgur.com/SPsb6Tl.png)

![import database](https://i.imgur.com/x3c35BU.png)

## Better IsJumpGoingToExecute

The function that analyzes the flags to see if a jump is going to execute has been re-implemented and should now be faster. In addition to that the `loop` instruction is correctly analyzed now. 

## Usual stuff

That has been about it for this week again. If you have any questions, contact us on [Telegram](http://telegram.x64dbg.com), [Gitter](http://gitter.x64dbg.com) or [IRC](http://webchat.freenode.net/?channels=x64dbg). If you want to see the changes in more detail, check the [commit log](https://github.com/x64dbg/x64dbg/commits).

You can always get the latest release of x64dbg [here](http://releases.x64dbg.com). If you are interested in contributing, check out [this page](http://contribute.x64dbg.com).

Finally, if someone is interested in hiring me to work on x64dbg more, please contact me!