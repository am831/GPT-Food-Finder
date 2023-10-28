import { Message } from '../models/messages'

type ChatBubbleProps = {
  text: string,
  date: number,
  sender: string
}

export function ChatBubbles({ text, date, sender }: ChatBubbleProps) {
  return (
    <div className="md: w-screen">
      {sender !== 'self' ? (
        <div className="chat chat-start">
          <div className="chat-bubble bg-pink-400 text-white">{text}</div>
        </div>
      ) : (
        <div className="chat chat-end">
          <div className="chat-bubble bg-purple-400 text-white">{text}</div>
        </div>
      )}
    </div>
  )
}
