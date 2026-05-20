# 📤 Git Commands Guide - Push to GitHub

This guide provides step-by-step instructions to push your project to GitHub.

## 🔧 Prerequisites

1. **Git installed** - Verify with: `git --version`
2. **GitHub account** - Sign up at https://github.com
3. **Repository created** - https://github.com/AB-1817/Malnutrition-Prediction-and-Analysis-System.git

---

## 🚀 Initial Setup (First Time Only)

### Step 1: Configure Git (if not already done)

```bash
# Set your name
git config --global user.name "Your Name"

# Set your email (use GitHub email)
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list
```

### Step 2: Navigate to Project Directory

```bash
cd e:\FoodSafety_Malnutrition
```

---

## 📦 Prepare Repository for Push

### Step 1: Initialize Git Repository

```bash
# Initialize git (if not already initialized)
git init
```

### Step 2: Add Remote Repository

```bash
# Add GitHub repository as remote
git remote add origin https://github.com/AB-1817/Malnutrition-Prediction-and-Analysis-System.git

# Verify remote
git remote -v
```

### Step 3: Check Current Status

```bash
# See which files will be committed
git status
```

---

## 📝 Stage and Commit Files

### Step 1: Add Files to Staging

```bash
# Add all files (respects .gitignore)
git add .

# Or add specific files/folders
git add README.md
git add requirements.txt
git add streamlit_app.py
git add FoodSafety_Malnutrition/
git add monitoring/
git add docker-compose.yml
git add Dockerfile
```

### Step 2: Verify Staged Files

```bash
# Check what's staged
git status

# See detailed changes
git diff --staged
```

### Step 3: Commit Changes

```bash
# Commit with descriptive message
git commit -m "Initial commit: Complete malnutrition prediction system with ML models, API, and dashboard"
```

---

## 🚀 Push to GitHub

### Option 1: Push to Main Branch (Recommended)

```bash
# Push to main branch
git push -u origin main
```

### Option 2: Push to Master Branch (if main doesn't exist)

```bash
# Rename branch to main (if needed)
git branch -M main

# Push to main
git push -u origin main
```

### If Authentication Required:

**For HTTPS (recommended):**
```bash
# You'll be prompted for username and password
# Use Personal Access Token (PAT) instead of password
```

**Generate Personal Access Token:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `workflow`
4. Copy token and use as password

**For SSH (alternative):**
```bash
# Change remote to SSH
git remote set-url origin git@github.com:AB-1817/Malnutrition-Prediction-and-Analysis-System.git

# Push
git push -u origin main
```

---

## 🔄 Subsequent Updates

After initial push, use these commands for updates:

### Step 1: Check Status
```bash
git status
```

### Step 2: Add Changes
```bash
# Add all changes
git add .

# Or add specific files
git add path/to/file.py
```

### Step 3: Commit
```bash
git commit -m "Description of changes"
```

### Step 4: Push
```bash
git push
```

---

## 📋 Common Git Commands

### View History
```bash
# View commit history
git log

# View compact history
git log --oneline

# View last 5 commits
git log -5
```

### Undo Changes
```bash
# Unstage file
git reset HEAD file.py

# Discard local changes
git checkout -- file.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

### Branching
```bash
# Create new branch
git checkout -b feature/new-feature

# Switch branch
git checkout main

# List branches
git branch

# Delete branch
git branch -d feature/old-feature
```

### Pull Latest Changes
```bash
# Pull from remote
git pull origin main

