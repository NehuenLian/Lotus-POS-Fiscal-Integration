<p align="center">
  <a href="https://codecov.io/github/NehuenLian/lotus-pos-desktop">
    <img src="https://codecov.io/github/NehuenLian/lotus-pos-desktop/graph/badge.svg?token=20WL0URAGI" alt="codecov"/>
  </a>
</p>

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.32-red?logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-6.9.1-green?logo=qt&logoColor=white)  
Compatibility: Windows

# Lotus POS: Point of Sale System

**Lotus POS** is a desktop application built for small to medium-sized businesses. It allows you to manage sales, inventory, pricing, and database configuration in a simple way.

---

### **Features:**

- Check stock.
- Register sales.
- Modify prices.
- Offline-first (Works without an internet connection).

To learn more about how the app is built, you can consult the Architecture Decision Records (ADRs) in `/docs/adr/`.

<p align="center">
  <img src="images/frontend_screenshot.jpg" alt="Lotus POS Frontend" width="700">
  <br>
  <em>The screenshot shows the app in Spanish, as requested by the client.</em>
</p>

---

# Installation

1.  **Clone the repository:**
  ```bash
  git clone https://github.com/NehuenLian/lotus-pos-desktop
  ```

2. **Go to repository:**
  ```bash
  cd Lotus-POS-Desktop
  ```

3. **Create and activate a virtual environment:**
  - On Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

4. **Install dependencies:**
  ```bash
  pip install -r requirements.txt
  ```

5. **Environment variables configuration:**  
Set the database URL in a `config.json` file in `url`:

```bash
{
  "database": {
    "url": "sqlite:///src/data_access/sample_database.db"
    }
}
```

# Test setup

For a quick test, the remote repository includes a sample database located at `src/data_access/sample_database.db` and a .CSV file with product data at `src/sample_data/inventory.csv`. To use this database, the `config.json` file already comes with this URL configured:
#
```bash
DB_URL="sqlite:///src/data_access/sample_database.db"
```
#    
The barcodes of the products registered in the sample database can be found in `src/sample_data/inventory.csv`.
These can be used to **check stock**, **register sales**, or **modify prices**.

# Packing

To run the packaging command, **pyinstaller** must be installed:
```bash
  pip install pyinstaller
```

- Basic command to package the app:
```bash
  pyinstaller --noconfirm --onedir --console --name "LotusPOS" `
  --icon "src/views/assets/app_icon.ico" `
  --add-data "src/views/assets;src/views/assets" `
  --collect-all "PySide6" `
  --hidden-import "sqlalchemy.sql.default_comparator" `
  --paths "src" `
  "main.py"
```

- Then set the database URL for the application to connect to in **settings**.

---

# How to use

1.  **Run the app:**
  ```bash
  python main.py
  ```
  Or open the .exe after packaging

2.  **Navigate through sections using the sidebar:**  
 - Stock Consultation
 - Price Management
 - Sales Registration
 - Configuration

3. Use product barcodes to search and interact with products: **check stock**, **register sales**, or **modify prices**.

### Run tests and see coverage

- All tests:
  ```bash
  pytest -v --cov
  ```

- Unit tests:
  ```bash
  pytest tests/unit -v --cov
  ```

- Integration tests:
  ```bash
  pytest tests/integration -v --cov
  ```

## Architecture

```text
.
├── .github/
├── docs/
├── images/
├── integration/
├── src/
│   ├── business_logic/
│   ├── controllers/
│   ├── data_access/
│   ├── logs/
│   ├── sample_data/
│   ├── utils/
│   ├── views/
│   └── exceptions.py
├── tests/
└── requirements.txt
```

## License

This project is licensed under the MIT license.
You are free to use, copy, modify, and distribute the software, always including the copyright notice and without any warranties.

---

Author: Nehuen Lián https://github.com/NehuenLian
