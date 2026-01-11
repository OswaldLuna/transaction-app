import { useState } from "react";
import { api } from "../services/api";
import type{ Transaction, TransactionCreate } from "../types";
import toast from "react-hot-toast";

interface Props {
  onCreated: (tx: Transaction) => void;
}

export default function TransactionForm({ onCreated }: Props) {
  const [form, setForm] = useState<TransactionCreate>({
    user_id: 1,
    amount: 0,
    type: "deposit",
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;

    setForm({
      ...form,
      [name]: name === "user_id" || name === "amount" ? Number(value) : value,
    });
  };

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.post<Transaction>("/transactions/create", form);
      onCreated(res.data);
      setForm({ user_id: 1, amount: 0, type: "deposit" });

      if (res.data.status === "procesado") {
        toast.success(`Esta transacción #${res.data.id} ya fue procesada`);
        return;
      }

      toast.success(`Transacción #${res.data.id} creada exitosamente`);

      await api.post("/transactions/async-process", {
        transaction_id: res.data.id
      });
    } catch (error) {
      console.error("Error al crear la transacción:", error);
      toast.error("Error al crear la transacción");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="p-4 bg-white shadow rounded" onSubmit={submit}>
      <h2 className="text-lg font-semibold mb-2">Crear Transacción</h2>

      <div className="mb-2">
        <label htmlFor="user_id" className="block text-sm font-medium mb-1">
          User ID
        </label>
        <input
          id="user_id"
          name="user_id"
          placeholder="User ID"
          value={form.user_id}
          type="number"
          min="1"
          onChange={handleChange}
          className="border p-2 w-full rounded"
          required
        />
      </div>

      <div className="mb-2">
        <label htmlFor="amount" className="block text-sm font-medium mb-1">
          Monto
        </label>
        <input
          id="amount"
          name="amount"
          placeholder="Monto"
          value={form.amount}
          type="number"
          onChange={handleChange}
          className="border p-2 w-full rounded"
          required
        />
      </div>

      <div className="mb-2">
        <label htmlFor="type" className="block text-sm font-medium mb-1">
          Tipo de transacción
        </label>
        <select
          id="type"
          name="type"
          value={form.type}
          onChange={handleChange}
          className="border p-2 w-full rounded"
        >
          <option value="deposit">Depósito</option>
          <option value="withdraw">Retiro</option>
        </select>
      </div>

      <button 
        type="submit"
        disabled={loading}
        className="mt-2 bg-blue-600 text-white px-4 py-2 rounded w-full hover:bg-blue-700 hover:cursor-pointer disabled:bg-blue-300 disabled:cursor-not-allowed flex items-center justify-center"
      >
        {loading ? (
          <>
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Creando...
          </>
        ) : (
          "Crear"
        )}
      </button>
    </form>
  );
}
