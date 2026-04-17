import { useState, useRef, useEffect } from 'react'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import ChatArea from './components/ChatArea'
import InputArea from './components/InputArea'
import Toast from './components/Toast'
import './App.css'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'https://huggingface.co/spaces/AryanDhanuka10/AI_Chat'

function App() {
  const [sessionId] = useState(`session-${Date.now()}`)
  const [domain, setDomain] = useState('General')
  const [model, setModel] = useState('llama-3.1-70b-versatile')
  const [messages, setMessages] = useState([])
  const [isTyping, setIsTyping] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [toast, setToast] = useState({ show: false, message: '', type: 'success' })
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [chatHistory, setChatHistory] = useState([])
  const [uploadedFiles, setUploadedFiles] = useState([])
  const messagesEndRef = useRef(null)
  const abortControllerRef = useRef(null)

  // Load chat history and uploaded files from localStorage on mount
  useEffect(() => {
    const savedHistory = localStorage.getItem('chatHistory')
    if (savedHistory) {
      setChatHistory(JSON.parse(savedHistory))
    }

    const savedFiles = localStorage.getItem('uploadedFiles')
    if (savedFiles) {
      setUploadedFiles(JSON.parse(savedFiles))
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
    if (!messageText.trim() || isLoading) return

    // Set loading state to prevent duplicate submissions
    setIsLoading(true)
    setIsTyping(true)

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

    // Create AbortController for timeout handling
    abortControllerRef.current = new AbortController()
    const timeoutId = setTimeout(() => abortControllerRef.current?.abort(), 60000) // 60 second timeout

    try {
      const response = await fetch(`${BACKEND_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: messageText,
          selected_domain: domain,
          model: model,
        }),
        signal: abortControllerRef.current.signal,
      })

      clearTimeout(timeoutId)

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      const aiResponse = data.response || 'No response received'

      // Check if this is a domain mismatch warning
      const isDomainMismatch =
        aiResponse.includes('Please switch to') ||
        aiResponse.includes('Wrong domain selected') ||
        aiResponse.startsWith('⚠️') ||
        aiResponse.startsWith('❌') ||
        data.domain === 'system'

      if (isDomainMismatch) {
        // Add as system warning message in chat
        const systemMessage = {
          role: 'system',
          text: aiResponse,
          timestamp: new Date().toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
          }),
          domain: 'system'
        }
        setMessages(prev => [...prev, systemMessage])
        showToast('Domain mismatch detected', 'warning')
      } else {
        // Add AI message (only if not a domain mismatch)
        const aiMessage = {
          role: 'assistant',
          text: aiResponse,
          timestamp: new Date().toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
          }),
          domain: data.domain || domain
        }
        setMessages(prev => [...prev, aiMessage])
      }

    } catch (error) {
      clearTimeout(timeoutId)
      console.error('Chat error:', error)

      // Provide specific error messages
      if (error.name === 'AbortError') {
        showToast('⏱️ Request timed out. The backend is taking too long to respond. Please try again.', 'error')
      } else if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        showToast('🔌 Cannot connect to backend. Please check your internet connection or try again later.', 'error')
      } else if (error.message.includes('HTTP 5')) {
        showToast('⚠️ Backend server error. Please try again in a moment.', 'error')
      } else if (error.message.includes('HTTP 4')) {
        showToast('❌ Invalid request. Please check your input and try again.', 'error')
      } else {
        showToast(`Error: ${error.message}`, 'error')
      }
    } finally {
      setIsTyping(false)
      setIsLoading(false)
      abortControllerRef.current = null
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

    // Create AbortController for timeout handling (longer timeout for file uploads)
    const uploadAbortController = new AbortController()
    const timeoutId = setTimeout(() => uploadAbortController.abort(), 120000) // 120 second timeout

    try {
      const uploadedFileMetadata = []

      for (const file of files) {
        const formData = new FormData()
        formData.append('files', file)

        const response = await fetch(`${BACKEND_URL}/upload/`, {
          method: 'POST',
          body: formData,
          signal: uploadAbortController.signal,
        })

        if (!response.ok) {
          throw new Error(`Failed to upload ${file.name}`)
        }

        const data = await response.json()

        // Store file metadata from backend response
        uploadedFileMetadata.push({
          filename: data.filename || file.name,
          chunks: data.chunks || 0,
          savedTo: data.saved_to || '',
          uploadedAt: new Date().toISOString(),
          size: file.size,
          type: file.type
        })
      }

      clearTimeout(timeoutId)

      // Update state and localStorage
      const updatedFiles = [...uploadedFiles, ...uploadedFileMetadata]
      setUploadedFiles(updatedFiles)
      localStorage.setItem('uploadedFiles', JSON.stringify(updatedFiles))

      showToast(`Successfully uploaded ${files.length} file(s)`, 'success')
    } catch (error) {
      clearTimeout(timeoutId)
      console.error('Upload error:', error)

      // Provide specific error messages
      if (error.name === 'AbortError') {
        showToast('⏱️ Upload timed out. File may be too large or connection is slow.', 'error')
      } else if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        showToast('🔌 Cannot connect to backend. Please check your connection.', 'error')
      } else {
        showToast(`Upload failed: ${error.message}`, 'error')
      }
    }
  }

  const handleRemoveFile = (filename) => {
    const updatedFiles = uploadedFiles.filter(f => f.filename !== filename)
    setUploadedFiles(updatedFiles)
    localStorage.setItem('uploadedFiles', JSON.stringify(updatedFiles))
    showToast(`Removed ${filename} from context`, 'success')
  }


  return (
    <div className="app-container">
      <Header />

      <div className={`main-layout ${!sidebarOpen ? 'sidebar-hidden' : ''}`}>
        <button
          className={`sidebar-edge-toggle ${!sidebarOpen ? 'closed' : ''}`}
          onClick={() => setSidebarOpen(!sidebarOpen)}
          title={sidebarOpen ? 'Close Sidebar' : 'Open Sidebar'}
        >
          {sidebarOpen ? '◀' : '▶'}
        </button>

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
          uploadedFiles={uploadedFiles}
          onRemoveFile={handleRemoveFile}
        />


        <div className="chat-container">
          <ChatArea
            messages={messages}
            domain={domain}
            model={model}
            onModelChange={setModel}
            sessionId={sessionId}
            messagesEndRef={messagesEndRef}
            uploadedFiles={uploadedFiles}
          />

          <InputArea
            onSendMessage={handleSendMessage}
            isTyping={isTyping}
            isLoading={isLoading}
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
