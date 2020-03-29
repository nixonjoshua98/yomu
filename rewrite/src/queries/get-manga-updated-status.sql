SELECT
id, title, chapters_read, latest_chapter
FROM
manga
WHERE
status=%s AND latest_chapter > chapters_read;