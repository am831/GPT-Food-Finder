import axios from 'axios'
import { Message } from '../models/messages'

const baseAddress = 'http://localhost:5000/messages/'
const fakeList = [
  {
    id: 1,
    date: 1,
    text: 'Hi 👋! Thanks for trying our app. What kind of food would you like today?',
    sender: 'bot',
  },
]

export async function postChatMessage(message: Message) {
  const response = await axios.post<Message>(baseAddress, message)
  return response.data
}

export function getMessages() {
  return fakeList
}
