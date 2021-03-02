#!/bin/sh
# Copyright (c) 2021 CyberTailor <cybertailor@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the LICENSE file for more details.

MD=$MARKDOWN_FILENAME
cd "$(dirname "$MD")" || exit

echo "HTTP/1.0 200 OK"
echo -e "Content-Type: text/html\n"
cat header.html
lowdown --html-no-skiphtml --html-no-owasp "$MD"
cat footer.html

