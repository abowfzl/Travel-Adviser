import { useState, KeyboardEvent } from "react";

// Define a unified type for all props
export type ChatInputProps = {
  onChatInput?: (chatText: string) => void;
  onClearChatHistory?: () => void;
  loading?: boolean;
};

declare module "react" {
  interface TextareaHTMLAttributes<T> extends HTMLAttributes<T> {
    enterKeyHint?:
      | "enter"
      | "done"
      | "go"
      | "next"
      | "previous"
      | "search"
      | "send";
  }
}

function ChatInput({ onChatInput, onClearChatHistory, loading = false }: ChatInputProps) {
  const [inputText, setInputText] = useState("");

  const handleSend = () => {
    if (!loading && inputText.trim() !== "" && onChatInput) {
      onChatInput(inputText);
      setInputText("");
    }
  };

  const handleClearChat = () => {
    if (!loading && onClearChatHistory) {
      onClearChatHistory();
      setInputText("");
    }
  };

return (
    <div className="flex items-center w-full gap-2 p-4">
      <textarea
        enterKeyHint="send"
        onChange={(e) => setInputText(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSend()}
        disabled={loading}
        value={inputText}
        rows={1}
        className="flex-1 p-3 bg-transparent border border-light-border dark:border-dark-border rounded-md outline-none resize-none placeholder-gray-500 dark:placeholder-dark-text focus:ring-2 focus:ring-blue-300 dark:focus:ring-dark-text dark:text-dark-text transition-all duration-200"
        placeholder="Ask about your trip..."
      ></textarea>
      <button
        className="flex items-center justify-center p-3 bg-blue-500 rounded-full shadow-md hover:bg-blue-600 transition-transform duration-200 transform hover:scale-105 active:scale-95"
        onClick={handleSend}
        disabled={loading}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth="1.5"
          stroke="currentColor"
          aria-hidden="true"
          className="w-6 h-6 text-white"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"
          ></path>
        </svg>
      </button>
      <button
        className="flex items-center justify-center p-3 bg-gray-300 dark:bg-dark-border rounded-full shadow-md hover:bg-red-500 transition-transform duration-200 transform hover:scale-105 active:scale-95"
        onClick={onClearChatHistory}
        disabled={loading}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth="1.5"
          stroke="currentColor"
          aria-hidden="true"
          className="w-6 h-6 text-black dark:text-dark-text"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M9 3v1H5.75C5.336 4 5 4.336 5 4.75v.5C5 5.664 5.336 6 5.75 6H18.25C18.664 6 19 5.664 19 5.25v-.5C19 4.336 18.664 4 18.25 4H15V3c0-.552-.448-1-1-1H10c-.552 0-1 .448-1 1zM4.5 8h15l-1.314 12.268A1.75 1.75 0 0116.447 22H7.553a1.75 1.75 0 01-1.739-1.732L4.5 8z"
          />
        </svg>
      </button>
    </div>

  );
}

export default ChatInput;
