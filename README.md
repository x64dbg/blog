# blog

Blog for [x64dbg](http://x64dbg.com). Feel free to send a pull request if you want to post something [here](http://blog.x64dbg.com)!

## Writing a post

Writing a new post for the [official x64dbg blog](http://blog.x64dbg.com) is very easy. It is basically [Markdown](https://simplemde.com/markdown-guide) with some extra setup to make [Jekyll](https://jekyllrb.com) render the post nicely.

Create a new file called `DD-MM-YYYY-Your-post-title.md` in the `_posts` directory and start with the following setup:

```
---
layout: post
title: Your post title!
author: John Doe
website: http://johndoe.me
---
```

After that write your post contents with Markdown. If you don't want to be attributed use `author: Anonymous` and `website: http://x64dbg.com`. These fields are **required** so keep that in mind.

Once you completed writing your post, send a pull request and it will be reviewed and finally added to the blog!
