# Lotus POS

**Lotus POS** is a desktop Point of Sale system designed for small and medium-sized businesses. It allows you to manage sales, inventory, pricing, and database configuration in a simple way.

---

## Main Features

- **Sales Management:** Fast sales registration, product selection by barcode, automatic total calculation, and payment method selection.
- **Inventory Control:** Instant stock lookup by product.
- **Price Management:** Search and update product prices.
- **Flexible Configuration:** Change the database URL from the interface and restart the app to apply changes.
- **Architecture:** Clear separation between business logic, data access, controllers, and views.
- **Logging:** Log management for auditing and debugging.
- **Ready for Fiscal Integration:** Designed to integrate with electronic invoicing middleware (AFIP/ARCA) Argentina.

---

## Tech Stack

- Python
- SQLAlchemy
- Pyside6

---

## Project Structure

```
src/
│
├── business_logic/      # Business logic (sales, stock, prices, settings)
├── controllers/         # Module controllers
├── data_access/         # Database access and management (SQLAlchemy)
├── utils/               # Utilities and logging configuration
├── views/               # PySide6 views (UI)
├── exceptions.py        # Custom exceptions
└── main.py              # Application entry point
```

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/NehuenLian/POS_MVP
   cd lotus-pos
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure the database:**
   - Create a `.env` file in the project root with:
     ```
     DB_URL="sqlite:///test_db.db"
     ```
     Or use your preferred database URL.

---

## Usage

1. Run the application:
   ```sh
   python src/main.py
   ```

2. Navigate through the sections from the sidebar:
   - **Stock Lookup**
   - **Price Management**
   - **Sales Registration**
   - **Settings**

---

## Main Dependencies

- [PySide6](https://pypi.org/project/PySide6/) (GUI)
- [SQLAlchemy](https://www.sqlalchemy.org/) (ORM)
- [python-dotenv](https://pypi.org/project/python-dotenv/) (Environment variables)
- [lxml, zeep, tenacity, ntplib] (for fiscal integration, optional)

---

## License

This project is licensed under the MIT License.  
You are free to use, modify, and distribute the software.

---

## Author

Developed by Nehuen Lian.

---

For questions or suggestions open an issue or contact me!