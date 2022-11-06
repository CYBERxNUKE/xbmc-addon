"""
    Plugin for ResolveURL
    Copyright (C) 2022 gujal

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
import base64
import json
import codecs
import hashlib
from resolveurl.lib import helpers, pbkdf2, pyaes
from resolveurl.resolver import ResolveUrl, ResolverError
from resolveurl import common
from six.moves import urllib_parse
import six


class ChillXResolver(ResolveUrl):
    name = 'ChillX'
    domains = ['chillx.top']
    pattern = r'(?://|\.)(chillx\.top)/v/([A-Za-z0-9]+)'

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        referer = urllib_parse.urljoin(web_url, '/')
        headers = {'User-Agent': common.FF_USER_AGENT,
                   'Referer': referer}
        html = self.net.http_GET(web_url, headers=headers).content
        edata = re.search(r"MasterJS\s*=\s*'([^']+)", html)
        if edata:
            edata = base64.b64decode(six.ensure_binary(edata.group(1)))
            edata = json.loads(edata)
            key = '\x34\x56\x71\x45\x33\x23\x4e\x37\x7a\x74\x26\x48\x45\x50\x5e\x61'
            ct = edata.get('ciphertext', False)
            salt = codecs.decode(edata.get('salt'), 'hex')
            iv = codecs.decode(edata.get('iv'), 'hex')
            secret = pbkdf2.PBKDF2(key, salt, 999, hashlib.sha512).read(32)
            decryptor = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(secret, iv))
            ddata = decryptor.feed(base64.b64decode(ct))
            ddata += decryptor.feed()
            r = re.search(r'sources:\s*\[{"file":"([^"]+)', ddata.decode('utf-8'))
            if r:
                headers.update({'Origin': referer[:-1], 'verifypeer': 'false'})
                return r.group(1) + helpers.append_headers(headers)

        raise ResolverError('No playable video found.')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://{host}/v/{media_id}/')
