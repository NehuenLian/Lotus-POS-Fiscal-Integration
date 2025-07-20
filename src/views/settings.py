from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QHeaderView, QVBoxLayout, QWidget

from src.views.shared_components import (display_header, display_send_button,
                                         display_textfield,
                                         show_message_box_notification)


class SettingsViewManager(QWidget):
    def __init__(self, settings_controller):
        super().__init__()
        self.components = DomainComponents()
        self.main_layout = QVBoxLayout(self)
        
        self.settings_controller = settings_controller

        self._set_main_layout()

    # Set layouts
    def _set_main_layout(self) -> None:
        header_layout = self._set_header()

        self.main_layout.addWidget(header_layout)
        self.main_layout.addStretch(1)

    def _set_header(self) -> QWidget:
        header_layout = QHBoxLayout()
        header_qwidget = QWidget()

        header = display_header("Ajustes")

        header_layout.addWidget(header)
        header_qwidget.setLayout(header_layout)

        return header_qwidget
    

class DomainComponents:
    def __init__(self):
        pass