# Pull with rebase
git pull --rebase origin main
```

---

## 🗂️ What Gets Pushed?

Based on `.gitignore`, these files **WILL BE** pushed:

✅ **Source Code:**
- `streamlit_app.py`
- `FoodSafety_Malnutrition/api/*.py`
- `monitoring/*.py`
- All Python scripts

✅ **Configuration:**
- `requirements.txt`
- `docker-compose.yml`
- `Dockerfile`
- `.dockerignore`

✅ **Documentation:**
- `README.md`
- `SETUP.md`
- `CONTRIBUTING.md`
- `LICENSE`
- All `.md` files

✅ **Notebooks:**
- `FoodSafety_Malnutrition/notebooks/*.ipynb`

✅ **Assets:**
- `FoodSafety_Malnutrition/assets/favicon.svg`

---

## 🚫 What Gets Ignored?

Based on `.gitignore`, these files **WILL NOT BE** pushed:

❌ **Virtual Environments:**
- `.venv/`, `.venv-1/`, `.venv-2/`, etc.

❌ **Large Model Files:**
- `*.h5`, `*.pkl`, `*.joblib`

❌ **Data Files:**
- `*.csv`, `*.xlsx` (except specific ones)

❌ **Generated Images:**
- `*.png`, `*.jpg` (except favicon)

❌ **Logs:**
- `*.log`, `*.out`, `*.err`

❌ **Environment Variables:**
- `.env`, `.env.txt`

❌ **IDE Files:**
- `.vscode/`, `.idea/`, `.claude/`

---

## 📦 Handling Large Files

### Option 1: Git LFS (Large File Storage)

For model files and datasets:

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.h5"
git lfs track "*.pkl"
git lfs track "*.csv"

# Add .gitattributes
git add .gitattributes

# Commit and push
git commit -m "Add Git LFS tracking"
git push
```

### Option 2: External Storage

Upload large files to:
- **Google Drive** - Share link in README
- **AWS S3** - Public bucket
- **Hugging Face** - Model hosting
- **Kaggle Datasets** - Public datasets

Update README with download links.

---

## 🔍 Verify Push Success

### Check on GitHub:

1. Visit: https://github.com/AB-1817/Malnutrition-Prediction-and-Analysis-System
2. Verify files are present
3. Check README renders correctly
4. Ensure notebooks display properly

### Check Locally:

```bash
# View remote branches
git branch -r

# View last commit
git log -1

# Check remote status
git remote show origin
```

---

## 🐛 Troubleshooting

### Issue: "Permission denied"

**Solution:**
```bash
# Use Personal Access Token
# Or set up SSH keys
ssh-keygen -t ed25519 -C "your.email@example.com"
# Add SSH key to GitHub account
```

### Issue: "Repository not found"

**Solution:**
```bash
# Verify remote URL
git remote -v

# Update remote URL
git remote set-url origin https://github.com/AB-1817/Malnutrition-Prediction-and-Analysis-System.git
```

### Issue: "Failed to push some refs"

**Solution:**
```bash
# Pull first, then push
git pull origin main --rebase
git push origin main
```

### Issue: "Large files detected"

**Solution:**
```bash
# Remove large files from commit
git rm --cached large_file.h5

# Add to .gitignore
echo "*.h5" >> .gitignore

# Commit and push
git commit -m "Remove large files"
git push
```

### Issue: "Merge conflict"

**Solution:**
```bash
# Pull and resolve conflicts
git pull origin main

# Edit conflicted files
# Remove conflict markers (<<<<, ====, >>>>)

# Add resolved files
git add .

# Commit merge
git commit -m "Resolve merge conflicts"

# Push
git push
```

---

## 📊 Complete Push Workflow

Here's the complete workflow in one script:

```bash
# Navigate to project
cd e:\FoodSafety_Malnutrition

# Initialize git (if needed)
git init

# Add remote
git remote add origin https://github.com/AB-1817/Malnutrition-Prediction-and-Analysis-System.git

# Check status
git status

# Add all files
git add .

# Commit
git commit -m "Initial commit: Complete malnutrition prediction system

- Added 13 Jupyter notebooks for ML pipeline
- Implemented Flask REST API with 8 endpoints
- Created Streamlit dashboard with 8 pages
- Included 15+ trained ML/DL models
- Added Docker deployment configuration
- Comprehensive documentation and setup guides
- Team: Akash Bhuyan, Rushikesh Kedar, Sujal Khandelwal, Namrata Ingole, Rutuja Shelke"

# Push to GitHub
git push -u origin main

# Verify
git log -1
```

---

## 🎯 Best Practices

1. **Commit Often**: Make small, focused commits
2. **Write Clear Messages**: Describe what and why
3. **Pull Before Push**: Avoid conflicts
4. **Use Branches**: For new features
5. **Review Changes**: Before committing
6. **Keep .gitignore Updated**: Exclude unnecessary files
7. **Tag Releases**: Use semantic versioning

### Commit Message Format:

```
Type: Brief description (50 chars max)

Detailed explanation of changes (if needed)
- Bullet point 1
- Bullet point 2

Fixes #issue_number
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

---

## 📚 Additional Resources

- **Git Documentation**: https://git-scm.com/doc
- **GitHub Guides**: https://guides.github.com/
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf
- **Pro Git Book**: https://git-scm.com/book/en/v2

---

## ✅ Final Checklist

Before pushing, ensure:

- [ ] README.md is complete and accurate
- [ ] .gitignore excludes sensitive files
- [ ] requirements.txt is up-to-date
- [ ] Documentation is clear
- [ ] Large files are handled properly
- [ ] Sensitive data is removed
- [ ] Code is tested and working
- [ ] Commit messages are descriptive

---

**Ready to push! 🚀**

```bash
git push -u origin main
```

**Your project is now live on GitHub! 🎉**
