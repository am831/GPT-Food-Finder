import axios from 'axios'
import { UserGeoLocation } from '../models/location'

const baseURL = 'https://localhost:3000/'

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

export async function postUserLocation(location: UserGeoLocation) {
  try {
    const response = await axios.post(baseURL, location)
  } catch (error) {
    console.error(error)
  }
}
