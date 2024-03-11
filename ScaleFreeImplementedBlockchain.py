import hashlib
import datetime as date
import random
import time

class Transaction:
    def __init__(self, sender, recipient, amount, signature=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "signature": self.signature,
        }

    def sign(self, signature):
        self.signature = signature

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, nonce=0, network_node=None):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.network_node = network_node  # Link block to a network node
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_header = str(self.index) + str(self.timestamp) + str(self.previous_hash) + str(self.nonce) + str(self.network_node)
        block_transactions = "".join([str(tx.to_dict()) for tx in self.transactions])
        hash_string = block_header + block_transactions
        return hashlib.sha256(hash_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print("Block mined: ", self.hash)

class SimpleBlockchain:
    def __init__(self, difficulty=2):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = 10

    def create_genesis_block(self):
        return Block(0, date.datetime.now(), [], "0", network_node=None)

    def mine_pending_transactions(self, mining_reward_address):
        if not self.pending_transactions:
            print("No transactions to mine.")
            return

        valid_transactions = [tx for tx in self.pending_transactions if self.validate_transaction(tx)]
        if not valid_transactions:
            print("No valid transactions to mine.")
            return

        block = Block(len(self.chain), date.datetime.now(), valid_transactions, self.get_latest_block().hash, network_node=None)
        block.mine_block(self.difficulty)

        print("Block successfully mined!")
        self.chain.append(block)
        self.pending_transactions = [Transaction(None, mining_reward_address, self.mining_reward)]

    def get_latest_block(self):
        return self.chain[-1]

    def create_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def validate_transaction(self, transaction):
        if transaction.amount <= 0:
            return False
        if not transaction.sender or not transaction.recipient:
            return False
        return True

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

class ScaleFreeNetwork:
    def __init__(self, initial_nodes=3):
        self.nodes = list(range(initial_nodes))
        self.edges = [(i, j) for i in self.nodes for j in self.nodes if i != j]  # Fully connect initial nodes

    def add_node(self, m=1):
        new_node_id = len(self.nodes)
        self.nodes.append(new_node_id)

        node_degrees = {node: 0 for node in self.nodes}
        for edge in self.edges:
            node_degrees[edge[0]] += 1
            node_degrees[edge[1]] += 1

        potential_edges = [(new_node_id, node) for node in self.nodes if node != new_node_id]
        chosen_edges = random.choices(potential_edges, weights=[node_degrees[edge[1]] for edge in potential_edges], k=m)

        self.edges.extend(chosen_edges)
        return new_node_id

class Blockchain(SimpleBlockchain):
    def __init__(self, difficulty=2):
        super().__init__(difficulty)
        self.network = ScaleFreeNetwork()  # Add scale free network
        self.chain[0].network_node = self.network.add_node()  # Assign network node to genesis block

    def mine_pending_transactions(self, mining_reward_address):
        new_node_id = self.network.add_node()  # For each new block, simulate adding a new node to the network
        super().mine_pending_transactions(mining_reward_address)
        self.chain[-1].network_node = new_node_id

def measure_performance(blockchain):
    start_time = time.time()
    for _ in range(100):
        blockchain.create_transaction(Transaction("Sender", "Recipient", 10))
        blockchain.mine_pending_transactions("Miner")
    end_time = time.time()
    elapsed_time = end_time - start_time
    throughput = 100 / elapsed_time
    latency = elapsed_time / 100
    return throughput, latency

# Measure and compare performance
simple_blockchain = SimpleBlockchain(difficulty=2)
simple_throughput, simple_latency = measure_performance(simple_blockchain)

scale_free_blockchain = Blockchain(difficulty=2)
scale_free_throughput, scale_free_latency = measure_performance(scale_free_blockchain)

print("Simple Blockchain - Throughput: {:.2f} tx/s, Latency: {:.6f} s/tx".format(simple_throughput, simple_latency))
print("Scale-Free Blockchain - Throughput: {:.2f} tx/s, Latency: {:.6f} s/tx".format(scale_free_throughput, scale_free_latency))
