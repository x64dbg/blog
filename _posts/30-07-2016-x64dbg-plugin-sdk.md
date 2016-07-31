---
layout: post
title: x64dbg plugin SDK
author: fearless
website: http://www.LetTheLight.in
---

# Contents

* [Overview](#overview)
* [Common questions](#common-questions)
    * [Wait, what? there are two plugin SDKs?](#wait-what-there-are-two-plugin-sdks)
    * [Which plugin SDK should i use?](#which-plugin-sdk-should-i-use)
    * [Why create a plugin SDK in assembler?](#why-create-a-plugin-sdk-in-assembler)
    * [What assembler should I use, if I'm to use the plugin SDK for assembler?](#what-assembler-should-i-use-if-im-to-use-the-plugin-sdk-for-assembler)
    * [Why write a plugin?](#why-write-a-plugin)
* [Understanding the x64dbg plugin architecture](#understanding-the-x64dbg-plugin-architecture)
* [The plugin load sequence](#the-plugin-load-sequence)
* [DllMain](#dllmain)
* [The pluginit exported function](#the-pluginit-exported-function)
* [The plugsetup exported function](#the-plugsetup-exported-function)
* [The callback exported functions and structures](#the-callback-exported-functions-and-structures)
    * [_plugin_registercallback](#pluginregistercallback)
    * [The registered event callback function for _plugin_registercallback](#the-registered-event-callback-function-for-pluginregistercallback)
    * [The CDECL export callback function](#the-cdecl-export-callback-function)
* [Summary](#summary)
* [Afterword](#afterword)
* [Additional resources of interest](#additional-resources-of-interest)

# Overview

The x64dbg plugin software development kit (SDK) is used to create plugins for the x64dbg debugger. This article aims to do a number of things:

* Highlight the existence of the x64dbg plugin SDK.
* Highlight the existence of the x64dbg plugin SDK for assembler.
* Technical overview of the plugin loading sequence.
* Cover the architecture and the inner workings of the x64dbg plugin SDK.
* Provide example code and structure definitions for some of the plugin SDK functions, for the use in creating plugins for x64dbg using C++ or assembler.

Please note that there is a lot of code listings in this article, which may make for rather dry reading, and more like a technical manual overall.

# Common questions

A number of questions might arise straight away, so lets answer them before we continue.

## Wait, what? there are two plugin SDKs?

Yes, the integrated one is already provided for by x64dbg, and comes included with the latest snapshots. The second one was created by myself, converting the existing plugin SDK to an assembler friendly one for use with Masm32 (x86) or JWasm / HJWasm (x64)

## Which plugin SDK should I use?

Whichever you feel more comfortable with. If you prefer to code in C or C++ then the integrated plugin SDK is probably more suited to you.

## Why create a plugin SDK in assembler?

In practice it comes down to what language you are most familiar coding with, and in my case it happens to be assembler, and by providing an SDK for assembler, it opens up the door to the possibility of other assembly coders using it. And another obvious answer would be to do with the nature of the product, which being a debugger shows its output (the disassembly) in raw assembly language - what better environment for assembly coders to learn and further their own development?

## What assembler should I use, if I'm to use the plugin SDK for assembler?

As the plugin SDK for x86 was written using Masm32, for x86 plugin development I recommend you use the [MASM32 SDK]((http://www.masm32.com/masmdl.htm)) along with the [x64dbg Plugin SDK For x86 Assembler](https://github.com/mrfearless/x64dbg-Plugin-SDK-For-x86-Assembler). The plugin SDK for x64 was written using JWasm (64bit) and for x64 plugin development both [JWasm](http://masm32.com/board/index.php?topic=3795.0) (the last/latest release) and [HJWasm](http://www.terraspace.co.uk/hjwasm.html#p2) (fork and continuation of JWasm) can be used along with [x64dbg Plugin SDK For x64 Assembler](https://github.com/mrfearless/x64dbg-Plugin-SDK-For-x64-Assembler). 

JWasm / HJWasm are considered masm compatible, so they could also be used for the x86 development if you so wish. Other assemblers can be used, but you might have to make a few changes here and there with the examples shown in this post.

## Why write a plugin?

* To add additional new features not originally provided for by the original software product.
* To enhance or complement existing features or functionality: convenience, ease of use, eliminate repetitive tasks.
* To replace older features or functionality that doesn't work or doesn't work as intended: bug fixes, outdated features, software product not being maintained, etc.
* To better learn the software products features, functionality and/or api.
* For fun, and because you can.

Those answers are more general and apply to plugin development in general, but with open source projects which can be more fluid in their development, there are other considerations and caveats.

### Ongoing development

Fixing issues (bug fixes) and enhancing functionality are an ongoing part of open source projects. So the additions of new features (via feature requests) is not uncommon. Also features or functionality that a plugin provide can become obsolete when the feature they provide is directly including in the open source project.

### Feature request alignment

Sometimes features requests and the overall direction and goal of the open source project may not align - even if they are directly or indirectly related to the overall project - sometimes it is more expedient for the feature requests to be moved out to a plugin. 

Other times, features that where planned for inclusion in the open source project are passed by as different milestones are set, which may mean directing the feature request out to plugin development.

Certain features may only used by a small amount of users, and again it is more efficient to outsource the feature to a plugin for the small amount of users who make use of the functionality.

# Understanding the x64dbg plugin architecture

The plugin files for x64dbg, are files that end with the `.dp32` or `.dp64` extension. These correspond to the processor architecture used in each version of x64dbg - 32bit and 64bit. In reality these plugin files (`.dp32` for 32bit x32dbg and `.dp64` for 64bit x64dbg) are just simple dynamic link libraries (`.dll` files).

Each plugin file has to export a number of functions for it to be recognised as a valid and usable plugin. These are:

* `DllMain` - The entry point into the dynamic link library.
* `pluginit` - Starts the initial plugin interface with x64dbg.

and optionally:

* `plugsetup` - Provides menu handles to the plugin.
* `plugstop` - For when we are exiting from our plugin (when x64dbg closes down)
* `CB*` - Optionally a number of callback functions, defined in the plugin SDK and exported by x64dbg for use with plugins - which we will explain further below.

Technically only `DllMain` and `pluginit` are required at a minimum, but it is considered a good practise to include `plugstop` to allow for cleanup of your plugins code, should it be required, and `plugsetup` for obtaining menu handles if your plugin will be creating its own menu items.

# The plugin load sequence

These are the steps that occur when plugins are being loaded by the x64dbg debugger. The functions and structures mentioned are covered in more detail in other sections below.

* A search is made in the `plugins` folder for all files ending with `.dp32` (for 32bit x32dbg.exe) or `.dp64` (for 64bit x64dbg.exe)

In a loop of all matching files the following takes place:

* A `PLUG_INITSTRUCT` structure (`initStruct`) for `pluginit` is prepared and is used to store `pluginHandle` for the next step.
* [LoadLibrary](https://msdn.microsoft.com/en-ie/library/windows/desktop/ms684175(v=vs.85).aspx) is called for the plugin filename. If it is not a valid dynamic link library then this file is ignored and skipped, a message is created in the log window indicated the failure to load this 'plugin' file, and the next matching plugin file is processed instead (if there are any left to process). If successfully loaded a unique identifier is stored in the `pluginHandle` field of the `PLUG_INITSTRUCT` structure (`initStruct`).
* [GetProcAddress](https://msdn.microsoft.com/en-us/library/windows/desktop/ms683212(v=vs.85).aspx) is called to look for a `pluginit` function, and if the dynamic link library has one, then it registers this function's address with x64dbg. Otherwise the plugin will fail to load.
* [GetProcAddress](https://msdn.microsoft.com/en-us/library/windows/desktop/ms683212(v=vs.85).aspx) is called to look for a `plugstop` and a `plugsetup` function. If they are present then the addresses of these functions are registered with x64dbg.
* [GetProcAddress](https://msdn.microsoft.com/en-us/library/windows/desktop/ms683212(v=vs.85).aspx) is used again a number of times to look for various callback export functions (explained in more detail in the section on callback functions below), and if these are present then the addresses of these functions are also registered with x64dbg.
* The `pluginit` function is called with one parameter: `initStruct` (a pointer to a `PLUG_INITSTRUCT structure`), the `sdkVersion` field of the `PLUG_INITSTRUCT` structure is checked on return to validate that it matches the required plugin sdk version number. If it does not then the plugin fails to load and processing continues with the next file. If it is valid a message is created in the log window indicating the plugin has been loaded.
* A number of system menu entries handles are created and reserved for the plugins use: in the Plugins menu, the right click context menus for the cpu view, the dump and the stack. No menus are shown, these are merely place holders for when, or if, a plugin creates its own menu items under any of theses system menus.
* If there was a `plugsetup` export function found previously a `PLUG_SETUPSTRUCT` structure (`setupStruct`) is prepared and the `plugsetup` function is called with one parameter: `setupStruct` (a pointer to a `PLUG_SETUPSTRUCT` structure), which holds the previously registered place holder menu handles for the plugin to potentially use when adding its own menus and menu items.
* The next plugin file is processed, if there are any left to do so.

Understanding the plugin loading sequence will hopefully help you understand where best to place your code for your plugin and the obvious impact of having cpu intensive code in the initialization and setup functions. Other plugins will be delayed in loading and the x64dbg debugger itself will be waiting for your code to finish before it can continue on to do its main job of debugging.

# DllMain

`DllMain` is the entry point into a dynamic link library, and is optional for each dll file to have one. The plugins, being dll files, can make use of this function by storing the `HINSTANCE` `hInst` value for later use in other api calls. The code required for creating a DllMain function is relatively straightforward.

Ive included an example of defining the DllMain using C++ (for both 32bit and 64bit), Masm32 for x86 assembly and JWasm / HJWasm for the x64 assembly.

_C++_:

```cpp
extern "C" DLL_EXPORT BOOL APIENTRY DllMain(HINSTANCE hInst, DWORD fdwReason, LPVOID lpvReserved)
{
    if(fdwReason == DLL_PROCESS_ATTACH)
    {
        hInstance = hInst; // save instance handle for future use
    }
    return TRUE;
}
```

_Assembler x86_:

```nasm
DllMain PROC hInst:HINSTANCE, fdwReason:DWORD, lpvReserved:DWORD
    .IF fdwReason == DLL_PROCESS_ATTACH
        mov eax, hInst
        mov hInstance, eax ; save instance handle for future use
    .ENDIF
    mov eax,TRUE
    ret
DllMain ENDP
```

_Assembler x64_:

```nasm
DllMain PROC hInst:HINSTANCE, fdwReason:DWORD, lpvReserved:LPVOID
    .IF fdwReason == DLL_PROCESS_ATTACH
        mov rax, hInst
        mov hInstance, rax ; save instance handle for future use
    .ENDIF
    mov rax,TRUE
    ret
DllMain ENDP
```

Fairly simple for each example, and minimal changes for the 64bit assembler version vs the 32bit, mainly the use of the `rax` register instead of `eax`.

Apart from `DllMain` all the plugin functions (except from your own internal functions) are required to be exported for the plugin to work.

An exported function is one that has been declared as accessible externally for other external callers to make use of. `DllMain` is 'seen' and automatically handled by the operating system when loading a dynamic link library, so we aren't required to explicitly export it, but the `pluginit`, `plugstop`, `plugsetup` and any other `CB*` callback functions are required to be exported.

# The pluginit exported function

`pluginit` is the first exported function that x64dbg calls after loading the dynamic link libraries (`.dp32` or `.dp64`), if `pluginit` isn't present then the loading of the plugin will fail at this point. 

`pluginit` passes a pointer to a `PLUG_INITSTRUCT` structure as the only parameter in the function: `initStruct`. This structure is used to register the plugin with x64dbg and for obtaining a valid plugin handle which is used in future api calls.

The definition for this structure is:

_C++_:

```cpp
typedef struct
{
    //provided by the debugger
    int pluginHandle;
    //provided by the pluginit function
    int sdkVersion;
    int pluginVersion;
    char pluginName[256];
} PLUG_INITSTRUCT;
```

_Assembler x86 and x64_:

```nasm
PLUG_INITSTRUCT   STRUCT
    pluginHandle  DWORD ? ; Plugin handle. Data provided by the debugger to the plugin.
    sdkVersion    DWORD ? ; Plugin SDK version, Data provided by the plugin to the debugger (required).
    pluginVersion DWORD ? ; Plugin version. Data provided by the plugin to the debugger (required).
    pluginName    DB 256 DUP (?) ; Plugin name. Data provided by the plugin to the debugger (required).
PLUG_INITSTRUCT   ENDS
```

So we must place valid information back into this structure for x64dbg to validate and recognise our plugin. A number of defines can be used to provide the information required by the structure's fields: `pluginVersion` (`PLUGIN_VERSION` - defined by user) and `sdkVersion` (`PLUG_SDKVERSION` - predefined in the SDK - version of the SDK that x64dbg expects). The `pluginName` is a string buffer that contains the name of your plugin. The `pluginHandle` field is provided to us as a handle that we can save and re-use in future api calls.

Of course we need to declare some of the variables and strings used to pass this information back via the `PLUG_INITSTRUCT` structure, and to store information returned to us (`pluginHandle` in `pluginit` and other handles in the `plugsetup` call later on). Here's how to define them:

_C++_:

```cpp
// Plugin SDK required variables
#define plugin_name "x64dbg_plugin" // rename to your plugins name 
#define plugin_version 1

// GLOBAL Plugin SDK variables
int pluginHandle;
HWND hwndDlg;
int hMenu;
int hMenuDisasm;
int hMenuDump;
int hMenuStack;
```

_Assembler x86_:

```nasm
.CONST
PLUGIN_VERSION      EQU 1

.DATA
PLUGIN_NAME         DB "x64dbg_plugin",0 ; rename to your plugins name

.DATA?
; Plugin SDK required variables
PUBLIC              pluginHandle
PUBLIC              hwndDlg
PUBLIC              hMenu
PUBLIC              hMenuDisasm
PUBLIC              hMenuDump
PUBLIC              hMenuStack

pluginHandle        DD ?
hwndDlg             DD ?
hMenu               DD ?
hMenuDisasm         DD ?
hMenuDump           DD ?
hMenuStack          DD ?
```

_Assembler x64_:

```nasm
.CONST
PLUGIN_VERSION      EQU 1

.DATA
PLUGIN_NAME         DB "x64dbg_plugin",0 ; rename to your plugins name

.DATA?
; Plugin SDK required variables
PUBLIC              pluginHandle
PUBLIC              hwndDlg
PUBLIC              hMenu
PUBLIC              hMenuDisasm
PUBLIC              hMenuDump
PUBLIC              hMenuStack

pluginHandle        DD ?
hwndDlg             DQ ?
hMenu               DD ?
hMenuDisasm         DD ?
hMenuDump           DD ?
hMenuStack          DD ?
```

Now that we have setup our variables and strings we are ready to construct our `pluginit` function. Below is a couple of examples of `pluginit` in C++ (for both 32bit and 64bit), Masm32 for x86 assembly and JWasm / HJWasm for the x64 assembly.

_C++_:

```cpp
DLL_EXPORT bool pluginit(PLUG_INITSTRUCT* initStruct)
{
    initStruct->pluginVersion = plugin_version;
    initStruct->sdkVersion = PLUG_SDKVERSION;
    strcpy(initStruct->pluginName, plugin_name);
    pluginHandle = initStruct->pluginHandle;

    // place any additional initialization code here
    
    return true;
}
```

_Assembler x86_:

```nasm
pluginit PROC C PUBLIC USES EBX initStruct:DWORD
    mov ebx, initStruct

    ; Fill in required information of initStruct, which is a pointer to a PLUG_INITSTRUCT structure
    mov eax, PLUGIN_VERSION
    mov [ebx].PLUG_INITSTRUCT.pluginVersion, eax
    mov eax, PLUG_SDKVERSION
    mov [ebx].PLUG_INITSTRUCT.sdkVersion, eax
    Invoke lstrcpy, Addr [ebx].PLUG_INITSTRUCT.pluginName, Addr PLUGIN_NAME
    
    mov ebx, initStruct
    mov eax, [ebx].PLUG_INITSTRUCT.pluginHandle
    mov pluginHandle, eax
    
    ; Do any other initialization here
    
    mov eax, TRUE
    ret
pluginit ENDP
```

_Assembler x64_:

```nasm
pluginit PROC FRAME USES RBX initStruct:QWORD
    mov rbx, initStruct

    ; Fill in required information of initStruct, which is a pointer to a PLUG_INITSTRUCT structure
    mov eax, PLUGIN_VERSION
    mov [rbx].PLUG_INITSTRUCT.pluginVersion, eax
    mov eax, PLUG_SDKVERSION
    mov [rbx].PLUG_INITSTRUCT.sdkVersion, eax
    Invoke lstrcpy, Addr [rbx].PLUG_INITSTRUCT.pluginName, Addr PLUGIN_NAME
    
    mov rbx, initStruct
    mov eax, [rbx].PLUG_INITSTRUCT.pluginHandle
    mov pluginHandle, eax
    
    ; Do any other initialization here
    
    mov rax, TRUE
    ret
pluginit ENDP
```

The coding for each example is simple and again we see minimal changes for the 64bit assembler version vs the 32bit.

In assembler (x86 and x64) you must also add your exported functions to a .def file for them to be visible to external callers when compiling and linking:

```nasm
LIBRARY MyPlugin
EXPORTS pluginit
        plugstop
        plugsetup
```

# The plugsetup exported function

`plugsetup` is the second export function that x64dbg calls - assuming the first call to `pluginit` was successful and the information passed back was correct.

It passes a pointer to a `PLUG_SETUPSTRUCT` structure as the only parameter in the function: `setupStruct`. This structure is used to pass back various menu handles to the plugin. These handles can be used in future api calls to create menus and menu items for your plugin.

The definition for this structure is:

_C++_:

```cpp
typedef struct
{
    //provided by the debugger
    HWND hwndDlg;       // gui window handle
    int hMenu;          // plugin menu handle
    int hMenuDisasm;    // plugin disasm menu handle
    int hMenuDump;      // plugin dump menu handle
    int hMenuStack;     // plugin stack menu handle
} PLUG_SETUPSTRUCT;
```

_Assembler x86 and x64_:

```nasm
; plugsetup - This structure is used by the function that allows the creation of plugin menu entries
PLUG_SETUPSTRUCT STRUCT 8
    hwndDlg      HWND ?  ; GUI window handle. Data provided by the debugger to the plugin.
    hMenu        DWORD ? ; Plugin menu handle. Data provided by the debugger to the plugin.
    hMenuDisasm  DWORD ? ; Plugin disasm menu handle. Data provided by the debugger to the plugin.
    hMenuDump    DWORD ? ; Plugin dump menu handle. Data provided by the debugger to the plugin.
    hMenuStack   DWORD ? ; Plugin stack menu handle. Data provided by the debugger to the plugin.
PLUG_SETUPSTRUCT ENDS
```

And below is a couple of examples in C++ and assembler of what the `plugsetup` function will look like (a bare bones version):

_C++_:

```cpp
DLL_EXPORT void plugsetup(PLUG_SETUPSTRUCT* setupStruct)
{
    hwndDlg = setupStruct->hwndDlg;
    hMenu = setupStruct->hMenu;
    hMenuDisasm = setupStruct->hMenuDisasm;
    hMenuDump = setupStruct->hMenuDump;
    hMenuStack = setupStruct->hMenuStack;
    
    // place any additional setup code here
    
    return true;
}
```

_Assembler x86_:

```nasm
plugsetup PROC C PUBLIC USES EBX setupStruct:DWORD
    mov ebx, setupStruct

    ; Extract handles from setupStruct which is a pointer to a PLUG_SETUPSTRUCT structure  
    mov eax, [ebx].PLUG_SETUPSTRUCT.hwndDlg
    mov hwndDlg, eax
    mov eax, [ebx].PLUG_SETUPSTRUCT.hMenu
    mov hMenu, eax
    mov eax, [ebx].PLUG_SETUPSTRUCT.hMenuDisasm
    mov hMenuDisasm, eax
    mov eax, [ebx].PLUG_SETUPSTRUCT.hMenuDump
    mov hMenuDump, eax
    mov eax, [ebx].PLUG_SETUPSTRUCT.hMenuStack
    mov hMenuStack, eax

    ; Do any setup here: add menus, menu items, callback and commands etc

    mov eax, TRUE
    ret
plugsetup endp
```

_Assembler x64_:

```nasm
plugsetup PROC FRAME USES RBX setupStruct:QWORD
    mov rbx, setupStruct

    ; Extract handles from setupStruct which is a pointer to a PLUG_SETUPSTRUCT structure  
    mov rax, [rbx].PLUG_SETUPSTRUCT.hwndDlg
    mov hwndDlg, rax
    mov eax, [rbx].PLUG_SETUPSTRUCT.hMenu
    mov hMenu, eax
    mov eax, [rbx].PLUG_SETUPSTRUCT.hMenuDisasm
    mov hMenuDisasm, eax
    mov eax, [rbx].PLUG_SETUPSTRUCT.hMenuDump
    mov hMenuDump, eax
    mov eax, [rbx].PLUG_SETUPSTRUCT.hMenuStack
    mov hMenuStack, eax
    
    ; Do any setup here: add menus, menu items, callback and commands etc

    mov rax, TRUE
    ret
plugsetup endp
```

In assembler (x86 and x64) you must also add your exported functions to a .def file for them to be visible to external callers when compiling and linking:

```nasm
LIBRARY MyPlugin
EXPORTS pluginit
        plugstop
        plugsetup
```

# The callback exported functions and structures

The callback functions are provided to help you use your plugin. When a specific event occurs in the x64dbg debugger, it passes this event call to each plugin that has 'registered' to receive this event. Typically events that would be of interest to a plugin developer are when debugging of a target process has begun (CB_INITDEBUG), or when a breakpoint has been reached (CB_BREAKPOINT or CB_SYSTEMBREAKPOINT) or other events of interest, like handling a menu interaction for your plugin (CB_MENUENTRY). 

These events provide your plugin with a way of interacting with the debugger at these points in time, when an event occurs.

Registering a callback is done in one of two ways:

* via the _plugin_registercallback function
* Having an CDECL export of a specific callback function in your plugin

## \_plugin\_registercallback

This function registers an event callback for a plugin. The definition for this function (defined in the plugin SDK) is:

_C++_:

```cpp
void _plugin_registercallback(
    int pluginHandle, //plugin handle
    CBTYPE cbType, //event type
    CBPLUGIN cbPlugin //callback function
);
```

_Assembler x86_:

```nasm
_plugin_registercallback PROTO :DWORD, :DWORD, :DWORD ; (int pluginHandle, CBTYPE cbType, CBPLUGIN cbPlugin)
```

_Assembler x64_:

```nasm
_plugin_registercallback PROTO :QWORD, :QWORD, :QWORD ; (int pluginHandle, CBTYPE cbType, CBPLUGIN cbPlugin)
```

pluginHandle is the handle of your plugin. In assembler this is passed as a DWORD (for x86) or a QWORD (for x64) value.

`cbType` is the specific callback type being registered, which is one of the following values (defined in the plugin SDK):

* `CB_INITDEBUG`
* `CB_STOPDEBUG`
* `CB_CREATEPROCESS`
* `CB_EXITPROCESS`
* `CB_CREATETHREAD`
* `CB_EXITTHREAD`
* `CB_SYSTEMBREAKPOINT`
* `CB_LOADDLL`
* `CB_UNLOADDLL`
* `CB_OUTPUTDEBUGSTRING`
* `CB_EXCEPTION`
* `CB_BREAKPOINT`
* `CB_PAUSEDEBUG`
* `CB_RESUMEDEBUG`
* `CB_STEPPED`
* `CB_ATTACH`
* `CB_DETACH`
* `CB_DEBUGEVENT`
* `CB_MENUENTRY`
* `CB_WINEVENT`
* `CB_WINEVENTGLOBAL`
* `CB_LOADDB`
* `CB_SAVEDB`

In assembler this is passed as a DWORD (for x86) or a QWORD (for x64) value.

`cbPlugin` is the address of your exported callback function that will be registered. In assembler this callback functions address is passed as a DWORD (for x86) or a QWORD (for x64) value.

## The registered event callback function for \_plugin\_registercallback

The callback function `CBPLUGIN` must be an exported library function. `CBPLUGIN` is replaced with the name of your plugin's callback function. The definition for your `CBPLUGIN` function in your plugin looks like this:

_C++:_

```cpp
void CBPLUGIN(
    CBTYPE bType // event type, one of the `cbType` CB_* values listed above
    void* callbackInfo // pointer to a structure of information
);
```

_Assembler x86_:

```nasm
CBPLUGIN PROTO :DWORD, :DWORD ; (CBTYPE bType, void* callbackInfo)
```

_Assembler x64_:

```nasm
CBPLUGIN PROTO :QWORD, :QWORD ; (CBTYPE bType, void* callbackInfo)
```

The `bType` parameter contains the event type that is occurring. Same as one of the CB_\* values listed above for `_plugin_registercallback` `cbType` parameter

The `callbackInfo` parameter contains a pointer to a specific PLUG_CB_\* structure. Each callback event type uses a different `callbackInfo` structure that contains various information related to that particular event. These PLUG_CB_\* structures (that are defined in the plugin SDK) are:

* `PLUG_CB_INITDEBUG`
* `PLUG_CB_STOPDEBUG`
* `PLUG_CB_CREATEPROCESS`
* `PLUG_CB_EXITPROCESS`
* `PLUG_CB_CREATETHREAD`
* `PLUG_CB_EXITTHREAD`
* `PLUG_CB_SYSTEMBREAKPOINT`
* `PLUG_CB_LOADDLL`
* `PLUG_CB_UNLOADDLL`
* `PLUG_CB_OUTPUTDEBUGSTRING`
* `PLUG_CB_EXCEPTION`
* `PLUG_CB_BREAKPOINT`
* `PLUG_CB_PAUSEDEBUG`
* `PLUG_CB_RESUMEDEBUG`
* `PLUG_CB_STEPPED`
* `PLUG_CB_ATTACHED`
* `PLUG_CB_DETACHED`
* `PLUG_CB_DEBUGEVENT`
* `PLUG_CB_MENUENTRY`
* `PLUG_CB_WINEVENT`
* `PLUG_CB_WINEVENTGLOBAL`
* `PLUG_CB_LOADSAVEDB`
* `PLUG_CB_LOADLOADDB`
    
We will cover more in depth usage of the specific callback structures later on.

## The CDECL export callback function

The second way of using callbacks, which may be easier to implement, is to have specifically named functions exported from your plugin. x64dbg will look for these exported functions when loading your plugin and if found will automatically register these as callback events. The exported functions that will be recognised are:

* `CBINITDEBUG`
* `CBSTOPDEBUG`
* `CBCREATEPROCESS`
* `CBEXITPROCESS`
* `CBCREATETHREAD`
* `CBEXITTHREAD`
* `CBSYSTEMBREAKPOINT`
* `CBLOADDLL`
* `CBUNLOADDLL`
* `CBOUTPUTDEBUGSTRING`
* `CBEXCEPTION`
* `CBBREAKPOINT`
* `CBPAUSEDEBUG`
* `CBRESUMEDEBUG`
* `CBSTEPPED`
* `CBATTACH`
* `CBDETACH`
* `CBDEBUGEVENT`
* `CBMENUENTRY`
* `CBWINEVENT`
* `CBWINEVENTGLOBAL`
* `CBSAVEDB`
* `CBLOADDB`

These function are defined in the plugin SDK for ease of use. And like the `CBPLUGIN` definition above, they have two parameters: `bType` and `callbackInfo`

You can create an export which has the name of the callback like so, taking `CBINITDEBUG` as our example.

The `callbackInfo` parameter for `CBINITDEBUG` is a pointer to `PLUG_CB_INITDEBUG` structure, defined as:

_C++:_

```cpp
typedef struct
{
    const char* szFileName;
} PLUG_CB_INITDEBUG;
```

_Assembler x86_:

```nasm
PLUG_CB_INITDEBUG STRUCT
    szFileName    DWORD ?
PLUG_CB_INITDEBUG ENDS
```

_Assembler x64_:

```nasm
PLUG_CB_INITDEBUG STRUCT 8
    szFileName    QWORD ?
PLUG_CB_INITDEBUG ENDS
```

This is our C++ example. In C++ you can easily create a CDECL export for the `CBINITDEBUG` function.

_C++_:

```cpp
extern "C" __declspec(dllexport) void CBINITDEBUG(CBTYPE bType, PLUG_CB_INITDEBUG* callbackInfo)
{
    // callbackInfo for CBINITDEBUG is a pointer to PLUG_CB_INITDEBUG 
    // structure containing one field called szFileName, which is a 
    // pointer to a string containing the name of the debuggee file 
    // about to be debugged.
    
    // do something with the filename: (const char*)callbackInfo->szFileName
    // do any other processing 
}
```

The prototype definitions for the exported `CBINITDEBUG` function in assembler are:

_Assembler x86_:

```nasm
CBINITDEBUG PROTO :DWORD, :DWORD ; (CBTYPE bType, void* callbackInfo)
```

_Assembler x64_:
```nasm
CBINITDEBUG PROTO :QWORD, :QWORD ; (CBTYPE bType, void* callbackInfo)
```

And the example code for each `CBINITDEBUG` function in assembler is:

_Assembler x86_:

```nasm
CBINITDEBUG PROC C PUBLIC USES EBX cbType:DWORD, callbackInfo:DWORD

    ; callbackInfo for CBINITDEBUG is a pointer to PLUG_CB_INITDEBUG 
    ; structure containing one field called szFileName, which is a 
    ; pointer to a string containing the name of the debuggee file 
    ; about to be debugged.
    
    mov ebx, callbackInfo
    mov eax, [ebx].PLUG_CB_INITDEBUG.szFileName
    
    ; eax now contains the pointer to the filename string.
    ; do any other processing 
    
    ret
CBINITDEBUG ENDP
```

_Assembler x64_:

```nasm
CBINITDEBUG PROC FRAME USES RBX cbType:QWORD, callbackInfo:QWORD

    ; callbackInfo for CBINITDEBUG is a pointer to PLUG_CB_INITDEBUG 
    ; structure containing one field called szFileName, which is a 
    ; pointer to a string containing the name of the debuggee file 
    ; about to be debugged.
    
    mov rbx, callbackInfo
    mov rax, [rbx].PLUG_CB_INITDEBUG.szFileName
    
    ; rax now contains the pointer to the filename string.
    ; do any other processing 
    
    ret
CBINITDEBUG ENDP
```

In assembler (x86 and x64) you must add your exported functions to a .def file for them to be exported when compiling and linking:

```nasm
LIBRARY MyPlugin
EXPORTS pluginit
        plugstop
        plugsetup
        CBINITDEBUG
```

In all the examples above, the CBINITDEBUG function is registered as our callback and called when debugging begins. The callbackInfo parameter contains the pointer to a PLUG_CB_INITDEBUG, from which we can retrieve the name of the file that is about to be debugged. We could display this information in the log window or do something else instead.

# Summary

Hopefully if you have read all this article it has covered the following:

* General questions that may have arisen about using the x64dbg plugin SDK and developing a plugin SDK for assembler.
* The question on why to create a plugin - generally, and for use with open source projects.
* Explanation of the basic overall plugin architecture (dynamic link library & DllMain)
* The plugin loading sequence - steps that occur when a plugin is loaded by x64dbg
* Specific plugin SDK functions required for creating a working (but basic) plugin: `pluginit` and `plugsetup`.
* Plugin SDK structures used with `pluginit` and `plugsetup`, namely `PLUG_INITSTRUCT` and `PLUG_SETUPSTRUCT`.
* `CB*` callback functions and the two ways in which to register them with your plugin: `_plugin_registercallback` or by exporting specific function names.

# Afterword

Lots of code listing and technical information, which might not necessarily be to everyone's taste, but hopefully in a future article I will cover a specific working plugin example and walk through the development of it - most likely in assembler x86.

I've included a list below of additional resources that are related to x64dbg and plugin development which you may find useful.

Thank you for taking the time to read this article.

fearless

# Additional resources of interest

## x64dbg

* [x64dbg Website](http://x64dbg.com)
* [x64dbg Github](https://github.com/x64dbg/x64dbg)
* [x64dbg Latest Release](http://releases.x64dbg.com)

## x64dbg Plugin SDK For Assembler

* [x64dbg Plugin SDK For x86 Assembler](https://github.com/mrfearless/x64dbg-Plugin-SDK-For-x86-Assembler)
* [x64dbg Plugin SDK For x64 Assembler](https://github.com/mrfearless/x64dbg-Plugin-SDK-For-x64-Assembler)

## Assemblers

* [Masm32 Assembler](http://www.masm32.com/masmdl.htm)
* [HJWasm Assembler](https://github.com/Terraspace/HJWasm)

## Other

* [x64dbg plugin template for Visual Studio](https://github.com/mrfearless/x64dbg-plugin-template-for-Visual-Studio)
* [fearless](https://github.com/mrfearless)