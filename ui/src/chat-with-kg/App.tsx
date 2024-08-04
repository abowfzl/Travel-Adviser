import { useCallback, useEffect, useState, ChangeEvent } from "react";
import ChatContainer from "./ChatContainer";
import type { ChatMessageObject, ChatMessageResponseObject } from "./ChatMessage";
import ChatInput from "./ChatInput";
import useWebSocket, { ReadyState } from "react-use-websocket";
import KeyModal from "../components/keymodal";
import type {
  ConversationState,
  WebSocketRequest,
  WebSocketResponse,
} from "./types/websocketTypes";

const SEND_REQUESTS = true;

const chatMessageObjects: ChatMessageObject[] = SEND_REQUESTS
  ? []
  : [
      {
        id: 0,
        type: "input",
        sender: "self",
        message:
          "This is the first message which has decently long text and would denote something typed by the user",
        complete: true,
      },
      {
        id: 1,
        type: "text",
        sender: "bot",
        message:
          "And here is another message which would denote a response from the server, which for now will only be text",
        complete: true,
      },
    ];

const URI =
  import.meta.env.VITE_KG_CHAT_BACKEND_ENDPOINT ??
  "ws://localhost:8000/text2text";

const HAS_API_KEY_URI =
  import.meta.env.VITE_HAS_API_KEY_ENDPOINT ??
  "http://localhost:8000/hasapikey";

const GENERATE_SESSION_ID_URI =
  import.meta.env.VITE_GENERATE_SESSION_ID_ENDPOINT ??
  "http://localhost:8000/generate_session_id";

const GET_CHAT_HISTORY_URI =
  import.meta.env.VITE_GET_CHAT_HISTORY_ENDPOINT ??
  "http://localhost:8000/chat_history?session_id=";

const CLEAR_CHAT_HISTORY_URI =
  import.meta.env.VITE_CLEAR_CHAT_HISTORY_ENDPOINT ??
  "http://localhost:8000/chat_history?session_id=";

function loadKeyFromStorage() {
  return localStorage.getItem("api_key");
}

function loadSessionIdFromStorage() {
  return localStorage.getItem("session_id");
}

const QUESTION_PREFIX_REGEXP = /^[0-9]{1,2}[\w]*[\.\)\-]*[\w]*/;

function stripQuestionPrefix(question: string): string {
  if (question.match(QUESTION_PREFIX_REGEXP)) {
    return question.replace(QUESTION_PREFIX_REGEXP, "");
  }
  return question;
}

