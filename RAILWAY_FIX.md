# Railway Deployment Fix - Manual Steps

Railway is still trying to use Nixpacks instead of Docker. Follow these steps to fix it:

## Option 1: Configure in Railway Dashboard (RECOMMENDED)

1. **Go to your Railway dashboard**
2. **Click on your service**: `ai-resume-scanner-backend`
3. **Go to Settings tab**
4. **Scroll to "Build & Deploy" section**
5. **Set the following:**
   - **Build Command**: Leave empty (Dockerfile will handle it)
   - **Dockerfile Path**: `Dockerfile` (or `backend/Dockerfile` if root is project root)
   - **Root Directory**: `backend`
6. **Make sure "Builder" is set to "Dockerfile"** (not Nixpacks)
7. **Click "Save"**
8. **Go to Deployments tab and click "Redeploy"**

## Option 2: Use Nixpacks with Python (Alternative)

If Docker doesn't work, we can fix Nixpacks:

1. **In Railway dashboard → Settings**
2. **Set Builder to "Nixpacks"**
3. **Add these environment variables:**
   - `PYTHON_VERSION` = `3.9`
   - `NIXPACKS_PYTHON_VERSION` = `3.9`
4. **Set Root Directory**: `backend`
5. **Redeploy**

## Option 3: Use Render.com Instead (Easiest)

If Railway keeps having issues, Render.com is simpler:

1. Go to [render.com](https://render.com)
2. New → Web Service
3. Connect GitHub repo
4. Settings:
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Deploy!

## Quick Test

After redeploying, check if it works:
- Visit: `https://your-backend-url.railway.app/health`
- Should return: `{"status":"ok"}`

