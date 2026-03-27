import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { MantineProvider } from "@mantine/core";
import { Notifications } from "@mantine/notifications";

import "@mantine/core/styles.css";
import "@mantine/notifications/styles.css";

import App from "./App";
import { getTelegramColorScheme, theme } from "./theme";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <MantineProvider theme={theme} defaultColorScheme={getTelegramColorScheme()}>
      <Notifications position="top-center" />
      <App />
    </MantineProvider>
  </StrictMode>,
);
