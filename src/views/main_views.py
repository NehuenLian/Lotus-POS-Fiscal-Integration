from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QPushButton,
                               QStackedWidget, QVBoxLayout, QWidget, QLabel)

from src.views.check_stock import CheckStockViewManager
from src.views.manage_prices import PriceViewsManager
from src.views.register_sale import SalesViewManager


class GeneralViewsManager(QWidget):
    def __init__(self, main_controller):
        super().__init__()
        self.setWindowTitle("Lotus POS")
        self.resize(1280, 720)

        self.components = UIComponents()
        self.main_controller = main_controller

        self.main_window = QHBoxLayout(self)
        self.sidebar = QVBoxLayout()
        self.sidebar_widget = QWidget()
        self.stacked_widget = QStackedWidget()

        self._set_layout()

    def _set_layout(self):

        self.divider = self.components.divider_line()
        self.check_stock = self.manage_stock_choice()
        self.manage_prices = self.manage_price_choice()
        self.register_sale = self.manage_sales_choice()
        self.quit = self.manage_quit_choice()

        self.sidebar.addWidget(self.check_stock)
        self.sidebar.addWidget(self.manage_prices)
        self.sidebar.addWidget(self.register_sale)
        self.sidebar.addStretch()
        self.sidebar.addWidget(self.quit)

        self.sidebar_widget.setLayout(self.sidebar)

        self.stacked_widget.addWidget(CheckStockViewManager())
        self.stacked_widget.addWidget(PriceViewsManager())
        self.stacked_widget.addWidget(SalesViewManager())

        self.main_window.addWidget(self.sidebar_widget)
        self.main_window.addWidget(self.divider)
        self.main_window.addWidget(self.stacked_widget)

    def manage_stock_choice(self):
        self.check_stock = self.components.check_stock_button()
        self.check_stock.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.check_stock.clicked.connect(self.main_controller.check_stock)

        return self.check_stock

    def manage_price_choice(self):
        self.manage_prices = self.components.manage_prices_button()
        self.manage_prices.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.manage_prices.clicked.connect(self.main_controller.manage_prices)

        return self.manage_prices

    def manage_sales_choice(self):
        self.register_sale = self.components.register_sale()
        self.register_sale.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.register_sale.clicked.connect(self.main_controller.register_sale)

        return self.register_sale

    def manage_quit_choice(self):
        self.quit = self.components.quit_button()
        self.quit.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.quit.clicked.connect(self.main_controller.quit_app)

        return self.quit


class UIComponents:
    def __init__(self):
        pass

    def check_stock_button(self) -> object:
        button = QPushButton("Consultar Stock")
        return button
    
    def manage_prices_button(self) -> object:
        button = QPushButton("Gestionar Precios")
        return button

    def register_sale(self) -> object:
        button = QPushButton("Registrar Ventas")
        return button
    
    def quit_button(self) -> object:
        button = QPushButton("Salir")
        return button

    def divider_line(self) -> object:
        divider = QFrame()
        divider.setFrameShape(QFrame.VLine)
        divider.setFrameShadow(QFrame.Sunken)
        return divider
