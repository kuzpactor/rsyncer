from . import items

from typing import List
import subprocess
BASE_CMD = 'rsync'
# Flags:
# -r: recurse
# -l: treat symlinks as symlinks, do not follow them
# -t: preserve mtime
# -D: handle devices and other specials
# -i, --itemize-changes: produce machine-readable summary of changes (twice: this is required to provide a complete list, not just
# changes)
# --delete-after: delete files on receiving end after the transfer was completed
FLAGS = ['-rltDi', '--itemize-changes', '--delete-after']
DRY_RUN = '--dry-run'
EXCLUDE = '--exclude'


class RsyncError(Exception):
    pass


class Rsync:
    cmd_executer = subprocess.run

    def __init__(self, src: str, dst: str, options: list = None, excludes: list = None):
        self.opts = options or []
        self.excludes = None
        if excludes:
            self.excludes = self._excludes(excludes)
        self.src = src
        self.dst = dst

    def _excludes(self, excludes: List[str]) -> List[str]:
        flags = []
        for exclude in excludes:
            flags.append(f'{EXCLUDE}={exclude}')
        return flags

    def prepare(self, dry_run: bool = False) -> List[str]:
        cmdline = [BASE_CMD]
        cmdline.extend(FLAGS)
        if dry_run:
            cmdline.append(DRY_RUN)
        if self.excludes:
            cmdline.extend(self.excludes)
        if self.opts:
            cmdline.extend(self.opts)
        cmdline.extend([self.src, self.dst])
        return cmdline

    def prepare_human(self, *args, **kwargs):
        return ' '.join(self.prepare(*args, **kwargs))

    def start(self, cmdline) -> subprocess.CompletedProcess:
        return subprocess.run(cmdline, capture_output=True)

    def run(self, dry_run: bool = False) -> items.RsyncResults:
        processed = []
        cmdline = self.prepare(dry_run)
        result = self.start(cmdline)
        if result.returncode != 0:
            raise RsyncError('error running "{cmd}": {err}'.format(
                cmd=' '.join(cmdline), err=result.stderr))
        for line in result.stdout.splitlines():
            processed.append(items.Item(line))
        return items.RsyncResults(processed)
