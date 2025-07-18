from tabnanny import check

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
                               QPushButton, QStackedWidget, QVBoxLayout,
                               QWidget)


class GeneralViewsManager(QWidget):
    def __init__(self, main_controller, stock_view, price_view, sales_view):
        super().__init__()
        self.setWindowTitle("Lotus POS")
        self.resize(1280, 720)

        self.components = DomainComponents()
        self.main_controller = main_controller

        self.main_window = QHBoxLayout(self)
        self.sidebar = QVBoxLayout()
        self.sidebar_widget = QWidget()
        self.stacked_widget = QStackedWidget()

        # Domain views
        self.stock_view = stock_view
        self.price_view = price_view
        self.sales_view = sales_view

        self._set_layout()

    def _set_layout(self) -> None:

        divider = self.components.divider_line()
        check_stock = self._manage_stock_choice()
        manage_prices = self._manage_price_choice()
        register_sale = self._manage_sales_choice()
        quit = self._manage_quit_choice()

        self.sidebar.addWidget(check_stock)
        self.sidebar.addWidget(manage_prices)
        self.sidebar.addWidget(register_sale)
        self.sidebar.addStretch()
        self.sidebar.addWidget(quit)

        self.sidebar_widget.setLayout(self.sidebar)

        self.stacked_widget.addWidget(self.stock_view)
        self.stacked_widget.addWidget(self.price_view)
        self.stacked_widget.addWidget(self.sales_view)

        self.main_window.addWidget(self.sidebar_widget)
        self.main_window.addWidget(divider)
        self.main_window.addWidget(self.stacked_widget)

    def _manage_stock_choice(self) -> QPushButton:
        check_stock = self.components.check_stock_button()
        check_stock.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        return check_stock

    def _manage_price_choice(self) -> QPushButton:
        manage_prices = self.components.manage_prices_button()
        manage_prices.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        return manage_prices

    def _manage_sales_choice(self) -> QPushButton:
        register_sale = self.components.register_sale()
        register_sale.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        return register_sale

    def _manage_quit_choice(self) -> QPushButton:
        quit = self.components.quit_button()
        quit.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        quit.clicked.connect(self.main_controller.quit_app)

        return quit


class DomainComponents:
    def __init__(self):
        pass

    def check_stock_button(self) -> QPushButton:
        button = QPushButton("Consultar Stock")
        return button
    
    def manage_prices_button(self) -> QPushButton:
        button = QPushButton("Gestionar Precios")
        return button

    def register_sale(self) -> QPushButton:
        button = QPushButton("Registrar Ventas")
        return button
    
    def quit_button(self) -> QPushButton:
        button = QPushButton("Salir")
        return button

    def divider_line(self) -> QFrame:
        divider = QFrame()
        divider.setFrameShape(QFrame.VLine)
        divider.setFrameShadow(QFrame.Sunken)
        return divider
