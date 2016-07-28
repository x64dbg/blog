---
layout: post
title: Control flow graph
author: mrexodia
website: http://mrexodia.cf
---

Today's post will be about control flow analysis and graphing, read on if you are interested!

**This blog is still looking for writers!** See [here](https://github.com/x64dbg/blog) for more information...

## Introduction

At the moment [x64dbg](http://x64dbg.com) is only capable of showing disassembly in a linear fashion. Control flow can be somewhat inferred from jump arrows, but this can be a tedious and overwhelming process. This is one of the reasons we are interested in representing disassembly as a control flow graph. Another good reason is that x86 instructions can overlap and sometimes linear disassembly cannot show the full picture.

## Analysis

The first thing to look at is analysis of a function. We represent the function as a directed graph. The graph nodes are so-called *basic blocks* and the graph's edges (arrows) are jumps in the disassembly. The function we will be looking at is shown below:

[![function1]({{ site.baseurl }}/public/images/blog27072916-function1.png)]({{ site.baseurl }}/public/images/blog27072916-function1.png)

In this case a basic block is a block of instructions, that *do not alter the control flow within the current function*. We (falsely) assume that `call` instructions always return to the instruction after said `call` instruction so the control flow of the block is not interrupted. Additionally a basic block ends at a `ret` instruction (since that marks the end of the current function).

Since the function is (implicitly) represented as a graph we can use [breadth first search (BFS)](https://en.wikipedia.org/wiki/Breadth-first_search) to traverse it. The algorithm implemented here combines the BFS with building the graph, which makes it quite compact and easy to understand (pseudocode):

```
analyze(entryPoint):
    graph = new Graph(entryPoint)
    queue = new Queue()
    visited = new Set()
    
    # Start at the entry point
    queue.enqueue(graph.entryPoint)
    
    # Traverse the graph
    while !queue.empty():
        # Check if we already visited this node
        start = queue.dequeue()
        if !start || visited.contains(start):
            continue
        visited.insert(start)
        
        # Create a new node
        node = new Node()
        node.start = node.end = start
        
        # Disassemble the current basic block
        while true:
            instr = disassemble(node.end)
            if isBranch(instr) || isRet(instr):
                # Enqueue 
                queue.enqueue(brtrue(instr))
                queue.enqueue(brfalse(instr))
                graph.AddNode(node)
                break
            node.end += instr.size
```

The functions `brtrue` and `brfalse` return the addresses of the destination blocks or zero. After running this analysis on the function the result looks something like this:

[![graph1]({{ site.baseurl }}/public/images/blog27072916-graph1.png)]({{ site.baseurl }}/public/images/blog27072916-graph1.png)

At the moment analysis is not working correctly. The analysis will have overlapping blocks if there are branches inside an existing block. It looks something like this (function is totally made up, don't read too much into it):

[![graph2]({{ site.baseurl }}/public/images/blog27072916-graph2.png)]({{ site.baseurl }}/public/images/blog27072916-graph2.png)

The first block should be split and a second pass easily solves this problem:

```
foreach node in nodes:
    addr = node.start
    size = disassemble(addr).size
    if graph.contains(addr + size):
        node.end = addr
        node.brtrue = addr + size
        node.brfalse = 0
        break
    addr += size
```

This splits the block correctly and inserts an extra edge between the nodes:

[![graph3]({{ site.baseurl }}/public/images/blog27072916-graph3.png)]({{ site.baseurl }}/public/images/blog27072916-graph3.png)

Now there are some remaining problems, like overlapping instructions, but those are fine the way it is in my opinion:

[![graph4]({{ site.baseurl }}/public/images/blog27072916-graph4.png)]({{ site.baseurl }}/public/images/blog27072916-graph4.png)

You can find the full code [here](https://github.com/x64dbg/x64dbg/blob/47f044eeb1ced86a9f191038b8991fac88b71764/src/dbg/analysis/recursiveanalysis.cpp#L58) if you are interested in the details.

## GUI

Now the next part was showing the function graph in the GUI, there was quite an effort [before](https://github.com/x64dbg/x64dbg/tree/graph_ogfd_new) doing this using [OGDF](http://www.ogdf.net) and someone mentioned the [Binary Ninja Prototype](https://github.com/Vector35/deprecated-binaryninja-python) so I decided to port that instead.

After about 7 hours of struggling with Python I ported the code and [people seem to like the results](https://twitter.com/GelosSnake/status/758644519189540864) :)

The details of the layout algorithm are beyond me and if you have any fixes, feel free to create a pull request!

Duncan