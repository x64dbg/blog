---
layout: post
title: Goodbye Capstone, hello Zydis!
author: athre0z
website: https://zyantific.com
---

Full disclosure: I'm a co-author of Zydis. Opinions certainly biased.

So... this all began about a month ago, when mrexodia came into our Gitter, explaining that he'd like to replace [Capstone](http://www.capstone-engine.org) in x64dbg. He asked whether we had considered writing a Capstone emulation interface on top of Zydis, allowing for drop-in replacement. We weren't opposed to the idea, but after checking out the Capstone interface, decided that full emulation and mapping of all structures, flags and constants would be far from trivial and extremely error prone. This is especially true since nobody in our team had previous experience with Capstone and how it behaves in all the edge cases that might come. So instead, we decided to go on the journey of just contributing the port to x64dbg ourselves!

I checked out the repo and wiki for a guide on how to build the project, located one, followed the instructions and a few minutes later, found myself standing in front of a freshly build x64dbg binary. The port itself was pretty straight-forward. I began by reworking the [Capstone](https://github.com/x64dbg/capstone_wrapper/blob/578d387f3c89692613990f049317194d70be1c14/capstone_wrapper.h#L10) wrapper class to no longer use Capstone, but Zydis instead. The rest of the work mainly consisted of replacing Capstone constants and structure accesses with their Zydis equivalents in places where the debugger and GUI code didn't just use the abstraction, but accessed disassembler structures directly. I really won't bore you with the [details](https://github.com/x64dbg/x64dbg/pull/1730) here, it was mostly search and replace work.

After completing the basic port, I threw my ass into the x64dbg IRC and had a little chit-chat with mrexodia. He suggested that we should copy & paste the old instruction formatter ([CsTokenizer](https://github.com/x64dbg/x64dbg/blob/9a2cb20682e957faaf580039dffa769ee8b58c6e/src/gui/Src/Disassembler/cs_capstone_gui.h#L13), the part of x64dbg that translates the binary instruction structure to the textual representation you see in the GUI) to a second file, using both Capstone and Zydis simultaneously, comparing their outputs. I quickly implemented that idea and started diffing.

Every time I found a collision between Capstone and Zydis, I added a whitelist entry, recompiled and continued diffing, throwing various different binaries and random data at it. This process not only showed up various issues in my ported [CsTokenizer](https://github.com/x64dbg/x64dbg/blob/9a2cb20682e957faaf580039dffa769ee8b58c6e/src/gui/Src/Disassembler/capstone_gui.h#L11), it also found us 3 bugs in Zydis and >20 in Capstone, some of which have open issues created in 2015 connected to them.

So, what did x64dbg gain from the switch?
- Most importantly: significantly more precise disassembly
  - As such, less room for misleading reversers
- Support for more X86 ISA extensions
- Support for many lesser known and undocumented instructions
  - We collected and diffed our data-tables from and against various different sources, such as Intel XED, LLVM and even did a full sweep through the Intel SDM for the sake of checking side-effects of all instructions
- A (minor) boost in performance
  - Zydis is about 50% faster than Capstone
    - 500% faster when decoding to binary structure only, without formatting to human readable text assembly (CS doesn't leave the user a choice right now)
  - However, in a project like x64dbg, that probably only affects the speed of whole module analysis (`CTRL+A`)
- A decrease in binary size
  - Zydis is about &#8531; the size of Capstone (CS X86 only, all features compiled in)
  - Not that anyone would practically have to care these days
    - Nevertheless, low-level people tend to have a thing for small binaries

Finally, aside from all the negativity, I would like to make it clear that we very much appreciate all the work done in Capstone. The project simply has a different focus: it's a great library if you're looking into supporting many different target architectures. Zydis, on the other hand, is focused on supporting X86 — and supporting it well.

If you're interested in checking out our work outside of x64dbg, you can take a look at the [repo](https://github.com/zyantific/zydis).
