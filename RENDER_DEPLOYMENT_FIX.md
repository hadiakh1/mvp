# Render Deployment Fix Guide

## Problem Summary

1. **Database Type Mismatch**: Render uses PostgreSQL, but your local database is SQLite
2. **Empty Database**: Render creates a fresh PostgreSQL database on each deployment
3. **No Data Migration**: The SQLite database file from GitHub doesn't work on Render
4. **Missing Lawyers**: Database is empty, so no lawyers show up

## Solutions Implemented

### 1. Fixed Database URL Configuration
- Updated `app/config.py` to handle Render's PostgreSQL URL format
- Converts `postgres://` to `postgresql://` (required by SQLAlchemy)
- Falls back to SQLite for local development

### 2. Automatic Database Seeding
- Created `seed_on_deploy.py` script
- Added `release` command to `Procfile`
- Automatically seeds the database with sample lawyers on first deployment

## How It Works

1. **On Render Deployment**:
   - Render runs the `release` command from Procfile
   - `seed_on_deploy.py` checks if database is empty
   - If empty, it runs `seed_db.py` to populate sample lawyers
   - If not empty, it skips seeding (prevents duplicates)

2. **Database Connection**:
   - Render automatically provides `DATABASE_URL` environment variable
   - The app detects this and uses PostgreSQL
   - Local development still uses SQLite

## What You Need to Do

### On Render Dashboard:

1. **Verify Environment Variables**:
   - Go to your Render service → Environment
   - Ensure `DATABASE_URL` is set (Render sets this automatically for PostgreSQL)
   - Add `SECRET_KEY` if not already set (generate a random string)

2. **Redeploy**:
   - Push these changes to GitHub
   - Render will automatically redeploy
   - Check the build logs to see the release command output
   - You should see: "Database is empty. Seeding with sample lawyers..."

3. **Verify Deployment**:
   - After deployment, check your website
   - Lawyers should now appear in the matches
   - You can create new accounts (they'll be stored in PostgreSQL)

## Testing Locally

To test the seeding script locally:
```bash
python seed_on_deploy.py
```

## Manual Database Seeding (if needed)

If automatic seeding doesn't work, you can manually seed via Render Shell:
1. Go to Render Dashboard → Your Service → Shell
2. Run: `python seed_db.py`

## Important Notes

- **Existing Accounts**: Accounts created on localhost (SQLite) won't exist on Render (PostgreSQL)
- **New Database**: Each Render deployment gets a fresh PostgreSQL database
- **Data Persistence**: Data in Render's PostgreSQL database persists between deployments
- **Local vs Production**: Your local SQLite database and Render's PostgreSQL database are separate

## Troubleshooting

### Lawyers still not showing?
1. Check Render build logs for release command output
2. Verify `seed_on_deploy.py` ran successfully
3. Check if database connection is working
4. Manually run `python seed_db.py` via Render Shell

### Database connection errors?
1. Verify `DATABASE_URL` is set in Render environment variables
2. Check that `psycopg2-binary` is in requirements.txt (it is)
3. Ensure PostgreSQL service is running on Render

### Accounts not working?
- Remember: Local SQLite accounts ≠ Render PostgreSQL accounts
- Create new accounts on the deployed site
- Or migrate data from SQLite to PostgreSQL (advanced)

