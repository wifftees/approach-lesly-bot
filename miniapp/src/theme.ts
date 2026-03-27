import { createTheme, type MantineColorScheme } from "@mantine/core";

declare global {
  interface Window {
    Telegram?: {
      WebApp?: {
        themeParams?: Record<string, string>;
        colorScheme?: string;
        initData?: string;
      };
    };
  }
}

export function getTelegramColorScheme(): MantineColorScheme {
  return window.Telegram?.WebApp?.colorScheme === "dark" ? "dark" : "light";
}

export function getInitData(): string {
  return window.Telegram?.WebApp?.initData ?? "";
}

export const theme = createTheme({
  primaryColor: "blue",
  fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
});
