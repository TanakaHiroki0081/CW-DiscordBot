import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QSpinBox)
from PyQt5.QtCore import Qt

class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('CrowdWorks Discord Monitor')
        layout = QVBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('CrowdWorks URL')
        layout.addWidget(QLabel('CrowdWorks URL:'))
        layout.addWidget(self.url_input)

        price_layout = QHBoxLayout()
        self.lower_price = QSpinBox()
        self.lower_price.setMaximum(1000000)
        self.lower_price.setPrefix('¥')
        self.lower_price.setValue(0)
        self.upper_price = QSpinBox()
        self.upper_price.setMaximum(1000000)
        self.upper_price.setPrefix('¥')
        self.upper_price.setValue(10000)
        price_layout.addWidget(QLabel('Price Range:'))
        price_layout.addWidget(self.lower_price)
        price_layout.addWidget(QLabel('to'))
        price_layout.addWidget(self.upper_price)
        layout.addLayout(price_layout)

        self.channel_id_input = QLineEdit()
        self.channel_id_input.setPlaceholderText('Discord Channel ID')
        layout.addWidget(QLabel('Discord Channel ID:'))
        layout.addWidget(self.channel_id_input)

        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText('Discord Bot Token')
        self.token_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel('Discord Bot Token:'))
        layout.addWidget(self.token_input)

        self.poll_interval = QSpinBox()
        self.poll_interval.setMinimum(1)
        self.poll_interval.setMaximum(120)
        self.poll_interval.setValue(5)
        layout.addWidget(QLabel('Polling Interval (minutes):'))
        layout.addWidget(self.poll_interval)

        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton('Start')
        self.stop_btn = QPushButton('Stop')
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)

        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)
        layout.addWidget(QLabel('Status:'))
        layout.addWidget(self.status_display)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec_()) 