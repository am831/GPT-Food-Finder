type ChatBubbleProps = {
  text: string
  sender: string
}

export function ChatBubbles({ text, sender }: ChatBubbleProps) {
  return (
    <div className=''>
      {sender !== 'self' ? (
        <div className='chat chat-start'>
          <div className='chat-bubble bg-pink-400 text-white'>{text}</div>
        </div>
      ) : (
        <div className='chat chat-end'>
          <div className='chat-bubble bg-purple-400 text-white'>{text}</div>
        </div>
      )}
    </div>
  )
}
