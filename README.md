# Learning FastAPI

A repository dedicated for learning FastAPI.

### Setup

1. Setup Python Virtual Environment

   `python -m venv fastapienv`

2. Activate the Virtual Environment

   `fastapienv\Scripts\activate.bat`

3. Install **fastapi**

   `pip install fastapi`

4. Install **uvicorn**

   `pip install "uvicorn[standard]"`

5. To run the server, navigate to project directory and use the command:

   `uvicorn [filename]:[variable name used to initialize FastAPI] --reload`

   Example:

   `uvicorn books:app --reload`

### Projects

- **Project 1 - FastAPI Request Method Logic**
  - Request and Response
  - CRUD Operations
  - HTTP Request Methods
- **Project 2 - Move Fast with FastAPI**
  - Data Validation (using Pydantic V2)
  - Exception Handling
  - Status Codes
  - Swagger Configuration
  - Request Objects
- **Project 3 - Complete RESTful APIs**
  - Full SQL Database
  - Authentication
  - Authorization
  - Hashing Passwords
- **Project 3.5 - Alembic Data Migration**
  - Database Revisions
  - Data Migration
- **Project 4 - MongoDB**
  - NoSQL Database
