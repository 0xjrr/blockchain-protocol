class Transaction:
    def __init__(self, inputs, outputs, signature):
        self.inputs = inputs
        self.outputs = outputs
        self.signature = signature
        self.id = self.calculate_tx_id()

    def calculate_tx_id(self):
        # Simplified ID calculation
        return hash(str(self.inputs) + str(self.outputs))
