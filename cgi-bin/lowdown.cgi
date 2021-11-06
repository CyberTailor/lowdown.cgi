#!/bin/sh
# Copyright (c) 2021 CyberTailor <cybertailor@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the LICENSE file for more details.

out_gmi () {
    [ "$(basename "$0")" = lowdown-gemini.cgi ] && return 0 || return 1
}

get_filename () {
    MD=$MARKDOWN_FILENAME
    [ "$MD" ] && return

    if out_gmi; then
        MD="${PATH_TRANSLATED?}"
    else
        MD="${DOCUMENT_ROOT?}${DOCUMENT_URI?}"
    fi
}

if out_gmi; then
    args="-Tgemini ${LOWDOWN_OPTS}"
    ext=gmi
else
    args="-Thtml --html-no-skiphtml --html-no-owasp --html-no-escapehtml ${LOWDOWN_OPTS}"
    ext=html
fi

get_filename || exit 1
cd "$(dirname "$MD")" || exit 1

if out_gmi; then
    printf "20 text/gemini\r\n"
else
    printf "HTTP/1.0 200 OK\r\n"
    printf "Content-Type: text/html\r\n\n"
fi

cat ./header.$ext
lowdown $args "$MD"
cat ./footer.$ext
