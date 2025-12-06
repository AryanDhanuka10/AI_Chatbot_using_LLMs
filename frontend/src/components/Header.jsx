import './Header.css'

function Header() {
    return (
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
    )
}

export default Header
