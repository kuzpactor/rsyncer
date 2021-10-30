from rsyncer import Rsync


def test_prepare():
    src = 'src'
    dst = 'dst'
    excludes = ['excl_a', 'excl_b']
    options = ['-v']

    cmdline = ['rsync', '-rltDi', '--itemize-changes', '--delete-after', '--exclude=excl_a', '--exclude=excl_b', '-v', 'src', 'dst']
    cmdline_dry = [
        'rsync', '-rltDi', '--itemize-changes', '--delete-after',
        '--dry-run', '--exclude=excl_a', '--exclude=excl_b',
        '-v', 'src', 'dst'
    ]

    rs = Rsync(src, dst, options=options, excludes=excludes)
    assert rs.prepare() == cmdline
    assert rs.prepare(dry_run=True) == cmdline_dry

