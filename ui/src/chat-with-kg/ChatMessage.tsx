import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export type ChatMessageObject = {
  id: number;
  type: "input" | "text" | "error";
  message: string;
  cypher?: string | null;
  sender: "bot" | "self";
  complete: boolean;
};

export interface ChatMessageResponseObject {
  content: string;
  type: "human" | "ai";
  additional_kwargs: object;
  response_metadata: object;
  name: string | null;
  id: string | null;
  example: boolean;
  tool_calls?: any[];
  invalid_tool_calls?: any[];
  usage_metadata?: any;
}

export type ChatMessageProps = {
  chatMessage: ChatMessageObject;
};

function ChatMessage({ chatMessage }: ChatMessageProps) {
  const { message, sender, cypher } = chatMessage;

  const isBot = sender === "bot";
  const chatClass = `flex relative max-w-full ${
    isBot ? "self-start mr-10" : "ml-10 self-end"
  }`;

  const backgroundColorClass = isBot
    ? "bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-200" // Bot message colors
    : "bg-blue-500 text-white dark:bg-gray-700 dark:text-gray-200";  // User message colors

  const messageBubbleClass = `min-w-0 max-w-lg px-5 py-3 rounded-xl shadow-md break-words ${backgroundColorClass} ${
    isBot ? "rounded-br-xl" : "rounded-bl-xl"
  }`;

  return (
    <div className={chatClass}>
      {isBot && <ChatMessageTail side="left" />}
      <div
        className={messageBubbleClass}
        dir="rtl"
        style={{ textAlign: "right" }}
      >
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            h1: ({ node, ...props }) => (
              <h1 className="text-2xl font-bold mb-2" {...props} />
            ),
            h2: ({ node, ...props }) => (
              <h2 className="text-xl font-semibold mb-2" {...props} />
            ),
            h3: ({ node, ...props }) => (
              <h3 className="text-lg font-semibold mb-1" {...props} />
            ),
            p: ({ node, ...props }) => <p className="mb-2" {...props} />,
            ul: ({ node, ...props }) => (
              <ul className="list-disc list-inside mb-2" {...props} />
            ),
            ol: ({ node, ...props }) => (
              <ol className="list-decimal list-inside mb-2" {...props} />
            ),
            li: ({ node, ...props }) => <li className="ml-4" {...props} />,
            blockquote: ({ node, ...props }) => (
              <blockquote className="border-l-4 border-blue-400 pl-4 italic mb-2" {...props} />
            ),
            code({ node, inline, className, children, ...props }) {
              return (
                <code
                  className={`bg-gray-100 dark:bg-gray-700 rounded px-1 ${
                    inline ? "inline" : "block p-2"
                  } font-mono`}
                  {...props}
                >
                  {children}
                </code>
              );
            },
            table: ({ children }) => (
              <div className="overflow-x-auto">
                <table className="min-w-full border-collapse">{children}</table>
              </div>
            ),
            th: ({ children }) => (
              <th className="px-4 py-2 border-b bg-gray-100 dark:bg-gray-700 font-semibold">
                {children}
              </th>
            ),
            td: ({ children }) => (
              <td className="px-4 py-2 border-b">{children}</td>
            ),
            tr: ({ children }) => (
              <tr className="hover:bg-gray-100 dark:hover:bg-gray-700">
                {children}
              </tr>
            ),
          }}
        >
          {message}
        </ReactMarkdown>
        {isBot && cypher && <ChatCypherDetail cypher={cypher} />}
      </div>
      {!isBot && <ChatMessageTail side="right" />}
    </div>
  );
}

function ChatMessageTail({ side }: { side: "left" | "right" }) {
  const chatTailStyle: React.CSSProperties = {
    width: "0.75rem",
    height: "0.75rem",
    WebkitMaskImage: `url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0nMycgaGVpZ2h0PSczJyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnPjxwYXRoIGZpbGw9J2JsYWNrJyBkPSdtIDAgMyBMIDMgMyBMIDMgMCBDIDMgMSAxIDMgMCAzJy8+PC9zdmc+)`,
    maskImage: `url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0nMycgaGVpZ2h0PSczJyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnPjxwYXRoIGZpbGw9J2JsYWNrJyBkPSdtIDAgMyBMIDMgMyBMIDMgMCBDIDMgMSAxIDMgMCAzJy8+PC9zdmc+)`,
    WebkitMaskPosition: "center",
    maskPosition: "center",
    maskSize: "contain",
    WebkitMaskSize: "contain",
    backgroundColor: side === "left" ? "#374151" : "#3B82F6",
  };

  if (side === "left") {
    chatTailStyle["left"] = "-0.75rem";
  } else {
    chatTailStyle["right"] = "-0.75rem";
    chatTailStyle["WebkitTransform"] = "scaleX(-1)";
    chatTailStyle["transform"] = "scaleX(-1)";
  }

  return <div style={chatTailStyle}></div>;
}

function ChatCypherDetail({ cypher }: { cypher: string }) {
  return (
    <details>
      <summary className="cursor-pointer text-blue-500">Cypher</summary>
      <div className="min-w-0 px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-200">
        {cypher}
      </div>
    </details>
  );
}

export default ChatMessage;
