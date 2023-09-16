
from logging import Logger
from logging import getLogger

from os import linesep as osLineSep

from importlib.abc import Traversable

from importlib.resources import files

from click import ClickException
from click import clear
from click import command
from click import option
from click import secho
from click import version_option

from click import echo as clickEcho

from codeallybasic.Environment import Environment

from stepversion import __version__

DEFAULT_FILE_NAME: str = '_version.py'


class StepVersion(Environment):
    def __init__(self, *, major: str, minor: str, patch: str, packageName: str):

        super().__init__(printCallback=self._printCallback)
        self.logger: Logger = getLogger(__name__)

        self._major:       str = major
        self._minor:       str = minor
        self._patch:       str = patch
        self._packageName: str = packageName

    def update(self):
        self._readVersionFile()

    def _readVersionFile(self):

        if self._packageName is None:
            packageName: str = self._projectDirectory
        else:
            packageName = self._packageName

        fqFileName: str = self._getFullyQualifiedResourceFileName(package=packageName, fileName=DEFAULT_FILE_NAME)

        with open(fqFileName, 'r') as versionFile:
            versionLine: str = versionFile.read()

        secho(f'{versionLine=}')
        justVersion: str = versionLine.split('=')[1].strip(osLineSep).strip("'").lstrip(" ").lstrip("'")
        secho(f'{justVersion=}')

        semanticVersion: SemananticVersion = SemanticVersion(justVersion)


    def _printCallback(self, message: str):
        secho(f'{message}', color=True, reverse=True)

    def computeVersionFileName(self) -> str:

        fqFileName: str = self._getFullyQualifiedResourceFileName(self.RESOURCES_PACKAGE_NAME, fileName=DEFAULT_FILE_NAME)
        return fqFileName

    def _getFullyQualifiedResourceFileName(self, package: str, fileName: str) -> str:
        """
        Use this method to get other unit test resources
        Args:
            package:    The fully qualified package name (dot notation)
            fileName:   The resources file name

        Returns:  A fully qualified path name
        """

        traversable: Traversable = files(package) / fileName

        return str(traversable)


@command()
@version_option(version=f'{__version__}', message='%(version)s')
@option('-m', '--major',        type=int, is_flag=False, flag_value=1, help='Bump major version (default 1)')
@option('-i', '--minor',        type=int, is_flag=False, flag_value=1, help='Bump minor version (default 1)')
@option('-p', '--patch',        type=int, is_flag=False, flag_value=1, help='Bump patch version (default 1)')
@option('-a', '--package-name', type=str, help='Use this option when the package name does not match the project name')
def commandHandler(major: str, minor: str, patch: str, package_name: str):
    """

    Args:
        major:
        minor:
        patch:

    Returns:

    """

    if major is None and minor is None and patch is None:
        raise ClickException('You must provide one option on what to patch.')
    clear()
    clickEcho(f'{major=} {minor=} {patch=}')
    stepVersion: StepVersion = StepVersion(major=major, minor=minor, patch=patch, packageName=package_name)
    secho('')
    stepVersion.update()


if __name__ == "__main__":

    commandHandler(['-p', '1', '-a', 'stepversion'])
