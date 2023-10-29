import axios from "axios";

const baseUrl = "http://localhost:5000"
export function postRadius(updatedRadius: number) {
  axios.post(baseUrl + "/settings/", updatedRadius)
}
