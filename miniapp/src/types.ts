export interface EntityType {
  id: number;
  slug: string;
  display_name: string;
  points: number;
}

export interface UserInfo {
  user_id: number;
  username: string | null;
  first_name: string | null;
}

export interface Stat {
  user_id: number;
  entity_type_slug: string;
  count: number;
  points: number;
}

export interface StatsResponse {
  users: UserInfo[];
  stats: Stat[];
  entity_types: EntityType[];
}

export interface ContactsResponse {
  contacts: (string | null)[];
  user: { username: string | null; first_name: string | null };
  entity_type: { display_name: string };
}

export interface Achievement {
  id: number;
  entity_type_slug: string;
  name: string;
  emoji: string;
  threshold: number;
  sort_order: number;
}

export interface AchievementsResponse {
  achievements: Achievement[];
  user_achievements: number[];
  users: UserInfo[];
}
