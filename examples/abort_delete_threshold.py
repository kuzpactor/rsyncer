import logging
from rsyncer import Rsync
import click

DELETED_SAFE_THRESH = 0.1  # Percentage from all files


@click.command()
@click.option('--rsh', help='transport shell to use and its options')
@click.option('--exclude', help='exclude pattern', multiple=True)
@click.argument('src')
@click.argument('dst')
def main(rsh, exclude, src, dst) -> None:
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s',
        level=logging.DEBUG)
    logging.debug('backup starting')
    rs_obj = Rsync(src, dst, options=[f'--rsh={rsh}'], excludes=exclude)
    logging.debug('execute: %s', rs_obj.prepare_human(dry_run=True))
    files = rs_obj.run(dry_run=True)

    for stat in ('deleted', 'updated', 'unchanged'):
        stat_perc = getattr(files, stat) / files.total
        logging.debug(f'files {stat} percentage: %s%%', stat_perc * 100)
    thresh = files.deleted / files.total
    if thresh >= DELETED_SAFE_THRESH:
        raise RuntimeError(f'Safe threshold for deletions exceeded: {thresh} >= {DELETED_SAFE_THRESH}')
    logging.debug('commencing run...')
    rs_obj.run()
    logging.debug('run finished')


if __name__ == '__main__':
    main()
