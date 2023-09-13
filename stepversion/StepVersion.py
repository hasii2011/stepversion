
from logging import Logger
from logging import getLogger

from click import command
from click import option
from click import version_option

from click import echo as clickEcho

from stepversion import __version__ as stepVersion


class StepVersion:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)


@command()
@version_option(version=f'{stepVersion}', message='%(version)s')
@option('-m', '--major',  type=int, is_flag=False, flag_value=1, help='Bump major version (default 1)')
@option('-i', '--minor',  type=int, is_flag=False, flag_value=1, help='Bump minor version (default 1)')
@option('-p', '--patch',  type=int, is_flag=False, flag_value=1, help='Bump patch version (default 1)')
def commandHandler(major: str, minor: str, patch: str):
    clickEcho(f'{major=} {minor=} {patch=}')


if __name__ == "__main__":

    commandHandler()
