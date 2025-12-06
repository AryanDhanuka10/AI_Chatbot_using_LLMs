import { useState } from 'react'
import { Plus, Upload, Download, History, Clock } from 'lucide-react'
import './Sidebar.css'

const DOMAINS = ['General', 'Education', 'Coding', 'Medical', 'Legal']

const DOMAIN_ICONS = {
    General: '🌐',
    Education: '📚',
    Coding: '💻',
    Medical: '🏥',
    Legal: '⚖️'
}

function Sidebar({ isOpen, onToggle, domain, onDomainChange, onNewChat, onExport, onFileUpload, sessionId, messageCount, chatHistory, onLoadChat }) {
    const [selectedFiles, setSelectedFiles] = useState([])
    const [isDragging, setIsDragging] = useState(false)

    const handleFileSelect = (e) => {
        const files = Array.from(e.target.files)
        setSelectedFiles(prev => [...prev, ...files])
    }

    const handleDrop = (e) => {
        e.preventDefault()
        setIsDragging(false)
        const files = Array.from(e.dataTransfer.files)
        setSelectedFiles(prev => [...prev, ...files])
    }

    const handleUpload = () => {
        if (selectedFiles.length > 0) {
            onFileUpload(selectedFiles)
            setSelectedFiles([])
        }
    }

    const removeFile = (index) => {
        setSelectedFiles(prev => prev.filter((_, i) => i !== index))
    }

    return (
        <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
            <div className="sidebar-header">
                <h2 className="sidebar-title">AI Controls</h2>
            </div>

            <button className="btn btn-primary" onClick={onNewChat}>
                <Plus size={20} />
                New Chat
            </button>

            <div className="control-group">
                <label className="control-label">Active Domain</label>
                <select
                    className="select-input"
                    value={domain}
                    onChange={(e) => onDomainChange(e.target.value)}
                >
                    {DOMAINS.map(d => (
                        <option key={d} value={d}>
                            {DOMAIN_ICONS[d]} {d}
                        </option>
                    ))}
                </select>
            </div>

            <div className="control-group">
                <h3 className="control-heading">Knowledge Upload</h3>
                <div
                    className={`file-upload-area ${isDragging ? 'dragging' : ''}`}
                    onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                    onDragLeave={() => setIsDragging(false)}
                    onDrop={handleDrop}
                    onClick={() => document.getElementById('fileInput').click()}
                >
                    <Upload size={48} />
                    <p>Click or drag files here</p>
                    <input
                        id="fileInput"
                        type="file"
                        multiple
                        accept=".pdf,.txt,.doc,.docx"
                        onChange={handleFileSelect}
                        style={{ display: 'none' }}
                    />
                </div>

                {selectedFiles.length > 0 && (
                    <div className="file-list">
                        {selectedFiles.map((file, index) => (
                            <div key={index} className="file-item">
                                <span className="file-item-name">{file.name}</span>
                                <button
                                    className="file-item-remove"
                                    onClick={() => removeFile(index)}
                                    aria-label="Remove file"
                                >
                                    ×
                                </button>
                            </div>
                        ))}
                    </div>
                )}

                <button
                    className="btn btn-secondary"
                    onClick={handleUpload}
                    disabled={selectedFiles.length === 0}
                >
                    Upload to RAG
                </button>
            </div>

            <div className="control-group">
                <h3 className="control-heading">Export Chat</h3>
                <div className="btn-group">
                    <button className="btn btn-secondary btn-small" onClick={() => onExport('json')}>
                        <Download size={16} />
                        JSON
                    </button>
                    <button className="btn btn-secondary btn-small" onClick={() => onExport('txt')}>
                        <Download size={16} />
                        TXT
                    </button>
                </div>
            </div>

            {/* Chat History */}
            {chatHistory && chatHistory.length > 0 && (
                <div className="control-group">
                    <div className="control-heading">
                        <History size={18} style={{ display: 'inline', marginRight: '8px' }} />
                        Recent Chats
                    </div>
                    <div className="chat-history-list">
                        {chatHistory.map((chat) => (
                            <div
                                key={chat.id}
                                className="history-item"
                                onClick={() => onLoadChat(chat)}
                            >
                                <div className="history-header">
                                    <span className="history-domain">{DOMAIN_ICONS[chat.domain]} {chat.domain}</span>
                                    <span className="history-count">{chat.messageCount} msgs</span>
                                </div>
                                <div className="history-preview">{chat.preview}</div>
                                <div className="history-time">
                                    <Clock size={12} />
                                    {new Date(chat.timestamp).toLocaleString()}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Session Info */}
            <div className="control-group">
                <h3 className="control-heading">Session Info</h3>
                <div className="session-info">
                    <p className="info-item">
                        <span className="info-label">Session ID:</span>
                        <span className="info-value">{sessionId.substring(0, 16)}...</span>
                    </p>
                    <p className="info-item">
                        <span className="info-label">Messages:</span>
                        <span className="info-value">{messageCount}</span>
                    </p>
                </div>
            </div>
        </aside>
    )
}

export default Sidebar
