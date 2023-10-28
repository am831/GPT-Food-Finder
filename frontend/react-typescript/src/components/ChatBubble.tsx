export type Message = {
  date: number
  text: string
}

export function ChatBubbles(message: Message) {
  return (
    <div className="chat-bubble">{message.text}</div>
  )
}
