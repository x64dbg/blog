---
layout: post
title: Analysis of memory access pattern has never been easier as now
author: torusrxxx
website: https://github.com/torusrxxx
contents: []

---
## Analysis of memory access pattern has never been easier as now

Analyzing memory access is an essential part of reverse engineering. There's no magical way to automatically find out where the input values are used by the program.
 Static analysis methods, for example, search for constant, only work in very limited cases. More often, hardware breakpoints and memory breakpoints are used. But these
 methods also have limitation. There are only 4 hardware breakpoints, and memory breakpoints can only be placed on an entire page. Only tracing allows recording
 full information of every memory access. But there was no dump, no stack in the trace view, and no convenient tools to analyze and visualize the rich information in the trace.
 The missing dump and stack windows were severe limitations to the usefulness of tracing in memory access pattern analysis.
 This is because all the memory access information are scattered in each instruction execution record, which makes it difficult to access.

I'm pleased to announce that the missing dump and stack windows in the trace view, are supported now. The new dump and stack windows in the trace view are like familiar dump and stack windows
 in the CPU view. The content of them are derived from the trace recording. Whenever an instruction is selected in the trace view, the new dump and stack windows in the trace view
 are updated to show the memory dump just before the instruction is executed. You can easily visualize how the program accesses memory, by observing how the memory dump change as you select
 the previous or next instruction. Not just hexadecimal format is supported. You can also use a floating point number format in the dump to visualize and copy intermediate results in a numerical calculation.
 Selecting the "Xref" menu action (default hotkey "X") in the context menu will search for all accesses to the selected address, so you can quickly move to wherever the selected variable is read or written.

In its core, a search index is maintained by the debugger. The search index contains information for each byte accessed in the trace recording.
 This allows instant access to memory content anywhere at any time in the trace recording, by using fast indexed search rather than scanning. The memory used to store the search index,
 and the CPU time used to load it, can become noticeable in larger trace files. Therefore, the trace dump is not loaded by default. The trace dump can be loaded by clicking the "Load dump"
 button at the bottom, setting the option "Automatically load dump in trace view", or using a feature that requires the search index. The debugger may stutter when the search index is being loaded.
 To reduce debugger stuttering time, the search index is only loaded up to the selected instruction. This will make all data previously accessed in the trace recording visible in the
 dump, but data accessed after the selected instruction could appear to be zeros. When you select the next instruction and then come back, some memory addresses no longer contain zeros.
 This is a normal situation, because those memory locations are not accessed by all previous instructions, it doesn't matter what data are stored there. The same also happens when recording a trace.
 The dump and stack view in the trace don't update when more instructions are traced. To see the memory dump at the end of tracing, you need to select the last instruction, then the content of dump and stack view
 will be properly loaded. Once the search index is loaded to a certain instruction, selecting any previous instruction no longer needs to load again, so the debugger will not be stuttering.

The search index is not only used to show memory dump. It can also be used to accelerate searching. The "Xref" menu action uses indexed search to search for memory accesses, which is a very convenient way to navigate the trace.
 However, when used for the first time, the search index is automatically loaded to the end of the trace. Therefore, it may appear to be slow for the first time. It is also a quick way to force the debugger
 to load search index fully. Further usage no longer needs to load again. You can also go to specific instruction by address. Technically, this is the same as finding memory accesses to the address due to
 instruction execution. When the destination address is executed more than once, the Xref dialog appears, and you will be able to select one iteration of a loop.

The "find pattern" command available in the dump, is another powerful tool. This command can be used to search for data in the trace recording.
 Compared with searching directly in the memory, this command in the trace view finds the pattern anywhere in the trace, and works even in the cases where the pattern is moved or overwritten.
 The user don't need to first pause at a point where the pattern is directly visible in memory - if the pattern ever exists while tracing, and is being used, then it will be found. It only finds what is in the trace, so irrelavant matches are also much fewer.
 The start index and end index shown in the result list, indicates the index of instruction when the pattern first and last appeared in memory.
 The instruction that writes the pattern in memory is also shown in the results.

As part of trace view feature update, trace view now uses a tabbed design. It's now possible to open multiple trace files simultaneously.

It's a big project for me as an x64dbg maintainer. These brand-new features, not being supported by other debuggers, are not so simple as its very intuitive user interface. I hope these new features are useful to the users.
 There will be future improvements to this new feature. If you find a bug, please report to x64dbg developers via http://report.x64dbg.com. We welcome contributions to the project. Without
 open-source contributors, x64dbg would not be the industry-leading debugger that all of us enjoy!
