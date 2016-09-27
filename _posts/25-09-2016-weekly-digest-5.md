---
layout: post
title: Weekly digest 5
author: mrexodia
website: http://mrexodia.cf

---

This is the fifth of (hopefully) many weekly digests. Basically it will highlight the things that happened to x64dbg and related projects during the week before.

## Register and argument view enhancements

There have been various improvements to the registers view. You can now display XMM/YMM registers as float, double or integers. If you want more information, check out pull request [#1101](https://github.com/x64dbg/x64dbg/pull/1101).

![simd display](https://i.imgur.com/P0MBXPp.png)

## Dynamically load/unload plugins

Another nice contribution from [blaquee](https://github.com/blaquee). The commands `plugload` and `plugunload` have been added. This is useful for plugin developers who want to test plugins without having to restart x64dbg all the time. In combination with favorite commands it will speed up development *a lot*. For more details on the implementation, see pull request [#1100](https://github.com/x64dbg/x64dbg/pull/1100).

![plugunload](https://i.imgur.com/hHCKLts.png)

## Improvements to the info box

A friendly gentle(wo)man requested ([#1094](https://github.com/x64dbg/x64dbg/issues/1094)) a change to the info box. Basically the pointer values in the instruction were not resolved (so if the instruction contained `qword ptr ds:[rsp+30]` it would not show the value of `rsp+30`). Personally this is quite useless since you can easily follow addresses wherever you want but it has been added regardless. It now shows both the context and the resolved address:

![infobox pointer](https://i.imgur.com/BB1WoyS.png)

## Fixed search for constant references

There have been various issues with references working incorrectly. Issue [#1092](https://github.com/x64dbg/x64dbg/issues/1092) has now been fixed and references are being found correctly again.

## Copy improvements

It is now possible to copy tables to the log and also to copy the log to global/debuggee notes. See pull request [#1105](https://github.com/x64dbg/x64dbg/pull/1105) for details.

![copy to log](https://i.imgur.com/tYfUjyb.png)

## Improved the favorites dialog

The favorites dialog now correctly disables buttons that would not do anything.

![disabled buttons](https://i.imgur.com/EVw2tIo.png)

## Fixed confusing wording

Some functions had confusing names. For example the "Remove analysis from module" option in the disassembly would only remove type analysis and the "Copy selection" option in the dump would copy the lines that the selection was on. These have been corrected and it should now be more clear.

## Better uppercase disassembly

When selecting the uppercase option for disassembly it would not generate uppercase assembly when patching an instruction. This has been fixed.

## Fixed compile error with yara in the pluginsdk

The includes for yara would throw an error because there is a missing `exception.h` file. This would throw an error when plugins try to use yara.

## Improved selection API

You can now query selection from the disassembly, dump, stack, graph, memory map and symbol modules. This will become especially useful once plugin menus have been added for these views as well. The performance of the selection API has also been improved.

## Improved dbload command

The command [dbload](http://x64dbg.readthedocs.io/en/latest/commands/user-database/dbload.html) would not unload the data first if you deleted the current program database. A command [dbclear](http://x64dbg.readthedocs.io/en/latest/commands/user-database/dbclear.html) has also been added.

## Expression functions for reading data

Various expression functions `ReadByte`, `ReadWord`, `ReadDword` etc. have been added. See the [documentation](http://x64dbg.readthedocs.io/en/latest/introduction/Expression-functions.html#byte-word-dword-qword-ptr) for more information.

## Improved documentation

Someone on [IRC](http://irc.x64dbg.com) was confused about the documentation and various things have been corrected:

> If you came here because someone told you to read the manual, start by reading **all sections** of the [introduction](http://x64dbg.readthedocs.io/en/latest/introduction/index.html).

There is also slightly better linking in the introduction section so people can easier see what the related topics are.

## Progress with a type system

A new project called [TypeRepresentation](https://github.com/x64dbg/TypeRepresentation) has been added. This project is meant to experiment with the representation of more complex types (structs/unions/function definitions). It has been heavily inspired by [radare2 types](https://github.com/radare/radare2/blob/master/doc/types.md) and it will hopefully help closing issues [#1108](https://github.com/x64dbg/x64dbg/issues/1108), [#783](https://github.com/x64dbg/x64dbg/issues/783), [#689](https://github.com/x64dbg/x64dbg/issues/689), [#334](https://github.com/x64dbg/x64dbg/issues/334) and [#225](https://github.com/x64dbg/x64dbg/issues/225). The basics have been completed, but a lot more work is needed to make it work in x64dbg.

Here is some [source code](https://github.com/x64dbg/TypeRepresentation/blob/master/TypeRepresentation/Type.cpp):

```c++
#include "Types.h"

int main()
{
    using namespace Types;

    struct ST
    {
        char a[3];
        char d;
        int y;
    };
    printf("sizeof(ST) = %d\n", int(sizeof(ST)));

    TypeManager t;

    t.AddStruct("ST");
    t.AppendMember("a", "char", -1, 3);
    t.AppendMember("d", "char");
    t.AppendMember("y", "int");
    printf("t.Sizeof(ST) = %d\n", t.Sizeof("ST"));

    t.AddType("DWORD", "unsigned int");
    printf("t.Sizeof(DWORD) = %d\n", t.Sizeof("DWORD"));

    t.AddStruct("_FILETIME");
    t.AppendMember("dwLoDateTime", "DWORD");
    t.AppendMember("dwHighDateTime", "DWORD");
    printf("t.Sizeof(_FILETIME) = %d\n", t.Sizeof("_FILETIME"));

    union UT
    {
        char a;
        short b;
        int c;
        long long d;
    };
    printf("sizeof(UT) = %d\n", int(sizeof(UT)));

    t.AddUnion("UT");
    t.AppendMember("a", "char");
    t.AppendMember("b", "short");
    t.AppendMember("c", "int");
    t.AppendMember("d", "long long");
    printf("t.Sizeof(UT) = %d\n", t.Sizeof("UT"));

    getchar();
    return 0;
}
```

It will output:

```
sizeof(ST) = 8
t.Sizeof(ST) = 8
t.Sizeof(DWORD) = 4
t.Sizeof(_FILETIME) = 8
sizeof(UT) = 8
t.Sizeof(UT) = 8
```

## Plugin template for Visual Studio

Last week I mentioned there will be a plugin template. This has now been realized. See the [PluginTemplate](https://github.com/x64dbg/PluginTemplate) repository for more information. The template is very simple. See the [plugin documentation](http://help.x64dbg.com/en/latest/developers/plugins/index.html) and [pluginsdk](https://github.com/x64dbg/PluginTemplate/tree/master/PluginTemplate/pluginsdk) for more information on what functions are available to plugins. Also see the [x64dbg plugin SDK](http://x64dbg.com/blog/2016/07/30/x64dbg-plugin-sdk.html) post by [fearless](http://www.letthelight.in) for a hands-on, tutorial on plugin development. If you are looking for a simplistic scripting experience, check out [ScriptDllTemplate](https://github.com/x64dbg/ScriptDllTemplate), [x64dbgpy](https://github.com/x64dbg/x64dbgpy), [chaiScript](https://github.com/jdavidberger/chaiScriptPlugin) or the [built-in script engine](http://help.x64dbg.com/en/latest/commands/index.html).

![plugin template](https://i.imgur.com/faUyeHq.png)

## GetRelocSize

The command [GetRelocSize](http://help.x64dbg.com/en/latest/commands/misc/grs.html) from the [testplugin](https://github.com/x64dbg/testplugin) has been added to x64dbg. This command is useful when trying to find the size of a relocation table from memory while unpacking.

## MxCsr

There were a few bugs with setting floating point status registers (such as `MxCsr`), these have been fixed. See issue [#1102](https://github.com/x64dbg/x64dbg/issues/1102) for more details.

## Final words

That has been about it for this week again. If you have any questions, contact us on [Telegram](http://telegram.x64dbg.com), [Gitter](http://gitter.x64dbg.com) or [IRC](http://webchat.freenode.net/?channels=x64dbg). If you want to see the changes in more detail, check the [commit log](https://github.com/x64dbg/x64dbg/commits).

You can always get the latest release of x64dbg [here](http://releases.x64dbg.com). If you are interested in contributing, check out [this page](http://contribute.x64dbg.com).

Finally, if someone is interested in hiring me to work on x64dbg more, please contact me!