function App() {
  const [serverAvailable, setServerAvailable] = useState(true);
  const [needsApiKeyLoading, setNeedsApiKeyLoading] = useState(true);
  const [needsApiKey, setNeedsApiKey] = useState(true);
  const [chatMessages, setChatMessages] = useState(chatMessageObjects);
  const [conversationState, setConversationState] =
    useState<ConversationState>("ready");
  const { sendJsonMessage, lastMessage, readyState } = useWebSocket(URI, {
    shouldReconnect: () => true,
    reconnectInterval: 5000,
  });
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [apiKey, setApiKey] = useState(loadKeyFromStorage() || "");
  const [sessionId, setSessionId] = useState(loadSessionIdFromStorage() || "");
  const [text2cypherModel, setText2cypherModel] = useState<string>("openai");

  const showContent = serverAvailable && !needsApiKeyLoading;

  useEffect(() => {
    const session_id = loadSessionIdFromStorage();
    if (session_id) {
      setSessionId(session_id);
    } else {
      fetch(GENERATE_SESSION_ID_URI, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
      }).then(
        (response) => {
          response.json().then(
            (result) => {
              const new_session_id = result.session_id;
              onSessionIdChange(new_session_id);
            },
            (error) => {
              setServerAvailable(false);
            }
          );
        },
        (error) => {
          setServerAvailable(false);
        }
      );
    }
  }, []);

  useEffect(() => {
    fetch(HAS_API_KEY_URI).then(
      (response) => {
        response.json().then(
          (result) => {
            // const needsKey = result.output;
            const needsKey = !result.output;
            setNeedsApiKey(needsKey);
            setNeedsApiKeyLoading(false);
            if (needsKey) {
              const api_key = loadKeyFromStorage();
              if (api_key) {
                setApiKey(api_key);
              } else {
                setModalIsOpen(true);
              }
            }
          },
          (error) => {
            setNeedsApiKeyLoading(false);
            setServerAvailable(false);
          }
        );
      },
      (error) => {
        setNeedsApiKeyLoading(false);
        setServerAvailable(false);
      }
    );
  }, []);

  useEffect(() => {
    const session_id = loadSessionIdFromStorage();
    const url = GET_CHAT_HISTORY_URI + sessionId
    fetch(url).then(
      (response) => {
        response.json().then(
          (result) => {
            const messages: ChatMessageResponseObject[] = result.messages;
            const newChatMessages: ChatMessageObject[] = messages.map((message: ChatMessageResponseObject, index: number): ChatMessageObject | null => {
              if (message.type === 'human') {
                return {
                  id: chatMessages.length + index,
                  type: 'text',
                  sender: 'self',
                  message: message.content,
                  complete: true,
                };
              } else if (message.type === 'ai') {
                return {
                  id: chatMessages.length + index,
                  type: 'text',
                  sender: 'bot',
                  message: message.content,
                  complete: true,
                };
              }
              return null;
            }).filter((message): message is ChatMessageObject => message !== null);

            setChatMessages((prevChatMessages) => prevChatMessages.concat(newChatMessages));
          },
          (error) => {
            setServerAvailable(false);
          }
        );
      },
      (error) => {
        setServerAvailable(false);
      }
    );
  }, []);

  useEffect(() => {
    if (!lastMessage || !serverAvailable) {
      return;
    }

    const websocketResponse = JSON.parse(lastMessage.data) as WebSocketResponse;

    if (websocketResponse.type === "debug") {
      console.log(websocketResponse.detail);
    } else if (websocketResponse.type === "error") {
      setConversationState("error");
      setErrorMessage(websocketResponse.detail);
      console.error(websocketResponse.detail);
    } else if (websocketResponse.type === "start") {
      setConversationState("streaming");

      setChatMessages((chatMessages) => [
        ...chatMessages,
        {
          id: chatMessages.length,
          type: "text",
          sender: "bot",
          message: "",
          complete: false,
        },
      ]);
    } else if (websocketResponse.type === "stream") {
      setChatMessages((chatMessages) => {
        const lastChatMessage = chatMessages[chatMessages.length - 1];
        const rest = chatMessages.slice(0, -1);

        return [
          ...rest,
          {
            ...lastChatMessage,
            message: lastChatMessage.message + websocketResponse.output,
          },
        ];
      });
    } else if (websocketResponse.type === "end") {
      setChatMessages((chatMessages) => {
        const lastChatMessage = chatMessages[chatMessages.length - 1];
        const rest = chatMessages.slice(0, -1);
        return [
          ...rest,
          {
            ...lastChatMessage,
            complete: true,
            cypher: websocketResponse.generated_cypher,
          },
        ];
      });
      setConversationState("ready");
    }
  }, [lastMessage]);

  useEffect(() => {
    if (conversationState === "error") {
      const timeout = setTimeout(() => {
        setConversationState("ready");
      }, 1000);
      return () => clearTimeout(timeout);
    }
  }, [conversationState]);

  const sendQuestion = (question: string) => {
    const webSocketRequest: WebSocketRequest = {
      type: "question",
      question: question,
      model: text2cypherModel,
      session_id: sessionId
    };
    sendJsonMessage(webSocketRequest);
  };

  const clearChatHistory = () => {
    const session_id = loadSessionIdFromStorage();
    const url = CLEAR_CHAT_HISTORY_URI + sessionId
    fetch(url, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(
      (response) => {
        response.json().then(
          (result) => {

            if (!result.success) {
              console.error("error on clearing chat history");
              setErrorMessage("error on clearing chat history")
            }
          },
          (error) => {
            setServerAvailable(false);
          }
        );
      },
      (error) => {
        setServerAvailable(false);
      }
    );
  };

  const onClearChatHistory = () => {
    if (conversationState === "ready") {
      setChatMessages((chatMessages) =>
        []
      );
      if (SEND_REQUESTS) {
        clearChatHistory();
      }
      setErrorMessage(null);
    }
  };

  const onChatInput = (message: string) => {
    if (conversationState === "ready") {
      setChatMessages((chatMessages) =>
        chatMessages.concat([
          {
            id: chatMessages.length,
            type: "input",
            sender: "self",
            message: message,
            complete: true,
          },
        ])
      );
      if (SEND_REQUESTS) {
        setConversationState("waiting");
        sendQuestion(message);
      }
      setErrorMessage(null);
    }
  };

  const openModal = () => {
    setModalIsOpen(true);
  };

  const onCloseModal = () => {
    setModalIsOpen(false);
  };

  const onApiKeyChange = (newApiKey: string) => {
    setApiKey(newApiKey);
    localStorage.setItem("api_key", newApiKey);
  };

  const onSessionIdChange = (newSessionId: string) => {
    setSessionId(newSessionId);
    localStorage.setItem("session_id", newSessionId);
  };

  const handleModelChange = (e: ChangeEvent<HTMLSelectElement>) => {
    setText2cypherModel(e.target.value)
  }

  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('darkMode') === 'true';
  });
  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode);
    localStorage.setItem('darkMode', darkMode.toString());
  }, [darkMode]);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

