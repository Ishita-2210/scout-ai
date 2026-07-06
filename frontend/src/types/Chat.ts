export interface ChatRequest {
  user_id: string;
  session_id: string;
  message: string;
}

export interface ChatResponse {
  response: string;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}