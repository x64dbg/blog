---
layout: post
title: Messages Breakpoints in x64dbg
author: ThunderCls
website: http://github.com/ThunderCls
contents: ["Introduction", "Using Windows Messages", "Event-driven programming", "Window Messages", "Window Procedures", "Getting External Window Procedures", "Intercepting Messages", "WinProc Conditional Breakpoints", "Use Cases", "Final Words", "References"]

---

## Introduction

Have you ever been trying to reverse a specific function in an application, but cannot really find it? For instance, let us assume you want to locate the code that is being called right after a click on a button or a keystroke. With certain applications (Delphi, CBuilder, Visual Basic, etc) it is as easy as dropping the executable inside a decompiler and locating the corresponding events/addresses in a matter of seconds. Sometimes it is not that easy, whether a packer or anti-decompiler technique is involved, or just for the simple reason that the application is not an event-driven one. What can you do in that case to obtain those addresses in a similar approach with the least effort?

## Using Windows Messages

Let us take a look at a sample crackme for demonstration purposes. In this case we have a simple executable coded in Visual C++:

![sample crackme](https://i.imgur.com/wCwBI5Y.png)

If we try to enter a text and click on the `Check!` button nothing is happening, not a text message, no nothing. At this point we could get creative and start looking for other alternatives to locate the exact location where our serial is processed and yes, we would probably succeed, but what if I tell you that there is an easier way for us to land just after the press of that button? Just like we would with any Delphi, Visual Basic or any other event-driven language? Let us find out how it works.

After loading and executing the file in x64dbg, we go and enter some text and just before pressing the `Check!` button we go to the `Handles` tab and refresh the view to obtain a window list of the debuggee. We can then see the button there so we right click over it and select the option to set a message breakpoint on it:

![windows widget](https://i.imgur.com/eF9i4U0.png)

Now we are given a window with some options to choose from in order to set a specific message breakpoint in our button control. In this case the configuration I am going to use is something like this:

![message bp dialog](https://i.imgur.com/4EqYM0X.png)

We are specifying that the execution is stopping as soon as a `WM_LBUTTONUP` (left mouse click is up) message is sent to our button control. Right after our breakpoint is set we click the button in the crackme and soon after that we step in our breakpoint.

At this point we achieved what we wanted. We just stopped the execution right after the button click, on the other hand we are in `user32.dll` and our purpose is to be in the main module code. Getting there is as simple as just using a breakpoint in the code section of our executable. You can also use the `Run to user code` option (Ctrl+F9).

![code section breakpoint](https://i.imgur.com/swm7zny.png)

When trying to resume the execution, the debugger is going to stop the execution once again, but this time right in the middle of the code we were looking for. In this case in the `DLGPROC` function (the callback in charge of processing the messages being sent to every window control in the main window dialog).

![dialog function](https://i.imgur.com/bxhfrhi.png)

## Event-driven programming

If you are a programmer, or have been in contact with programming languages in general and coding tasks, you should know the concept of the so called event-driven programming. Event-driven programming is a programming paradigm in which the stream of a program execution is dictated by events; a user action, a mouse click, a key press, etc. An event-driven application is intended to identify events as they happen, and afterwards manage them, utilizing a suitable event-handling procedure. Some programming languages are particularly intended to encourage event-driven programming, and give an IDE that halfway computerizes the generation of code, and gives an extensive choice of inherent built-in objects and controls, Visual Basic, Borland Delphi/CBuilder, C#, Java, etc are some of these types of languages. [(1)][1]

## Window Messages

Even if a programmer is not using one of the above languages or even if they are using them in a non event-driven manner, Microsoft Windows applications are event-driven by nature, which means that you are going to be dealing with window messages anyway. According to the MSDN: 

> The system passes all input for an application to the various windows in the application. Each window has a function, called a window procedure, that the system calls whenever it has input for the window. The window procedure processes the input and returns control to the system.

> The system sends a message to a window procedure with a set of four parameters: a window handle, a message identifier, and two values called message parameters. The window handle identifies the window for which the message is intended. The system uses it to determine which window procedure should receive the message.

> A message identifier is a named constant that identifies the purpose of a message. When a window procedure receives a message, it uses a message identifier to determine how to process the message. [(2)][2]

## Window Procedures

According to the previous information, in order to intercept window messages for a certain window, we need to first locate the window procedure of the desired "control". To so do from the application that contains the window procedure is quite easy, it can be located by using the following functions:

```c++
LONG WINAPI GetWindowLong(
  _In_ HWND hWnd,
  _In_ int  nIndex
);

DWORD WINAPI GetClassLong(
  _In_ HWND hWnd,
  _In_ int  nIndex
);
```

`nIndex = GWL_WNDPROC`: Retrieves the address of the window procedure, or a handle representing the address of the window procedure. You must use the `CallWindowProc` function to call the window procedure.

```c++
BOOL WINAPI GetClassInfo(
  _In_opt_ HINSTANCE  hInstance,
  _In_     LPCTSTR    lpClassName,
  _Out_    LPWNDCLASS lpWndClass
);

BOOL WINAPI GetClassInfoEx(
  _In_opt_ HINSTANCE    hinst,
  _In_     LPCTSTR      lpszClass,
  _Out_    LPWNDCLASSEX lpwcx
);

typedef struct tagWNDCLASS {
  UINT      style;
  WNDPROC   lpfnWndProc;
  ...
} WNDCLASS, *PWNDCLASS;
```

`lpfnWndProc`: A pointer to the window procedure.

At this point everything looks very straightforward, but nonetheless, there is one limitation imposed by our OS: Microsoft Windows will not let you get this information from an external application (such as a debugger). If you want to get the window procedure address of a given window or control that _is owned by another process_ using one of the above functions, you will end up with an `ACCESS_VIOLATION` exception. In our case x64dbg will be no different and hence none of the previous functions will work properly...well...yes and no. Here comes the workaround used by x64dbg to get the correct window procedure address.

## Getting External Window Procedures

At this point it is not clear why this behavior occurs and whether it is OS bug. The thing is, that it can be used in all previous Windows versions. The important function here is:

```c++
DWORD WINAPI GetClassLong(
  _In_ HWND hWnd,
  _In_ int  nIndex
);
```

The hack relies on testing for the given window's charset before calling the correct function version of `GetClassLong` (ANSI/UNICODE) accordingly. The code used by x64dbg is something as simple as this:

```c++
duint wndProc;
if(IsWindowUnicode(hWnd))
    wndProc = GetClassLongPtrW(hWnd, GCLP_WNDPROC);
else
    wndProc = GetClassLongPtrA(hWnd, GCLP_WNDPROC);
```

To write code that is compatible with both 32-bit and 64-bit versions of Windows, you have to use `GetClassLongPtr`. When compiling for 32-bit Windows, `GetClassLongPtr` is defined as a call to the usual `GetClassLong` function.

## Intercepting Messages

Now that the window procedure is located, any message could be intercepted with a proper conditional expression, but before that, let us check the logic behind this. The structure being processed each time by the window procedure looks like this:

```c++
typedef struct tagMSG {
  HWND   hwnd;
  UINT   message;
  WPARAM wParam;
  LPARAM lParam;
  DWORD  time;
  POINT  pt;
} MSG, *PMSG, *LPMSG;
```

As we can see the structure give us some useful information at this point, most importantly `hwnd` and `message`. According to these fields we could know to which specific control what message is being sent to. Before going any further let us see an example for an specific message (`WM_LBUTTONUP`) being sent to a given `Button` control.

![message breakpoint dialog](https://i.imgur.com/2ckFJyM.png)

After clicking the OK button we step on the breakpoint and when we inspect the stack arguments we can see something like this

![breakpoint stack](https://i.imgur.com/Da1ZZHM.png)

The first as can be seen is the handle corresponding to our `Button` control and the second corresponding to the message `WM_LBUTTONUP` (0x202).

## WinProc Conditional Breakpoints

The last thing to get this feature fully working is the possibility to pause the application only when specifics handles and messages are in play. As you can read in the [help](http://help.x64dbg.com/en/latest/introduction/index.html), x64dbg integrates a very nice and powerful set of expressions to allow this. As shown in the above picture there are three options involved:

1. **Break on any window**: Using this option we stop on the given message regardless the window handle. For this we need the simplest expression: 

```c++
bpcnd WINPROC, "arg.get(1) == MESSAGE"
```

2. **Break on current window only**: This feature will add an additional condition to the expression in order to stop the execution only when the handle of the specific window is involved, the expression in this case would be:

```c++
bpcnd WINPROC, "arg.get(1) == MESSAGE && arg.get(0) == HANDLE"
```

3. **Use TranslateMessage**: Sometimes the winproc technique will not give the expected results so this other feature goes out of the scope of the previous technique as it relies in the *TranslateMessage* API to intercept messages and not in the window procedures themselves. Althought the logic is more or less the same.

```c++
BOOL WINAPI TranslateMessage(
  _In_ const MSG *lpMsg
);
```

As seen the function uses the same `MSG` structure that we saw before, hence the functioning with the expressions will be more of the same with some minor changes depending on the OS platform:

```c++
ifdef _WIN64
bpcnd TranslateMessage, "4:[arg.get(0)+8] == MESSAGE"
bpcnd TranslateMessage, "4:[arg.get(0)+8] == MESSAGE && 4:[arg.get(0)] == HANDLE"
#else //x86
bpcnd TranslateMessage, "[arg.get(0)+4] == MESSAGE"
bpcnd TranslateMessage, "[arg.get(0)+4] == MESSAGE && [arg.get(0)] == HANDLE"
#endif //_WIN64
```

## Use Cases

As seen in this post, this is a very convenient and strong feature in x64dbg and can be used in numerous scenarios. Having the possibility to control on which events to pause a debuggee, even if it is not and event-driven application like a Delphi or Visual Basic, open the doors and give the reverser even more resources to debug. If you want to pause the execution when entering a char in an *Edit* control in a MASM application just set a messages breakpoint on the control itself with the message *WM_KEYUP*, simple as that. Same goes for Button clicks, showing windows, etc. There are a whole bunch of messages options to choose from.

## Final Words

With these lines I tried to give an in-depth view of the messages breakpoints feature and some of the multiple scenarios where and how to use it. And this is all for this post, see ya around.

ThunderCls signing out

## References

[1]: https://www.technologyuk.net/computing/software-development/event-driven-programming.shtml
[2]: https://msdn.microsoft.com/en-us/library/windows/desktop/ms644927(v=vs.85).asp

1. https://www.technologyuk.net/computing/software-development/event-driven-programming.shtml
2. https://msdn.microsoft.com/en-us/library/windows/desktop/ms644927(v=vs.85).asp

