import { useEffect, useState } from 'react'
import { ChatPage } from './components/ChatPage'
import { NavBar } from './components/NavBar'
import { postUserLocation } from './services/location'
import { HomePage } from './components/HomePage'

function App() {
  const [loggedIn, setLoggedIn] = useState(false)
  useEffect(() => {
    postUserLocation()
  }, [])

  return (
    <div className='flex flex-col'>
      <NavBar></NavBar>
      {loggedIn ? <ChatPage></ChatPage> : <HomePage></HomePage>}
      {!loggedIn && <button className='max-w-xs self-center -my-72 btn bg-purple-300' onClick={() => setLoggedIn(true)}>Start now.</button>}
    </div>
  )
}

export default App
