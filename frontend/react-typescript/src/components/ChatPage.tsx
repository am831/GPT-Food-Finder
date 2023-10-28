import { useState } from 'react'
import { Message } from './ChatBubble'
import { ChatBubbles } from './ChatBubble'

type MessageList = {
  list: Message[]
}

async function fakeLoad() {
  console.log('hello')
}

export function ChatPage(messages: MessageList) {
  const [message, setMessage] = useState('')
  return (
    <div className="flex flex-col">
      <div>Restaurant Recommendation App</div>
      <div>
        {messages.list.map((message) => (
          <ChatBubbles date={1} text={message.text}></ChatBubbles>
        ))}
      </div>
      <form>
        <input
          type="text"
          placeholder="Enter your text here..."
          onInput={(event: React.ChangeEvent<HTMLInputElement>) => {
            setMessage(event.target.value)
          }}
        />
        <button type="submit" onSubmit={fakeLoad}>
          Send
        </button>
      </form>
    </div>
  )
}
