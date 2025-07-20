from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QVBoxLayout, QWidget)

from src.views.shared_components import (display_header, horizontal_divider,
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
        database_field_qwidget = self._set_database_url_layout()

        self.main_layout.addWidget(header_layout)
        self.main_layout.addWidget(database_field_qwidget)
        self.main_layout.addStretch(1)

    def _set_header(self) -> QWidget:
        header_layout = QHBoxLayout()
        header_qwidget = QWidget()

        header = display_header("Ajustes")

        header_layout.addWidget(header)
        header_qwidget.setLayout(header_layout)

        return header_qwidget
    
    def _set_database_url_layout(self) -> QWidget:
        outer_layout = QVBoxLayout()
        outer_widget = QWidget()

        context_label = self._display_context_label()
        divider = horizontal_divider()
        db_url_input = self._display_database_input_field()
        connect_to_db_button = self._display_connect_to_db_button()

        top_layout = QVBoxLayout()
        top_layout.addWidget(context_label)
        top_layout.addWidget(divider)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(db_url_input)
        bottom_layout.addWidget(connect_to_db_button)
        bottom_layout.addStretch(1)

        outer_layout.addLayout(top_layout)
        outer_layout.addLayout(bottom_layout)
        outer_widget.setLayout(outer_layout)

        return outer_widget

    def _display_context_label(self) -> QLabel:
        context_label = self.components.section_label()
        return context_label

    def _display_database_input_field(self) -> QLineEdit:
        db_url_input = self.components.database_input_field()
        return db_url_input
    
    def _display_connect_to_db_button(self) -> QPushButton:
        connect_to_db_button = self.components.connect_to_db_button()
        connect_to_db_button.clicked.connect(self.settings_controller.connect_to_db)

        return connect_to_db_button

class DomainComponents:
    def __init__(self):
        pass

    def section_label(self) -> QLabel:
        label = QLabel("Conectarse a Base de Datos")
        return label

    def database_input_field(self) -> QLineEdit:
        input_field = QLineEdit()
        input_field.setPlaceholderText("Ingrese una URL...")
        input_field.setFixedWidth(200)
        input_field.setFixedHeight(30)
        input_field.setMaxLength(40)

        return input_field
    
    def connect_to_db_button(self) -> QPushButton:
        connect_button = QPushButton("Conectarse")
        connect_button.setFixedWidth(100)
        connect_button.setFixedHeight(30)

        return connect_button