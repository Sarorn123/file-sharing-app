# File Sharing Application

A web application for securely sharing files, built with a FastAPI backend and a React frontend.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Running the Project](#running-the-project)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- User authentication with secure token-based access.
- File upload and download functionality.
- Set files as public or private.
- Responsive user interface.

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React (JavaScript/TypeScript)
- **Database**: TBD (e.g., PostgreSQL, MongoDB, SQLite)

## Setup Instructions

### Backend Setup (FastAPI)

1. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   ```

2. **Dependency**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Dev**:

```bash
  fastapi dev main.py
```

### Front End Setup (React + Vite)

1. **Dependency**:

   ```bash
   cd ui
   ```

   ```bash
   npm install
   ```

1. **Dev**:
   ```bash
   npm run dev
   ```
