# Internship Tracker

A lightweight local web app to track internship applications — built with Flask and SQLite, runs entirely on your machine.

## Features

- Add and manage internship applications with a customizable set of fields
- Track status across 5 stages: **Did not apply yet → Applied → Interviewed → Accepted → Rejected**
- Dashboard with live stats and date-range filtering
- Choose which columns appear on the home dashboard
- Default fields pre-filled on every new application: Status, Company, Position, Date Applied, Deadline, Application Link, Location, Duration, Salary

## Project Structure

```
├── app.py          # Flask routes
├── database.py     # SQLite logic
├── tracker.db      # Auto-generated database (created on first run)
├── launch.bat      # One-click launcher (Windows)
└── templates/      # HTML templates
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repo
git clone https://github.com/your-username/internship-tracker.git
cd internship-tracker

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # macOS / Linux

# Install dependencies
pip install flask
```

### Running

**Windows — one click:**
```
launch.bat
```
This activates the virtual environment, starts the server, and opens the app in your browser automatically.

**Manual:**
```bash
python app.py
```
Then open [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Usage

1. Click **Add Application** on the dashboard to create a new entry
2. Open an application to fill in its fields (status, company, dates, etc.)
3. Add custom fields of type `text`, `date`, `number`, or `choice` if needed
4. Use the **column selector** on the dashboard to show/hide fields in the table view
5. Filter entries by date range using the date pickers at the top

## Data

Everything is stored locally in `tracker.db` (SQLite). No account, no cloud, no external dependencies beyond Flask.
