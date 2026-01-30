# 🚀 GitHub Events Dashboard - Complete Setup Guide

> **Real-time GitHub webhook receiver** that captures **Push**, **Pull Request**, and **Merge** events, stores them in **MongoDB**, and displays them in a **beautiful live-updating UI** (15s auto-refresh).

[

## ✨ Features

- ✅ **Push events**: `{author} pushed to {branch}`
- ✅ **Pull Request events**: `{author} submitted PR {from} → {to}`
- ✅ **Merge events** (Brownie points!): `{author} merged {from} → {to}`
- ✅ **Live UI** - Auto-refreshes every 15 seconds
- ✅ **Beautiful design** - Glass morphism + hover effects
- ✅ **Production-ready** - Clean Flask architecture
- ✅ **Real GitHub webhook integration**

## 📋 Prerequisites

| Required | Tool | Install Command |
|----------|------|-----------------|
| ✅ | **Python 3.8+** | `python3 --version` |
| ✅ | **MongoDB Atlas** | Free cloud DB (sign up) |
| ✅ | **ngrok** | `brew install ngrok` or download |
| ❌ | **Git** | Already have GitHub |
| ❌ | **Postman/curl** | For testing |

***

## 🚀 Quick Start (5 Minutes)

### **1. Clone & Install Dependencies**
```bash
# Clone webhook-repo
git clone https://github.com/YOUR_USERNAME/webhook-repo.git
cd webhook-repo

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### **2. Setup MongoDB Atlas (Free)**
```bash
# 1. Go to https://cloud.mongodb.com → Create Free Cluster
# 2. Create Database User: webhookuser / CRzFnZIzVkszEJBD
# 3. Network Access → Add IP: 0.0.0.0/0
# 4. Connection String:
MONGO_URI="mongodb+srv://webhookuser:CRzFnZIzVkszEJBD@cluster0.aqykpy4.mongodb.net/github_webhooks"
```

**Update `app/extensions.py`:**
```python
MONGO_URI = "mongodb+srv://webhookuser:CRzFnZIzVkszEJBD@cluster0.aqykpy4.mongodb.net/github_webhooks"
```

### **3. Run Flask App**
```bash
# Terminal 1: Start Flask
python app.py
# See: "MongoDB connected successfully!" → http://localhost:8000
```

### **4. Test with curl (Verify Working)**
```bash
# Terminal 2: Test PUSH
curl -X POST http://localhost:8000/webhook/receiver \
  -H "X-GitHub-Event: push" \
  -H "Content-Type: application/json" \
  -d '{"pusher":{"name":"test-user"},"ref":"refs/heads/main","head_commit":{"timestamp":"2026-01-30T23:10:00Z"}}'

# Check UI: http://localhost:8000/events
# See: "test-user pushed to main"
```

### **5. Expose with ngrok + GitHub Integration**
```bash
# Terminal 3: ngrok (keep Flask running)
ngrok http 8000
# Copy HTTPS URL: https://abc123.ngrok-free.dev
```

**GitHub Setup:**
```
1. Create new repo: action-repo
2. action-repo → Settings → Webhooks → Add webhook
3. Payload URL: https://abc123.ngrok-free.dev/webhook/receiver
4. Content type: application/json
5. Events: ☑️ Push ☑️ Pull requests
```

### **6. Test Real GitHub Events**
```bash
cd action-repo
echo "# Test" >> README.md
git add . && git commit -m "Test webhook" && git push origin main

# Watch Flask logs + UI updates LIVE! ✨
```

***

## 🧪 Manual Testing (All 3 Scenarios)

| Scenario | Command |
|----------|---------|
| **PUSH** | `git commit -m "test" && git push` |
| **PULL REQUEST** | `git checkout -b feat/test && git push && Create PR` |
| **MERGE** | `GitHub: PR → Merge pull request` |

**Expected UI (newest first):**
```
"merge-user" merged feature/test → main     [23:14]
"test-user" submitted PR feature/test → main [23:12] 
"test-user" pushed to main                  [23:10]
```

***

## 📁 Project Structure

```
webhook-repo/
├── app/
│   ├── controllers/     # Flask routes
│   ├── services/        # Business logic
│   ├── repositories/    # MongoDB layer
│   ├── extensions.py    # MongoDB config
│   └── templates/
│       └── events.html  # Live dashboard
├── app.py               # Entry point
├── requirements.txt
└── README.md
```

***

## 🔧 Configuration

| File | Setting | Value |
|------|---------|-------|
| `app/extensions.py` | `MONGO_URI` | MongoDB Atlas connection string |
| `app.py` | `PORT` | `8000` |
| GitHub Webhook | `Payload URL` | `https://your-ngrok-url.ngrok-free.dev/webhook/receiver` |

***

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **"Waiting for events"** | Run `list(cursor)` fix in `get_recent_events()` |
| **GitHub webhook RED** | Check `action-repo → Settings → Webhooks → Recent Deliveries` |
| **415 Error** | `request.get_json(force=True)` in controller |
| **No data in UI** | Verify `db.github_events.find()` in MongoDB |
| **ngrok fails** | Use **HTTPS** URL only |

**Debug Commands:**
```bash
# Check MongoDB data
mongo "your-mongo-uri" --eval 'db.github_events.find().sort({timestamp:-1}).limit(3)'

# Test webhook
curl -X POST http://localhost:8000/webhook/receiver -H "X-GitHub-Event: push" ...
```

***

## 📤 Submission Checklist

```
✅ [ ] webhook-repo: https://github.com/YOUR_USERNAME/webhook-repo
✅ [ ] action-repo: https://github.com/YOUR_USERNAME/action-repo  
✅ [ ] Live demo: https://abc123.ngrok-free.dev/events
✅ [ ] 3 events visible (Push/PR/Merge)
✅ [ ] 15s auto-refresh working
✅ [ ] Clean, modern UI
✅ [ ] README with setup instructions
```

***

## 🎉 Success Screenshots

**Expected UI:**
```
Header: "Auto-refreshing every 15 seconds ⏰ | Found 3 events"
[Green] push-user pushed to main
[Blue] test-user submitted PR feat → main  
[Purple] merge-user merged feat → main
```

**Flask Logs:**
```
🚀 GITHUB WEBHOOK RECEIVED!
📨 Event type: push/pull_request/merge
💾 Saved event ID: 697ce...
📊 Found 3 events in DB
```

***

**Built for production. Ready for interviews. 100% complete! 🚀**

*⭐ Star this repo if it helped you!*
