#!/bin/sh
# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2021-2011 Anna <cyber@sysrq.in>
#
# Processes a single find(1) result and prints a <url> sitemap entry.
# Usage: HTTP_HOST=example.com ./sitemap_print_url.sh blog/index.md

DATE="date"
command -v gdate && \
	DATE="gdate"

file=${1}
name=${file}
[ "$(basename "${file}")" = index.md ] && name="$(dirname "${file}")/"
[ "${file}" = index.md ] && name=""
uri="https://${HTTP_HOST?}/${name}"

result="<url>\n"
result="${result}  <loc>${uri}</loc>\n"
result="${result}  <lastmod>$(${DATE} -Iminutes -r "./${file}")</lastmod>\n"
result="${result}</url>\n"

printf "${result}"
