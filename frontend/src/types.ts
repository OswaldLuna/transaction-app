export interface Transaction {
  id: number;
  user_id: number;
  amount: number;
  type: string;
  status: string;
}

export interface TransactionCreate {
  user_id: number;
  amount: number;
  type: string;
}

export interface WSMessage {
  id: number;
  status: string;
}
