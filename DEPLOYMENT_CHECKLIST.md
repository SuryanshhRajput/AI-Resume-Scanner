# 🚀 Quick Deployment Checklist

Use this checklist to ensure you've completed all steps for deployment.

## Pre-Deployment

- [ ] Code is committed to GitHub
- [ ] All local changes are pushed to GitHub
- [ ] You have a GitHub account
- [ ] You have access to the repository

## Backend Deployment (Railway)

- [ ] Signed up at [railway.app](https://railway.app)
- [ ] Connected GitHub account
- [ ] Created new project from GitHub repo
- [ ] Set root directory to `backend/`
- [ ] Backend deployed successfully
- [ ] Got backend URL (e.g., `https://your-app.railway.app`)
- [ ] Tested backend health endpoint: `https://your-backend-url/health`
- [ ] (Optional) Added `OPENAI_API_KEY` environment variable in Railway

## Frontend Deployment (Vercel)

- [ ] Signed up at [vercel.com](https://vercel.com)
- [ ] Connected GitHub account
- [ ] Created new project from GitHub repo
- [ ] Vercel auto-detected Vite/React settings
- [ ] Added environment variable:
  - Name: `VITE_BACKEND_URL`
  - Value: `https://your-backend.railway.app` (your Railway URL)
  - Environments: All (Production, Preview, Development)
- [ ] Frontend deployed successfully
- [ ] Got frontend URL (e.g., `https://your-app.vercel.app`)

## Testing

- [ ] Visited frontend URL in browser
- [ ] Uploaded a test PDF resume
- [ ] Resume analysis works correctly
- [ ] (If using chat) Chat feature works (may need API key)

## Post-Deployment

- [ ] Bookmarked both URLs
- [ ] Shared the frontend URL with others
- [ ] Verified automatic deployments work (push to GitHub triggers deploy)

## Troubleshooting

If something doesn't work:
- [ ] Check backend logs in Railway dashboard
- [ ] Check frontend build logs in Vercel dashboard
- [ ] Verify `VITE_BACKEND_URL` is correct in Vercel
- [ ] Test backend directly: `https://your-backend-url/health`
- [ ] Check browser console for errors (F12)

---

## 🎉 You're Done!

Your app is now live and accessible to anyone with the frontend URL!

