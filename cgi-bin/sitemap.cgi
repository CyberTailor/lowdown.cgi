#!/bin/sh
# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2021-2011 Anna <cyber@sysrq.in>
#
# Generates a sitemap.xml file from local markdown files according to the spec.

export HTTP_HOST
cd "${DOCUMENT_ROOT?}" || exit 1

printf "HTTP/1.0 200 OK\r\n"
printf "Content-Type: application/xml; charset=UTF-8\r\n\n"

echo '<?xml version="1.0" encoding="UTF-8"?>'
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
find . -name '*.md' -printf '%P\0' | \
	xargs -0 -I {} "$(dirname -- "${0}")"/sitemap_print_url.sh {} \
	|| exit 1
echo '</urlset>'
