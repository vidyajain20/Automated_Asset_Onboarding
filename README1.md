# Asset Automation Dashboard

A Django-based application for automating asset onboarding, tracking, and management.

## Features
- **Dashboard**: Visual overview of asset status, compliance, and metrics.
- **Bulk Upload**: Upload assets via Excel files with auto-cleanup and validation.
- **Asset Editing**: Edit asset details with form validation.
- **Mock DMR Scan**: Simulates background scanning of assets.
- **Auto-Generation**: Automatically generates Asset IDs and CI Names if missing.

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd Automated_Asset_Onboarding
    ```

2.  **Create a virtual environment** (Optional but recommended):
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations**:
    ```bash
    python manage.py migrate
    ```

## Running the Application

1.  **Start the development server**:
    ```bash
    python manage.py runserver
    ```

2.  **Access the dashboard**:
    Open your browser and navigate to `http://127.0.0.1:8000/`.

## Usage Guide

### Uploading Assets
1.  Go to the **Upload** tab.
2.  Select an Excel file (`.xlsx`).
3.  Ensure columns roughly match: `Serial Number`, `Asset Tag`, `Model Id`, `Model Category`, `Location`, `IP Address`, `Mac Address`.
    - *Note*: CI Name will be auto-generated (`Category-Serial`) if left blank.

### Editing Assets
1.  Click **Edit** on any asset in the dashboard list.
2.  Update fields as necessary.
3.  If you see an error (e.g., Invalid IP), correct the data and Save.

## Project Structure
- `asset_manager/`: Project settings.
- `assets/`: Main application logic (Models, Views, Forms).
- `assets/templates/`: HTML templates for Dashboard, Upload, and Edit pages.
- `db.sqlite3`: Local database file.

