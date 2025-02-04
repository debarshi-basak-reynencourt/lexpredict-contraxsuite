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
# -*- coding: utf-8 -*-
# Tika imports
import os
import tempfile
from tika import parser
from tika.parser import _parse
from tika.tika import getRemoteFile, callServer
from typing import Tuple, Dict


__author__ = "ContraxSuite, LLC; LexPredict, LLC"
__copyright__ = "Copyright 2015-2018, ContraxSuite, LLC"
__license__ = "https://github.com/LexPredict/lexpredict-contraxsuite/blob/1.2.2/LICENSE"
__version__ = "1.2.2"
__maintainer__ = "LexPredict, LLC"
__email__ = "support@contraxsuite.com"


class TikaParametrizedParser:
    def __init__(self):
        self.tika_files_path = tempfile.gettempdir()
        self.tika_jar_path = tempfile.gettempdir()
        serverHost = "localhost"
        port = "9998"
        self.server_endpoint = os.getenv(
            'TIKA_SERVER_ENDPOINT', 'http://' + serverHost + ':' + port)

    def parse_default_pdf_ocr(self,
              option: str,
              url_or_path: str,
              server_endpoint: str = None) -> Dict:
        return self.parse(option, url_or_path, server_endpoint,
                          extra_headers={'pdf-parse': 'pdf_ocr'})

    def parse(self,
              option: str,
              url_or_path: str,
              server_endpoint: str = None,
              verbose: int = 0,
              tika_server_jar: str = None,
              response_mime_type: str = 'application/json',
              services: dict = None,
              raw_response: bool = False,
              extra_headers: Dict[str, str] = None) -> Dict:

        services = services if services else \
            {'meta': '/meta', 'text': '/tika', 'all': '/rmeta/text'}
        tika_server_jar = tika_server_jar if tika_server_jar else self.tika_jar_path
        server_endpoint = server_endpoint if server_endpoint else self.server_endpoint

        path, file_type = getRemoteFile(url_or_path, self.tika_files_path)
        service = services.get(option, services['all'])
        if service == '/tika':
            response_mime_type = 'text/plain'
        content_path = self.make_content_disposition_header(path)

        headers = {
            'Accept': response_mime_type,
            'Content-Disposition': content_path
        }
        if extra_headers:
            headers = {**headers, **extra_headers}

        status, response = callServer('put',
                                      server_endpoint,
                                      service,
                                      open(path, 'rb'),
                                      headers,
                                      verbose,
                                      tika_server_jar,
                                      rawResponse=raw_response)

        if file_type == 'remote':
            os.unlink(path)
        return _parse((status, response))

    def make_content_disposition_header(self, fn):
        return 'attachment; filename=%s' % os.path.basename(fn)


parametrized_tika_parser = TikaParametrizedParser()


def tika2text(file_path):
    """
    https://github.com/chrismattmann/tika-python

    Firstly run tika server
    To parse buffer:
    parsed = parser.from_buffer(buffer)

    parsed has ['metadata'] with useful info
    """

    # Call via python-tika API
    parsed = parser.from_file(file_path)
    return parsed['content']
