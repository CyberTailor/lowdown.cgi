#!/bin/sh
# TODO: this script is POSIX-incompatible since it uses `+=` and `export -f`

cd "${DOCUMENT_ROOT?}" || exit 1

print_url () {
    file=$1
    name=$file
    [ "$(basename "$file")" = index.md ] && name="$(dirname "$file")/"
    [ "$file" = index.md ] && name=""
    uri="https://${HTTP_HOST?}/$name"

    result='<url>\n'
    result+="  <loc>$uri</loc>\n"
    result+="  <lastmod>$(date -Iminutes -r "./$file")</lastmod>\n"
    result+='</url>\n'

    printf "$result"
}

export -f print_url

printf "HTTP/1.0 200 OK\r\n"
printf "Content-Type: application/xml; charset=UTF-8\r\n\n"

echo '<?xml version="1.0" encoding="UTF-8"?>'
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
find . -name '*.md' -printf '%P\0' | xargs -0 -I {} sh -c 'print_url "$@"' _ {}
echo '</urlset>'
