export type Domain =
  "school" | "scholarship" | "document" | "housing" | "legal" | "counselling";
export interface ResultSection {
  domain: Domain;
  title: string;
  guidance: string;
  data: Record<string, unknown>;
}
export interface AssistantResult {
  text: string;
  sections?: ResultSection[];
  sources?: { title: string; url: string }[];
  references?: string[];
  warnings?: string[];
}
export interface ChatRequest {
  session_id: string;
  request_id: string;
  message: string;
}
export interface ChatResponse {
  response: AssistantResult;
  request_id: string;
}
export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string | AssistantResult;
}
export interface Conversation {
  id: string;
  title: string;
  updated_at: string;
}
export interface ServiceStatus {
  ready: boolean;
  search_available: boolean;
}
