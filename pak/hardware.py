from abc import ABC
from subprocess import Popen, PIPE
from .platform import Platform


class HardwareBase(object):
    @property
    def get_OS(self):
        raise NotImplementedError

    @property
    def get_CPU_temp(self):
        raise NotImplementedError

    @property
    def get_GPU_temp(self):
        raise NotImplementedError


def popen_with_response(command: str):
    process = Popen(command.split(), stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()
    if err:
        raise BrokenPipeError(err.decode())
    return out.decode()


def dict_like_splitter(stdout: str):
    """
    parse string like: NAME="Raspbian"\nID_LIKE="debian" into dictionary
    """
    parse = {}
    for line in stdout.splitlines():
        sp = line.split('=')
        if len(sp) != 2:
            print(f'{sp} not parsable')
            continue
        parse[sp[0]] = sp[1].replace('"', '')
    return parse


class MacOsHardware(HardwareBase, ABC):
    def __init__(self):
        super().__init__()


class LinuxHardware(HardwareBase, ABC):
    def __init__(self):
        super().__init__()


class RaspberryPiHardware(HardwareBase, ABC):
    def __init__(self):
        super().__init__()

    def get_os_all(self):
        """
        dictionary os-release operating system info

        output looks like:
        {'PRETTY_NAME': 'Raspbian GNU/Linux 10 (buster)',
         'NAME': 'Raspbian GNU/Linux',
         'VERSION_ID': '10',
         'VERSION': '10 (buster)',
         'VERSION_CODENAME': 'buster',
         'ID': 'raspbian',
         'ID_LIKE': 'debian',
         'HOME_URL': 'http://www.raspbian.org/',
         'SUPPORT_URL': 'http://www.raspbian.org/RaspbianForums',
         'BUG_REPORT_URL': 'http://www.raspbian.org/RaspbianBugs'}
        """
        out = popen_with_response('cat /etc/os-release')
        return dict_like_splitter(out)

    @property
    def get_OS(self):
        return self.get_os_all()['NAME']


class WindowsHardware(HardwareBase, ABC):
    def __init__(self):
        super().__init__()


def hardware():
    os = Platform().info['OS']
    if os == 'Windows':
        return WindowsHardware()
    elif os == 'Linux':
        return RaspberryPiHardware()
    elif os == 'macOS':
        return MacOsHardware()
