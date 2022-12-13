import requests
import random

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QPushButton,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QVBoxLayout
)
from PyQt6.QtCore import Qt


API_URL_TEMPLATE = "https://api.hejto.pl/posts/XXX/likes?limit=10000"

def prepare_api_url(url):
    """Return URL to API based on WEBSITE URL.
       If given URL is empty or not leading to hejto.pl, return error message starting with "ERROR! ".
    """
    if url == '':
        error_message = 'ERROR! Nie podano URL!'
        print(error_message)
        return error_message

    #  example of url = https://www.hejto.pl/wpis/czesc-dzis-update
    url_parts = url.split('/')
    #  example of url_parts = ['https:', '', 'www.hejto.pl', 'wpis', 'czesc-dzis-update']
    
    #  check if url is for hejto service
    if url_parts != 'www.hejto.pl':
        error_message = 'ERROR! Podany URL nie odnosi się do hejto!'
        print(error_message)
        return error_message
    
    post_title = url_parts[-1]

    api_url = API_URL_TEMPLATE.replace('XXX', post_title)

    return api_url


def losowanie(post_url):
    """Return nickname of randomly chosen winner.
       If error occurs, return error message starting with "ERROR! ".
    """
    #  example of post_url = https://www.hejto.pl/wpis/czesc-dzis-update
    api_url_or_error = prepare_api_url(post_url)
    if api_url_or_error.startswith('ERROR! '):
        return api_url_or_error

    response = requests.get(api_url_or_error).json()

    list_of_users_objects = response['_embedded']['items']

    usernames = []
    for u_object in list_of_users_objects:
        username = u_object['author']['username']
        usernames.append(username)

    print(usernames)

    winner = random.choice(usernames)
    return winner


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        text_for_label = "WPISZ URL WPISU W POLU EDYCJI"
        if random.random() < 0.2137:
            text_for_label = "ZAINSTALOWANO WIRUSA WATYKAŃCZYKA\nZHACKOWANO PŁYTĘ GŁÓWNĄ"
        self.label = QLabel(text_for_label)
        self.input = QLineEdit()


        btn = QPushButton("KLIK")
        btn.pressed.connect(self.activate_tab_1)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(btn)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        #  Set the central widget of the Window.
        self.setCentralWidget(container)

    def activate_tab_1(self):
        winner_or_error = losowanie(self.input.text())
        #  Check if winner was chosen or error occured.
        if winner_or_error.startswith('ERROR! '):
            self.label.setText(winner_or_error)
        else:
            self.label.setText(winner_or_error)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()