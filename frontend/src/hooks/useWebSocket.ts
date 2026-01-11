import { useEffect } from "react";
import type { WSMessage } from "../types";

export function useWebSocket(onMessage: (msg: WSMessage) => void) {
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/transactions/stream");

    ws.onopen = () => {
      console.log("WebSocket conectado");
    };

    ws.onmessage = (event: MessageEvent) => {
      const data: WSMessage = JSON.parse(event.data);
      onMessage(data);
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    ws.onclose = () => {
      console.log("WebSocket cerrado");
    };

    return () => ws.close();
  }, [onMessage]);
}


