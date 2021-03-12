#!/bin/sh
# Copyright (c) 2021 CyberTailor <cybertailor@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the LICENSE file for more details.

bool_arg_from_env () {
    value=$1
    prefix=$2
    name=$3

    case $value in
        [Yy]*|[Tt]*|1)
            ARGS="$ARGS --$prefix-$name"
            ;;
        [Nn]*|[Ff]*|0)
            ARGS="$ARGS --$prefix-no-$name"
            ;;
    esac
}

arg_parse () { bool_arg_from_env "$1" parse "$2" ; }
arg_html  () { bool_arg_from_env "$1" html "$2" ; }
arg_out   () { bool_arg_from_env "$1" out "$2" ; }

MD=$MARKDOWN_FILENAME
cd "$(dirname "$MD")" || exit

arg_html "$LOWDOWN_HTML_SKIP_HTML" skiphtml
arg_html "$LOWDOWN_HTML_ESCAPE"    escapehtml
arg_html "$LOWDOWN_HTML_HARD_WRAP" hardwrap
arg_html "$LOWDOWN_HTML_HEAD_IDS"  head-ids
arg_html "$LOWDOWN_HTML_OWASP"     owasp
arg_html "$LOWDOWN_HTML_NUM_ENT"   num-ent

arg_out "$LOWDOWN_SMARTY"     smarty
arg_out "$LOWDOWN_STANDALONE" standalone

arg_parse "$LOWDOWN_HILITE"     hilite
arg_parse "$LOWDOWN_TABLES"     tables
arg_parse "$LOWDOWN_FENCED"     fenced
arg_parse "$LOWDOWN_FOOTNOTES"  footnotes
arg_parse "$LOWDOWN_AUTOLINK"   autolink
arg_parse "$LOWDOWN_STRIKE"     strike
arg_parse "$LOWDOWN_SUPER"      super
arg_parse "$LOWDOWN_MATH"       math
arg_parse "$LOWDOWN_CODEINDENT" codeindent
arg_parse "$LOWDOWN_INTEM"      intraemph
arg_parse "$LOWDOWN_METADATA"   metadata
arg_parse "$LOWDOWN_COMMONMARK" cmark
arg_parse "$LOWDOWN_DEFLIST"    deflists
arg_parse "$LOWDOWN_IMG_EXT"    img-ext

echo "HTTP/1.0 200 OK"
echo -e "Content-Type: text/html\n"
cat header.html
lowdown --html-no-skiphtml --html-no-owasp $ARGS "$MD"
cat footer.html
