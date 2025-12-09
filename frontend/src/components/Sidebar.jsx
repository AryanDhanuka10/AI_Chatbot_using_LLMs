import { Plus, Download, History, Clock, ChevronLeft, ChevronRight, FileText, X } from 'lucide-react'
import './Sidebar.css'

const DOMAINS = ['General', 'Education', 'Coding', 'Medical', 'Legal']

const DOMAIN_ICONS = {
    General: '🌐',
    Education: '📚',
    Coding: '💻',
    Medical: '🏥',
    Legal: '⚖️'
}

function Sidebar({ isOpen, onToggle, domain, onDomainChange, onNewChat, onExport, sessionId, messageCount, chatHistory, onLoadChat, uploadedFiles = [], onRemoveFile }) {
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

            {/* Active Documents */}
            <div className="control-group">
                <div className="control-heading">
                    <FileText size={18} style={{ display: 'inline', marginRight: '8px' }} />
                    Active Documents
                </div>
                {uploadedFiles.length > 0 ? (
                    <div className="uploaded-files-list">
                        {uploadedFiles.map((file, index) => (
                            <div key={index} className="uploaded-file-item">
                                <div className="file-info">
                                    <FileText size={16} className="file-icon" />
                                    <div className="file-details">
                                        <span className="file-name" title={file.filename}>
                                            {file.filename}
                                        </span>
                                        <span className="file-chunks">{file.chunks} chunks</span>
                                    </div>
                                </div>
                                <button
                                    className="remove-file-btn"
                                    onClick={() => onRemoveFile(file.filename)}
                                    aria-label="Remove file"
                                    title="Remove from context"
                                >
                                    <X size={16} />
                                </button>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="empty-state">
                        <FileText size={24} style={{ opacity: 0.3 }} />
                        <p>No documents uploaded</p>
                    </div>
                )}
            </div>


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
