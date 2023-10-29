import { useEffect, useState } from 'react'
import { ChatPage } from './components/ChatPage'
import { NavBar } from './components/NavBar'
import { postUserLocation } from './services/location'

function App() {
  const [loggedIn, setLoggedIn] = useState(true)
  useEffect(() => {
    postUserLocation()
  }, [])

  return (
    <div className='flex flex-col overflow-hidden'>
      <NavBar></NavBar>
      {loggedIn && <ChatPage></ChatPage>}
    </div>
  )
}

export default App
