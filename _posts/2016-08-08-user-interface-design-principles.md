---
layout: post
title: User interface design principles
author: torusrxxx
website: http://github.com/torusrxxx
contents: ["Access any feature, anywhere", "Offer to show the most needed data to user", "Guide the user to do the right thing", "Easy to understand and master", "User interface customization is important", "Fast and responsive", "Afterword"]

---

I just committed branch destination preview tooltip recently. When the project leader, Duncan, comes to me to express the users' appreciation, I feel a bit surprised. I just feel it will be needed by our users, and it indeed is. A good user interface design is a key to x64dbg's success. As users are demanding better user interface design, it is useful to share my ideas about what is a good user interface, and how to implement it.

There is significant difference between GUI design for x64dbg and other software. Imagine, what GUI do you wish to see on a software? You might recall your memory with IOS/Android, Google/Facebook/Twitter and other favourite software. They typically feature brief design, colorful text and buttons, large buttons and images to attract users. But come back to x64dbg, things are a bit different. Most issues on [Github](https://github.com/x64dbg/x64dbg/issues) on GUI design are not about ugly buttons and images, but rather about accessing features and data from GUI. If you dislike the dull interface lacking images and color blending, you may still bear it. However when the function is not in the context menu when you need it most, you will probably feel very disappointed. The user expectation for x64dbg is different. They need a really powerful GUI, instead of a beautiful but feature-lacking GUI. So I usually favor feature improvement tasks over visual improvement.

In my opinion, a good graphical user interface has the following features:

## Access any feature, anywhere

A feature without interface in the GUI is not complete. It is very disappointing to find that the most needed feature is inaccessible from the current user interface. To fit the users' demand, we have to add various commands to the context menus everywhere where they are applicable. That's a great amount of work. Disassembly and Dump views have a long list of context menu items, but the same cannot be said on other views. And when we add some new feature, for example, watch view, we have to add that feature to all the relevant menus. Failing to do so results in increased inconvenience.

To add feature in context menu more easily, we have written some very useful utility components. But since we want every feature to appear everywhere where it is applicable, it is still not enough. It will be a good idea to group the features together, so they can be added in groups, to a context menu. For example, we can group all address-related functions, such as breakpoint, dump, watch, etc, together in a package, so we can add all these features in the menu with little code, and also ensure no feature is missing from the context menu.

## Offer to show the most needed data to user

We are always complaining the screen being too small to show the entire program and data. Protected programs tend to access non-local data and execute large routines. It is often the case that only a small portion of the screen is displaying useful things, and most of the program's important states, are hidden in the remote part of memory not shown on the screen. To enlarge the sight of the user, I have introduced many features that can display a non-continuous range of memory, such as watch view, code folding, and recently introduced branch destination previewing. When used properly, they can help concentrate useful information together on the same screen, despite being separated by a large gap in address.

However, there is another thing that makes branch destination preview more success. It displays on mouse over, not on a context menu event. In this way, the tooltip will automatically appear as soon as the user is interested on a particular call instruction. By offering to show the most needed data to user, we save a lot of mouse clicks and keyboard actions. Without branch destination preview, the user would press "Enter", and have a glimpse at the disassembly, then press "-" or "*" to go back to the current location. It is far more complicated and less convenient than mouse over. Also, I provided an option to disable it.

By contrast, code folding requires the user to select a range and then click on the checkbox. Code folding has cost me more effort to implement than branch destination preview, but it is less useful. I don't know how often you fold a section of disassembly, but I think many of you will seldom use it. Duncan added an ability to fold the entire function more easily, but I think that is very misleading (see the comment on [#829](https://github.com/x64dbg/x64dbg/issues/829)) and misses the principle 3. That can probably lead to a further decreased usage of code folding. The proper usage of code folding is in a large loop with lots of unexecuted branches. By folding these inactive branches, you can display more active instructions on screen, thus gain a better overview of the operation of the large loop.

Of course, to implement these features, we have to make lots of non-standard controls. That requires quite an effort. But for better user satisfaction, we are continuously working.

## Guide the user to do the right thing

x64dbg has so many features that sometimes the user might not know which action to take. A good user interface should make the most frequent and useful actions very easy, and make the less used features still accessible. Take exception handling debug commands for example. By gaining experience from Ollydbg, we know it is really time to change something. Skipping first-chance exceptions is almost always the wrong practice in reverse engineering. So Duncan made it the default behaviour to pass these exceptions to the debuggee. In this way, in case an exception is thrown by the debuggee and you don't know what to do, you can just step and see what's happening. But to advanced users, we also make it possible to skip first-chance exceptions.

## Easy to understand and master

Graphical user interface is the reason for which many users choose x64dbg. [GDB](https://sourceware.org/gdb) and [radare](https://github.com/radare/radare2) are great, but they are less popular than [Ollydbg](http://ollydbg.de) and [IDA Pro](https://www.hex-rays.com/products/ida) due to lack of graphical user interface. Good GUI design will greatly reduce the time to learn and master a piece of software for the user, and also increase the comfort of using the software daily. To improve the usability of the GUI of x64dbg, we have hundreds of different icons for the menu items, a rich color design scheme to help the user understand the debuggee better.

A good help system is also important. Although the current help system is better than before, we still receive user complaints about not knowing how to accomplish a certain goal. We need to improve the documentation by adding more examples, as well as adding more tips directly in the GUI to help the user use the software more correctly.

Dissatisfied with English user interface, I added internationalization support for x64dbg and first translated x64dbg to Chinese. The program has since been translated to many languages worldwide, helping its users get the native experience. You are always welcome to contribute to the translations of x64dbg at [Crowdin](https://crowdin.com/project/x64dbg).

## User interface customization is important

The default layout, keyboard and color scheme may not suit everyone's needs. A customizable workspace is better than the best fixed workspace. x64dbg has detachable views and resizable splitters, but if we can introduce a draggable panel, that would be even better.

To accelerate the most common operations, we have customizable key shortcuts for most actions. I contributed the favourites menu to allow further customization. It can bind a shortcut to custom tools and any single command, greatly improves production when some custom actions need to perform repeatedly.

## Fast and responsive

Performance problems often occur in custom graphical user interface designs. We have spent effort on optimizing the performance with drawing, but the CPU usage is still high on the disassembly view. A non-responsive user interface gives the users very bad experience no matter how beautiful it is. We will continue improving the performance of drawing to make it responsive on most computer hardware.

## Afterword

The continuous improvement of x64dbg relies on voluntary work of the community. We sincerely welcome you to contribute to x64dbg. Contributing is very easy. There are many [easy issues](https://github.com/x64dbg/x64dbg/issues?q=is%3Aissue+is%3Aopen+label%3Aeasy) on the issue list. Within a few hours, you will be able to help the users of x64dbg worldwide and have your name on the contributors list. Please check [contribute.x64dbg.com](http://contribute.x64dbg.com) for more information.