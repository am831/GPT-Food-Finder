import axios from 'axios'
import { UserGeoLocation } from '../models/location'

const baseURL = 'http://localhost:5000/'

export function getUserLocation() {
  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const currLocation = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        }
        console.log('Latitude:', position.coords.latitude)
        console.log('Longitude:', position.coords.longitude)
        resolve(currLocation)
      },
      (error) => {
        console.error(error)
        reject(error)
      },
      {
        enableHighAccuracy: false,
        timeout: 5000,
        maximumAge: Infinity,
      }
    )
  })
}

export async function postUserLocation() {
  try {
    const location = getUserLocation()
    const response = await axios.post(baseURL, location)
    console.log(response)
  } catch (error) {
    console.error(error)
  }
}
