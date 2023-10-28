import { useState } from 'react'
import { ChatBubbles, Message } from './components/ChatBubble'
import { ChatPage } from './components/ChatPage'

function App() {
  const [message, setMessage] = useState('')
  const [loggedIn, setLoggedIn] = useState(true)
  const fakeList = [
    { date: 1, text: 'hi' },
    { date: 1, text: 'hi' },
    { date: 1, text: 'hi' },
    { date: 1, text: 'hi' },
  ]

  return (
    <div className="flex flex-col">
      <ChatBubbles date={1} text="this is a test message"></ChatBubbles>
      {loggedIn && <ChatPage list={fakeList}></ChatPage>}
    </div>
  )
}

export default App
