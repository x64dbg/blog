---
layout: post
title: The big handle gamble
author: mrexodia
website: https://mrexodia.cf
---

Yesterday I was debugging some programs and after restarting I saw that the status label stayed stuck on `Initializing`. At first it didn't seem to impact anything, but pretty soon after that other things started breaking as well.

Reproduction steps:

- Load some debuggee
- Hold step for some time
- Press restart
- Repeat until the bug shows

Observed behaviours:

1. The label stays stuck on `Initializing`
2. The label stays stuck on `Paused` (appears to be more rare)

## A shot in the dark

After getting more or less stable reproductions I started to look into why this could be happening. On the surface the [TaskThread](https://x64dbg.com/blog/2016/10/20/threading-model.html#taskthread) appeared to be correct, but since the WakeUp function was probably failing I put an assert on `ReleaseSemaphore`, which should trigger the TaskThread:

```c++
template <typename F, typename... Args>
void TaskThread_<F, Args...>::WakeUp(Args... _args)
{
    ++this->wakeups;
    EnterCriticalSection(&this->access);
    this->args = CompressArguments(std::forward<Args>(_args)...);
    LeaveCriticalSection(&this->access);
    // This will fail silently if it's redundant, which is what we want.
    if(!ReleaseSemaphore(this->wakeupSemaphore, 1, nullptr))
        __debugbreak();
}
```

I tried to reproduce the bug and unsurprisingly the assert triggered! At this point I suspected memory corruption, so I inserted a bunch of debug tricks in the TaskThread to store the original handle in a safe memory location:

```c++
struct DebugStruct
{
    HANDLE wakeupSemaphore = nullptr;
};

template <int N, typename F, typename... Args>
TaskThread_<N, F, Args...>::TaskThread_(F fn,
                                     size_t minSleepTimeMs, DebugStruct* debug) : fn(fn), minSleepTimeMs(minSleepTimeMs)
{
    //make the semaphore named to find it more easily in a handles viewer
    wchar_t name[256];
    swprintf_s(name, L"_TaskThread%d_%p", N, debug);
    this->wakeupSemaphore = CreateSemaphoreW(nullptr, 0, 1, name);
    if(debug)
    {
        if(!this->wakeupSemaphore)
            __debugbreak();
        debug->wakeupSemaphore = this->wakeupSemaphore;
    }
    InitializeCriticalSection(&this->access);

    this->thread = std::thread([this, debug]
    {
        this->Loop(debug);
    });
}
```

The TaskThread instance is now initialized and called like so:

```c++
void GuiSetDebugStateAsync(DBGSTATE state)
{
    GuiSetDebugStateFast(state);
    static TaskThread_<
               6,
               decltype(&GuiSetDebugState),
               DBGSTATE>
           GuiSetDebugStateTask(
               &GuiSetDebugState,
               300,
               new (VirtualAlloc(0,
                                 sizeof(DebugStruct),
                                 MEM_RESERVE | MEM_COMMIT,
                                 PAGE_EXECUTE_READWRITE)
                   ) DebugStruct()
           );
    GuiSetDebugStateTask.WakeUp(state, true);
}
```

![Semaphore handle](https://i.imgur.com/lmOLK6O.png)

Now I started x64dbg and used [Process Hacker](http://processhacker.sourceforge.net) to find the `_TaskThread6_XXXXXXXX` semaphore to take note of the handle. I then reproduced and found to my surprise that the value of `wakeupSemaphore` was 0x640, the same value as on startup!

However when I checked the handle view again, 0x640 was no longer the handle to a semaphore, but rather to a mapped file!

![Mapped file handle](https://i.imgur.com/xrxe0g7.png)

## Pushing our luck

This started to smell more and more like bad WinAPI usage. Tools like [Application Verifier](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/application-verifier) exist to find these kind of issues, but I could not get it to work so I had to roll my own.

The idea is rather simple:

1. Use [minhook](https://github.com/TsudaKageyu/minhook) to hook the `CloseHandle` API.
2. Save the correct semaphore handle to a global variable
3. Crash if this handle is ever closed

```c++
static DebugStruct* g_Debug = nullptr;
typedef BOOL(WINAPI* CLOSEHANDLE)(HANDLE hObject);
static CLOSEHANDLE fpCloseHandle = nullptr;

static BOOL WINAPI CloseHandleHook(HANDLE hObject)
{
    if(g_Debug && g_Debug->wakeupSemaphore == hObject)
        __debugbreak();
    return fpCloseHandle(hObject);
}

static void DoHook()
{
    if(MH_Initialize() != MH_OK)
        __debugbreak();
    if(MH_CreateHook(GetProcAddress(GetModuleHandleW(L"kernelbase.dll"), "CloseHandle"), &CloseHandleHook, (LPVOID*)&fpCloseHandle) != MH_OK)
        __debugbreak();
    if(MH_EnableHook(MH_ALL_HOOKS) != MH_OK)
        __debugbreak();
}
```

This time reproducing the issue gave some *very* useful results:

![WinDbg callstack](https://i.imgur.com/fjbC8Mw.png)

## Winner winner chicken dinner!

The actual bug turned out to be in TitanEngine. The [ForceClose](https://bitbucket.org/titanengineupdate/titanengine-update/src/e089f4af41a461b69017db3750f79fbaed1008df/TitanEngine/TitanEngine.Debugger.Control.cpp?at=master&fileviewer=file-view-default#TitanEngine.Debugger.Control.cpp-34) function is supposed to close all the DLL handles from the current debug session, but some of these handles were already closed where the `UNLOAD_DLL_DEBUG_EVENT` is [handled](https://bitbucket.org/titanengineupdate/titanengine-update/src/e089f4af41a461b69017db3750f79fbaed1008df/TitanEngine/TitanEngine.Debugger.DebugLoop.cpp?at=master&fileviewer=file-view-default#TitanEngine.Debugger.DebugLoop.cpp-382).

But how does the semaphore handle value come to be the same as a previous file handle? The answer to that puzzling question is given when you look at the flow of events:

- `LOAD_DLL_DEBUG_EVENT` gets a file handle that is stored in the library list.
- `UNLOAD_DLL_DEBUG_EVENT` closes said file handle during the debug session.
- The `static` initializer for the `TaskThread` is called when the debugger pauses for the first time and the semaphore is created with the same handle value as the (now closed) file handle from the `LOAD_DLL_DEBUG_EVENT`.
- All goes well, *until* the `ForceClose` function is called and the file handle from `LOAD_DLL_DEBUG_EVENT` is closed once again.
- Hell breaks loose because the `TaskThread` breaks.

Now for why this doesn't happen every single time (sometimes I had to restart the debuggee 20 or more times), the handle value is 'randomly' reused from the closed handle pool and it's kind of a coin toss as to when this happens. I found that you can greatly increase the likelyhood of this happening when your PC has been on for a few days and you have 70k handles open. Probably the kernel will use a more aggressive recycling strategy when low on handles, but that's just my guess.

If you are interested in trying to reproduce this at home, you can use the [handle_gamble](https://github.com/x64dbg/x64dbg/tree/handle_gamble) branch. You can also take a look at the relevant [issue](https://github.com/x64dbg/x64dbg/issues/1793).

Duncan