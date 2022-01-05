---
layout: post
title: Weekly digest 14
author: mrexodia
website: https://mrexodia.github.io
contents: ["Types", "Fix log links and show suspected call stack frame", "Finished layered loop implementation", "Fixed 'cannot get module filename'", "Allow for more customization", "Usual things"]

---

This is already number fourteen of the weekly digests! It will highlight the things that happened to and around x64dbg this week.

## Types

There has been quite a lot of progress on the type system in the last few months, but it has now (sort of) come together and you can really start using it. Currently you can get types in the following ways:

- Add them with [commands](http://help.x64dbg.com/en/latest/commands/types/index.html);
- Load them from [JSON](https://gist.github.com/mrexodia/e949ab26d5986a5fc1fa4944ac68147a#file-types-json);
- Load simple C++ [headers](https://gist.github.com/mrexodia/e949ab26d5986a5fc1fa4944ac68147a#file-context32-h).

If you want to show a structure (as seen below) you first have to load/parse the types and then you can 'visit' the type with an (optional) address to lay it over linear memory. Pointers are supported but the [VisitType](http://help.x64dbg.com/en/latest/commands/types/VisitType.html) command has to be used with an explicit pointer depth to expand pointers.

![menu](https://i.imgur.com/Gz2w5N4.png)

This took all my time for the week, which is why this post is very short. The technical details are interesting though. The built-in type system has no/limited support for dynamic types (variable array sizes are not supported). This was needed to keep the structures simple and get started quickly. The GUI however is designed to be more generic and the API is much simpler.

```c++
typedef struct _TYPEDESCRIPTOR
{
    bool expanded; //is the type node expanded?
    bool reverse; //big endian?
    const char* name; //type name (int b)
    duint addr; //virtual address
    duint offset; //offset to addr for the actual location
    int id; //type id
    int size; //sizeof(type)
    TYPETOSTRING callback; //convert to string
    void* userdata; //user data
} TYPEDESCRIPTOR;

BRIDGE_IMPEXP void* GuiTypeAddNode(void* parent, const TYPEDESCRIPTOR* type);
BRIDGE_IMPEXP bool GuiTypeClear();
```

You can directly build the tree and a callback is provided to convert a `TYPEDESCRIPTOR` to a string value to display, which allows for great flexibility. Some possible use cases would be:

- Parse types with [clang](http://clang.llvm.org) and show them in the GUI;
- Support [Binary Templates](http://www.sweetscape.com/010editor/templates.html);
- Support [Kaitai Struct](http://kaitai.io).

In the future I want to add often-used types to a database and ship that with x64dbg. There will (eventually) be a blogpost describing everything in detail, but if you are interested you should come and talk to me on [Telegram](http://telegram.x64dbg.com).

## Fix log links and show suspected call stack frame

In pull request [#1282](https://github.com/x64dbg/x64dbg/pull/1282), torusrxxx added an alternative view for the callstack (without using the dbghelp `StackWalk` function) that might help in certain situations with displaying possible return values. The hyperlink in the logs of x32dbg are now also working again!

## Finished layered loop implementation

You can now add (layered) loop markers with the `loopadd` command (undocumented). The API for plugins is `DbgLoopAdd`.

![layered loops](http://i.imgur.com/L6RFxh2.png)

## Fixed 'cannot get module filename'

Various people had issues with x64dbg showing 'Cannot get module filename' or 'GetModuleFileNameExW failed'. These should now be fixed. In addition you can now properly debug executables from a (VirtualBox) network share on Windows XP (and older versions of Windows 7).

## Allow for more customization

You can now customize more details of the graph, which allows for some nice themes. See [Solarized Dark](https://github.com/x64dbg/x64dbg/wiki/Stylesheets#solarized-dark-mod-by-storm-shadow) by Storm Shadow. There have also been various fixes with some color options not behaving correctly.

![solarized dark graph](http://i.imgur.com/jSSLbec.png) 

## Usual things

That has been about it for this week again. If you have any questions, contact us on [Telegram](http://telegram.x64dbg.com), [Gitter](http://gitter.x64dbg.com) or [IRC](http://webchat.freenode.net/?channels=x64dbg). If you want to see the changes in more detail, check the [commit log](https://github.com/x64dbg/x64dbg/commits).

You can always get the latest release of x64dbg [here](http://releases.x64dbg.com). If you are interested in contributing, check out [this page](http://contribute.x64dbg.com).

Finally, if someone is interested in hiring me to work on x64dbg more, please contact me!