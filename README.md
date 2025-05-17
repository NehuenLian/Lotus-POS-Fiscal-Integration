# 🧾 Point of Sale System (MVP)

***
### Stack
- Python
- SQLAlchemy ORM
- MySQL/SQLite
- Flet Framework

### Features
- 🧾 Register sales
- 📦 Check stock
- 💰 Update prices

***
### 🛠️ Architecture
This project is based on a layered architecture. Partially decoupled and prepared for a potential transition to Clean Architecture:

```text
POS_MVP/
├── src/
│   ├── __pycache__/
│   ├── config/
│   │   └── __pycache__/
│   ├── controllers/
│   │   ├── __pycache__/
│   │   ├── check_stock_controller.py
│   │   ├── controller.py
│   │   ├── price_management_controller.py
│   │   ├── sales_management_controller.py
│   │   └── settings_controller.py
│   ├── core/
│   │   ├── __pycache__/
│   │   ├── check_stock.py
│   │   ├── price_management.py
│   │   └── sales_management.py
│   ├── database/
│   │   ├── __pycache__/
│   │   ├── connection.py
│   │   ├── models.py
│   │   └── session_manager.py
│   ├── repository/
│   │   ├── __pycache__/
│   │   ├── sale_details_dao.py
│   │   ├── sales_dao.py
│   │   └── stock_dao.py
│   ├── utils/
│   │   ├── __pycache__/
│   │   ├── flags.py
│   │   └── logging_config.py
│   └── views/
│       ├── __pycache__/
│       ├── check_stock_views.py
│       ├── general_views.py
│       ├── price_management_views.py
│       ├── sales_management_views.py
│       ├── settings_view.py
│       ├── ui_notifications.py
│       └── exceptions.py
├── tests/
│   ├── inventory.csv
│   ├── show_sales.ipynb
│   └── test_db.db
├── .env
├── .gitignore
├── LICENSE
├── main.py
├── README.md
└── requirements.txt
```

***

### 🧪 Getting started

1. Clone the repository

`git clone github.com/NehuenLian/POS_MVP`

`cd pos_mvp`


2. Install the dependencies
   
`pip install -r requirements.txt`

3. Run the main file

`python main.py`

***

### 📘 How to use
- This app uses a mock SQLite database, allowing you to test all functionalities effortlessly: `pos_mvp/tests/test_db.db`

- You can find the barcodes to use in `pos_mvp/tests/inventory.csv`.<br>
  1.  When the program asks you to input a barcode, you can copy any barcode in `inventory.csv` (Example: `7790895000997`) and paste it and press `Enter`.
  2.  Then, follow the instructions and continue with the app flow.

- `pos_mvp/tests/show_sales.ipynb`: A Jupyter Notebook is provided where you can run a pre-built SQL statement to view your registered sales.

- Also, there is a `pos_mvp/tests/database.csv` file (that will be created when you run the app) where you can see all the sales you made. Feel free to use it as needed.

***

### 📄 License

This project is licensed under the MIT License.  
See the [LICENSE](./LICENSE) file for more information.
