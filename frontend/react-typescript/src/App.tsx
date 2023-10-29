import { useEffect } from 'react'
import { ChatPage } from './components/ChatPage'
import { NavBar } from './components/NavBar'
import { postUserLocation } from './services/location'

function App() {
  useEffect(() => {
    postUserLocation()
  }, [])

  return (
    <div className="flex flex-col overflow-hidden">
      <NavBar></NavBar>
      <ChatPage></ChatPage>
    </div>
  )
}

export default App
