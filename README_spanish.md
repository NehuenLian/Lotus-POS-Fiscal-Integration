<p align="center">
  <a href="https://codecov.io/github/NehuenLian/Lotus-POS-Desktop">
    <img src="https://codecov.io/github/NehuenLian/Lotus-POS-Desktop/graph/badge.svg?token=20WL0URAGI" alt="codecov"/>
  </a>
</p>

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.32-red?logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-6.9.1-green?logo=qt&logoColor=white)  
Compatible con: Windows

# Lotus POS: Sistema de punto de venta

**Lotus POS** es una aplicación de escritorio creada para pequeños-medianos negocios. Permite manejar ventas, inventario, precios y configurar una base de datos de forma simple.

---

### **Funcionalidades:** 
- Consultar Stock.
- Registrar ventas.
- Modificar precios.
- Offline-first (Funciona sin internet).

Para saber más sobre cómo está construida la app, se pueden consultar los Registros de Decisiones de Arquitectura (ADRs) en `/docs/adr/`.

<h3 align="center">Screenshot del frontend</h3>
<p align="center">
  <img src="images/frontend_screenshot.jpg" alt="Lotus POS Frontend" width="700">
  <br>
</p>

---

# Instalación

1.  **Clonar el repositorio:**
  ```bash
  git clone https://github.com/NehuenLian/Lotus-POS-Desktop
  ```

2. **Ir al repositorio:**
  ```bash
  cd Lotus-POS-Desktop
  ```

3. **Crear y activar un entorno virtual:**
  - En Linux:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
  - En Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

4. **Instalar dependencias:**
  ```bash
  pip install -r requirements.txt
  ```

5. **Configuración de base de datos:**  
Colocar la URL de la base de datos en el archivo `config.json` en `url`:
#
`
{
  "database": {
    "url": "sqlite:///src/data_access/sample_database.db"
  }
}
`

# Setup de prueba

Para una prueba rápida, se encuentra en el repositorio remoto una base de datos de ejemplo en `src/data_access/sample_database.db` y un archivo .CSV con datos de productos en `src/sample_data/inventory.csv`. Para usar esta base de datos, el archivo `config.json` ya trae configurada esta URL:
#
`
DB_URL="sqlite:///src/data_access/sample_database.db"
`
#    
Los códigos de barras de los productos registrados en la base de datos de prueba se encuentran en `src/sample_data/inventory.csv`.  
Estos se pueden usar para **consultar stock**, **registrar ventas** o **modificar precios.**

# Empaquetado

Para ejecutar el comando de empaquetado, se debe tener **pyinstaller** instalado:
```bash
  pip install pyinstaller
```

- Comando básico para empaquetar la app:
```bash
  pyinstaller --noconfirm --onedir --console --name "LotusPOS" `
  --icon "src/views/assets/app_icon.ico" `
  --add-data "src/views/assets;src/views/assets" `
  --add-data "src/data_access/sample_database.db;src/data_access" `
  --add-data "src/sample_data;src/sample_data" `
  --collect-all "PySide6" `
  --hidden-import "sqlalchemy.sql.default_comparator" `
  --paths "src" `
  "main.py"
```

- Luego colocar en **settings** la URL de la base de datos a conectar con la aplicación.

---

# Como usar

1.  **Ejecutar la aplicación:**
  ```bash
  python main.py
  ```
  O abrir el .exe luego de empaquetar.

2.  **Se puede navegar por las secciones desde la barra lateral:**  
  - Consulta de Stock  
  - Gestión de Precios  
  - Registro de Ventas  
  - Configuración  

3. Utilizar código de barras para buscar e interactuar con productos: **consultar stock**, **registrar ventas** o **modificar precios.**

### Correr tests y ver coverage

- Todos los tests:
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

## Arquitectura

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

## Licencia

Este proyecto está bajo la licencia [MIT](./LICENSE) (licencia permisiva de código abierto).

Estás autorizado para usar, copiar, modificar y distribuir el software libremente, siempre incluyendo el aviso de copyright y sin garantías.

---

Autor del proyecto: Nehuen Lián https://github.com/NehuenLian