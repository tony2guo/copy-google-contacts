#!/usr/bin/env python3

import csv
import time
import pyperclip
from pynput import mouse, keyboard


class CopyGoogleContacts:

    def __init__(self):
        self.scroll_dir = None
        self.start()

    def __on_scroll(self, x, y, dx, dy):
        self.scroll_dir = dy < 0  # True for down

    def start(self):
        contacts = {}

        listener = mouse.Listener(on_scroll=self.__on_scroll)
        listener.start()

        mc = mouse.Controller()
        kc = keyboard.Controller()

        print("1. Select contacts text and hold.\n2. Scroll down to start, scroll up to stop.")
        while self.scroll_dir is None:
            time.sleep(0.1)

        while True:
            if self.scroll_dir is False:
                print("stop")
                break

            kc.press(keyboard.Key.ctrl)
            kc.press('c')
            kc.release('c')
            kc.release(keyboard.Key.ctrl)
            time.sleep(0.01)

            text = pyperclip.paste()
            wait_loading = False

            for contact in text.split("\r\n"):
                if contact == '. . .':
                    wait_loading = True
                else:
                    contact_info = contact.split("\t")
                    if len(contact_info) >= 2:
                        email = contact_info[1]
                        contacts[email] = contact_info

            if not wait_loading:
                mc.scroll(0, -1)

            time.sleep(0.1)

        print("Save to contacts.csv")
        with open('contacts.csv', 'w', newline='', encoding='utf-8') as f:
            write = csv.writer(f)
            write.writerows(contacts.values())


if __name__ == '__main__':
    CopyGoogleContacts()