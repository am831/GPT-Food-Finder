import axios from 'axios'

export function getUserLocation() {
  const currLocation = { longitude: 0, latitude: 0 }
  navigator.geolocation.getCurrentPosition(
    (position) => {
      currLocation.latitude = position.coords.latitude
      console.log('Latitude:', position.coords.latitude)
      currLocation.longitude = position.coords.longitude
      console.log('Longitude:', position.coords.longitude)
    },
    (error) => {
      console.error(error)
    }
  )

  return currLocation
}
