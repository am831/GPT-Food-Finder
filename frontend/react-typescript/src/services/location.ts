import axios from "axios";
import { Message } from "discord.js";
import React, { useEffect, useState } from "react";
export async function postMessage () {

}

function App() {
  const [coords, setCoords] = useState<{ latitude: number | null; longitude: number | null }>({
    latitude: null,
    longitude: null,
  });
  
  useEffect(() => {
    const fetchUserLocation = () => {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const coordX = position.coords.latitude;
          const coordY = position.coords.longitude;
          console.log("Latitude:", coordX);
          console.log("Longitude:", coordY);
          setCoords({ latitude: coordX, longitude: coordY });
        },
        (error) => {
          console.error("Error getting location:", error.message);
        }
      );
    };

    fetchUserLocation();
  }, []); 

  return (
    // TODO
    <div>
      <h1>Your Location</h1>
      <p>Latitude: {coords.latitude}</p>
      <p>Longitude: {coords.longitude}</p>
    </div>
  );
}

export default App;