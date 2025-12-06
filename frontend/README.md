# AI Chatbot - React Frontend

Enterprise-grade React application for AI Chatbot using LLMs with professional SaaS design.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The app will run at `http://localhost:3000`

### 3. Build for Production

```bash
npm run build
```

## 📋 Prerequisites

- **Node.js** 18+ and npm
- **Backend Server** running at `http://127.0.0.1:8000`

## 🎨 Features

✅ **Enterprise Design**
- Professional SaaS aesthetics (Google Cloud inspired)
- Glassmorphism effects
- Smooth animations and transitions
- Fully responsive design

✅ **Core Functionality**
- Real-time chat with AI backend
- Multi-domain support (Education, Coding, Medical, Legal, General)
- File upload for RAG
- Export chat history (JSON/TXT)
- Session management
- Typing indicators

✅ **Modern Stack**
- React 18
- Vite for fast development
- Lucide React icons
- CSS custom properties

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx          # App header
│   │   ├── Header.css
│   │   ├── Sidebar.jsx         # Control panel
│   │   ├── Sidebar.css
│   │   ├── ChatArea.jsx        # Message display
│   │   ├── ChatArea.css
│   │   ├── InputArea.jsx       # Message input
│   │   ├── InputArea.css
│   │   ├── Toast.jsx           # Notifications
│   │   └── Toast.css
│   ├── App.jsx                 # Main app component
│   ├── App.css
│   ├── main.jsx                # Entry point
│   └── index.css               # Global styles & design system
├── index.html                  # HTML template
├── vite.config.js              # Vite configuration
└── package.json                # Dependencies
```

## 🔧 Configuration

### Backend URL

The app uses Vite proxy to connect to the backend. Edit `vite.config.js` if your backend runs on a different port:

```javascript
server: {
  port: 3000,
  proxy: {
    '/chat': {
      target: 'http://127.0.0.1:8000',  // Change this
      changeOrigin: true,
    },
    '/upload': {
      target: 'http://127.0.0.1:8000',  // Change this
      changeOrigin: true,
    },
  },
}
```

### Design Tokens

All design tokens are in `src/index.css`. You can customize:
- Colors
- Typography
- Spacing
- Border radius
- Shadows
- Transitions

## 🎨 Color Palette

**Professional SaaS Theme (Default)**
- Primary: `#1A73E8` (Google Blue)
- Accent: `#34A853` (Green)
- Background: `#0F172A` (Deep Navy)
- Surface: `#1E293B`

## 📱 Responsive Breakpoints

- Desktop: 1920px+
- Laptop: 1024px - 1919px
- Tablet: 768px - 1023px
- Mobile: < 768px

## 🚀 Deployment

### Vercel / Netlify

```bash
npm run build
```

Upload the `dist` folder to your hosting service.

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## 🗑️ Files to Delete (Old HTML Version)

If you're migrating from the HTML version, you can safely delete:

```bash
# Old HTML/CSS/JS files
rm index.html (old version)
rm styles.css
rm script.js
rm README_FRONTEND.md

# Keep only the React app files
```

## 🔍 Troubleshooting

### Backend Connection Issues

1. Ensure backend is running at `http://127.0.0.1:8000`
2. Check CORS is enabled in FastAPI:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Build Errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📦 Dependencies

- **react** - UI library
- **react-dom** - React DOM renderer
- **lucide-react** - Icon library
- **vite** - Build tool
- **@vitejs/plugin-react** - React plugin for Vite

## 🎯 Future Enhancements

- [ ] Speech-to-text integration
- [ ] Theme toggle (Dark/Light)
- [ ] Chat history persistence
- [ ] Markdown rendering in messages
- [ ] Code syntax highlighting
- [ ] Image upload support

## 📄 License

Part of the AI Chatbot using LLMs project.
