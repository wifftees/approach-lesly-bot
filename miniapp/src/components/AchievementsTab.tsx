import { useEffect, useState } from "react";
import { Box, Group, Loader, Paper, Select, Stack, Text, Title } from "@mantine/core";

import { fetchAchievements } from "../api/client";
import type { Achievement, AchievementsResponse, UserInfo } from "../types";

export function AchievementsTab() {
  const [data, setData] = useState<AchievementsResponse | null>(null);
  const [selectedUserId, setSelectedUserId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [initialized, setInitialized] = useState(false);

  useEffect(() => {
    fetchAchievements()
      .then((res) => {
        setData(res);
        setInitialized(true);
      })
      .catch((err) => console.error("failed to load achievements", err))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!initialized || !selectedUserId) return;
    setLoading(true);
    fetchAchievements(Number(selectedUserId))
      .then(setData)
      .catch((err) => console.error("failed to load achievements", err))
      .finally(() => setLoading(false));
  }, [selectedUserId]);

  if (!data) {
    return loading ? <Loader size="sm" /> : null;
  }

  const userOptions = data.users.map((u: UserInfo) => ({
    value: String(u.user_id),
    label: u.username ? `@${u.username}` : u.first_name || String(u.user_id),
  }));

  const girlAchievements = data.achievements
    .filter((a) => a.entity_type_slug === "girl")
    .sort((a, b) => a.sort_order - b.sort_order);

  const beautifulGirlAchievements = data.achievements
    .filter((a) => a.entity_type_slug === "beautiful_girl")
    .sort((a, b) => a.sort_order - b.sort_order);

  const unlockedSet = new Set(data.user_achievements);

  return (
    <Stack gap="md">
      <Select
        placeholder="Выбери пользователя"
        data={userOptions}
        value={selectedUserId}
        onChange={setSelectedUserId}
        searchable
      />

      {loading ? (
        <Loader size="sm" />
      ) : (
        <>
          <Box>
            <Title order={5} mb="xs">Девочка</Title>
            <ProgressChain achievements={girlAchievements} unlockedIds={unlockedSet} />
          </Box>

          <Box>
            <Title order={5} mb="xs">Красивая девочка</Title>
            <ProgressChain achievements={beautifulGirlAchievements} unlockedIds={unlockedSet} />
          </Box>
        </>
      )}
    </Stack>
  );
}

function ProgressChain({ achievements, unlockedIds }: { achievements: Achievement[]; unlockedIds: Set<number> }) {
  return (
    <Group gap={0} wrap="nowrap" style={{ overflowX: "auto" }}>
      {achievements.map((ach, idx) => {
        const unlocked = unlockedIds.has(ach.id);
        return (
          <Group key={ach.id} gap={0} wrap="nowrap" align="center">
            <Paper
              p="xs"
              radius="md"
              withBorder
              style={{
                minWidth: 80,
                textAlign: "center",
                borderColor: unlocked ? "var(--mantine-color-green-6)" : "var(--mantine-color-gray-4)",
                backgroundColor: unlocked ? "var(--mantine-color-green-0)" : "var(--mantine-color-gray-0)",
                opacity: unlocked ? 1 : 0.6,
              }}
            >
              <Text size="xl">{ach.emoji}</Text>
              <Text size="xs" fw={500} lineClamp={1}>{ach.name}</Text>
              <Text size="xs" c="dimmed">{ach.threshold}</Text>
            </Paper>
            {idx < achievements.length - 1 && (
              <Box
                style={{
                  width: 24,
                  height: 2,
                  backgroundColor: "var(--mantine-color-gray-4)",
                  flexShrink: 0,
                }}
              />
            )}
          </Group>
        );
      })}
    </Group>
  );
}
