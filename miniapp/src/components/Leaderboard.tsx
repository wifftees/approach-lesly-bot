import { Text } from "@mantine/core";
import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, XAxis, YAxis, LabelList } from "recharts";

interface LeaderboardEntry {
  name: string;
  points: number;
  count: number;
}

interface LeaderboardProps {
  data: LeaderboardEntry[];
  showCount?: boolean;
}

const COLORS = ["#228be6", "#40c057", "#fab005", "#fa5252", "#7950f2", "#15aabf", "#e64980"];

export function Leaderboard({ data, showCount = false }: LeaderboardProps) {
  if (data.length === 0) {
    return <Text c="dimmed" ta="center" py="xl">Пока нет данных</Text>;
  }

  const sorted = [...data]
    .sort((a, b) => b.points - a.points)
    .map((entry) => ({
      ...entry,
      label: showCount ? `${entry.points} pts (${entry.count} шт)` : `${entry.points}`,
    }));

  return (
    <ResponsiveContainer width="100%" height={Math.max(250, sorted.length * 50)}>
      <BarChart data={sorted} layout="vertical" margin={{ top: 5, right: 80, left: 10, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis type="number" />
        <YAxis type="category" dataKey="name" width={100} tick={{ fontSize: 12 }} />
        <Bar dataKey="points" radius={[0, 4, 4, 0]}>
          {sorted.map((_entry, index) => (
            <Cell key={index} fill={COLORS[index % COLORS.length]} />
          ))}
          <LabelList
            dataKey="label"
            position="right"
            style={{ fontSize: 11, fill: "var(--mantine-color-text)" }}
          />
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
