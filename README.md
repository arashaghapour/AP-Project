# Skin Shop - E-Commerce & Skincare Analysis Platform

Skin Shop is a modern, full-stack web application designed for a cosmetics and skincare store. Built on top of **FastAPI** and **SQLAlchemy**, it doesn't just sell products—it features an advanced skin assessment system. Users can take an interactive quiz or upload a selfie to analyze their skin attributes, helping the app generate highly personalized skincare routines dynamically mapped out of a seed database of 1,000 products.

## Features

- **Automated Database Seeding**: On the very first startup, the application automatically populates the SQLite database with 1,000 randomized skincare items across various categories (cleansers, serums, moisturizers), targeted skin types, and skin concerns.
- **AI Skin Analysis & Quiz**: Integrates an interactive questionnaire and third-party AI skin analysis via image upload to determine user skin profiles (oily, dry, sensitive, etc.).
- **Smart Product Discovery**: Dynamic full-text searching and database logging of user browsing interaction types (`view`).
- **Complete Shopping Workflow**: User authentication (Signup/Login) with hashed credentials via PassLib, interactive store browsing, product details view, persistent Cart tracking, and simulated inventory-checked checkouts.
- **Modern Template Architecture**: Utilizes FastAPI Jinja2 HTML rendering compliant with updated asynchronous routing specifications.

---

## Tech Stack

- **Backend Framework**: FastAPI (Python)
- **ORM / Database**: SQLAlchemy with SQLite
- **Template Engine**: Jinja2 Templates (HTML5 / CSS3 / JavaScript frontend)
- **Security & Auth**: HTTPBearer, JWT Tokens, PassLib (Bcrypt)
- **Data Validation**: Pydantic v2

---

## Project Structure

```text
├── mlenv/                  # Virtual environment folder (auto-generated)
├── src/
│   ├── main.py             # Main application entry point & API Router
│   ├── models.py           # SQLAlchemy Database models 
│   ├── schemas.py          # Pydantic data validation schemas
│   ├── database.py         # Database engine and session configurations
│   ├── utils.py            # Quiz analysis and business logic
│   ├── questions.py        # Static quiz structures
│   ├── token_utils.py      # JWT authentication helpers
│   ├── search.py           # Database search operations
│   └── add_product_to_routin.py  # Skincare routine generation logic
├── static/                 # Static assets (CSS, JS, Images)
├── templates/              # HTML frontend layouts (shop, login, product, cart)
├── requirements.txt        # Project dependencies
├── windows_start.bat               # Single-click execution script for Windows
└── linux_start.sh          # Shell execution script for Linux/Mac
```
## Quick Start & Installation
Befor everything download the images that project need on https://drive.iust.ac.ir/index.php/s/AWw7GJBPaSkmrnx and extract the images folder into static folder then getting the environment ready and starting the server requires no manual setup. Automation scripts handle virtual environment creation, pip upgrades, dependency installation, and server launching.

## On Windows
Simply double-click the execution batch file located in the root directory:
```bash
start_windows.bat
```
## On Linux / macOS
1.Open your terminal in the project's root directory.

2.Grant executable permissions to the shell script:
```bash
chmod +x linux_start.sh
```
3.Run the script:
```bash
./linux_start.sh
```
