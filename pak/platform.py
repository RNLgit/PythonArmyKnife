"""
This module collects and summarizes info of the operating system script is running on
"""
import platform
import sys

OS_TYPE = {'Darwin': 'macOS', 'Windows': 'Windows', 'Linus': 'Linux'}


class Platform(object):
    def __init__(self):
        self._info = dict()
        self._info['OS'] = OS_TYPE[platform.system()]
        self._init_routine()

    def _init_routine(self):
        """
        Init routine that iterates all useful platform functions. So that .info function have data in there.
        """
        self.summary()
        self.architecture()
        self.network_name()
        self.processor()
        self.machine()
        self.release()
        self.version()

    @property
    def info(self):
        return self._info

    def architecture(self):
        """
        Returns Python interpreter binary 32bit or 64bit
        """
        self._info['arch'] = platform.architecture()[0]
        return self._info['arch']

    def network_name(self):
        """
        Returns computer’s network name
        """
        self._info['network_name'] = platform.node()
        return self._info['network_name']

    def machine(self):
        """
        get type of machine instruction set.
        e.g. AMD64: x64 on Windows; x86_64 on macOS and Linux;
        """
        self._info['machine_type'] = platform.machine()
        return self._info['machine_type']

    def processor(self):
        """
        get processor description
        """
        self._info['processor'] = platform.processor()
        return self._info['processor']

    def summary(self):
        """
        summary of current platform info
        """
        self._info['summary'] = platform.platform()
        return self._info['summary']

    def release(self):
        """
        system release version or kernel version
        e.g. 10 in Windows 10 and 20.6.0 in macOS Kernel
        """
        self._info['platform_release'] = platform.release()
        return self._info['platform_release']

    def version(self):
        """
        system version summary string
        """
        self._info['version_summary'] = platform.version()
        return self._info['version_summary']


class Python(object):
    def __init__(self):
        self._info = dict()
        self._init_routine()

    def _init_routine(self):
        """
        Init routine that iterates all useful python info. So that .info function have data in there.
        """
        self.version()
        self.implementation()
        self.compiler()
        self.python_branch()
        self.python_revision()

    @property
    def info(self):
        return self._info

    def version(self):
        """
        Python version
        """
        self._info['version'] = platform.python_version()
        return self._info['version']

    def implementation(self):
        """
        Python implementation. ‘CPython’, ‘IronPython’, ‘Jython’, ‘PyPy’ etc.
        """
        self._info['python_implementation'] = platform.python_implementation()
        return self._info['python_implementation']

    def compiler(self):
        """
        Python compiler used
        """
        self._info['python_compiler'] = platform.python_compiler()
        return self._info['python_compiler']

    def python_branch(self):
        """
        get python branch name
        """
        self._info['python_branch'] = platform.python_branch()
        return self._info['python_branch']

    def python_revision(self):
        """
        python revision string
        """
        self._info['python_revision'] = platform.python_revision()
        return self._info['python_revision']


