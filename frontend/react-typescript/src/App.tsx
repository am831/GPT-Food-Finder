import { useState } from 'react'
import { ChatPage } from './components/ChatPage'
import { NavBar } from './components/NavBar'

function App() {
  const [loggedIn, setLoggedIn] = useState(true)

  return (
    <div className="flex flex-col">
      <NavBar></NavBar>
      {loggedIn && <ChatPage></ChatPage>}
    </div>
  )
}

export default App
