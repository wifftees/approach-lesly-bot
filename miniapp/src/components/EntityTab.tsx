import { useState } from "react";
import { Button, Group, Select, Stack, Text } from "@mantine/core";
import { notifications } from "@mantine/notifications";

import { fetchContacts, sendContacts } from "../api/client";
import type { EntityType, StatsResponse, UserInfo } from "../types";
import { ContactsList } from "./ContactsList";
import { Leaderboard } from "./Leaderboard";

interface EntityTabProps {
  entityType: EntityType;
  data: StatsResponse | null;
}

export function EntityTab({ entityType, data }: EntityTabProps) {
  const [selectedUserId, setSelectedUserId] = useState<string | null>(null);
  const [contacts, setContacts] = useState<(string | null)[] | null>(null);
  const [loading, setLoading] = useState(false);

  if (!data) return null;

  const entityStats = data.stats.filter((s) => s.entity_type_slug === entityType.slug);

  const chartData = entityStats.map((s) => {
    const user = data.users.find((u) => u.user_id === s.user_id);
    return {
      name: displayName(user),
      points: s.points,
      count: s.count,
    };
  });

  const userOptions = data.users.map((u) => ({
    value: String(u.user_id),
    label: displayName(u),
  }));

  const handleShowContacts = async () => {
    if (!selectedUserId) return;
    setLoading(true);
    try {
      const res = await fetchContacts(Number(selectedUserId), entityType.slug);
      setContacts(res.contacts);
    } catch {
      notifications.show({ title: "Ошибка", message: "Не удалось загрузить контакты", color: "red" });
    } finally {
      setLoading(false);
    }
  };

  const handleSendContacts = async () => {
    if (!selectedUserId) return;
    setLoading(true);
    try {
      await sendContacts(Number(selectedUserId), entityType.slug);
      notifications.show({ title: "Готово", message: "Контакты отправлены в чат!", color: "green" });
    } catch {
      notifications.show({ title: "Ошибка", message: "Не удалось отправить контакты", color: "red" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Stack gap="md">
      <Leaderboard data={chartData} showCount />

      <Text fw={500} size="sm">Контакты пользователя</Text>
      <Select
        placeholder="Выбери пользователя"
        data={userOptions}
        value={selectedUserId}
        onChange={setSelectedUserId}
        searchable
      />
      <Group>
        <Button size="xs" onClick={handleShowContacts} loading={loading} disabled={!selectedUserId}>
          Показать контакты
        </Button>
        <Button size="xs" variant="outline" onClick={handleSendContacts} loading={loading} disabled={!selectedUserId}>
          Отправить контакты
        </Button>
      </Group>

      {contacts !== null && <ContactsList contacts={contacts} />}
    </Stack>
  );
}

function displayName(user?: UserInfo | null): string {
  if (!user) return "???";
  return user.username ? `@${user.username}` : String(user.user_id);
}
