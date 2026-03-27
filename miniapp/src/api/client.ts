import { getInitData } from "../theme";
import type { ContactsResponse, EntityType, StatsResponse } from "../types";

const BASE_URL = "";

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "X-Telegram-Init-Data": getInitData(),
      ...options?.headers,
    },
  });
  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }
  return res.json();
}

export async function fetchEntityTypes(): Promise<EntityType[]> {
  return apiFetch<EntityType[]>("/api/entity-types");
}

export async function fetchStats(): Promise<StatsResponse> {
  return apiFetch<StatsResponse>("/api/stats");
}

export async function fetchContacts(userId: number, entityTypeSlug: string): Promise<ContactsResponse> {
  return apiFetch<ContactsResponse>(`/api/contacts?user_id=${userId}&entity_type_slug=${entityTypeSlug}`);
}

export async function sendContacts(targetUserId: number, entityTypeSlug: string): Promise<{ ok: boolean; message?: string }> {
  return apiFetch("/api/send-contacts", {
    method: "POST",
    body: JSON.stringify({ target_user_id: targetUserId, entity_type_slug: entityTypeSlug }),
  });
}
