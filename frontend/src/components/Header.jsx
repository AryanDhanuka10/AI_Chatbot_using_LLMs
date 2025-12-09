import { Sun, Moon } from 'lucide-react'
import { useState, useEffect } from 'react'
import './Header.css'

function Header() {
    const [isDarkMode, setIsDarkMode] = useState(() => {
        // Check localStorage first
        const saved = localStorage.getItem('darkMode')
        if (saved !== null) {
            return JSON.parse(saved)
        }
        // If no saved preference, check system preference
        return window.matchMedia('(prefers-color-scheme: dark)').matches
    })

    useEffect(() => {
        // Apply theme to document
        document.documentElement.setAttribute('data-theme', isDarkMode ? 'dark' : 'light')
        document.body.classList.toggle('dark-mode', isDarkMode)

        // Save to localStorage
        localStorage.setItem('darkMode', JSON.stringify(isDarkMode))
    }, [isDarkMode])

    const toggleTheme = () => {
        setIsDarkMode(!isDarkMode)
    }

    return (
        <>
            {/* Fixed theme toggle button at top-right */}
            <button
                className="theme-toggle-fixed"
                onClick={toggleTheme}
                title={isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
                aria-label={isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
            >
                {isDarkMode ? <Sun size={18} /> : <Moon size={18} />}
            </button>

            <header className="header">
                <div className="header-content">
                    <div className="header-brand">
                        <div className="logo">🤖</div>
                        <div className="header-text">
                            <h1 className="header-title">AI Chatbot Using LLMs</h1>
                            <p className="header-subtitle">Multi-Domain Intelligent Assistant</p>
                        </div>
                    </div>
                </div>
            </header>
        </>
    )
}

export default Header
