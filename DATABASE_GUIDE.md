# Database Guide

## How to Open SQLite Database

### Method 1: Using SQLite Command Line
```bash
sqlite3 lawyerconnect.db
```

Once inside, you can run SQL commands:
```sql
.tables                    -- List all tables
.schema                    -- Show database schema
SELECT * FROM user;        -- View all users
SELECT * FROM lawyer_profile;  -- View all lawyers
.quit                      -- Exit
```

### Method 2: Using DB Browser for SQLite (GUI)
1. Download DB Browser for SQLite: https://sqlitebrowser.org/
2. Open the application
3. Click "Open Database"
4. Navigate to `lawyerconnect.db`
5. Browse tables and data visually

### Method 3: Using Python
```python
import sqlite3

conn = sqlite3.connect('lawyerconnect.db')
cursor = conn.cursor()

# View all users
cursor.execute("SELECT * FROM user")
print(cursor.fetchall())

# View all lawyers
cursor.execute("SELECT * FROM lawyer_profile")
print(cursor.fetchall())

conn.close()
```

## Render Deployment Issues

### Problem
- Render uses PostgreSQL (not SQLite)
- The SQLite database file from GitHub doesn't work on Render
- Fresh PostgreSQL database = no existing data
- Need to seed the database on deployment

### Solution
The database will be automatically seeded on first deployment using the release command in Procfile.

