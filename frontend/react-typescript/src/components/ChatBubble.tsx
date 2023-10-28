import { Message } from "../models/messages"

export function ChatBubbles(message: Message) {
  return (
    <div className="chat-bubble">{message.text}</div>
  )
}
