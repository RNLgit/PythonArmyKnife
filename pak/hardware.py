from abc import ABC
from subprocess import Popen, PIPE
from .platform import Platform


class HardwareBase(object):
    @property
    def get_os(self):
        raise NotImplementedError

    @property
    def get_cpu_info(self):
        raise NotImplementedError

    @property
    def get_cpu_temp(self):
        raise NotImplementedError

    @property
    def get_gpu_temp(self):
        raise NotImplementedError

    @property
    def get_memory_info(self):
        raise NotImplementedError

    @property
    def summary(self):
        raise NotImplementedError


def popen_with_response(command: str):
    process = Popen(command.split(), stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()
    if err:
        raise BrokenPipeError(err.decode())
    return out.decode()


def dict_like_splitter(stdout: str, splitter='='):
    """
    parse string like: NAME="Raspbian"\nID_LIKE="debian" into dictionary
    """
    parse = {}
    for line in stdout.splitlines():
        sp = [i.strip() for i in line.split(splitter)]  # split and strip the data
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

    @property
    def get_cpu_temp(self):
        """
        get Raspberry pi CPU temperature
        """
        out = popen_with_response('vcgencmd measure_temp')
        return float(dict_like_splitter(out, splitter='=')['temp'].split("'")[0])

    @property
    def get_cpu_info(self):
        """
        get cpu information
        """
        out = popen_with_response('cat /proc/cpuinfo')
        info = dict_like_splitter(out, splitter=':')
        if 'processor' in info.keys():
            info['processor'] = str(int(info['processor']) + 1)  # debian count core from 0
        return info

    @property
    def get_memory_info(self):
        """
        get a dictionary of memory info with unit in kilobytes. Example of a list of keys:

        'MemTotal', 'MemFree', 'MemAvailable', 'Buffers', 'Cached', 'SwapCached', 'Active', 'Inactive', 'Active(anon)',
        'Inactive(anon)', 'Active(file)', 'Inactive(file)', 'Unevictable', 'Mlocked', 'HighTotal', 'HighFree',
        'LowTotal', 'LowFree', 'SwapTotal', 'SwapFree', 'Dirty', 'Writeback', 'AnonPages', 'Mapped', 'Shmem',
        'KReclaimable', 'Slab', 'SReclaimable', 'SUnreclaim', 'KernelStack', 'PageTables', 'NFS_Unstable', 'Bounce',
        'WritebackTmp', 'CommitLimit', 'Committed_AS', 'VmallocTotal', 'VmallocUsed', 'VmallocChunk', 'Percpu',
        'CmaTotal', 'CmaFree'
        """
        out = popen_with_response('cat /proc/meminfo')
        info = dict_like_splitter(out, splitter=':')
        for k, v in info.items():
            try:
                info[k] = int(v.replace('kB', '').strip())  # get rid of kb unit mark
            except ValueError:  # if cannot int stripped value, keep original
                continue
        return info

    @property
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
        return dict_like_splitter(out, splitter='=')

    @property
    def get_os(self):
        return self.get_os_all['NAME']


class WindowsHardware(HardwareBase, ABC):
    def __init__(self):
        super().__init__()


def hardware():
    """
    Auto detecting the OS running and init corresponding supported functions
    """
    os = Platform().info['OS']
    if os == 'Windows':
        return WindowsHardware()
    elif os == 'Linux':
        return RaspberryPiHardware()
    elif os == 'macOS':
        return MacOsHardware()
