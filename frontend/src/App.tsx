import { useState, useCallback } from "react";
import TransactionForm from "./components/TransactionForm";
import TransactionList from "./components/TransactionList";
import { useWebSocket } from "./hooks/useWebSocket";
import type{ Transaction, WSMessage } from "./types";
import toast from "react-hot-toast";

export default function App() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);

  const addTransaction = (tx: Transaction) => {
    setTransactions((prev) => {
      // No agregar si ya existe una transacción con el mismo id
      if (prev.some((t) => t.id === tx.id)) {
        return prev;
      }
      return [...prev, tx];
    });
  };

  const handleWS = useCallback((msg: WSMessage) => {
    setTransactions((prev) =>
      prev.map((t) =>
        t.id === msg.id ? { ...t, status: msg.status } : t
      )
    );

    // Notificación cuando cambia estado
    const statusText = msg.status === "procesado" 
      ? "procesada" 
      : msg.status === "fallido" 
      ? "fallida" 
      : msg.status;
    
    toast(`Transacción #${msg.id} → ${statusText}`, {
      icon:
        msg.status === "procesado"
          ? "✅"
          : msg.status === "fallido"
          ? "❌"
          : "⏳",
    });
  }, []);

  useWebSocket(handleWS);

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Gestión de Transacciones</h1>

      <TransactionForm onCreated={addTransaction} />

      <TransactionList transactions={transactions} />
    </div>
  );
}


