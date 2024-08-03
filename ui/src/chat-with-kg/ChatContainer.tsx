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
  return (
    <div className="relative flex flex-col w-full min-w-[320px] max-w-full overflow-x-auto rounded-lg shadow-lg bg-light-bg dark:bg-dark-bg transition-colors duration-300 p-6">
      <div className="flex flex-col w-full max-w-4xl mx-auto space-y-4">
        {chatMessages.length > 0 ? (
          chatMessages.map((chatMessage) => (
            <ChatMessage key={chatMessage.id} chatMessage={chatMessage} />
          ))
        ) : (
          <div className="text-gray-500 dark:text-gray-400">Start a conversation...</div>
        )}
      </div>
    </div>
  );
}

export default ChatContainer;
