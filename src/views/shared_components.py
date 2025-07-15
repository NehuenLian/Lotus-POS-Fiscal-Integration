from typing import Callable

from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton


def display_header(label: str) -> QLabel:
    header_label = QLabel(label)
    return header_label


def display_textfield(action: Callable[[], None]) -> QLineEdit:
    input_field = QLineEdit()
    input_field.setPlaceholderText("Ingrese el código de barras...")
    input_field.setFixedWidth(200)
    input_field.setFixedHeight(30)
    input_field.setMaxLength(40)

    input_field.returnPressed.connect(action)

    return input_field


def display_send_button(action: Callable[[], None]) -> QPushButton:
    button = QPushButton("Enviar")
    button.setFixedWidth(100)
    button.setFixedHeight(30)

    button.clicked.connect(action)

    return button
