---
layout: post
title: Architecture of x64dbg
author: torusrxxx
website: https://github.com/torusrxxx
---

x64dbg has a complex architecture. There are three basic parts, namely "DBG", "BRIDGE" and "GUI", but in fact there is a fourth part, "EXE". "EXE" is the main executable. It compiles into "x64dbg.exe".

# Bootstraping

When the user starts x64dbg, it will follow this initialization path to get x64dbg running:

WinMain -> BridgeInit {-> LoadLibrary("x64gui.dll") {-> Initializes global variables in "GUI" part.} -> LoadLibrary("x64dbg.dll") {-> Initializes global variables in "DBG" part.} -> Load function pointers} -> BridgeStart {-> _dbg_sendmessage(DBG_INITIALIZE_LOCKS, nullptr, nullptr); -> _gui_guiinit(0, 0); {-> main() {-> Application object created -> set up event filter -> load translations -> create default bridge object -> show main window.

# Debugging

To start debugging, the GUI sends an "init" command to the DBG. Then the following things start:

(in function cbDebugInit)check various things -> run threadDebugLoop in another thread {(in function debugLoopFunction) -> initialize various variables -> DbSetPath -> create process -> check for Wow64 mismatch -> set up TitanEngine handlers -> Tell GUI to enter initialized state -> call plugin callback -> enter debug loop.

# message passing from GUI to DBG

There are 3 methods to call DBG from GUI. They are commands, exported functions, and DbgFunctions(). Currently the exported functions are frozen, new functions may only be added into DbgFunctions. The message flows for each way will be described below:

## export functions dispatch

Many Dbg\*\*\* functions are exported by BRIDGE. It then calls _dbg_sendmessage exported by DBG to pass information. Some Dbg\*\*\* functions have exports directly in DBG.

## DbgFunctions

_dbgfunctions.cpp has a function table that is accessible by anyone. GUI can call functions in DBG through this table directly.

## commands dispatch

DbgCmdExec and DbgCmdExecDirect are relayed by the bridge to DBG, and further relayed to cmddirectexec in DBG. DbgCmdExec will post the command first to a command queue, so it may be processed asynchronized. The command is then parsed and dispatched to various registered command callbacks. A command callback is similar to main() functions. It can recieve number of arguments (plus one), and pointer to every argument string.

Commands are registered in registercommands() in x64dbg.cpp . If you want to get a total list of supported commands, or add your own, just go to that file.

# message flow from DBG to GUI

There are various Gui\*\*\* functions exported by BRIDGE. The control flow is described below:

Gui\*\*\* -> BRIDGE (then calls _gui_sendmessage) -> Bridge::getBridge()->processMessage in Bridge.cpp -> a long list of switch statements in processMessage(), basically to emit corresponding signal. If you want to recieve a system event, connect the slot to one of the signals in Bridge::getBridge().

# Important subsystems in GUI

## Tables in GUI

There is three-level class architecture to support various tables. The first-level class is AbstractTableView, which only includes some basic functions. The second-level classes are Disassebler, HexDump, StdTable. They all inherit from AbstractTableView. Many basic and common functions are defined here, such as table painting, selection, content presentation and column reordering. The third-level classes inherit from the second-level classes. There are many third-level classes. The most common parent for these tables is StdTable.

## Context menu management

There are two styles of context menu management. The traditional one builds actions in setupContextMenu and adds them into a menu object in contextMenuEvent. CPUStack uses this style currently. A newer way to manage context menu is to use MenuBuilder. You can see CPUDisassembly for its example. It is the perfered way to manage context menu in newer tables, but it does not support non-table widgets currently. We want to convert traditional context menu systems into MenuBuilder to speed up development.

## Configuration management

Configurations are stored in Config() object which uses "UTF8INI" in BRIDGE as its backend. When you want to add a new configuration, you have to modify the following files: Configuration.cpp, SettingsDialog. If you are adding a color then you have to modify AppearanceDialog.cpp as well. Config() can emit settings change signals.

# Important subsystems in DBG

There are many subsystems in DBG. The following subsystems are important if you want to contribute:

## threading.h

It includes various locks to prevent race condition. Without it, x64dbg will crash much more often. Don't forget to acquire the lock when you are accessing a subsystem.

## x64dbg.cpp

It registers all commands in x64dbg. The details of command processing is described above.

## memory.h , module.h and thread.h, label.h and breakpoint.h, etc

They manages corresponding information of the debuggee.

## scriptapi

It is intended to be used by plugins. It provides easy scripting experience for developers. x64dbg does not call any of these functions.
