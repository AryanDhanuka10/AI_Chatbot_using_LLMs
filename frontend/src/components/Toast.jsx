import './Toast.css'

function Toast({ show, message, type }) {
    return (
        <div className={`toast ${type} ${show ? 'show' : ''}`}>
            {message}
        </div>
    )
}

export default Toast
