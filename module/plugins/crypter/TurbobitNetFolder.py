# -*- coding: utf-8 -*-

############################################################################
# This program is free software: you can redistribute it and/or modify     #
# it under the terms of the GNU Affero General Public License as           #
# published by the Free Software Foundation, either version 3 of the       #
# License, or (at your option) any later version.                          #
#                                                                          #
# This program is distributed in the hope that it will be useful,          #
# but WITHOUT ANY WARRANTY; without even the implied warranty of           #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
# GNU Affero General Public License for more details.                      #
#                                                                          #
# You should have received a copy of the GNU Affero General Public License #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
############################################################################

from math import ceil
import re

from module.plugins.internal.SimpleCrypter import SimpleCrypter
from module.common.json_layer import json_loads


def format_links(fid):
    return 'http://turbobit.net/%s.html' % fid


class TurbobitNetFolder(SimpleCrypter):
    __name__ = "TurbobitNetFolder"
    __type__ = "crypter"
    __pattern__ = r"http://(?:www\.)?turbobit\.net/download/folder/(?P<ID>\w+)"
    __version__ = "0.02"
    __description__ = """Turbobit.net Folder Plugin"""
    __author_name__ = ("stickell", "Walter Purcaro")
    __author_mail__ = ("l.stickell@yahoo.it", "vuolter@gmail.com")

    TITLE_PATTERN = r"src='/js/lib/grid/icon/folder.png'> <span>(?P<title>.+?)</span>"

    def _getLinks(self, id, page=1):
        gridFile = self.load('http://turbobit.net/downloadfolder/gridFile',
                             get={'rootId': id, 'rows': 200, 'page': page}, decode=True)
        grid = json_loads(gridFile)

        pages = int(ceil(grid["records"] / 200.0))

        for i in grid['rows']:
            yield i['id']

        if page < pages:
            self._getLinks(id, page + 1)

    def getLinks(self):
        folder_id = re.match(self.__pattern__, self.pyfile.url).group('ID')
        return map(format_links, self._getLinks(folder_id))
