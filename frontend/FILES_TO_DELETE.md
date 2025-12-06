# Files to Delete (Migration from HTML to React)

## ❌ DELETE These Files

These are the old HTML/CSS/JS files that are no longer needed:

```bash
# Old static files (not in use anymore)
styles.css
script.js
README_FRONTEND.md

# Streamlit app (if you're fully switching to React)
app.py
static/style.css
```

## ✅ KEEP These Files

React application files:

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── Header.css
│   │   ├── Sidebar.jsx
│   │   ├── Sidebar.css
│   │   ├── ChatArea.jsx
│   │   ├── ChatArea.css
│   │   ├── InputArea.jsx
│   │   ├── InputArea.css
│   │   ├── Toast.jsx
│   │   └── Toast.css
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   └── index.css
├── index.html (React version)
├── vite.config.js
├── package.json
└── README.md
```

## 🗑️ Quick Cleanup Command

Run this to delete old files:

```bash
cd /home/aryan-dhanuka/AI_Chatbot_using_LLMs/frontend
rm -f styles.css script.js README_FRONTEND.md
```

## ⚠️ Optional: Keep Streamlit App

If you want to keep both frontends:
- Keep `app.py` and `static/style.css` for Streamlit
- Run Streamlit on a different port: `streamlit run app.py --server.port 8501`
- Run React on port 3000: `npm run dev`

## 📝 Summary

**Delete:**
- `styles.css` (old CSS)
- `script.js` (old JavaScript)
- `README_FRONTEND.md` (old README)

**Keep:**
- Everything in `src/` folder
- `index.html` (React version)
- `vite.config.js`
- `package.json`
- `README.md` (new README)
