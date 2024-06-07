import tkinter as tk
from tkinter import messagebox
from blockchain import Blockchain
from crypto_utils import sign_transaction
from transaction import Transaction

class WalletGUI:
    def __init__(self, wallet):
        self.wallet = wallet
        self.blockchain = Blockchain()

        self.window = tk.Tk()
        self.window.title("Wallet")

        self.balance_label = tk.Label(self.window, text="Saldo: 0")
        self.balance_label.pack()

        self.balance_pesos_label = tk.Label(self.window, text="Saldo en Pesos Colombianos: 0")
        self.balance_pesos_label.pack()

        self.recipient_label = tk.Label(self.window, text="Destinatario:")
        self.recipient_label.pack()
        self.recipient_entry = tk.Entry(self.window)
        self.recipient_entry.pack()

        self.amount_label = tk.Label(self.window, text="Cantidad:")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self.window)
        self.amount_entry.pack()

        self.send_button = tk.Button(self.window, text="Enviar", command=self.send_transaction)
        self.send_button.pack()

        self.transactions_label = tk.Label(self.window, text="Transacciones:")
        self.transactions_label.pack()

        self.transactions_frame = tk.Frame(self.window)
        self.transactions_frame.pack(expand=True, fill='both')

        self.transactions_text = tk.Text(self.transactions_frame, height=10, width=100)
        self.transactions_text.pack(expand=True, fill='both')

        self.update_balance()
        self.update_transactions()

    def send_transaction(self):
        recipient = self.recipient_entry.get()
        amount = float(self.amount_entry.get())

        if self.wallet.balance >= amount:
            transaction = Transaction(amount, self.wallet.address, recipient)
            transaction.signature = sign_transaction(transaction, self.wallet.private_key)
            self.blockchain.add_transaction(transaction)  # Añadir la transacción a las transacciones pendientes
            
            # Minar un nuevo bloque con las transacciones pendientes
            previous_hash = self.blockchain.chain[-1].block_hash if self.blockchain.chain else "0" * 64
            new_block = self.blockchain.create_block(previous_hash)
            mined_block = new_block.proof_of_work(4)  # Dificultad de 4
            if mined_block:
                self.blockchain.add_block(mined_block)

            self.wallet.balance -= amount
            self.update_balance()
            self.update_transactions()
            messagebox.showinfo("Éxito", "Transacción enviada correctamente.")
        else:
            messagebox.showerror("Error", "Saldo insuficiente.")

    def update_balance(self):
        local_balance = self.wallet.get_balance(self.blockchain)
        self.balance_label.config(text="Saldo: " + str(local_balance))
        
        balance_in_pesos = self.wallet.convert_to_pesos(local_balance)
        self.balance_pesos_label.config(text="Saldo en Pesos Colombianos: " + str(balance_in_pesos))

    def update_transactions(self):
        self.transactions_text.delete("1.0", tk.END)
        for block in self.blockchain.chain:
            for transaction in block.transactions:
                self.transactions_text.insert(tk.END, str(transaction) + "\n")

    def start(self):
        self.window.mainloop()
