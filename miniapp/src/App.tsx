import { useEffect, useState } from "react";
import { ActionIcon, Container, Group, Tabs, Text, Title } from "@mantine/core";

import { fetchEntityTypes, fetchStats } from "./api/client";
import { AchievementsTab } from "./components/AchievementsTab";
import { EntityTab } from "./components/EntityTab";
import { OverallTab } from "./components/OverallTab";
import type { EntityType, StatsResponse } from "./types";

export default function App() {
  const [entityTypes, setEntityTypes] = useState<EntityType[]>([]);
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    setLoading(true);
    try {
      const [et, st] = await Promise.all([fetchEntityTypes(), fetchStats()]);
      setEntityTypes(et);
      setStats(st);
    } catch (err) {
      console.error("failed to load data", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <Container size="sm" py="md">
      <Group justify="space-between" mb="md">
        <Title order={3}>Статистика</Title>
        <ActionIcon variant="subtle" onClick={loadData} loading={loading} size="lg">
          <Text size="lg">🔄</Text>
        </ActionIcon>
      </Group>

      <Tabs defaultValue="overall">
        <Tabs.List>
          <Tabs.Tab value="overall">Общая</Tabs.Tab>
          {entityTypes.map((et) => (
            <Tabs.Tab key={et.slug} value={et.slug}>
              {et.display_name}
            </Tabs.Tab>
          ))}
          <Tabs.Tab value="achievements">🏆 Ачивки</Tabs.Tab>
        </Tabs.List>

        <Tabs.Panel value="overall" pt="md">
          <OverallTab data={stats} />
        </Tabs.Panel>

        {entityTypes.map((et) => (
          <Tabs.Panel key={et.slug} value={et.slug} pt="md">
            <EntityTab entityType={et} data={stats} />
          </Tabs.Panel>
        ))}

        <Tabs.Panel value="achievements" pt="md">
          <AchievementsTab />
        </Tabs.Panel>
      </Tabs>
    </Container>
  );
}
