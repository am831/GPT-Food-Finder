import axios from 'axios'
import { Message } from '../models/messages'

const fakeList = [
  {
    id: 1,
    date: 1,
    text: "Hi 👋! Thanks for trying our app. What kind of food would you like today?",
    sender: 'bot',
  },
  { id: 2, date: 1, text: 'I\'d like to order a slice of pizza', sender: 'self' },
  { id: 3, date: 1, text: 'hello world', sender: 'self' },
  { id: 4, date: 1, text: 'hello world', sender: 'self' },
  { id: 5, date: 1, text: 'hello world', sender: 'bot' },
  { id: 6, date: 1, text: 'hello world', sender: 'self' },
]

export function postChatMessage(message: Message) {
  fakeList.push(message)
  return message
}

export function getMessages() {
  return fakeList
}
