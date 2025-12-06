import { useState, useRef, useEffect } from 'react'
import { Send, Settings, Sun, Moon, Paperclip, X, Image } from 'lucide-react'
import './InputArea.css'

function InputArea({ onSendMessage, isTyping, onFileUpload }) {
    const [message, setMessage] = useState('')
    const [showSettings, setShowSettings] = useState(false)
    const [fontSize, setFontSize] = useState('18')
    const [isDarkMode, setIsDarkMode] = useState(false)
    const [selectedFiles, setSelectedFiles] = useState([])
    const textareaRef = useRef(null)
    const fileInputRef = useRef(null)

    const handleSend = () => {
        if (message.trim() || selectedFiles.length > 0) {
            if (selectedFiles.length > 0) {
                onFileUpload(selectedFiles)
            }
            if (message.trim()) {
                onSendMessage(message)
            }
            setMessage('')
            setSelectedFiles([])
        }
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    }

    const handleFontSizeChange = (e) => {
        const newSize = e.target.value
        setFontSize(newSize)
        if (textareaRef.current) {
            textareaRef.current.style.fontSize = `${newSize}px`
        }
    }

    const toggleTheme = () => {
        setIsDarkMode(!isDarkMode)
        document.documentElement.setAttribute('data-theme', !isDarkMode ? 'dark' : 'light')
    }

    const handleFileSelect = (e) => {
        const files = Array.from(e.target.files)
        setSelectedFiles(prev => [...prev, ...files])
    }

    const removeFile = (index) => {
        setSelectedFiles(prev => prev.filter((_, i) => i !== index))
    }

    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto'
            textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px'
        }
    }, [message])

    return (
        <div className="input-area">
            {/* File Preview */}
            {selectedFiles.length > 0 && (
                <div className="file-preview-container">
                    {selectedFiles.map((file, index) => (
                        <div key={index} className="file-preview-item">
                            {file.type.startsWith('image/') ? (
                                <div className="image-preview">
                                    <img src={URL.createObjectURL(file)} alt={file.name} />
                                    <button
                                        className="remove-file-btn"
                                        onClick={() => removeFile(index)}
                                        aria-label="Remove file"
                                    >
                                        <X size={16} />
                                    </button>
                                </div>
                            ) : (
                                <div className="document-preview">
                                    <Paperclip size={20} />
                                    <span className="file-name">{file.name}</span>
                                    <button
                                        className="remove-file-btn"
                                        onClick={() => removeFile(index)}
                                        aria-label="Remove file"
                                    >
                                        <X size={16} />
                                    </button>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}

            <div className="input-container">
                <textarea
                    ref={textareaRef}
                    className="message-input"
                    placeholder="Type your message here..."
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={handleKeyDown}
                    rows={1}
                    style={{ fontSize: `${fontSize}px` }}
                />
                <div className="input-actions">
                    <input
                        ref={fileInputRef}
                        type="file"
                        multiple
                        accept="image/*,.pdf,.txt,.doc,.docx"
                        onChange={handleFileSelect}
                        style={{ display: 'none' }}
                    />
                    <button
                        className="action-btn"
                        onClick={() => fileInputRef.current?.click()}
                        aria-label="Attach files"
                        title="Attach files or images"
                    >
                        <Paperclip size={20} />
                    </button>
                    <button
                        className="action-btn"
                        onClick={() => setShowSettings(!showSettings)}
                        aria-label="Settings"
                        title="Settings"
                    >
                        <Settings size={20} />
                    </button>
                    <button className="send-btn" onClick={handleSend} aria-label="Send message">
                        <Send size={20} />
                    </button>
                </div>
            </div>

            {showSettings && (
                <div className="settings-panel">
                    <h4>Chat Settings</h4>

                    <div className="setting-item">
                        <label className="setting-label">
                            Theme Mode
                        </label>
                        <button className="theme-toggle" onClick={toggleTheme}>
                            {isDarkMode ? <Sun size={18} /> : <Moon size={18} />}
                            <span>{isDarkMode ? 'Light Mode' : 'Dark Mode'}</span>
                        </button>
                    </div>

                    <div className="setting-item">
                        <label className="setting-label">
                            Font Size: {fontSize}px
                        </label>
                        <input
                            type="range"
                            min="14"
                            max="24"
                            value={fontSize}
                            onChange={handleFontSizeChange}
                            className="font-slider"
                        />
                    </div>

                    <div className="setting-item">
                        <label className="setting-checkbox">
                            <input type="checkbox" defaultChecked />
                            Enable auto-scroll
                        </label>
                    </div>

                    <div className="setting-item">
                        <label className="setting-checkbox">
                            <input type="checkbox" defaultChecked />
                            Show timestamps
                        </label>
                    </div>

                    <div className="setting-item">
                        <label className="setting-checkbox">
                            <input type="checkbox" />
                            Enable sound notifications
                        </label>
                    </div>

                    <div className="setting-item">
                        <label className="setting-checkbox">
                            <input type="checkbox" defaultChecked />
                            Show typing indicator
                        </label>
                    </div>
                </div>
            )}

            {isTyping && (
                <div className="typing-indicator">
                    <span className="dot"></span>
                    <span className="dot"></span>
                    <span className="dot"></span>
                    <span className="typing-text">AI is typing...</span>
                </div>
            )}
        </div>
    )
}

export default InputArea
