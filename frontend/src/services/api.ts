import type {
  CatalogResponse,
  Dataset,
  HealthResponse,
  RecommendationResponse,
} from "../types/api";

const BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000"
).replace(/\/$/, "");

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  let response: Response;

  try {
    response = await fetch(`${BASE_URL}/api/v1${endpoint}`, options);
  } catch {
    throw new Error("Cannot reach FastAPI. Start backend on http://127.0.0.1:8000.");
  }

  const data: unknown = await response.json();
  if (!response.ok) {
    const detail = (data as { detail?: unknown })?.detail;
    const message = typeof detail === "string" ? detail : JSON.stringify(detail ?? data);
    throw new Error(message);
  }

  return data as T;
}

export const api = {
  health: () => request<HealthResponse>("/health"),
  catalog: (dataset: Dataset) =>
    request<CatalogResponse>(`/catalog?dataset=${encodeURIComponent(dataset)}`),
  recommend: (dataset: Dataset, items: string[], limit = 8) =>
    request<RecommendationResponse>("/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dataset, items, limit }),
    }),
};
