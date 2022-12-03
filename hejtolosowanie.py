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


def losowanie(post_url):
    post_title = post_url.split('/')[-1]
    api_url = API_URL_TEMPLATE.replace('XXX', post_title)

    response = requests.get(api_url).json()

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

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    def activate_tab_1(self):
        winner = losowanie(self.input.text())
        self.label.setText(winner)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()