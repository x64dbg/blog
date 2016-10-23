---
layout: post
title: Weekly digest 9
author: mrexodia
website: http://mrexodia.cf

---

This is already number nine of the weekly digests! It will highlight the things that happened to and around x64dbg this week.

## Autocomment for call $0

Thanks to [joesavage](https://github.com/joesavage) there will now be a comment on `call $0` (call the next instruction). This is useful for various packers that use this instruction to get the address of the current instruction.

![call 0](https://i.imgur.com/cdtOyYk.png)

## Improvements to the disassembly popup

The disassembly popup will now do slightly better analysis of where to stop displaying the preview. It will do some basic heuristic analysis to determine function ends and thus where to stop.

![analysis branch](https://i.imgur.com/smXYoGs.png)

![analysis jmp](https://i.imgur.com/2Jey427.png)

## Source line and autocomments

Autocomments will now combine source line information and other information. This means that you can more easily spot the context even if you have line information loaded!

![source and autocomment](https://i.imgur.com/lcEMLEP.png)

## Show CIP in graph overview

The current CIP block will now be highlighted in your configured color in the graph overview.

![cip overview](https://i.imgur.com/UDAzY51.png)

## Less jumpy experience while debugging in the graph

The initial GIF that showed off graph debugging had a very "jumpy" feel, mainly because the currently selected instruction would be forced to be shown as close to the middle as possible. It will now only force the middle if the selection is out of view. You can still force the current instruction in the middle by using the "Refresh" action in the context menu.

![force refresh](https://i.imgur.com/1HnbRVK.png)

![stable debugging](https://i.imgur.com/FjP8Xf0.gif)

## Fine-grained dump offset control

In some cases you might want to slightly adjust the dump alignment without having to use the go to dialog. You can now do this with Ctrl+Up/Down. All it does is set the first dump address to the current address +/-1.

![adjust alignment](https://i.imgur.com/qapeCje.gif)

## Allow checkable menu items for plugins

The [_plugin_menuentrysetchecked](http://help.x64dbg.com/en/latest/developers/plugins/API/menuentrysetchecked.html) API allows you to set your plugin menu items as checkable. This can be useful for visualizing boolean options or just for having some fun!

![checked plugin menu](https://i.imgur.com/N0iBS5I.png)

## Codename iconic

Lots of (almost all) context menu items now have icons for a more fun and colorful experience!

![iconic](https://i.imgur.com/Fqz1pQb.png)

## Updated capstone, keystone and asmjit

The dependencies [capstone](http://www.capstone-engine.org), [keystone](http://www.keystone-engine.org) and [asmjit](https://github.com/x64dbg/asmjit_xedparse) have been updated. This fixed various bugs with assembling and disassembling.

## Copy as base64

The data copy dialog now allows you to copy data as Base64. Quite useful if you need to dump some private keys or something. It also supports various other formats, including C-style array (various types), string, GUID, IP addresses and Delphi arrays.

![copy base64](https://i.imgur.com/xQ00j45.png)

## Callback for changed selection

It is now possible to register the `CB_SELCHANGED` callback (currently undocumented). This callback informs you of selection changes.

```c++
typedef struct
{
    int hWindow;
    duint VA;
} PLUG_CB_SELCHANGED;
```

This can be used in complement with the `GuiAddInfoLine` function to do context-aware analysis and display it in the GUI.

## Analysis plugins

Don't like the analysis x64dbg does? Don't worry, you can now fully customize the graph analysis in a plugin. The (currently undocumented) `CB_ANALYZE` plugin callback allows you to troll your friends by adding exits to every terminal node with this simple code.

```c++
PLUG_EXPORT void CBANALYZE(CBTYPE cbType, PLUG_CB_ANALYZE* info)
{
    auto graph = BridgeCFGraph(&info->graph, true);
    for(auto & nodeIt : graph.nodes)
    {
        auto & node = nodeIt.second;
        if(node.terminal)
            node.exits.push_back(graph.entryPoint);
    }
    info->graph = graph.ToGraphList();
}
```

![maximum confusion](http://i.imgur.com/IvwuqU5.png)

Trolls aside, this can be extremely powerful if applied in the right manner. For example deobfuscate VMProtect handlers on the fly...

![vmprotect surgery](https://i.imgur.com/IC7YW4c.png)

## Maximum trace count option

The default maximum step count for tracing is now customizable through the settings dialog.

![max trace count](https://i.imgur.com/9kmXJOT.png)

## Copy selection to file

Issue [#1096](https://github.com/x64dbg/x64dbg/issues/1096) has been fixed in pull request [#1177](https://github.com/x64dbg/x64dbg/pull/1177) by [shamanas](https://github.com/shamanas). You can now copy bigger selections directly to a file.

## Disassembly speed improvements

There has been quite a big improvement in disassembly and overall GUI speed. The disassembly would reload itself three times, effectively disassembling every visible instruction six times. This has now been reduced to disassembling once. Additionally the GUI would be force-refreshed unnecessarily which should now also be fixed. If you encounter any issues with this, please report an [issue](http://issues.x64dbg.com). Scrolling in the current view will always force-refresh it. 

## Copy symbolic name

In addition to the "Help on Symbolic Name" option, that uses your favorite search engine (Google) to help you figure out what's going on, you can now also copy the symbolic name directly if you need it for some reason. This was also implemented by [shamanas](https://github.com/shamanas)!

![help on symbolic name](https://i.imgur.com/8o46bjP.png)

![copy symbolic name](https://i.imgur.com/dGXl4yV.png)

## Allow customizing of the main menus

Ever thought the menus in x64dbg are too complicated? You can now hide options you don't use in `Options | Customize menus`

![uncomplicated menu](https://i.imgur.com/tnvSeda.png)

## Fixed a bug with little/big endian when editing FPU registers

The FPU register edit dialog will now respect the configured endianness and always change the register bytes to the way you see it in the edit dialog. 

## Show extended exception information on exception events

The [exinfo](http://x64dbg.readthedocs.io/en/latest/commands/analysis/exinfo.html) command is now executed every time an exception occurs to provide you with more information while examining the log later on.

```
EXCEPTION_DEBUG_INFO:
           dwFirstChance: 1
           ExceptionCode: C0000005 (EXCEPTION_ACCESS_VIOLATION)
          ExceptionFlags: 00000000
        ExceptionAddress: 00007FF7F686240F x64dbg.00007FF7F686240F
        NumberParameters: 2
ExceptionInformation[00]: 0000000000000001
ExceptionInformation[01]: FFFF8F500045DF0C
First chance exception on 00007FF7F686240F (C0000005, EXCEPTION_ACCESS_VIOLATION)!
```

## Final words

That has been about it for this week again. If you have any questions, contact us on [Telegram](http://telegram.x64dbg.com), [Gitter](http://gitter.x64dbg.com) or [IRC](http://webchat.freenode.net/?channels=x64dbg). If you want to see the changes in more detail, check the [commit log](https://github.com/x64dbg/x64dbg/commits).

You can always get the latest release of x64dbg [here](http://releases.x64dbg.com). If you are interested in contributing, check out [this page](http://contribute.x64dbg.com).

Finally, if someone is interested in hiring me to work on x64dbg more, please contact me!