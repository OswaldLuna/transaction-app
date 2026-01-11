import type{ Transaction } from "../types";

interface Props {
  transactions: Transaction[];
}

export default function TransactionList({ transactions }: Props) {
  return (
    <div className="mt-6">
      <h2 className="text-lg font-semibold mb-2">Transacciones</h2>

      <table className="w-full bg-white shadow rounded">
        <thead className="bg-gray-100">
          <tr>
            <th className="p-2">ID</th>
            <th className="p-2">User</th>
            <th className="p-2">Monto</th>
            <th className="p-2">Tipo</th>
            <th className="p-2">Estado</th>
          </tr>
        </thead>

        <tbody>
          {transactions.map((t) => (
            <tr key={t.id} className="border-b text-center">
              <td className="p-2">{t.id}</td>
              <td className="p-2">{t.user_id}</td>
              <td className="p-2">{t.amount}</td>
              <td className="p-2">{t.type}</td>
              <td className="p-2 font-semibold">
                <span
                  className={
                    t.status === "procesado"
                      ? "text-green-600"
                      : t.status === "fallido"
                      ? "text-red-600"
                      : "text-yellow-500"
                  }
                >
                  {t.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
