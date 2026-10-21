import type {
  ChatRequest,
  ChatResponse,
  Conversation,
  Message,
  ServiceStatus,
} from "../types/Chat";

export class ApiError extends Error {
  retryAfter: number;
  status: number;
  constructor(message: string, status = 0, retryAfter = 0) {
    super(message);
    this.status = status;
    this.retryAfter = retryAfter;
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`/api${path}`, {
      ...options,
      credentials: "same-origin",
      headers: { "Content-Type": "application/json", ...options.headers },
    });
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError")
      throw error;
    throw new ApiError(
      "Scout could not be reached. Check your connection and try again.",
    );
  }
  if (!response.ok) {
    const data = await response.json().catch(() => null);
    const detail = data?.detail;
    const message = typeof detail === "string" ? detail : detail?.message;
    throw new ApiError(
      message || "Scout could not complete the request. Please try later.",
      response.status,
      Number(response.headers.get("Retry-After")) || 0,
    );
  }
  return response.status === 204 ? (undefined as T) : response.json();
}

// Share initialization across React StrictMode mounts; no automatic chat retries.
let initialization: Promise<ServiceStatus> | undefined;
export function initializeSession() {
  initialization ??= request<ServiceStatus>("/session", {
    method: "POST",
  }).catch((error) => {
    initialization = undefined;
    throw error;
  });
  return initialization;
}
export const getConversations = () => request<Conversation[]>("/conversations");
export const getMessages = (id: string, signal?: AbortSignal) =>
  request<Message[]>(`/conversations/${id}`, { signal });
export const deleteConversation = (id: string) =>
  request<void>(`/conversations/${id}`, { method: "DELETE" });
export const deleteAllData = () => request<void>("/data", { method: "DELETE" });
export const sendMessage = (body: ChatRequest, signal: AbortSignal) =>
  request<ChatResponse>("/chat", {
    method: "POST",
    body: JSON.stringify(body),
    signal,
  });
