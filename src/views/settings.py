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
        self.db_url_input = self._display_database_input_field()
        update_db_url_button = self._display_update_db_url_button()
        restart_app_button = self._display_restart_button()

        section_header_layout = QVBoxLayout()
        section_header_layout.addWidget(context_label)
        section_header_layout.addWidget(divider)

        input_db_url_layout = QHBoxLayout()
        input_db_url_layout.addWidget(self.db_url_input)
        input_db_url_layout.addWidget(update_db_url_button)
        input_db_url_layout.addStretch(1)
        input_db_url_layout.addWidget(restart_app_button)

        outer_layout.addLayout(section_header_layout)
        outer_layout.addLayout(input_db_url_layout)
        outer_widget.setLayout(outer_layout)

        return outer_widget

    def _display_context_label(self) -> QLabel:
        context_label = self.components.section_label()
        return context_label

    def _display_database_input_field(self) -> QLineEdit:
        db_url_input = self.components.database_input_field()
        return db_url_input
    
    def _display_update_db_url_button(self) -> QPushButton:
        update_button = self.components.update_url_button()
        update_button.clicked.connect(self._update_database_url_handler)

        return update_button
    
    def _display_restart_button(self) -> QPushButton:
        restart_button = self.components.restart_app_button()
        restart_button.clicked.connect(self.settings_controller.restart_program)

        return restart_button
    
    # Handlers
    def _update_database_url_handler(self):
        db_url = self.db_url_input.text()
        self.settings_controller.update_db_url(db_url)


class DomainComponents:
    def __init__(self):
        pass

    def section_label(self) -> QLabel:
        label = QLabel("Cambiar de Base de Datos (Reiniciar para aplicar cambios)")
        return label

    def database_input_field(self) -> QLineEdit:
        input_field = QLineEdit()
        input_field.setPlaceholderText("Ingrese una URL...")
        input_field.setFixedWidth(200)
        input_field.setFixedHeight(30)
        input_field.setMaxLength(40)

        return input_field
    
    def update_url_button(self) -> QPushButton:
        update_button = QPushButton("Actualizar")
        update_button.setFixedWidth(100)
        update_button.setFixedHeight(30)

        return update_button
    
    def restart_app_button(self) -> QPushButton:
        restart_button = QPushButton("Reiniciar aplicación")
        restart_button.setFixedWidth(120)
        restart_button.setFixedHeight(30)

        return restart_button