---
layout: post
title: Analyzing memory access patterns is easier than ever
author: torusrxxx
website: https://github.com/torusrxxx
contents: ["Analyzing memory access patterns is easier than ever", "Example: finding the write that caused a crash", "Example: finding data that only existed during tracing"]

---
## Analyzing memory access patterns is easier than ever

Analyzing memory access is an essential part of reverse engineering. There is no magical way to automatically find where input values are used by a program.
 Static analysis methods, for example searching for constants, work only in limited cases. Hardware breakpoints and memory breakpoints are more common, but they
 also have limitations. There are only four hardware breakpoints, and memory breakpoints can only be placed on an entire page. Tracing records
 every memory access, but the trace view lacked dump and stack windows and convenient tools to analyze and visualize the data.
 The missing dump and stack windows were severe limitations for memory access pattern analysis.
 The memory access information was scattered across instruction execution records, which made it difficult to inspect.

The missing dump and stack windows in the trace view are supported now. They work like the familiar dump and stack windows in the CPU view.
 Their contents are derived from the trace recording. Whenever an instruction is selected in the trace view, the dump and stack windows
 are updated to show memory just before that instruction is executed. You can visualize how the program accesses memory by observing how the dump changes as you select
 the previous or next instruction. Hexadecimal and floating point formats are supported, so you can visualize and copy intermediate results in a numerical calculation.
 Selecting the "Xref" menu action (default hotkey "X") in the context menu searches for all accesses to the selected address, so you can quickly move to wherever the selected variable is read or written.

The screenshots below use two small example programs. Download [trace-memory.zip]({{ site.baseurl }}/public/files/trace-memory.zip), which contains the source code, prebuilt executables, PDB files, and build instructions. The source files are also available as a text-only [gist](https://gist.github.com/mrexodia/42c1fa6eb21b705a007c612adbbda7c8). The executables are compiled with ASLR disabled so addresses are stable across runs.

### Example: finding the write that caused a crash

In `trace_overflow`, a fixed-size buffer is copied without bounds checking. The copy first overwrites a greeting string and then overwrites a function pointer with `43 43 43 43 43 43 43 43` (`CCCCCCCC`). When the program later calls that function pointer, it crashes. Trace until the access violation, open the trace dump at the function pointer address, and use the Xref action. The last write before the crash points to the byte-copy instruction that crossed the end of the buffer; the later read is the indirect call through the corrupted pointer.

![Crash at the indirect call]({{ site.baseurl }}/public/images/crash-indirect-call.png)

![Trace xref]({{ site.baseurl }}/public/images/trace-xref.png)

### Example: finding data that only existed during tracing

In `trace_rc4`, the expected serial is stored encrypted, decrypted into a stack buffer, compared with the user input, and wiped. The plaintext string is absent from the executable and gone from live memory after the check. Trace pattern search can still find it because the bytes existed during the recording. Searching the trace dump for `78 36 34 64 62 67 7B` finds the ASCII prefix `x64dbg{`, and Xref on one byte of the buffer shows the decrypt write, the compare read, and the wipe write.

![trace pattern search]({{ site.baseurl }}/public/images/pattern-found.png)

![flag found]({{ site.baseurl }}/public/images/flag-found.png)

Internally, the debugger maintains a search index. The search index contains information for each byte accessed in the trace recording.
 This allows instant access to memory content anywhere in the trace recording by using indexed search rather than scanning. The memory used to store the search index,
 and the CPU time used to load it, can become noticeable in larger trace files. Therefore, the trace dump is not loaded by default. The trace dump can be loaded by clicking the "Load dump"
 button at the bottom, setting the option "Automatically load dump in trace view", or using a feature that requires the search index. The debugger may stutter when the search index is being loaded.
 To reduce stuttering, the search index is only loaded up to the selected instruction. This makes all data previously accessed in the trace recording visible in the
 dump, but data accessed after the selected instruction can appear as zeros. When you select the next instruction and then come back, some memory addresses no longer contain zeros.
 This is normal because those memory locations were not accessed by previous instructions, so their contents are unknown to the trace. The same also happens when recording a trace.
 The dump and stack views in the trace do not update when more instructions are traced. To see the memory dump at the end of tracing, select the last instruction, and the dump and stack views
 will be loaded correctly. Once the search index is loaded to a certain instruction, selecting any previous instruction no longer needs to load it again, so the debugger will not stutter.

The search index is used for both the memory dump and faster searches. The "Xref" menu action uses indexed search to search for memory accesses, which is a convenient way to navigate the trace.
 When used for the first time, the search index is automatically loaded to the end of the trace, so it may be slow the first time. It is also a quick way to force the debugger
 to load the search index fully. Further usage no longer needs to load it again. You can also go to a specific instruction by address. Technically, this is the same as finding memory accesses to the address due to
 instruction execution. When the destination address is executed more than once, the Xref dialog appears, and you can select one iteration of a loop.

The "find pattern" command available in the dump is another powerful tool. This command searches for data in the trace recording.
 Compared with searching directly in memory, this command in the trace view finds the pattern anywhere in the trace, and works even when the pattern is moved or overwritten.
 The user does not need to pause at a point where the pattern is directly visible in memory. If the pattern ever exists while tracing, and is being used, it will be found. It only finds what is in the trace, so irrelevant matches are fewer.
 The start index and end index shown in the result list indicate the instruction indexes where the pattern first and last appeared in memory.
 The instruction that writes the pattern to memory is also shown in the results.

As part of this trace view update, the trace view now uses a tabbed design. It is now possible to open multiple trace files simultaneously.

This was a large project for me as an x64dbg maintainer. The interface is simple, but the implementation is complex and the feature set is unusual among debuggers.
 Future improvements are planned. If you find a bug, please report it to the x64dbg developers via http://report.x64dbg.com. Contributions are welcome.
