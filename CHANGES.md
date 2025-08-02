# CHANGES.md – Retain Coding Challenge

## ✅ Major Issues Identified
- 🔓 SQL Injection risk due to raw queries
- 🔐 Plaintext passwords
- 😱 No input validation
- 🧨 All logic inside a single file (`app.py`)
- 💀 Missing proper error handling & status codes
- ❌ Poor API response structure (string, not JSON)

## ✅ Changes Made
- Restructured code into modular folders: `routes`, `utils`, `database`
- Secured SQL queries with parameterized queries
- Used `bcrypt` to hash passwords
- Added validators for email format and password strength
- Replaced string responses with proper JSON and status codes
- Implemented clean error handling with `try/except`
- Added basic unit tests using `unittest`

## 🔧 Tools Used
- ChatGPT for guidance and best practices
- Flask, sqlite3, bcrypt, unittest
- Postman for API testing

## 💭 Trade-Offs / Assumptions
- Assumed SQLite is fine for demo; would switch to PostgreSQL in prod
- Didn’t include pagination or JWT for simplicity
- No Dockerization as per scope

## 🚀 If I Had More Time
- Add pagination and filtering
- Migrate to FastAPI for better performance
- Add JWT-based authentication
- Use environment variables (`.env`)
- Write more robust test coverage
