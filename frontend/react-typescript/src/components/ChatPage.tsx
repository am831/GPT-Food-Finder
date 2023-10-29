import { useEffect, useState } from 'react'
import { ChatBubbles } from './ChatBubble'
import { Message } from '../models/messages'
import { getMessages, postChatMessage } from '../services/messages'

export function ChatPage() {
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    async function fetchData() {
      const initialMessages = await getMessages()
      setMessages(initialMessages)
    }
    fetchData()
  }, [])

  return (
    <div className='flex flex-col gap-1 items-center h-5/6 overflow-hidden'>
      <div className='grid grid-cols-1 gap-1 my-10'>
        {messages.map((message) => (
          <ChatBubbles
            key={message.id}
            date={message.date}
            text={message.text}
            sender={message.sender}
          ></ChatBubbles>
        ))}
        {loading && (
          <div className='chat chat-start'>
            <div className='chat-bubble bg-pink-400 text-white'>
              <span className='loading loading-dots loading-md'></span>
            </div>
          </div>
        )}
        <form
          className='my-32 flex grow self-center'
          onSubmit={async (event) => {
            event.preventDefault()
            const newMsg = {
              id: messages.length + 1,
              date: Date.now(),
              text: message,
              sender: 'self',
            }
            setLoading(true)
            const responseMsg = await postChatMessage(newMsg)
            setLoading(false)
            setMessages([...messages, newMsg, responseMsg])
          }}
        >
          <input
            className='input input-bordered w-full'
            type='text'
            placeholder='Enter your text here...'
            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
              setMessage(event.target.value)
            }}
          />
          <button className='btn' type='submit'>
            Send
          </button>
        </form>
      </div>
    </div>
  )
}
