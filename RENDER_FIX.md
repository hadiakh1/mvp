# Render Deployment Fix

## Problem
Render is trying to run `gunicorn app:app` but it should be `gunicorn run:app`

## Solution

### Option 1: Use render.yaml (Recommended)
I've created a `render.yaml` file that explicitly sets the start command:
```yaml
startCommand: gunicorn --bind 0.0.0.0:$PORT run:app
```

### Option 2: Set Start Command in Render Dashboard
1. Go to Render Dashboard → Your Service
2. Click "Settings"
3. Scroll to "Start Command"
4. Set it to: `gunicorn --bind 0.0.0.0:$PORT run:app`
5. Save and redeploy

### Option 3: Verify Procfile
The Procfile should contain:
```
web: gunicorn --bind 0.0.0.0:$PORT run:app
```

## Why This Happens
- Render might not be reading the Procfile correctly
- Or there's a configuration override in Render dashboard
- The `render.yaml` file ensures the correct command is used

## After Fix
1. Push changes to GitHub
2. Render will redeploy automatically
3. Check logs - should see app starting successfully

