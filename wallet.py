class Wallet:
    def __init__(self, address, private_key, balance=0, exchange_rate=3800):
        self.address = address
        self.private_key = private_key
        self.balance = balance
        self.exchange_rate = exchange_rate 

    def get_balance(self, blockchain):
        balance = self.balance
        for block in blockchain.chain:
            for transaction in block.transactions:
                if transaction.sender_id == self.address:
                    balance -= transaction.amount
                if transaction.recipient_id == self.address:
                    balance += transaction.amount
        return balance

    def convert_to_pesos(self, amount):
        """
        Convierte una cantidad de la moneda local a Pesos Colombianos.

        :param amount: Cantidad en moneda local.
        :return: Cantidad equivalente en Pesos Colombianos.
        """
        return amount * self.exchange_rate

    def get_balance_in_pesos(self, blockchain):
        """
        Obtiene el saldo de la cartera en Pesos Colombianos.

        :param blockchain: Instancia de la blockchain.
        :return: Saldo en Pesos Colombianos.
        """
        local_balance = self.get_balance(blockchain)
        return self.convert_to_pesos(local_balance)