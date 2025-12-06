import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'
import rehypeRaw from 'rehype-raw'
import 'highlight.js/styles/github-dark.css'
import './ChatArea.css'

function ChatArea({ messages, domain, model, onModelChange, sessionId, messagesEndRef }) {
    const getDomainIcon = (domain) => {
        const icons = {
            General: '🌐',
            Education: '📚',
            Coding: '💻',
            Medical: '🏥',
            Legal: '⚖️'
        }
        return icons[domain] || '🌐'
    }

    return (
        <div className="chat-area">
            <div className="chat-header">
                <div className="chat-header-info">
                    <span className="domain-badge">
                        {getDomainIcon(domain)} {domain}
                    </span>
                    <select
                        className="model-selector"
                        value={model}
                        onChange={(e) => onModelChange(e.target.value)}
                    >
                        <option value="llama-3.1-70b-versatile">🦙 Groq Llama-3.1-70B</option>
                        <option value="gpt-4o">🤖 GPT-4o</option>
                        <option value="gpt-3.5-turbo">⚡ GPT-3.5 Turbo</option>
                    </select>
                    <span className="session-badge">
                        Session: {sessionId.substring(0, 12)}...
                    </span>
                </div>
            </div>

            <div className="messages-container">
                {messages.length === 0 ? (
                    <div className="welcome-message">
                        <div className="welcome-icon">🤖</div>
                        <h2>Welcome to AI Chatbot</h2>
                        <p>Start a conversation by typing your message below. Select a domain for specialized responses.</p>
                    </div>
                ) : (
                    messages.map((msg, index) => (
                        <div key={index} className={`message ${msg.role}`}>
                            <div className="message-avatar">
                                {msg.role === 'user' ? '👤' : '🤖'}
                            </div>
                            <div className="message-content">
                                <div className="message-bubble">
                                    {msg.role === 'assistant' ? (
                                        <ReactMarkdown
                                            remarkPlugins={[remarkGfm]}
                                            rehypePlugins={[rehypeHighlight, rehypeRaw]}
                                            components={{
                                                code({ node, inline, className, children, ...props }) {
                                                    return inline ? (
                                                        <code className="inline-code" {...props}>
                                                            {children}
                                                        </code>
                                                    ) : (
                                                        <code className={className} {...props}>
                                                            {children}
                                                        </code>
                                                    )
                                                }
                                            }}
                                        >
                                            {msg.text}
                                        </ReactMarkdown>
                                    ) : (
                                        msg.text
                                    )}
                                </div>
                                <div className="message-timestamp">{msg.timestamp}</div>
                            </div>
                        </div>
                    ))
                )}
                <div ref={messagesEndRef} />
            </div>
        </div>
    )
}

export default ChatArea
