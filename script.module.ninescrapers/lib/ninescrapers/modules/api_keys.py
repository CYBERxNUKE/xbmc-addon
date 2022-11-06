# -*- coding: utf-8 -*-

import base64, sys
from six import ensure_text


def chk():
    return True;

tmdb_key = ensure_text(base64.b64decode(b'NTY5ZTI1ZTA0NDBjODQyZDdhY2YxNjdjNWE2MDM0NmM=')) if chk() else ''
tvdb_key = ensure_text(base64.b64decode(b'MzYzYzFmYmQwYzIxNDk1ODAzMzFiYTRmOGU5NDAwZWM=')) if chk() else ''
omdb_key = ensure_text(base64.b64decode(b'Yzc5ODQxNzA=')) if chk() else ''
fanarttv_key = ensure_text(base64.b64decode(b'YzI1MGI5NDgxM2Q0MzBiMjRjYzgwMTZhYjA3MWQzOWM=')) if chk() else ''
yt_key = ensure_text(base64.b64decode(b'QUl6YVN5QU15OW82WWpZZ1NkVlJzSUtXNFNHN1Fkelh3V0ZmLWxR')) if chk() else ''
trakt_client_id = ensure_text(base64.b64decode(b'NWFjOTI4YjAzYTI5ZDBlYzkzMjI1MDZmMTAwZjE5MmI2Mzc5YmQ3YTI2YTFhNzJjNTczY2EyMDI4Mjk4YTQyZg==')) if chk() else ''
trakt_secret = ensure_text(base64.b64decode(b'MTBmYzU5OTEzZjA5ZjMyNWZjZjdiN2NjZDhiY2FhYjkwYzgwODEyYTIwMzg4MzA4YmQ0YzFlNGQyMDRlYjZhNg==')) if chk() else ''
orion_key = ensure_text(base64.b64decode(b'SlFITEFFSlk4RjZERlZETVJMS0tUN1JHN0ZQTkdWS0U==')) if chk() else ''
