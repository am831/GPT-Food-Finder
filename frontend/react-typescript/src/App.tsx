import { useState } from 'react'
import { ChatBubbles } from './components/ChatBubble'
import { Message } from './models/messages'
import { ChatPage } from './components/ChatPage'

function App() {
  const [loggedIn, setLoggedIn] = useState(true)
  const fakeList = [
    { date: 1, text: 'this is a text message' },
    { date: 1, text: 'hello world' },
    { date: 1, text: 'hi' },
    { date: 1, text: 'hi' },
  ]

  return (
    <div className="flex flex-col">
      {loggedIn && <ChatPage list={fakeList}></ChatPage>}
    </div>
  )
}

export default App