return (
  <div className="flex flex-col h-screen w-full bg-light-bg dark:bg-dark-bg transition-colors duration-300 overflow-hidden">
    <header className="flex justify-between items-center p-4 shadow-md bg-light-surface dark:bg-dark-surface w-full">
      <button
        onClick={toggleDarkMode}
        className="px-4 py-2 text-sm font-semibold text-light-text dark:text-dark-text bg-light-surface dark:bg-dark-surface rounded-md shadow-md hover:bg-light-border dark:hover:bg-dark-border transition duration-200"
      >
        Toggle {darkMode ? 'Light' : 'Dark'} Mode
      </button>
      {needsApiKey && (
        <button
          onClick={openModal}
          className="px-4 py-2 text-sm font-semibold text-light-text dark:text-dark-text bg-green-500 hover:bg-green-600 rounded-md shadow-md transition duration-200"
        >
          API Key
        </button>
      )}
      <select
        value={text2cypherModel}
        onChange={handleModelChange}
        className="p-2 text-sm font-semibold border border-light-border dark:border-dark-border rounded-md shadow-sm focus:outline-none focus:ring focus:ring-blue-300 bg-light-surface dark:bg-dark-surface text-light-text dark:text-dark-text transition duration-200"
      >
        <option value="openai">OpenAI</option>
        <option value="gpt4all">GPT4All</option>
      </select>
    </header>
    <div className="flex-1 flex flex-col items-center justify-center w-full overflow-hidden">
      {!serverAvailable && (
        <div className="text-center text-red-600 dark:text-red-400">
          Server is unavailable, please reload the page to try again.
        </div>
      )}
      {serverAvailable && needsApiKeyLoading && (
        <div className="text-center text-light-text dark:text-dark-text">
          Initializing...
        </div>
      )}
      <KeyModal
        isOpen={showContent && needsApiKey && modalIsOpen}
        onCloseModal={onCloseModal}
        onApiKeyChanged={onApiKeyChange}
        apiKey={apiKey}
      />
      {showContent && readyState === ReadyState.OPEN && (
        <>
          <div className="flex flex-1 w-full overflow-hidden max-w-xl">
            <ChatContainer
              chatMessages={chatMessages}
              loading={conversationState === 'waiting'}
            />
          </div>
          <div className="w-full max-w-xl bg-white dark:bg-gray-800 shadow-lg">
            <ChatInput
              onChatInput={onChatInput}
              onClearChatHistory={onClearChatHistory}
              loading={conversationState === 'waiting'}
            />
          </div>
          {errorMessage && (
            <div className="text-center text-red-600 dark:text-red-400">
              {errorMessage}
            </div>
          )}
        </>
      )}
      {showContent && readyState === ReadyState.CONNECTING && (
        <div className="text-center text-yellow-600 dark:text-yellow-400">
          Connecting...
        </div>
      )}
      {showContent && readyState === ReadyState.CLOSED && (
        <div className="text-center text-light-text dark:text-dark-text">
          <div>Could not connect to server, reconnecting...</div>
        </div>
      )}
    </div>
  </div>
);

}

export default App;
