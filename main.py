import subprocess as sp


def get_list_of_networks() -> list:
    cmd1 = sp.Popen('ls', cwd='/etc/NetworkManager/system-connections/', stdout=sp.PIPE)
    output_data: str = cmd1.stdout.read().decode()
    networks = [network for network in output_data.split('\n') if network]
    return networks


def get_network_password(network_name: str) -> str:
    sudo_password = 'sudo_password'
    command = ['cat', network_name]

    cmd1 = sp.Popen(['echo', sudo_password], stdout=sp.PIPE)
    cmd2 = sp.Popen(['sudo'] + command, stdin=cmd1.stdout, stdout=sp.PIPE,
                    cwd='/etc/NetworkManager/system-connections/')
    password = ''
    output = cmd2.stdout.read().decode().split()
    for words in output:
        if words.startswith('psk'):
            password = words
            break
    return password


def collect_all_info():
    result = dict()
    list_of_networks = get_list_of_networks()
    for network_name in list_of_networks:
        password = get_network_password(network_name=network_name)
        result.update({network_name: password})
    return result
