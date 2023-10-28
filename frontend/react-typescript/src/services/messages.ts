import axios from 'axios'
import { Message } from '../models/messages'

const fakeList = [
  {
    id: 1,
    date: 1,
    text: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
    sender: 'self',
  },
  { id: 2, date: 1, text: 'hello world', sender: 'self' },
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
