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
    <div className='flex flex-col'>
      <NavBar></NavBar>
      {loggedIn && <ChatPage></ChatPage>}
      <button onClick={() => postUserLocation}>text</button>
    </div>
  )
}

export default App
