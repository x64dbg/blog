---
layout: post
title: Architecture of x64dbg
author: torusrxxx
website: https://github.com/torusrxxx
contents: ["Bootstrapping", "Debugging", "Message passing from GUI to DBG", "Commands dispatch", "Directly exported functions", "Export functions dispatch", "DbgFunctions", "Message flow from DBG to GUI", "Important subsystems in GUI", "Tables in GUI", "Context menu management", "Configuration management", "Important subsystems in DBG", "threading.h", "x64dbg.cpp", "memory.h , module.h and thread.h, label.h and breakpoint.h, etc", "scriptapi"]

---

x64dbg has a complex architecture. There are three basic parts, namely [DBG](https://github.com/x64dbg/x64dbg/tree/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg), [BRIDGE](https://github.com/x64dbg/x64dbg/tree/7eecb558a02defe2739623117995ab78dc5c3c67/src/bridge) and [GUI](https://github.com/x64dbg/x64dbg/tree/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui), but in fact there is a fourth part, [EXE](https://github.com/x64dbg/x64dbg/tree/7eecb558a02defe2739623117995ab78dc5c3c67/src/exe). This is the main executable, it compiles into `x64dbg.exe`.

![architecture diagram](https://i.imgur.com/DatgCBa.png)

## Bootstrapping

When the user starts x64dbg, it will follow this initialization path to get x64dbg running:

- [WinMain](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/exe/x64dbg_exe.cpp#L26)
- [BridgeInit](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/bridge/bridgemain.cpp#L45)
  - LoadLibrary("x64gui.dll")
    - Initialize global variables in the GUI
  - LoadLibrary("x64dbg.dll")
    - Initialize global variables in the DBG
  - Load function pointers
- [BridgeStart](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/bridge/bridgemain.cpp#L98)
  - [_dbg_sendmessage](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/_exports.cpp#L713)([DBG_INITIALIZE_LOCKS](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/_exports.cpp#L1212))
  - [_gui_guiinit](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/Bridge/Bridge.cpp#L678) -> [main](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/main.cpp#L67)
    - [#70](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/main.cpp#L70): Application object created
    - [#82](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/main.cpp#L82): Set up event filter
    - [#95](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/main.cpp#L95): Load translations
    - [#128](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/main.cpp#L128): Create default bridge object
    - [#134](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/main.cpp#L134): Initialize [MainWindow](
    - [#140](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/main.cpp#L140): [DbgInit]() -> [_dbg_dbginit](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/x64dbg.cpp#L582)
      - [#584](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/x64dbg.cpp#L584): Initialize modules
      - [#665](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/x64dbg.cpp#L665): Initialize variables ([varinit](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/variable.cpp#L60))
      - [#667](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/x64dbg.cpp#L667): Register commands ([registercommands](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/x64dbg.cpp#L80))
      - [#670](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/x64dbg.cpp#L670): Register expression functions ([ExpressionFunctions::Init](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/expressionfunctions.cpp#L41))
      - [#689](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/x64dbg.cpp#L689): Load plugins ([pluginloadall](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/plugin_loader.cpp#L361))
      - [#694](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/x64dbg.cpp#L694): Handle potential command line
    - [#150](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/main.cpp#L150): Execute the application (starting the user event loop). 

## Debugging

To start debugging, the GUI sends an [init](http://help.x64dbg.com/en/latest/commands/debug-control/InitDebug.html) command to the DBG. Then the following things start:

- [cbDebugInit](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/commands/cmd-debug-control.cpp#L26)
  - Check various things
  - Run [threadDebugLoop](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/debugger.cpp#L2484) in a new thread
    - [debugLoopFunction](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/debugger.cpp#L2292)
      - [#2289](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/debugger.cpp#L2298): Initialize various variables
      - [#2323](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/debugger.cpp#L2323): [DbSetPath](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/database.cpp#L268)
      - [#2338](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/debugger.cpp#L2338): CreateProcess
      - [#2351](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/debugger.cpp#L2351): Check for Wow64 mismatch
      - [#2379](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/debugger.cpp#L2379): Set up [TitanEngine](https://bitbucket.org/titanengineupdate/titanengine-update) handlers
      - [#2392](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/debugger.cpp#L2392): Tell GUI to enter the `initialized` state
      - [#2404](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/debugger.cpp#L2404) Call the [CB_INITDEBUG]() plugin callback
      - [#2429](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/debugger.cpp#L2429) Enter the [DebugLoop](https://bitbucket.org/titanengineupdate/titanengine-update/src/e089f4af41a461b69017db3750f79fbaed1008df/TitanEngine/TitanEngine.Debugger.DebugLoop.cpp?at=master&fileviewer=file-view-default#TitanEngine.Debugger.DebugLoop.cpp-17)

## Message passing from GUI to DBG

There are four methods to call DBG from GUI. They are commands, directly exported functions, bridge exported functions (messages) and DbgFunctions(). Currently the directly exported functions are frozen and no new ones should be added. The message flows for each way will be described below.

### Commands dispatch

[DbgCmdExec](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/bridge/bridgemain.cpp#L301) is relayed by the bridge to the DBG and eventually received by the [cmdloop](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/command.cpp#L222) running in the command thread. This is done asynchronously (meaning DbgCmdExec will not wait until the command is completed).

[DbgCmdExecDirect](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/bridge/bridgemain.cpp#L489) is relayed by the bridge to DBG and then directly in [cmddirectexec](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/command.cpp#L288). This will only return after the command is completed.

In both cases the command is parsed and dispatched to various registered command callbacks. A command callback is similar to main() functions. It can receive number of arguments (plus one), and pointer to every argument string.

Commands are registered in the [registercommands](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/x64dbg.cpp#L80) function. If you want to get a total list of supported commands, or add your own, just go to that file. Make sure to put your command in the correct category and also make sure to add it to the [documentation](https://github.com/x64dbg/docs).

### Directly exported functions

There are some legacy functions still unconverted to another method, these can be found in [exports.h](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/_exports.h).

### Export functions dispatch

Many Dbg\*\*\* functions are exported by the bridge. It then calls [_dbg_sendmessage](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/_exports.cpp#L713) exported by DBG to pass information. Some Dbg\*\*\* functions have exports directly in DBG.

### DbgFunctions

[_dbgfunctions.cpp](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/_dbgfunctions.cpp) has a [function table](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/dbg/_dbgfunctions.h#L153) that is accessible by anyone. The GUI can call functions in DBG through this table directly.

## Message flow from DBG to GUI

There are various Gui\*\*\* functions exported by the bridge. The control flow is described below:

- Gui\*\*\* export
- Bridge calls [_gui_sendmessage](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/Bridge/Bridge.cpp#L683)
- Bridge calls [Bridge::processMessage](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/Bridge/Bridge.cpp#L81)
- A long list of switch statements in `processMessage`, basically to emit the corresponding signal. If you want to receive a system event, connect to one of the signals in `Bridge::getBridge()`

## Important subsystems in GUI

### Tables in GUI

There is three-level class architecture to support various tables. The first-level class is [AbstractTableView](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/BasicView/AbstractTableView.cpp), which only includes some basic functions. The second-level classes are [Disassembly](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/BasicView/Disassembly.cpp), [HexDump](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/BasicView/HexDump.cpp) and [StdTable](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/BasicView/StdTable.cpp). They all inherit from `AbstractTableView`. Many basic and common functions are defined here, such as table painting, selection, content presentation and column reordering. The third-level classes inherit from the second-level classes. There are many third-level classes. The most common parent for these tables is `StdTable`.

### Context menu management

There are two styles of context menu management. The traditional one builds actions in `setupContextMenu` and adds them into a menu object in `contextMenuEvent`. [CPUStack](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/Gui/CPUStack.cpp) uses this style currently. A newer way to manage context menu is to use [MenuBuilder](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/Utils/MenuBuilder.h). You can see [CPUDisassembly](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/Gui/CPUDisassembly.cpp) or this [blog post](https://mrexodia.github.io/x64dbg/2016/02/03/Dynamic-menu-builder) for more details. It is the preferred way to manage context menu in newer tables, but it does not support non-table widgets out of the box. We want to convert traditional context menu systems into `MenuBuilder` to speed up development.

### Configuration management

Configurations are stored in the `Config()` object which uses [Utf8Ini](https://github.com/mrexodia/Utf8Ini) in the bridge as its backend. When you want to add a new configuration, you have to modify the following files: [Configuration.cpp](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/Utils/Configuration.cpp) and the [SettingsDialog](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/Gui/SettingsDialog.cpp). If you are adding a color then you have to modify the [AppearanceDialog](https://github.com/x64dbg/x64dbg/blob/7eecb558a02defe2739623117995ab78dc5c3c67/src/gui/Src/Gui/AppearanceDialog.cpp) as well. `Config()` can emit settings change signals.

## Important subsystems in DBG

There are many subsystems in DBG. The following subsystems are important if you want to contribute:

### threading.h

It includes various locks to prevent race condition. Without it, x64dbg will crash much more often. Don't forget to acquire the lock when you are accessing a subsystem.

### x64dbg.cpp

It registers all commands in x64dbg. The details of command processing is described above.

### memory.h , module.h and thread.h, label.h and breakpoint.h, etc

They manages corresponding information of the debuggee.

### scriptapi

It is intended to be used by plugins. It provides easy scripting experience for developers. x64dbg does not call any of these functions.
