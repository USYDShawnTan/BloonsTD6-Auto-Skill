import sys
import random
import threading
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTimer
from pynput.keyboard import Controller
from pynput.mouse import Listener
import pygetwindow as gw

class KeyBinderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.keyboard = Controller()
        self.threads = []
        self.active_buttons = [False] * 12
        self.is_within_game_window = False
        self.initUI()
        self.initMouseListener()
        self.initWindowChecker()

    def initUI(self):
        self.setWindowTitle('Auto-Skill')
        self.setWindowIcon(QIcon('app_icon_multisize.ico'))
        self.setStyleSheet('background-color: #2E2E2E; color: white;')

        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        control_layout = QHBoxLayout()

        title = QLabel('Auto-Skill Key Binder')
        title.setFont(QFont('Arial', 20))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.buttons = []
        keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=']
        for i, key in enumerate(keys):
            btn = QPushButton(key)
            btn.setFont(QFont('Arial', 12, QFont.Bold))
            btn.setStyleSheet(self.button_style('gray'))
            btn.setCheckable(True)
            btn.clicked.connect(self.create_button_handler(i))
            button_layout.addWidget(btn)
            self.buttons.append(btn)

        start_all_btn = QPushButton('Start All')
        start_all_btn.setFont(QFont('Arial', 12, QFont.Bold))
        start_all_btn.setStyleSheet(self.button_style('#4CAF50'))
        start_all_btn.clicked.connect(self.start_all)

        stop_all_btn = QPushButton('Stop All')
        stop_all_btn.setFont(QFont('Arial', 12, QFont.Bold))
        stop_all_btn.setStyleSheet(self.button_style('#F44336'))
        stop_all_btn.clicked.connect(self.stop_all)

        control_layout.addWidget(start_all_btn)
        control_layout.addWidget(stop_all_btn)

        layout.addLayout(button_layout)
        layout.addLayout(control_layout)
        self.setLayout(layout)
        self.show()

    def button_style(self, color):
        return f'''
            QPushButton {{
                background-color: {color};
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 10px;
            }}
            QPushButton:checked {{
                background-color: green;
            }}
        '''

    def create_button_handler(self, index):
        def handler():
            self.buttons[index].setStyleSheet(self.button_style('green' if self.buttons[index].isChecked() else 'gray'))
            self.active_buttons[index] = self.buttons[index].isChecked()
            if self.active_buttons[index]:
                t = threading.Thread(target=self.press_key, args=(index,))
                t.start()
                self.threads.append(t)
        return handler

    def press_key(self, index):
        key = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='][index]
        while self.active_buttons[index]:
            if self.is_within_game_window:
                self.keyboard.press(key)
                self.keyboard.release(key)
            time.sleep(random.uniform(0.1, 0.6))

    def start_all(self):
        for btn in self.buttons:
            if not btn.isChecked():
                btn.click()

    def stop_all(self):
        for btn in self.buttons:
            if btn.isChecked():
                btn.click()

    def initMouseListener(self):
        listener = Listener(on_move=self.on_mouse_move)
        listener.start()

    def on_mouse_move(self, x, y):
        if self.is_game_window_active():
            if not self.is_within_game_window:
                self.is_within_game_window = True
        else:
            if self.is_within_game_window:
                self.is_within_game_window = False

    def initWindowChecker(self):
        self.window_checker = QTimer(self)
        self.window_checker.timeout.connect(self.check_window_active)
        self.window_checker.start(1000)  # 每秒检查一次

    def check_window_active(self):
        self.is_within_game_window = self.is_game_window_active()

    def is_game_window_active(self):
        active_window = gw.getActiveWindow()
        return active_window and 'BloonsTD6' in active_window.title

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KeyBinderApp()
    sys.exit(app.exec_())
