---
layout: post
title: Limitations in x64dbg
author: torusrxxx
website: https://github.com/torusrxxx
contents: ["Export functions", "Access to features", "Performance"]

---

A year ago I wrote about architecture of x64dbg. Basically, I think it is of good quality for a software with extremely complex requirements, although there's some legacy. For example, if you have experience with other debuggers, you might wonder why label view in x64dbg doesn't update automatically, and doesn't support deleting all labels. Today I will talk about limitations of x64dbg, and possible future enhancements. If you are going to contribute a feature which is listed below, be prepared for additional complexity you might not thought of before.

## Export functions

Adding a feature that interacts with DBG usually means exposing one or more features across the Bridge. This usually means modifications to all three components are necessary, and also less stability of API. Reading some information from DBG is also more difficult. This is why script commands are most preferred and stable interface between DBG and GUI. The original design of using Bridge to separate DBG and GUI, now seems a bit obsolete. The fact that debug thread and GUI thread are different also means certain tasks, such as saving a copy of current dump to compare it later with new dump content, to highlight the changed bytes in red, now requires thread synchronization and is thus harder to code than in single-threaded model.

## Access to features

As mentioned earlier, x64dbg doesn't support many features in references view. It is because, unlike other views, references view is multi-purposed. The references view can be used as labels view, search result view, or variables view. Because the code in references view doesn't have the code to do specific task in given context, tasks such as updating automatically can't be done.

A more general problem exists in other views. In info box below disassembly view, you can see many features are missing, for example, follow in specified dump window. Although the code to accomplish this task already exists, info box has not been updated to use it.

The problem of mixing code for features and container views in the same class has resulted in much code duplication and lack of features in certain views. To solve the problem, x64dbg is moving feature menus into dedicated class files. BreakpointMenu class is the first successful attempt that not only simplifies code, but also brings hardware breakpoint features to other views.

A proposed enhancement to references view is to let code in references view have more insight of current context. I added GuiReferenceAddCommand function to references view. First tried in main window, this function can add a context menu in references view to execute a common task, such as deleting labels. If references view has further information about its context, more tasks can certainly be done. If this information is made visible to all other views in a standard interface, it can be possible to implement tasks that require interaction of references view in other views, such as go to next match. Of course, this will indicate a new enhancement in x64dbg architecture and therefore must be considered carefully.

## Performance

Some users are complaining about why copying a table doesn't copy all content, but only visible part. Some users are disappointed by the fact that dump view doesn't support UTF-16 very well. And perhaps most users have noticed the inability of x64dbg to set a memory breakpoint with specified size. In fact, these operations are somewhat expensive. For example, a memory breakpoint usually decreases stepping performance significantly. x64dbg sets a very high standard for performance, and in order to achieve that, some features are not implemented yet, or disabled and only should be used when necessary.

In my opinion, "performance" not only refers to software performance, but also means the ability for users to complete a task in shorter time. Therefore, expensive operations such as memory breakpoints and Unicode dump, will eventually be implemented if we find a way to implement it efficiently. If an operation is slow and will not help most users