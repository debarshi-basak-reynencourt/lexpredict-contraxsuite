"""
    Copyright (C) 2017, ContraxSuite, LLC

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    You can also be released from the requirements of the license by purchasing
    a commercial license from ContraxSuite, LLC. Buying such a license is
    mandatory as soon as you develop commercial activities involving ContraxSuite
    software without disclosing the source code of your own applications.  These
    activities include: offering paid services to customers as an ASP or "cloud"
    provider, processing documents on the fly in a web application,
    or shipping ContraxSuite within a closed source product.
"""
import os
import tempfile
from contextlib import contextmanager
from typing import List
from typing import Optional
from urllib.parse import quote

import requests

from .file_access import FileAccessHandler


class NginxHttpFileAccess(FileAccessHandler):
    def __init__(self, root_url: str):
        self.root_url = root_url

    def _list_impl(self, file_list: List[str], path: str):
        path = path.lstrip('/')
        full_path = os.path.join(
            self.root_url,
            quote(path) or '')
        r = requests.get(full_path)
        if r.status_code != 200:
            if path and not path.endswith('/'):
                self._list_impl(file_list, path + '/')
            return
        path = path.strip('/')

        try:
            dir_json = r.json()
            for entry in dir_json:
                if entry['type'] == 'file':
                    file_list.append(
                        os.path.join(
                            path,
                            entry['name'] if path else entry['name']))
                else:
                    self._list_impl(file_list, path + '/' + entry['name'])
        except ValueError or KeyError:
            file_list.append(path)

    def list(self, rel_file_path: str = ''):
        file_list = []
        self._list_impl(file_list, rel_file_path)
        return file_list

    @contextmanager
    def get_as_local_fn(self, rel_file_path: str):
        if rel_file_path.startswith('/'):
            rel_file_path = rel_file_path[1]
        url = self.root_url + '/' + quote(rel_file_path)
        r = requests.get(url, stream=True)
        _, ext = os.path.splitext(rel_file_path)
        _fd, fn = tempfile.mkstemp(suffix=ext)
        try:
            with open(fn, 'bw') as f:
                for chunk in r.iter_content(chunk_size=4096):
                    if chunk:
                        f.write(chunk)
            r.close()
            yield fn, rel_file_path
        finally:
            r.close()
            os.remove(fn)

    def read(self, rel_file_path: str) -> Optional[bytes]:
        if rel_file_path.startswith('/'):
            rel_file_path = rel_file_path[1]
        url = self.root_url + '/' + quote(rel_file_path)
        r = requests.get(url, stream=True)
        if r.status_code == 404:
            return None
        elif r.status_code != 200:
            raise RuntimeError('Unable to read file: {0}. Http status code: {1}. Http message: {2}'
                               .format(rel_file_path, r.status_code, r.text))
        try:
            return r.content
        finally:
            r.close()

    def __str__(self):
        return 'NginxFileAccess: {0}'.format(self.root_url)
