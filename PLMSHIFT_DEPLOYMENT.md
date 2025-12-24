# PLMshift Deployment Guide

## What's Been Prepared

✅ **CORS settings** - Temporarily set to allow all origins (`["*"]`) for initial deployment
✅ **Dockerfile** - Created and ready for PLMshift deployment
✅ **Frontend files** - Added TODO comments indicating where to update the API URL

## Next Steps (Manual Actions Required)

### Step 1: Deploy on PLMshift

1. Go to https://plmshift.math.cnrs.fr/ and log in
2. Create a new project/application (or use existing)
3. Choose "Deploy from Dockerfile" or "Import from Git"
4. Point to the `sanmiao_site_backend` directory
5. PLMshift will build and deploy your application
6. **IMPORTANT:** Note the URL PLMshift assigns (e.g., `https://sanmiao-backend.plmshift.math.cnrs.fr`)

### Step 2: Test Deployment

1. Visit `https://your-plmshift-url/health` in a browser
2. You should see: `{"status": "ok"}`
3. If it works, proceed to Step 3

### Step 3: Update CORS in main.py

After you have your PLMshift URL, update `main.py` (lines 9-14):

**Replace:**
```python
allow_origins=["*"],  # Temporary - will restrict after deployment to PLMshift
```

**With:**
```python
allow_origins=[
    "https://norbert.huma-num.fr",
    "https://YOUR-ACTUAL-PLMSHIFT-URL.plmshift.math.cnrs.fr",  # Replace with your actual URL
],
```

### Step 4: Update Frontend API Endpoints

Update both frontend files with your PLMshift URL:

**Files to update:**
- `sanmiao_frontend/en/sanmiao/index.html` (line 228)
- `sanmiao_frontend/fr/sanmiao/index.html` (line 228)

**Replace:**
```javascript
const API = "https://norbert.huma-num.fr/sanmiao/convert";
```

**With:**
```javascript
const API = "https://YOUR-ACTUAL-PLMSHIFT-URL/convert";
```

(Note: Remove the `/sanmiao` path - your backend is at the root on PLMshift)

### Step 5: Redeploy Backend (if needed)

If you updated `main.py` with restricted CORS:
- PLMshift may auto-redeploy if connected to Git
- Or manually trigger a rebuild in the PLMshift dashboard

### Step 6: Final Testing

1. Open your frontend in a browser
2. Try converting a date
3. Verify it successfully calls the PLMshift backend
4. Check that results appear correctly

## Troubleshooting

- **Port issues:** PLMshift sets the `PORT` env var automatically - the Dockerfile handles this
- **Logs:** Check PLMshift dashboard for application logs if something isn't working
- **CORS errors:** Make sure you've updated the CORS settings with the exact PLMshift URL (including `https://`)

