"""
Version file:
    curr x.x.x
    server_until x.y.z 
    browser_until x.y.z
    total x.y.z
"""
class version_no():
    def __init__(self, no):
        self.major = int(no[0])
        self.minor = int(no[1])
        self.sub = int(no[2])
    def __gt__(self, other):
        if isinstance(other, version_no):
            return (self.major > other.major) or (self.major == other.major and self.minor > other.minor) or (self.major == other.major and self.minor == other.minor and self.sub > other.sub)
    def __lt__(self, other):
        if isinstance(other, version_no):
            return (self.major < other.major) or (self.major == other.major and self.minor < other.minor) or (self.major == other.major and self.minor == other.minor and self.sub < other.sub)
    def __eq__(self, other):
        if isinstance(other, version_no):
            return (not self.__lt__(other) and not self.__gt__(other))
    def __ge__(self, other):
        if isinstance(other, version_no):
            return (self.__gt__(other) or self.__eq__(other))
    def __le__(self, other):
        if isinstance(other, version_no):
            return (self.__lt__(other) or self.__eq__(other))


class version_info():
    """
    Version class.
    """
    def __init__(self, inp):
        self.current_version = version_no(inp[0].split(' ')[-1].split('.'))
        self.server_restart = version_no(inp[1].split(' ')[-1].split('.'))
        self.browser_restart = version_no(inp[2].split(' ')[-1].split('.'))
        self.total_restart = version_no(inp[3].split(' ')[-1].split('.'))
    def check_against(self, inp):
        """
        returns the following:
        0 - same version
        1 - server restart required
        2 - browser refresh required
        3 - server and browser restart required
        4 - too old, system restart required
        """
        if isinstance(inp, version_info):
            if self.current_version == inp.current_version:
                return 0
            if self.current_version < inp.total_restart:
                return 4
            if self.current_version < inp.server_restart:
                if self.current_version >= inp.browser_restart:
                    return 1
                else:
                    return 3
            if self.current_version < inp.browser_restart:
                return 2

if __name__ == '__main__':
    current = version_info(['a 2.3.4', 'b 2.3.3', 'c 2.2.4', 'd 1.3.4'])
    server = version_info(['a 2.3.7', 'b 2.3.5', 'c 2.2.4', 'd 1.3.4'])
    browser = version_info(['a 2.4.1', 'b 2.3.4', 'c 2.3.6', 'd 1.3.4'])
    both = version_info(['a 2.4.1', 'b 2.3.6', 'c 2.3.5', 'd 1.3.4'])
    total = version_info(['a 4.4.1', 'b 4.3.5', 'c 4.3.4', 'd 4.3.4'])

    print(f'current vs current: {current.check_against(current)} - 0')
    print(f'current vs server: {current.check_against(server)} - 1')
    print(f'current vs browser: {current.check_against(browser)} - 2')
    print(f'current vs both: {current.check_against(both)} - 3')
    print(f'current vs total: {current.check_against(total)} - 4')