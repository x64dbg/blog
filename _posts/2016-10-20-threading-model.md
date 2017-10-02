---
layout: post
title: The x64dbg threading model
author: mrexodia
website: http://mrexodia.cf
contents: ["Command loop thread", "Debug thread", "Script thread", "Worker threads", "TaskThread", "GUI Thread"]

---

In a recent post about the [architecture of x64dbg](https://x64dbg.com/blog/2016/10/04/architecture-of-x64dbg.html) there was a comment to explain the "little bit of a mess" that is the threading model of x64dbg. It is indeed not particularly pretty, but everything has a purpose.

## Command loop thread

The first thread of interest is the [command thread](https://github.com/x64dbg/x64dbg/blob/33024f567230620eaa5cd5188b0c0f2c9903e1a9/src/dbg/command.cpp#L268). This thread is created during the initialization phase and it infinitely waits and executes commands that are given to it through the so-called [CommandProvider](https://github.com/x64dbg/x64dbg/blob/33024f567230620eaa5cd5188b0c0f2c9903e1a9/src/dbg/x64dbg.cpp#L441). In the [very first version of x64dbg](https://bitbucket.org/mrexodia/x64_dbg_old/commits/24b5251f492aad0ac76b952ec783b6005f27fb1b#Lcommand.cppT56) the command thread was the main thread and since the [introduction of the GUI](https://bitbucket.org/mrexodia/x64_dbg_old/commits/d8b1abc6ac1b1ee98dd18ca8218fa53bfa4bc289#Lx64_dbg_dbg/x64_dbg.cppT138) this has been moved to a separate thread in favor of the GUI thread.

## Debug thread

The debug thread runs the [TitanEngine](https://bitbucket.org/titanengineupdate/titanengine-update) debug loop. It still works the same as [two years ago](http://mrexodia.cf/x64_dbg/2014/12/24/x64_dbg-from-top-to-bottom-1): 

![debug loop](https://i.imgur.com/ulOZUnN.png)

Between `WaitForDebugEvent` and `ContinueDebugEvent`, the debuggee is in a paused state. The event handlers use [event objects](http://goo.gl/H3lEZL) to communicate with the GUI. When you click the 'Run' button it will set an event object and continue the debug loop and in that way also continue the debuggee.

Here is a simplified version of the [cbDebugRun](https://github.com/x64dbg/x64dbg/blob/33024f567230620eaa5cd5188b0c0f2c9903e1a9/src/dbg/commands/cmd-debug-control.cpp#L35) command callback (running on the command thread):

```c++
bool cbDebugRun(int argc, char* argv[])
{
    // Don't "run" twice if the program is already running.
    if(dbgisrunning())
        return false;
    
    //Set the event, which makes calls to wait(WAITID_RUN) return.
    unlock(WAITID_RUN); 
    
    return true;
}
```

On the debug loop thread we have the [cbPauseBreakpoint](https://github.com/x64dbg/x64dbg/blob/33024f567230620eaa5cd5188b0c0f2c9903e1a9/src/dbg/debugger.cpp#L683) breakpoint event handler that waits for the user to resume the debug loop (again, simplified):

```c++
void cbPauseBreakpoint()
{
    //Unset (reset) the event.
    lock(WAITID_RUN);
    //Wait for the event to be set, a call to unlock(WAITID_RUN).
    wait(WAITID_RUN);
}
```

Here is a simple diagram giving you an overview of what's going on with the basic threads.

![basic threading](https://i.imgur.com/AwoWDqJ.png)

- A block represents a thread;
- A dashed arrow represents starting a new thread;
- A red arrow represents thread termination;
- A circle contains the termination condition. 

Some challenging areas are properly signaling the termination of the debuggee. Issues [#303](https://github.com/x64dbg/x64dbg/issues/303), [#323](https://github.com/x64dbg/x64dbg/issues/323) and [#438](https://github.com/x64dbg/x64dbg/issues/438) were, with the great help and patience of [wk-952](https://github.com/x64dbg/x64dbg/issues/438), fixed and this signaling appears to be working now!

## Script thread

When dealing with scripting, you usually want to simulate user interaction. This means that the expectation is that the following [x64dbgpy](https://github.com/x64dbg/x64dbgpy) (Python) script should be equivalent to:

- Setting a breakpoint on `__security_init_cookie`
- Pressing the run button
- Stepping five times
- Setting `RAX` to `0x2b992ddfa232`
- Stepping out of the function

```python
from x64dbgpy.pluginsdk import *

debug.SetBreakpoint(x64dbg.DbgValFromString("__security_init_cookie"))
debug.Run()
for _ in range(0,5):
    debug.StepIn()
register.SetRAX(0x2b992ddfa232)
debug.StepOut()
```

There has to be some sort of synchronization at the end of `debug.Run` and `debug.StepOut` to make sure the debuggee is paused before the next command is executed. The implementation for this is in [_plugin_waituntilpaused](https://github.com/x64dbg/x64dbg/blob/33024f567230620eaa5cd5188b0c0f2c9903e1a9/src/dbg/_plugins.cpp#L146) and looks like this:

```c++
PLUG_IMPEXP bool _plugin_waituntilpaused()
{
    while(DbgIsDebugging() && dbgisrunning()) //wait until the debugger paused
        Sleep(1);
    return DbgIsDebugging();
}
```

The implementation of [dbgisrunning](https://github.com/x64dbg/x64dbg/blob/33024f567230620eaa5cd5188b0c0f2c9903e1a9/src/dbg/debugger.cpp#L286) is a check if `lock(WAITID_RUN)` has been called.

## Worker threads

There are various threads that just do periodic background work. These include:

- Refreshing the [memory map](https://github.com/x64dbg/x64dbg/blob/33024f567230620eaa5cd5188b0c0f2c9903e1a9/src/dbg/debugger.cpp#L163)
- Refreshing the [dumps](https://github.com/x64dbg/x64dbg/blob/33024f567230620eaa5cd5188b0c0f2c9903e1a9/src/dbg/debugger.cpp#L215)
- Refreshing the [time-wasted counter](https://github.com/x64dbg/x64dbg/blob/33024f567230620eaa5cd5188b0c0f2c9903e1a9/src/dbg/debugger.cpp#L192)

Other threads are triggered once to fulfill a specific purpose. These include:

- Command [animation](https://github.com/x64dbg/x64dbg/blob/33024f567230620eaa5cd5188b0c0f2c9903e1a9/src/dbg/animate.cpp#L9)
- Executing asynchronous [Script DLLs](https://github.com/x64dbg/x64dbg/blob/33024f567230620eaa5cd5188b0c0f2c9903e1a9/src/dbg/x64dbg.cpp#L489)
- Loading [databases from disk](https://github.com/x64dbg/x64dbg/blob/33024f567230620eaa5cd5188b0c0f2c9903e1a9/src/dbg/x64dbg.cpp#L553)
- Executing [Scylla](https://github.com/x64dbg/x64dbg/blob/33024f567230620eaa5cd5188b0c0f2c9903e1a9/src/dbg/commands/cmd-plugins.cpp#L9)
- Querying the [name of a handle](https://github.com/x64dbg/x64dbg/blob/33024f567230620eaa5cd5188b0c0f2c9903e1a9/src/dbg/handles.cpp#L52)
- Loading a [script from disk](https://github.com/x64dbg/x64dbg/blob/33024f567230620eaa5cd5188b0c0f2c9903e1a9/src/dbg/simplescript.cpp#L455)

## TaskThread

For interaction with the GUI, performance is very important. For this purpose [jdavidberger](https://github.com/jdavidberger) has implemented [TaskThread](https://github.com/x64dbg/x64dbg/blob/33024f567230620eaa5cd5188b0c0f2c9903e1a9/src/dbg/taskthread.h). It's some variadic templates that basically allow you to trigger an arbitrary function from a different thread to then quickly return to the real work.

The actual thread runs in an infinite loop, waiting for the `TaskThread` instance to receive a `WakeUp` (trigger). Once awake, the specified function is executed and after that the thread is being delayed for a configurable amount of time. This ignores all triggers (except the last one) within the delay time to avoid unnecessary work.

The relevant code:

```c++
template <typename F, typename... Args> void TaskThread_<F, Args...>::WakeUp(Args... _args)
{
    wakeups++;
    EnterCriticalSection(&access);
    args = CompressArguments(std::forward<Args>(_args)...);
    LeaveCriticalSection(&access);
    // This will fail silently if it's redundant, which is what we want.
    ReleaseSemaphore(wakeupSemaphore, 1, nullptr);
}

template <typename F, typename... Args> void TaskThread_<F, Args...>::Loop()
{
    std::tuple<Args...> argLatch;
    while(active)
    {
        WaitForSingleObject(wakeupSemaphore, INFINITE);

        EnterCriticalSection(&access);
        argLatch = args;
        ResetArgs();
        LeaveCriticalSection(&access);

        if(active)
        {
            apply_from_tuple(fn, argLatch);
            std::this_thread::sleep_for(std::chrono::milliseconds(minSleepTimeMs));
            execs++;
        }
    }
}
```

As an example, here is the declaration and wake of the thread that updates the call stack (an expensive operation in some cases):

```c++
static DWORD WINAPI updateCallStackThread(duint csp)
{
    stackupdatecallstack(csp);
    GuiUpdateCallStack();
    return 0;
}

void updateCallStackAsync(duint csp)
{
    static TaskThread_<decltype(&updateCallStackThread), duint> updateCallStackTask(&updateCallStackThread);
    updateCallStackTask.WakeUp(csp);
}
```

Having a different thread handle expensive operations is critial to a responsive interface. Lots of information is rarely looked at (memory map, call stack, SEH information) and can suffer a little delay (100ms) before being updated. This is the same with the current state of the disassembly. When holding F7 to quickly step a little you don't need perfect accuracy, as long as the disassembly lands on the correct state within reasonable time after releasing the step button.

## GUI Thread

The most important (and the most annoying) thread is the Qt GUI thread. If you want to know more, check out the Qt [Threading Basics](http://doc.qt.io/qt-5/thread-basics.html) for a 6 page introduction on how it works.