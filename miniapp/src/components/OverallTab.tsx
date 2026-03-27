import { Leaderboard } from "./Leaderboard";
import type { StatsResponse, UserInfo } from "../types";

interface OverallTabProps {
  data: StatsResponse | null;
}

export function OverallTab({ data }: OverallTabProps) {
  if (!data) return null;

  const userTotals = new Map<number, { name: string; points: number; count: number }>();

  for (const user of data.users) {
    userTotals.set(user.user_id, {
      name: displayName(user),
      points: 0,
      count: 0,
    });
  }

  for (const stat of data.stats) {
    const entry = userTotals.get(stat.user_id);
    if (entry) {
      entry.points += stat.points;
      entry.count += stat.count;
    }
  }

  const chartData = Array.from(userTotals.values()).filter((e) => e.points > 0);

  return <Leaderboard data={chartData} />;
}

function displayName(user: UserInfo): string {
  return user.username ? `@${user.username}` : String(user.user_id);
}
