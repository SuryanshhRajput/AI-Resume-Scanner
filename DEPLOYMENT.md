# Free Hosting Deployment Guide

This guide will help you deploy your AI Resume Scanner application completely free using free hosting services.

## 🎯 Recommended Setup: Vercel (Frontend) + Railway (Backend)

### Why This Setup?
- **Vercel**: Free tier with unlimited deployments, great for React/Vite
- **Railway**: $5/month free credit (effectively free for low-traffic apps)
- **Both**: Easy setup, automatic deployments from GitHub

---

## 📋 Prerequisites

1. **GitHub Account** - Both services deploy from GitHub
2. **Git Repository** - Your code should be in a GitHub repository
3. **Basic Setup** - Make sure your code is committed and pushed to GitHub

---

## 🚀 Step 1: Deploy Backend to Railway (Free)

### 1.1 Sign Up for Railway
1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Sign up with GitHub (recommended for easy repo access)

### 1.2 Deploy Backend
1. In Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Connect your GitHub account if not already connected
4. Select your repository: `AI Resume Scanner`
5. Railway will auto-detect Python, but you need to configure:
   - Click on the service that was created
   - Go to **Settings** tab
   - Set **Root Directory** to: `backend`
   - Railway will automatically detect `requirements.txt` and `railway.json`

### 1.3 Get Backend URL
1. Once deployed, Railway will give you a URL like: `https://your-app-name.up.railway.app`
2. Click on your service → **Settings** → **Generate Domain**
3. Copy the URL (e.g., `https://your-backend.railway.app`) - you'll need this next!

### 1.4 (Optional) Add Environment Variables
If you have an OpenAI API key for the chat feature:
1. In Railway, go to your service → **Variables**
2. Add: `OPENAI_API_KEY` = `your-api-key-here`
3. This keeps your API key secure (server-side only)

---

## 🌐 Step 2: Deploy Frontend to Vercel (Free)

### 2.1 Sign Up for Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click "Sign Up" and sign in with GitHub

### 2.2 Deploy Frontend
1. In Vercel dashboard, click **"Add New..."** → **"Project"**
2. Import your GitHub repository: `AI Resume Scanner`
3. Vercel will auto-detect Vite/React settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `dist` (auto-detected)
   - **Install Command**: `npm install` (auto-detected)

### 2.3 Add Environment Variable
**CRITICAL STEP**: Connect your frontend to your backend!

1. In Vercel project settings, go to **Settings** → **Environment Variables**
2. Click **"Add New"**
3. Add:
   - **Name**: `VITE_BACKEND_URL`
   - **Value**: `https://your-backend.railway.app` (the URL from Step 1.3)
   - **Environment**: Select all (Production, Preview, Development)
4. Click **"Save"**

### 2.4 Deploy
1. Click **"Deploy"** button
2. Wait for deployment to complete (~2-3 minutes)
3. Vercel will give you a URL like: `https://your-app.vercel.app`

### 2.5 Redeploy (if you added env vars after first deploy)
1. Go to **Deployments** tab
2. Click the **"..."** menu on latest deployment
3. Click **"Redeploy"**

---

## ✅ Step 3: Test Your Deployment

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Try uploading a PDF resume
3. The analysis should work! 🎉

---

## 🔄 Alternative Free Hosting Options

### Option 2: Render (Both Frontend & Backend)

**Backend on Render:**
1. Go to [render.com](https://render.com) and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub repo
4. Configure:
   - **Name**: `ai-resume-scanner-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (spins down after 15 min inactivity)
5. Get the URL and add to Vercel env vars as `VITE_BACKEND_URL`

**Frontend on Render:**
1. In Render, click **"New +"** → **"Static Site"**
2. Connect GitHub repo
3. Configure:
   - **Name**: `ai-resume-scanner-frontend`
   - **Root Directory**: `./`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. Add environment variable: `VITE_BACKEND_URL` = your backend URL

### Option 3: Netlify (Frontend) + Fly.io (Backend)

**Backend on Fly.io:**
1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Sign up: `fly auth signup`
3. In your project root, run:
   ```bash
   cd backend
   fly launch
   ```
4. Follow prompts, Fly.io will auto-detect Python
5. Get URL and add to Netlify env vars

**Frontend on Netlify:**
1. Go to [netlify.com](https://netlify.com)
2. **"Add new site"** → **"Import an existing project"**
3. Connect GitHub repo
4. Build settings:
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
5. Add environment variable: `VITE_BACKEND_URL`

---

## 🔧 Troubleshooting

### Backend Issues

**"Failed to fetch" error:**
- Check that backend URL in Vercel env vars is correct (no trailing slash)
- Verify backend is running: Visit `https://your-backend.railway.app/health`
- Should return: `{"status":"ok"}`

**Backend not starting:**
- Check Railway/Render logs
- Verify `requirements.txt` is in `backend/` directory
- Make sure `Procfile` or start command is correct

**CORS errors:**
- Backend already has CORS enabled for all origins (`allow_origins=["*"]`)
- If issues persist, check backend logs

### Frontend Issues

**Environment variable not working:**
- Make sure variable name is exactly: `VITE_BACKEND_URL` (case-sensitive)
- Redeploy after adding env vars
- Check Vercel deployment logs

**Build failures:**
- Check Vercel build logs
- Ensure all dependencies are in `package.json`
- Try clearing Vercel cache and redeploying

---

## 📝 Important Notes

1. **Free Tier Limitations:**
   - **Railway**: $5/month credit (usually enough for small apps)
   - **Render**: Free tier spins down after 15 min inactivity (slow first request)
   - **Vercel**: Unlimited deployments, 100GB bandwidth/month

2. **Environment Variables:**
   - Always add `VITE_BACKEND_URL` to your frontend hosting service
   - Never commit `.env` files with secrets to GitHub
   - Use hosting service's environment variable settings

3. **Automatic Deployments:**
   - Both Vercel and Railway auto-deploy on git push
   - Make sure to push changes to trigger new deployments

4. **Domain Names:**
   - Both services provide free subdomains
   - You can add custom domains later (paid feature on some platforms)

---

## 🎉 Success!

Once deployed, your app will be live at:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-backend.railway.app`

Share your app URL with others! 🚀
