lowdown.cgi
===========
Use this simple CGI script to write your websites/blogs/homepages in Markdown
without relying on bloated static website generators.

Installation
------------
The only dependency is [lowdown](https://kristaps.bsd.lv/lowdown/) but you can
edit [cgi-bin/lowdown.cgi](/lowdown.cgi/tree/cgi-bin/lowdown.cgi) to use any
other markdown-to-html translator. It's that simple lmao.

The script receives __mandatory__ `$MARKDOWN_FILENAME` environment variable and
some optional ones.

### Nginx
This is an example config section for nginx using fcgiwrap.

```nginx
location / {
    root /var/www/htdocs;
    try_files $uri @lowdown;
}

location @lowdown {
    root /var/www;

    set $fn $document_root$document_uri;

    if (-d $fn) {
        set $fn $fn/index.md;
    }
    if (!-f $fn) {
        return 404;
    }
    include             fastcgi_params;
    fastcgi_param       MARKDOWN_FILENAME $fn;
    fastcgi_param       SCRIPT_FILENAME $document_root/cgi-bin/lowdown.cgi;
    fastcgi_pass        unix:/run/fcgiwrap.sock-1;
}
```

Usage
-----
Every directory that has markdown files should also have `header.html` and
`footer.html` in it. Use symlinks if you need the same template in multiple
folders.

See an example directory layout.

    /var/www
    ├── cgi-bin
    │   └── lowdown.cgi
    ├── blog
    │   ├── footer.html -> /var/www/footer.html
    │   ├── header.html
    │   └── index.md
    ├── htdocs
    │   ├── icon.png
    │   └── styles.css
    ├── about.md
    ├── footer.html
    ├── header.html
    └── index.md

### Environment
|      Variable name     | Default |               Description                 |
| ---------------------- | ------- | ----------------------------------------- |
`MARKDOWN_FILENAME`      |   -     | Absolute path to a Markdown file
`LOWDOWN_HTML_SKIP_HTML` | *false* | Do not render in-document HTML at all
`LOWDOWN_HTML_ESCAPE`    | true    | Escapes in-document HTML
`LOWDOWN_HTML_HARD_WRAP` | *false* | Retain line-breaks within paragraphs
`LOWDOWN_HTML_HEAD_IDS`  | true    | Output id attributes for headers
`LOWDOWN_HTML_OWASP`     | *false* | When escaping text, be extra paranoid
`LOWDOWN_HTML_NUM_ENT`   | true    | Convert HTML entities to their numeric form
`LOWDOWN_SMARTY`         | true    | Use smart typography formatting
`LOWDOWN_STANDALONE`     | *false* | Emit a full document instead of a fragment
`LOWDOWN_HILITE`         | *false* | Parse `==highlit==` sequences
`LOWDOWN_TABLES`         | true    | Parse GFM tables
`LOWDOWN_FENCED`         | true    | Parse GFM fenced code blocks
`LOWDOWN_FOOTNOTES`      | true    | Parse MMD style footnotes
`LOWDOWN_AUTOLINK`       | true    | Parse links or link fragments
`LOWDOWN_STRIKE`         | true    | Parse `~~strikethrough~~` sequences
`LOWDOWN_SUPER`          | true    | Parse `super^scripts`
`LOWDOWN_MATH`           | *false* | Parse mathematics equations
`LOWDOWN_CODEINDENT`     | true    | Parse indented content as code blocks
`LOWDOWN_INTEM`          | true    | Parse emphasis within words and links
`LOWDOWN_METADATA`       | true    | Parse in-document MMD metadata
`LOWDOWN_COMMONMARK`     | true    | Parse with CommonMark constraints
`LOWDOWN_DEFLIST`        | true    | Parse PHP single-key extra definition lists
`LOWDOWN_IMG_EXT`        | true    | Parse PHP extra image extended attributes

Contributing
------------
Patches and pull requests are welcome. Please use either [git-send-email(1)][1]
or [git-request-pull(1)][2], addressed to cybertailor@gmail.com.

[1]: https://git-send-email.io/
[2]: https://git-scm.com/docs/git-request-pull

