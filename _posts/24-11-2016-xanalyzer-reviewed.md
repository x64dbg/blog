---
layout: post
title: xAnalyzer Reviewed
author: ThunderCls
website: http://reversec0de.wordpress.com

---

## Introduction

First of all I want to thank mrexodia for giving me the opportunity to be part of x64dbg community, to collaborate on the project and even write an entry for this blog. I'm known as [ThunderCls](http://github.com/ThunderCls) and I come from a group of enthusiasts and reverse engineers called CrackSLatinoS, a big family leaded by a great cracker, exploit writer and person, Ricardo Narvaja.

In this post I pretend to give a first look from my perspective, of the task of interacting with x64dbg debugger plugins API to extend and give some extra functionality to this awesome and modern debugger.

## Going back

Like a year ago I started having my first contact with x64dbg and due to the simplicity and similarities with my first debugger ([OllyDbg](http://ollydbg.de) I began using it for some debugging sessions, but as an Olly user I couldn't resist to start missing some of the features that Oleh's debugger had, and I'm referring in this case to the extra analysis OllyDbg does over API functions calls and their arguments and values. I opened an [issue](https://github.com/x64dbg/x64dbg/issues/334) in the project page asking for such a feature. 

At the time of opening, the development team and collaborators were not able to get into it, instead I was given a couple choices like [APIInfo](https://github.com/mrfearless/APIInfo-Plugin-x86) by [mrfearless](https://github.com/mrfearless), and I even found another one [StaticAnalysis](https://github.com/x64dbg/StaticAnalysis) written by tr4ceflow. Both of them were very close to what I wanted, but still they didn't fulfil all of my cravings. Like a month ago I came back to x64dbg community just to see how improved the debugger was from my last contact with it and this made me gain some interest in developing and collaborating with the project, and so xAnalyzer came in.

## What is xAnalyzer?

xAnalyzer is a x64dbg plugin written by me to extend and/or complement the core analysis functionality in this debugger. The plugin was written and intended as a feature that, in the present day of writing this article, has not been implemented yet as a builtin functionality in x64dbg, and I quote: 

> This plugin is based on mrfearless APIInfo Plugin code, although some improvements and additions have been included. xAnalyzer is capable of calling internal x64dbg commands to make various types of analysis... This plugin is going to make extensive API functions call detections to add functions definitions, arguments and data types as well as any other complementary information, something close at what you get with OllyDbg.


## Basic functionality

As I said before, this plugin took as base code to APIInfo, so most of its core functionality is from mrfearless' code. Apart from that, I wanted to go a little bit further than just make a translation of his code into C++ and so I came up with something more like the kind of features I wanted before. The process of creating your own plugins for x64dbg is explained [here](http://x64dbg.com/blog/2016/07/30/x64dbg-plugin-sdk.html) and even the documentation and plugin templates for Visual Studio and other several compilers have been created, so I don't pretend to cover all of that in this post.

Anyway, the functioning of the plugin is pretty straightforward. In the image below it's found a flowchart of its main backbone functions.

![backbone flowchart](https://i.imgur.com/HZMKA43.png)

The plugin starts by launching some of the internal analysis algorithms of x64dbg, such as: [cfanal](http://x64dbg.readthedocs.io/en/latest/commands/analysis/cfanalyze.html), [exanal](http://x64dbg.readthedocs.io/en/latest/commands/analysis/exanalyse.html), [analx](http://x64dbg.readthedocs.io/en/latest/commands/analysis/analxrefs.html), [analadv](http://x64dbg.readthedocs.io/en/latest/commands/analysis/analadv.html) or [anal](http://x64dbg.readthedocs.io/en/latest/commands/analysis/analyse.html). Soon after that it goes into API call analysis. The plugin gets the start and end address of the section in which the current `CONTEXT` is, this in order to loop and make the analysis overall these bytes. For processing each instruction the plugin uses `DbgDisasmFastAt` function which has the following definition:


```c++
void DbgDisasmFastAt(duint addr, BASIC_INSTRUCTION_INFO* basicinfo);

Addr: Address being disassembled.
basicinfo: Pointer to a struct of type BASIC_INSTRUCTION_INFO.

typedef struct
{
    DWORD type; //value|memory|addr
    VALUE_INFO value; //immediat
    MEMORY_INFO memory;
    duint addr; //addrvalue (jumps + calls)
    bool branch; //jumps/calls
    bool call; //instruction is a call
    int size;
    char instruction[MAX_MNEMONIC_SIZE * 4];
} BASIC_INSTRUCTION_INFO;
```

All the values we need are present in the returned structure. In case of calls found, the plugin makes some checks to try to include as many scenarios as it can. Some of these different schemes are: 

### CALL -> JMP -> API (Indirect Call)

![indirect call](https://i.imgur.com/ubYOOdL.png)

![indirect jmp](https://i.imgur.com/o6WKXSn.png)

### CALL -> POINTER -> API (Indirect Call)

![call pointer](https://i.imgur.com/614cwqo.png)

![infobox](https://i.imgur.com/XiPFT4I.png)

### CALL -> API (Direct Call)

![call MessageBox](https://i.imgur.com/AAFrqT9.png)

The plugin creates and emulates a stack for saving all of the possible functions arguments. These instructions are filtered in the function `IsArgumentInstruction()`. The code depends on the platform, for x86 an argument would be any `push` instruction, except for `push ebp`, `push esp`, `push ds`, `push es`. Once a valid argument is found is saved to the global stack container. 

On the other hand x64 platforms differ in this point, so to find if an instruction is a valid candidate it would have to be any of the instructions `mov`, `lea`, `xor`, `or`, `and`. But an additional check has to be made since x64 doesn't use `push` instructions anymore. The x64 platform uses the registers `RCX`, `RDX`, `R8`, `R9` for a four argument function, including floating points registers `XMM0`, `XMM1`, `XMM2`, `XMM3` and for the rest of arguments it uses the stack `[RSP + DISPLACEMENT]`. So the check consist of checking if these instructions have any of those, including 32, 16 and 8 bits variants. The stack would be cleared if a function prolog or epilog is found as well as jumps (no jumps among arguments) and internal subs. 

Finally, the key is that when a call is found, it will traverse the stack to find the valid arguments for it. Here once again x64 brings some differences to the table, as for the x64 functions calls arguments might have been saved to the registers or stack without any specific order, going against the function arguments definition order. Another hack had to be made, in this case, x64 depends on the registers order as the arguments order, so the scheme would be:

1. `RCX`  First argument of the function;
2. `RDX` Second argument of the function;
3. `R8` Third argument of the function;
4. `R9` Fourth argument of the function;
5. `STACK ([RSP + DISPLACEMENT])` The rest of the arguments of the function including floating points registers XMM0, XMM1, XMM2, XMM3.

With that in consideration, the rest is easy. Taking the same path of APIInfo plugin, xAnalyzer has a folder which should contain all the API definition files as `.ini` with the following structure:

`Filename` This is the name of the module on which the API function is located with extension `.api` (kernel32.api, shell32.api, etc)

A single entry in any of these files would be like:

```
[MessageBoxA]
1=HWND hWnd
2=LPCSTR lpText
3=LPCSTR lpCaption
4=UINT uType
ParamCount=4
@=MessageBoxA(HWND hWnd, LPCSTR lpText, LPCSTR lpCaption, UINT uType);
```

In this case, all of these definition files may be customized and populated by each user following the same shown pattern. If you find that a certain API call definition is not being detected by xAnalyzer it might mean that it's not present in the definition files, so in this case an addition could be made to include any missing function.

To set the API function name comment, as well as its arguments, the plugin read over the definition files to get the correct data. Finally it also uses some of the functions in the SDK of x64dbg such as: `DbgGetCommentAt`, `DbgSetCommentAt`, `DbgClearAutoCommentRange` and `Script::Argument::Add*` to set up the visual aid for the current executable function.

As for now, x64dbg doesn't allow nested function arguments, even though xAnalyzer does, definition is going to be present, while arguments brackets won't. xAnalyzer has been made compatible with 64 bits binaries in the latest release and even a couple more features are also coming soon.

And this is all for this post, xAnalyzer x64dbg plugin exposed. For latest relases, info, issues, etc go to the [project page](https://github.com/ThunderCls/xAnalyzer).

ThunderCls signing out

