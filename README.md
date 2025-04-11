# 🧾 Point of Sale System (MVP)

***
### Stack
- Python
- SQLAlchemy ORM
- MySQL/SQLite

### Features
- 🧾 Register sales
- 📦 Check stock
- 💰 Update prices

***
### 🛠️ Architecture
This project is based on a layered architecture. Partially decoupled and prepared for a potential transition to Clean Architecture:

```text
pos_mvp
├── logs/
├── src/
│   ├── controllers/ # Controllers
│   ├── core/ # Business logic
│   ├── database/
│   │   └── repository/ # DAOs
│   ├── utils/ # Logging config
│   ├── views/
│   └── exceptions.py # Custom exceptions
├── tests/
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

***

### 🧪 Getting started

1. Clone the repository

`git clone https://github.com/NehuenLian/POS_MVP`

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
