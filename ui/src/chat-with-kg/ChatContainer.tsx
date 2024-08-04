import React, { useRef, useEffect } from "react";
import ChatMessage, { ChatMessageObject } from "./ChatMessage";

export type ChatContainerProps = {
  chatMessages?: ChatMessageObject[];
  loading?: boolean;
};

const loadingMessage: ChatMessageObject = {
  id: -1,
  type: "text",
  message: "Loading...",
  sender: "bot",
  complete: true,
};

function ChatContainer(props: ChatContainerProps) {
  const { chatMessages = [], loading } = props;
  const chatEndRef = useRef<HTMLDivElement | null>(null);

  const scrollToBottom = () => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatMessages]);

  return (
    <div className="relative flex flex-col w-full min-w-[320px] max-w-full overflow-y-auto rounded-lg shadow-lg bg-light-bg dark:bg-dark-bg transition-colors duration-300 p-6">
      <div className="flex flex-col w-full max-w-4xl mx-auto space-y-4">
        {chatMessages.length > 0 ? (
          chatMessages.map((chatMessage) => (
            <ChatMessage key={chatMessage.id} chatMessage={chatMessage} />
          ))
        ) : (
          <div className="text-center text-black dark:text-white">
            <p>Hi, Let's start a conversation...</p>
          </div>
        )}
        {loading && <ChatMessage chatMessage={loadingMessage} />}
        <div ref={chatEndRef} />
      </div>
    </div>
  );
}

export default ChatContainer;
