"""
Contains output item parser (`--out-format='%i %n%L'` or `--itemize-changes`)
"""
from typing import List


class Item:
    __slots__ = 'path', 'deleted', 'updated', 'created'

    def __init__(self, line: bytes):
        self.deleted = False
        self.updated = False
        self.created = False
        self.path = None
        self._parse(self._decode_line(line))

    def _decode_line(self, line: bytes):
        exc = None
        for encoding in ('utf8', 'cp1251'):
            try:
                return line.decode(encoding)
            except UnicodeDecodeError as err:
                exc = err
        raise exc

    def _parse(self, line: str) -> None:
        if not line:
            raise RuntimeError('got empty line')
        msg, _,path = line.partition(' ')
        self.path = path.strip()
        # * line starts with a human-readable message
        if msg.startswith('*'):
            return self._parse_message(msg)
        # anything else: line is a formatted string
        if msg[0] in ('>', 'c'):  # received from remote ('>') or created ('c')
            self.updated = True
            self.created = True
        # there is also '.', meaning "no changes", but since it all is already false,
        # we skip working on it

    def _parse_message(self, msg: str) -> None:
        if msg[1:] == 'deleting':
            self.deleted = True


class RsyncResults:
    def __init__(self, file_list: List[Item]):
        self._items = file_list
        self.total = len(self._items)
        self.deleted = self._attr_count('deleted')
        self.updated = self._attr_count('updated')
        self.created = self._attr_count('created')
        self.unchanged = self.total - self.deleted - self.updated

    def _attr_count(self, attr: str) -> int:
        number = 0
        for item in self._items:
            if getattr(item, attr):
                number += 1
        return number