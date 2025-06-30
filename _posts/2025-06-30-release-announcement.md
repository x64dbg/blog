---
layout: post
title: 'Type System and Modernization'
author: mrexodia
website: https://mrexodia.re
contents: ["✨ Revamped Type System", "💻 AVX-512 and Half-Float Support", "⚡ Small Changes, Big Impact", "🚀 Modern Tooling and a New Release Cycle", "🔮 Looking Ahead: A Cross-Platform Future", "🤝 Community", "❤️ Sponsors"]

---

We're excited to announce a major [new release of x64dbg](https://x64dbg.com), the open-source user mode debugger for Windows. For those new to the project, x64dbg is designed to make reverse engineering and malware analysis faster and more intuitive. This release marks a significant step forward, overhauling our core type system and modernizing our entire toolchain to bring you a more powerful and stable debugging experience.

## ✨ Revamped Type System
In previous versions, analyzing data structures was a tedious, manual process and many features were not supported. This release adds support for bitfields, enums and anonymous types, which allows all types in the Windows SDK to be represented and displayed.

The [ManyTypes](https://github.com/notpidgey/ManyTypes) plugin by @notpidgey (who also drove this revamp) allows you to import C header files and see the results directly in x64dbg. While we plan to streamline this workflow even further in future updates, this is a huge leap in making data inspection easier.

This isn't just about convenience; it's about speed. We've introduced **drastic performance improvements** to the struct widget, so you can now browse deeply nested pointers and large data structures without the lag.

![](https://github.com/user-attachments/assets/973d101c-5dab-4f66-ac10-fc68873d52f0)

We’ve also added a host of quality-of-life improvements:
- **Interactive type selection**: While selecting the type you will instantly see what the data looks like, enabling a more interactive workflow.
- **Smarter Displays:** Character arrays are now automatically rendered as strings, saving you an extra step.
- **Better Integration:** You can now invoke the "Display type" action directly from the register and stack views, making it easier than ever to inspect data on the fly.

## 💻 AVX-512 and Half-Float Support
This release introduces support for the latest CPU instruction sets, ensuring you can analyze even the most modern applications.
- **AVX-512 Support:** You now have the power to debug and analyze code that leverages the AVX-512 instruction set, a critical feature for high-performance computing and complex malware.
- **Half-Float Support:** We've added support for 16-bit half-precision floating-point numbers in the dump, a feature especially useful when reversing graphics applications or machine learning models.

## ⚡ Small Changes, Big Impact
Sometimes it’s the little things that count. Based on your feedback, we've added several small but mighty workflow enhancements:
- **Copy Graph Image:** You can now copy the function graph directly to your clipboard, making it effortless to share your findings or add visuals to your reports.
- **Copy Calling Convention Arguments:** A new context menu option lets you quickly copy function arguments, streamlining the process of reconstructing code or documenting function calls.
- **Focus on Window in Handles View:** You can now bring a target window to the foreground directly from the handles view, which is incredibly useful for UI-heavy debugging.
- **Revamped Launcher**: The launcher now has checkboxes and an uninstall option.

![image](https://github.com/user-attachments/assets/2557aa1c-d5dc-416d-9825-c17b05ce9f33) ![image](https://github.com/user-attachments/assets/1a556c0b-85ac-49a4-a5a8-307695585297)

## 🚀 Modern Tooling and a New Release Cycle
We've completed a monumental migration of our entire build system to **Visual Studio 2022 and CMake**. This massive undertaking provides a more stable foundation, makes it easier for new developers to contribute, and accelerates the pace of future improvements. The [compilation instructions](https://github.com/x64dbg/x64dbg/wiki/Compiling-the-whole-project) were cut down from _13 steps to a single one._

There has also been movement on a _headless version of x64dbg_. The main focus for now is automated testing, but eventually it will be expanded to allow [headless automations](https://x64dbg.com/blog/2025/03/04/analysis-at-scale-with-x64dbg-automate.html).

Starting with this release, we will be using **[CalVer](https://calver.org)** (Calendar Versioning) with proper GitHub releases and tags. This will keep our releases more organized and allow package managers and users to reference specific versions more easily. Additionally Windows XP is [no longer supported](https://github.com/x64dbg/x64dbg/wiki/Transition) and for Windows 7/8.1 you will get an unskippable deprecation warning:

![image](https://github.com/user-attachments/assets/d692924b-8647-4508-bbc5-12ffcc958285)

## 🔮 Looking Ahead: A Cross-Platform Future
We're excited to share a glimpse into our experimental [`cross-platform`](https://github.com/x64dbg/x64dbg/pull/3224) branch. This is our testbed for separating core GUI widgets into a reusable library, with the goal of bringing x64dbg's powerful tools to all major platforms (Windows, macOS, and Linux).

Current experimental tools include:
- A simple **hex viewer** that uses the [ImHex Pattern Language](https://github.com/WerWolv/PatternLanguage) to visualize data structures.
- A **minidump viewer** to browse `.dmp` files on any platform.
- A **remote table** tool that showcases fetching data over a high-latency network.

![image](https://github.com/user-attachments/assets/eb3b8dfd-ebf4-454b-ac83-d4f8741b364b)

These tools are still in early development and not part of the release, but they represent a critical step toward a more versatile and platform-independent future for our components.

## 🤝 Community
x64dbg is a community-driven project, and this release would not have been possible without the incredible work of our contributors. A huge thank you to everyone who contributed code, reported bugs, and helped shape this release ❤️

We recently revamped the Discord community, which you can join below:

[![](https://dcbadge.limes.pink/api/server/PRfRYbt)](https://discord.x64dbg.com)

You can also get the `XDBG` tag after joining the server:

![image](https://github.com/user-attachments/assets/a428369d-fff4-47ec-877a-9471961743d1)

Other platforms are synchronized with the `#general` channel:

[![Slack](https://img.shields.io/badge/chat-on%20Slack-red.svg)](https://slack.x64dbg.com) [![Gitter](https://img.shields.io/badge/chat-on%20Gitter-lightseagreen.svg)](https://gitter.im/x64dbg/x64dbg) [![Matrix](https://img.shields.io/badge/chat-on%20Matrix-yellowgreen.svg)](https://riot.im/app/#/room/#x64dbg:matrix.org) [![IRC](https://img.shields.io/badge/chat-on%20IRC-purple.svg)](https://web.libera.chat/#x64dbg)

## ❤️ Sponsors
This project is partially made possible by the generous support of sponsors. We would like to give a special shout out to the following sponsors who donated at the highest tier since the last release:
- 🥇 [**FLOSS/fund**](https://floss.fund) - Funding for Free and Open Source projects.
- [**SEKTOR7 Institute**](https://institute.sektor7.net/)
- [**Back Engineering**](https://back.engineering)
- [**aslrnk**](https://aslr.ac)
- [**RedOps**](https://redops.at/en)

Also many thanks to the other active sponsors: @adam-the, @verdeckt, @emesare, @daaximus, @stevemk14ebr, @as0ni, @sedrakpc, @Dan0xE, @Invoke-RE, @leandrofroes, @shu-tom, @buzzer-re, @expend20, @crudd, @clayne, @fr0zenbag, @merces, @dzzie

**If you find x64dbg valuable in your work, please consider [becoming a sponsor](https://github.com/sponsors/mrexodia?metadata_source=releases). Your support directly funds development and helps us continue to build the future of debugging.** For companies we also offer custom services depending on the level of sponsorship, please [reach out](mailto:contact@x64dbg.com) for more details!
