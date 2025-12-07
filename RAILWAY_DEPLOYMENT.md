# Railway Deployment Guide

## How Railway Deployment Works

Railway will automatically redeploy when you push changes to your connected GitHub repository. The setup is now configured to:

1. **Auto-detect Database**: Uses Railway's `DATABASE_URL` environment variable (PostgreSQL)
2. **Auto-seed on First Deploy**: Database is automatically seeded with sample lawyers if empty
3. **Works with Procfile**: Uses `gunicorn run:app` for the web server

## What Happens on Deployment

1. Railway detects your push to GitHub
2. Builds your application
3. Runs the app initialization
4. **Auto-seeds database** if it's empty (first deployment)
5. Starts the web server

## Setup Steps

### 1. Connect Railway to GitHub
- Go to Railway dashboard
- Create new project
- Connect your GitHub repository
- Railway will auto-detect it's a Python app

### 2. Add PostgreSQL Database
- In Railway dashboard, click "New" → "Database" → "Add PostgreSQL"
- Railway automatically sets `DATABASE_URL` environment variable

### 3. Set Environment Variables
- Go to your service → Variables
- Add `SECRET_KEY` (generate a random string)
- `DATABASE_URL` is automatically set by Railway when you add PostgreSQL

### 4. Deploy
- Push your code to GitHub
- Railway will automatically deploy
- Check the logs - you should see "Database is empty. Seeding with sample lawyers..."

## How Auto-Seeding Works

The app now automatically seeds the database on first run:
- Checks if database is empty (no lawyers)
- Only runs in production (when `DATABASE_URL` is set)
- Seeds sample lawyers automatically
- Won't duplicate if lawyers already exist

## Manual Seeding (if needed)

If automatic seeding doesn't work:

1. Go to Railway dashboard → Your service
2. Click "Deployments" → Select latest deployment
3. Click "View Logs" to see if seeding ran
4. Or use Railway CLI:
   ```bash
   railway run python seed_db.py
   ```

## Troubleshooting

### Lawyers not showing?
1. Check Railway deployment logs
2. Look for "Database is empty. Seeding..." message
3. Verify `DATABASE_URL` is set in environment variables
4. Manually run: `railway run python seed_db.py`

### Database connection errors?
1. Verify PostgreSQL service is running in Railway
2. Check `DATABASE_URL` is set (Railway sets this automatically)
3. Ensure `psycopg2-binary` is in requirements.txt (it is)

### Accounts not working?
- Local SQLite accounts ≠ Railway PostgreSQL accounts
- Create new accounts on the deployed site
- The database is separate from your local one

## Key Differences from Local

- **Database**: PostgreSQL (Railway) vs SQLite (local)
- **Environment**: Production vs Development
- **Auto-seeding**: Happens automatically on first deploy
- **Data persistence**: Data persists between deployments

## Redeploying

Railway automatically redeploys when you:
- Push to your connected GitHub branch
- Manually trigger redeploy from dashboard

The database seeding only runs if the database is empty, so redeploying won't duplicate lawyers.

