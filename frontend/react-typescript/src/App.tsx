import { useEffect, useState } from 'react'
import { ChatPage } from './components/ChatPage'
import { NavBar } from './components/NavBar'
import { getUserLocation } from './services/location'
import { UserGeoLocation } from './models/location'

function App() {
  const [loggedIn, setLoggedIn] = useState(true)
  const [location, setLocation] = useState<UserGeoLocation>()

  useEffect(() => {
    setLocation(getUserLocation())
  }, [])

  return (
    <div className="flex flex-col">
      <NavBar></NavBar>
      {loggedIn && <ChatPage></ChatPage>}
    </div>
  )
}

export default App
