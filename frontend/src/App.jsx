import { useState, useRef, useEffect } from 'react'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import ChatArea from './components/ChatArea'
import InputArea from './components/InputArea'
import Toast from './components/Toast'
import './App.css'

const BACKEND_URL = 'http://127.0.0.1:8000'

function App() {
  const [sessionId] = useState(`session-${Date.now()}`)
  const [domain, setDomain] = useState('General')
  const [messages, setMessages] = useState([])
  const [isTyping, setIsTyping] = useState(false)
  const [toast, setToast] = useState({ show: false, message: '', type: 'success' })
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [chatHistory, setChatHistory] = useState([])
  const messagesEndRef = useRef(null)

  // Load chat history from localStorage on mount
  useEffect(() => {
    const savedHistory = localStorage.getItem('chatHistory')
    if (savedHistory) {
      setChatHistory(JSON.parse(savedHistory))
    }
  }, [])

  // Save current chat to history when messages change
  useEffect(() => {
    if (messages.length > 0) {
      const currentChat = {
        id: sessionId,
        domain: domain,
        timestamp: new Date().toISOString(),
        messageCount: messages.length,
        preview: messages[messages.length - 1]?.text.substring(0, 50) + '...',
        messages: messages
      }

      const updatedHistory = [currentChat, ...chatHistory.filter(chat => chat.id !== sessionId)].slice(0, 10)
      setChatHistory(updatedHistory)
      localStorage.setItem('chatHistory', JSON.stringify(updatedHistory))
    }
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const showToast = (message, type = 'success') => {
    setToast({ show: true, message, type })
    setTimeout(() => setToast({ show: false, message: '', type: 'success' }), 3000)
  }

  const handleSendMessage = async (messageText) => {
    if (!messageText.trim()) return

    // Add user message
    const userMessage = {
      role: 'user',
      text: messageText,
      timestamp: new Date().toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      }),
      domain
    }
    setMessages(prev => [...prev, userMessage])

    // Show typing indicator
    setIsTyping(true)

    try {
      const response = await fetch(`${BACKEND_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: messageText,
          domain: domain,
        }),
      })

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status}`)
      }

      const data = await response.json()
      const aiResponse = data.response || 'No response received'

      // Add AI message
      const aiMessage = {
        role: 'assistant',
        text: aiResponse,
        timestamp: new Date().toLocaleTimeString('en-US', {
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        }),
        domain
      }
      setMessages(prev => [...prev, aiMessage])

    } catch (error) {
      console.error('Chat error:', error)
      const errorMessage = {
        role: 'assistant',
        text: `⚠️ Connection Error: ${error.message}. Please ensure the backend is running.`,
        timestamp: new Date().toLocaleTimeString('en-US', {
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        }),
        domain
      }
      setMessages(prev => [...prev, errorMessage])
      showToast('Failed to send message', 'error')
    } finally {
      setIsTyping(false)
    }
  }

  const handleNewChat = () => {
    setMessages([])
    showToast('Started new chat session', 'success')
  }

  const loadChat = (chat) => {
    setMessages(chat.messages)
    setDomain(chat.domain)
    showToast('Chat loaded successfully', 'success')
  }

  const handleExport = (format) => {
    if (messages.length === 0) {
      showToast('No messages to export', 'warning')
      return
    }

    let content, filename, mimeType

    if (format === 'json') {
      content = JSON.stringify(messages, null, 2)
      filename = `chat_history_${Date.now()}.json`
      mimeType = 'application/json'
    } else if (format === 'txt') {
      content = messages.map(msg =>
        `[${msg.timestamp}] ${msg.role.toUpperCase()}: ${msg.text}`
      ).join('\n\n')
      filename = `chat_history_${Date.now()}.txt`
      mimeType = 'text/plain'
    }

    const blob = new Blob([content], { type: mimeType })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)

    showToast(`Chat exported as ${format.toUpperCase()}`, 'success')
  }

  const handleFileUpload = async (files) => {
    if (files.length === 0) return

    try {
      for (const file of files) {
        const formData = new FormData()
        formData.append('file', file)

        const response = await fetch(`${BACKEND_URL}/upload`, {
          method: 'POST',
          body: formData,
        })

        if (!response.ok) {
          throw new Error(`Failed to upload ${file.name}`)
        }
      }

      showToast(`Successfully uploaded ${files.length} file(s)`, 'success')
    } catch (error) {
      showToast(`Upload failed: ${error.message}`, 'error')
    }
  }

  return (
    <div className="app-container">
      <Header />

      <div className={`main-layout ${!sidebarOpen ? 'sidebar-hidden' : ''}`}>
        <Sidebar
          isOpen={sidebarOpen}
          onToggle={() => setSidebarOpen(!sidebarOpen)}
          domain={domain}
          onDomainChange={setDomain}
          onNewChat={handleNewChat}
          onExport={handleExport}
          sessionId={sessionId}
          messageCount={messages.length}
          chatHistory={chatHistory}
          onLoadChat={loadChat}
        />

        <div className="chat-container">
          <ChatArea
            messages={messages}
            domain={domain}
            sessionId={sessionId}
            messagesEndRef={messagesEndRef}
          />

          <InputArea
            onSendMessage={handleSendMessage}
            isTyping={isTyping}
            onFileUpload={handleFileUpload}
          />
        </div>
      </div>

      <Toast
        show={toast.show}
        message={toast.message}
        type={toast.type}
      />
    </div>
  )
}

export default App
