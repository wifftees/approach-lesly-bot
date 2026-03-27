import { List, Text, ThemeIcon } from "@mantine/core";

interface ContactsListProps {
  contacts: (string | null)[];
}

export function ContactsList({ contacts }: ContactsListProps) {
  if (contacts.length === 0) {
    return <Text c="dimmed" ta="center">Нет контактов</Text>;
  }

  return (
    <List spacing="xs" size="sm">
      {contacts.map((contact, i) => (
        <List.Item
          key={i}
          icon={
            <ThemeIcon color={contact ? "blue" : "gray"} size={20} radius="xl">
              <Text size="xs">{i + 1}</Text>
            </ThemeIcon>
          }
        >
          {contact ? `@${contact}` : "без контакта"}
        </List.Item>
      ))}
    </List>
  );
}
