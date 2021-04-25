lowdown.cgi
===========
Use this simple CGI script to write your websites/blogs/homepages in Markdown
without relying on bloated static website generators.

Installation
------------
1. Install [lowdown](https://kristaps.bsd.lv/lowdown)
2. Clone this repository:  
       $ git clone git://sysrq.in:/lowdown.cgi /var/www/mysite

   or add it as a submodule:  
       $ git submodule add git://sysrq.in:/lowdown.cgi  
       $ ln -s ./lowdown.cgi/cgi-bin cgi-bin
3. Setup your web and/or gemini server 

If your server supports FastCGI, it's advised to pass `MARKDOWN_FILENAME`
parameter. Otherwise, lowdown.cgi defaults to `$DOCUMENT_ROOT$DOCUMENT_URI` and
lowdown-gemini.cgi defaults to `$PATH_TRANSLATED`.

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

location /sitemap.xml {
    root /var/www;
    include         fastcgi_params;
    fastcgi_param   SCRIPT_FILENAME $document_root/cgi-bin/sitemap.cgi;
    fastcgi_pass    unix:/run/fcgiwrap.sock-1;
}
```

Usage
-----
Every directory that has markdown files should also have `header.html` and
`footer.html` in it (`header.gmi` and `footer.gmi` for Gemini). Use symlinks if
you need the same template in multiple folders.

See an example directory layout.

    /var/www
    ├── cgi-bin
    │   └── ...
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
    ├── index.md
    └── lowdown_params

### CGI Parameters
```rst
+-------------------|---------|----------------------------------------------+
| Variable name     | Default | Description                                  |
+===================|:=======:|==============================================+
| MARKDOWN_FILENAME |    -    | Absolute path to a Markdown file.            |
| HTML_SKIP_HTML    |  false  | Do not render in-document HTML at all.       |
| HTML_ESCAPE       |  false  | Escapes in-document HTML so that it is       |
|                   |         | rendered as opaque text.                     |
| HTML_HARD_WRAP    |  false  | Retain line-breaks within paragraphs.        |
| HTML_HEAD_IDS     |   true  | Output id attributes for headers.            |
| HTML_OWASP        |  false  | Be extra paranoid in following the OWASP     |
|                   |         | suggestions for which characters to escape.  |
| HTML_NUM_ENT      |   true  | Convert HTML entities to their numeric form. |
| GEMINI_LINK_END   |  false  | Emit the queue of links at the end of the    |
|                   |         | document.                                    |
| GEMINI_LINK_IN    |  false  | Render all links within the flow of text.    |
| GEMINI_LINK_REF   |   true  | Format link labels.                          |
| GEMINI_LINK_ROMAN |  false  | When formatting link labels, use lower-case  |
|                   |         | Roman numerals.                              |
| GEMINI_METADATA   |  false  | Print metadata as the canonicalised key      |
|                   |         | followed by a colon then the value.          |
| SMARTY            |   true  | Use smart typography formatting.             |
| STANDALONE        |  false  | Emit a full document instead of a fragment.  |
| HILITE            |  false  | Parse ==highlit== sequences.                 |
| TABLES            |   true  | Parse GFM tables.                            |
| FENCED            |   true  | Parse GFM fenced code blocks.                |
| FOOTNOTES         |   true  | Parse MMD style footnotes.                   |
| AUTOLINK          |   true  | Parse links or link fragments.               |
| STRIKE            |   true  | Parse ~~strikethrough~~ sequences.           |
| SUPER             |   true  | Parse super^scripts.                         |
| MATH              |  false  | Parse mathematics equations.                 |
| CODEINDENT        |   true  | Parse indented content as code blocks.       |
| INTEM             |   true  | Parse emphasis within words and links.       |
| METADATA          |   true  | Parse in-document MMD metadata.              |
| COMMONMARK        |   true  | Parse with CommonMark constraints.           |
| DEFLIST           |   true  | Parse PHP single-key extra definition lists. |
| IMG_EXT           |   true  | Parse PHP extra image extended attributes.   |
```

Contributing
------------
Patches and pull requests are welcome. Please use either [git-send-email(1)][1]
or [git-request-pull(1)][2], addressed to <cyber@sysrq.in>.

[1]: https://git-send-email.io/
[2]: https://git-scm.com/docs/git-request-pull
