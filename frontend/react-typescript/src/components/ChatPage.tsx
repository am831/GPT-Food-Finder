import { useEffect, useState } from 'react'
import { ChatBubbles } from './ChatBubble'
import { Message } from '../models/messages'
import { getMessages, postChatMessage } from '../services/messages'

export function ChatPage() {
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchData() {
      const initialMessages = await getMessages()
      setMessages(initialMessages)
    }
    fetchData()
  }, [])

  return (
    <div className="flex flex-col gap-1 p-5 items-center h-screen">
      <div className="p-4 flex flex-col gap-1">
        {messages.map((message) => (
          <ChatBubbles
            key={message.id}
            date={message.date}
            text={message.text}
            sender={message.sender}
          ></ChatBubbles>
        ))}
        {loading &&
        <div className="chat chat-start">
          <div className="chat-bubble bg-pink-400 text-white"><span className='loading loading-dots loading-md'></span></div>
        </div>}
        <form
          className="my-32 flex grow w-11/12 self-center"
          onSubmit={async (event) => {
            event.preventDefault()
            const newMsg = {
              id: messages.length + 1,
              date: Date.now(),
              text: message,
              sender: 'self',
            }
            setMessages(messages.concat(newMsg))
          }}
        >
          <input
            className="input input-bordered w-full"
            type="text"
            placeholder="Enter your text here..."
            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
              setMessage(event.target.value)
            }}
          />
          <button className="btn" type="submit">
            Send
          </button>
        </form>
      </div>
    </div>
  )
}
