export type WebSocketRequest = {
  type: "question";
  question: string;
  session_id?: string;
  model?: string;
};

export type WebSocketResponse =
  | { type: "start" }
  | {
      type: "stream";
      output: string;
    }
  | {
      type: "end";
      output: string;
      generated_cypher: string | null;
    }
  | {
      type: "error";
      detail: string;
    }
  | {
      type: "debug";
      detail: string;
    };

export type ConversationState = "waiting" | "streaming" | "ready" | "error";
