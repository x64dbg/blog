---
layout: post
title: Weekly digest 11
author: mrexodia
website: http://mrexodia.cf
contents: ["More advanced conditional tracing", "Fixed more GUI update issues", "Remember history in goto file offset and RVA", "Reverted default behavior for null and nonprint characters", "Cleaner GUI look", "Traced background in reference, source and symbol view", "ScyllaHide", "Update trace record when changing CIP manually", "Allow skipping of INT3 instruction on run", "Command to print stack trace", "Set foreground on system breakpoint", "Option to not highlight operands separately", "Removed the toggle option for certain registers", "Translations", "Usual things"]

---

This is already number eleven of the weekly digests! It will highlight the things that happened to and around x64dbg this week.

## More advanced conditional tracing

Just like [conditional breakpoints](http://help.x64dbg.com/en/latest/introduction/ConditionalBreakpoint.html) there is now more advanced [conditional tracing](http://help.x64dbg.com/en/latest/introduction/ConditionalTracing.html). This allows you to (conditionally) [log](http://help.x64dbg.com/en/latest/introduction/Formatting.html) stuff and (conditionally) execute commands during tracing. In combination with plugin commands and expression functions you can make this arbitrarily complex, yay! 

![advanced trace dialog](https://i.imgur.com/2uU1bY4.png)

## Fixed more GUI update issues

Sadly the recent [performance improvements](http://x64dbg.com/blog/#disassembly-speed-improvements) have introduced lots of GUI refresh bugs. Many were fixed and even more have been solved this week...

## Remember history in goto file offset and RVA

The goto dialog has an edit box that has a history (use up/down to browse it). This feature is now available in all goto dialogs.

## Reverted default behavior for null and nonprint characters

There was a discussion at issue [#1196](https://github.com/x64dbg/x64dbg/issues/1196) and on Reddit and it seems like nobody likes the new behavior for null and nonprint characters. It has been reverted to use dots again. If you still want to show unicode replacements you can add the following to the `GUI` section of your config file.

```
[GUI]
NonprintReplaceCharacter=25CA
NullReplaceCharacter=2022
```

## Cleaner GUI look

The GUI should look a little bit cleaner now (less borders mostly), see this GIF for a comparison.

![cleaner gui](https://i.imgur.com/50tYPvh.gif)

## Traced background in reference, source and symbol view

The trace record will now also show up in various views to help you understand where you might have already been.

![traced source](https://i.imgur.com/7906jIT.png)

## ScyllaHide

The user [gureedo](https://github.com/gureedo) has updated [ScyllaHide](https://github.com/x64dbg/ScyllaHide) and it should now work correctly on Windows 10 anniversary edition!

## Update trace record when changing CIP manually

When you set CIP it will now execute the trace record on that address.

## Allow skipping of INT3 instruction on run

The setting to skip INT3 instructions (mostly useful for ASM-level debugging) now also allows you to use the run command so INT3 instructions can be used as breakpoints directly.

## Command to print stack trace

The (currently undocumented) `printstack` command will print the callstack in the log.

```
5 call stack frames (RIP = 00007FF7995A202F , RSP = 000000957F1FFD58 , RBP = 0000000000000000 ):
000000957F1FFDB0 return to 000000957F3E4829 from x64dbg.00007FF7995A202F
000000957F1FFDB8 return to x64dbg.00007FF7995A2555 from 000000957F3E4829
000000957F1FFDF8 return to kernel32.00007FFB74F013D2 from x64dbg.00007FF7995A2555
000000957F1FFE28 return to ntdll.00007FFB75B254E4 from kernel32.00007FFB74F013D2
000000957F1FFE78 return to 0000000000000000 from ntdll.00007FFB75B254E4
```

## Set foreground on system breakpoint

[Some time ago](http://x64dbg.com/blog/2016/09/11/weekly-digest-3.html#setting-to-not-call-setforegroundwindow) an option was introduced that would disable calls to set x64dbg as the foreground window. One of these calls is now removed and x64dbg will always be on the foreground after you started a new debug session.

## Option to not highlight operands separately

A user on Telegram requested an option to expand the highlighting of the mnemonic to the whole instruction. This has now been added and this allows you to create absolutely stunning syntax highlighting!

[![ugly af](https://i.imgur.com/dacTMsc.png)](https://i.imgur.com/dacTMsc.png)

## Removed the toggle option for certain registers

General purpose registers had an option to 'Toggle' their state, but this did nothing particularly useful. This option has now been removed.

## Translations

Some time ago a [translation](http://translate.x64dbg.com) was opened at [Crowdin](https://crowdin.com). There has been great progress and here are some of the top languages. Thanks to all the translators!

- Spanish (95%)
- German (86%)
- Chinese Simplified (80%)
- Korean (64%)
- Russian (59%)
- Polish (47%)
- French (32%)

If you have some time it would be appreciated if you could translate a few sentences in your language!

## Usual things

That has been about it for this week again. If you have any questions, contact us on [Telegram](http://telegram.x64dbg.com), [Gitter](http://gitter.x64dbg.com) or [IRC](http://webchat.freenode.net/?channels=x64dbg). If you want to see the changes in more detail, check the [commit log](https://github.com/x64dbg/x64dbg/commits).

You can always get the latest release of x64dbg [here](http://releases.x64dbg.com). If you are interested in contributing, check out [this page](http://contribute.x64dbg.com).

Finally, if someone is interested in hiring me to work on x64dbg more, please contact me!