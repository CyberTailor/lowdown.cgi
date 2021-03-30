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

bool_arg_from_env () {
    value=$1
    prefix=$2
    name=$3

    case $value in
        [Yy]*|[Tt]*|on|ON|1)
            args="$args --$prefix-$name"
            ;;
        [Nn]*|[Ff]*|off|OFF|0)
            args="$args --$prefix-no-$name"
            ;;
    esac
}

arg_parse () { bool_arg_from_env "$1" parse "$2" ; }
arg_html  () { bool_arg_from_env "$1" html "$2" ; }
arg_gmi   () { bool_arg_from_env "$1" gemini "$2" ; }
arg_out   () { bool_arg_from_env "$1" out "$2" ; }

if out_gmi; then
    args="-Tgemini"
    ext=gmi
else
    args="-Thtml --html-no-skiphtml --html-no-owasp --html-no-escapehtml"
    ext=html
fi

get_filename || exit 1
cd "$(dirname "$MD")" || exit 1

arg_html "$HTML_SKIP_HTML" skiphtml
arg_html "$HTML_ESCAPE"    escapehtml
arg_html "$HTML_HARD_WRAP" hardwrap
arg_html "$HTML_HEAD_IDS"  head-ids
arg_html "$HTML_OWASP"     owasp
arg_html "$HTML_NUM_ENT"   num-ent

arg_gmi "$GEMINI_LINK_END"   link-end
arg_gmi "$GEMINI_LINK_ROMAN" link-roman
arg_gmi "$GEMINI_LINK_REF"   link-noref
arg_gmi "$GEMINI_LINK_IN"    link-in
arg_gmi "$GEMINI_METADATA"   metadata

arg_out "$SMARTY"     smarty
arg_out "$STANDALONE" standalone

arg_parse "$HILITE"     hilite
arg_parse "$TABLES"     tables
arg_parse "$FENCED"     fenced
arg_parse "$FOOTNOTES"  footnotes
arg_parse "$AUTOLINK"   autolink
arg_parse "$STRIKE"     strike
arg_parse "$SUPER"      super
arg_parse "$MATH"       math
arg_parse "$CODEINDENT" codeindent
arg_parse "$INTEM"      intraemph
arg_parse "$METADATA"   metadata
arg_parse "$COMMONMARK" cmark
arg_parse "$DEFLIST"    deflists
arg_parse "$IMG_EXT"    img-ext

if out_gmi; then
    printf "20 text/gemini\r\n"
else
    printf "HTTP/1.0 200 OK\r\n"
    printf "Content-Type: text/html\r\n\n"
fi

cat ./header.$ext
lowdown $args "$MD"
cat ./footer.$ext
