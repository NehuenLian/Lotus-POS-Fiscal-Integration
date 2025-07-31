from typing import Callable

from PySide6.QtWidgets import (QFrame, QLabel, QLineEdit, QMessageBox,
                               QPushButton)


def display_header(label: str) -> QLabel:
    header_label = QLabel(label)
    return header_label


def display_textfield(action: Callable[[], None]) -> QLineEdit:
    input_field = QLineEdit()
    input_field.setPlaceholderText("Ingrese el código de barras...")
    input_field.setFixedWidth(200)
    input_field.setFixedHeight(35)
    input_field.setMaxLength(40)

    input_field.returnPressed.connect(action)

    return input_field


def display_send_button(action: Callable[[], None]) -> QPushButton:
    button = QPushButton("Enviar")
    button.setFixedWidth(100)
    button.setFixedHeight(35)

    button.clicked.connect(action)

    return button


def show_message_box_notification(message: str) -> None:
    msg_box = QMessageBox()
    
    msg_box.setWindowTitle("Notificación")
    msg_box.setText(message)
    msg_box.setIcon(QMessageBox.Information)
    
    msg_box.addButton("Aceptar", QMessageBox.AcceptRole)
    msg_box.exec()


def horizontal_divider() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)

    return line