---
layout: post
title: Weekly digest 16
author: mrexodia
website: http://mrexodia.cf

---

This is number sixteen of the weekly digests. Last week I have been sick so this one will again account for two weeks...

## Christmas

Merry Christmas everyone!

## x64dbgpylib

Some effort has been made towards supporting [mona.py](https://github.com/corelan/mona) by porting [windbglib](https://github.com/corelan/windbglib) to [x64dbgpy](https://github.com/x64dbg/x64dbgpy). You can help out by porting a few functions outlined in [this](https://github.com/x64dbg/x64dbgpylib/issues/1) issue.

## Translations

Various people worked very hard to completely translate x64dbg in Korean, the state of the translation is as follows:

- Korean (100%)
- Turkish (96%)
- Dutch (94%)
- Chinese Simplified (89%)
- Spanish (87%)
- German (87%)
- Russian (83%)

## Restart as admin

If a process requires elevation on start, CreateProcess would fail with `ERROR_ELEVATION_REQUIRED`. This is now detected and you can allow x64dbg to restart itself as administrator.

![restart as admin question](http://i.imgur.com/U4Avy0y.png)

Certain operations (such as setting x64dbg as JIT debugger), also require elevation and a menu option has been added! It will automatically reload the current debuggee, but it (obviously) cannot restore the current state so think of this as the restart option.

![restart as admin menu](http://i.imgur.com/gJTASTX.png)

## Secure symbol servers

The default symbol servers have been switched to HTTPS. See pull request [#1300](https://github.com/x64dbg/x64dbg/pull/1300) by xiaoyinl.

*Microsoft symbol servers currently have issues and you might have to try to download symbols multiple times.*

## Fixed weird display issue on the tab bar

Issue [#1339](https://github.com/x64dbg/x64dbg/issues/1339) has been fixed and the buttons to scroll in the tab bar should now appear correctly.

![button bug](https://cloud.githubusercontent.com/assets/4343900/20826207/40584b9a-b8a4-11e6-8007-3f724fc8bb49.png)

## Various copying enhancements

There are various enhancements to copying addresses and disassembly. See pull request [#1363](https://github.com/x64dbg/x64dbg/pull/1363) by ThunderCls for more details.

## Fixed a bug if IMAGE\_DOS\_HEADERS is malformed

Executables with a malformed header, where `e_lfanew` points higher than 0x1000 bytes would be detected as invalid by x64dbg. This has now been corrected by jossgray in pull request [#1369](https://github.com/x64dbg/x64dbg/pull/1369).

## Fixed some bugs with handling big command lines

The maximum command line size has been increased to 65k to support modification of very long command lines (such as custom JVMs with many arguments).

## Launcher improvements

There have been various improvements to the launcher, mostly with .NET executables and also the handling of the `IMAGE_DOS_HEADER`.

## Load/free library in the symbols view

Pull request [#1372](https://github.com/x64dbg/x64dbg/pull/1372) by ThunderCls introduced the `freelib` command that allows you to unload a library from the debuggee. In addition to a GUI for the [loadlib](http://x64dbg.readthedocs.io/en/latest/commands/misc/loadlib.html) command.

![free library menu](http://i.imgur.com/2kKMz5n.png)

## String search improvements

There have been various improvements to the string search and UTF-8 strings will be escaped correctly.

## Don't change the active window when closing a tab

Previously if you detached a tab and pressed the close button it would keep that tab active, while usually the desired behaviour is to hide the tab in the background. See pull request [#1375](https://github.com/x64dbg/x64dbg/pull/1375) by changeofpace for more details.

## Workaround for a capstone bug

The instruction `test eax, ecx` is [incorrectly disassembled](https://github.com/aquynh/capstone/issues/702) by capstone as `test ecx, eax`. This has been worked around by the following ugly code that simply swaps the arguments...

```c++
//Nasty workaround for https://github.com/aquynh/capstone/issues/702
if(mSuccess && GetId() == X86_INS_TEST && x86().op_count == 2 && x86().operands[0].type == X86_OP_REG && x86().operands[1].type == X86_OP_REG)
{
    std::swap(mInstr->detail->x86.operands[0], mInstr->detail->x86.operands[1]);
    char* opstr = mInstr->op_str;
    auto commasp = strstr(opstr, ", ");
    if(commasp)
    {
        *commasp = '\0';
        char second[32] = "";
        strcpy_s(second, commasp + 2);
        auto firstsp = commasp;
        while(firstsp >= opstr && *firstsp != ' ')
            firstsp--;
        if(firstsp != opstr)
        {
            firstsp++;
            char first[32] = "";
            strcpy_s(first, firstsp);
            *firstsp = '\0';
            strcat_s(mInstr->op_str, second);
            strcat_s(mInstr->op_str, ", ");
            strcat_s(mInstr->op_str, first);
        }
    }
}
```

## Improve autocomments

The option 'Autocomments only on CIP' would only show non-user comments on the CIP instruction. Issue [#1386](https://github.com/x64dbg/x64dbg/issues/1383) proposed a different solution and currently only register-based comments will be hidden.

## Save and restore the window position and size

Pull request [#1385](https://github.com/x64dbg/x64dbg/pull/1385) by changeofpace introduced saving of the main window position and size.

## Allow permanent highlighting mode

Some people prefer the way IDA handles highlighting. Clicking on a register/immediate will highlight it everywhere else, even if you want to keep the previous highlighting but want to click somewhere else. I personally think this is a bad way of handling highlighting, but an option has been introduced that has *similar* behaviour. Pull request [#1388](https://github.com/x64dbg/x64dbg/pull/1388) had similar functionality, but I rewrote it to be optional and more intuitive.

![enable permanent highlighting mode](http://i.imgur.com/UM7xhY8.png)

If you don't click on a highlightable object it will not change the highlighting so (unlike IDA) you can do your normal operations while keeping the desired highlighting.

![highlighting behaviour](http://i.imgur.com/gjxkWBt.gif)

## Copy as HTML

Pull request [#1394](https://github.com/x64dbg/x64dbg/pull/1394) by torusrxxx introduces an option that copies the disassembly/dump as HTML allowing you to paste it in Word:

![x64dbg word](http://i.imgur.com/r8qZAJc.png)

## Usual things

*Thanks a lot to all the contributors!*

That has been about it for this time again. If you have any questions, contact us on [Telegram](http://telegram.x64dbg.com), [Gitter](http://gitter.x64dbg.com) or [IRC](http://webchat.freenode.net/?channels=x64dbg). If you want to see the changes in more detail, check the [commit log](https://github.com/x64dbg/x64dbg/commits).

You can always get the latest release of x64dbg [here](http://releases.x64dbg.com). If you are interested in contributing, check out [this page](http://contribute.x64dbg.com).

Finally, if someone is interested in hiring me to work on x64dbg more, please contact me!