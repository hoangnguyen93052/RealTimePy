import json
import hashlib
from datetime import datetime

class SmartContract:
    def __init__(self, contract_id, terms, parties):
        self.contract_id = contract_id
        self.terms = terms  # A dict containing the contract terms
        self.parties = parties  # List of parties involved
        self.timestamp = datetime.now().isoformat()
        self.is_executed = False
        self.execution_result = None

    def execute(self):
        if self.is_executed:
            raise Exception("Contract has already been executed.")
        self.execution_result = self.process_terms()
        self.is_executed = True

    def process_terms(self):
        # This method would contain the logic to enact the contract terms
        return f"Executed terms: {self.terms}"

    def to_dict(self):
        return {
            "contract_id": self.contract_id,
            "terms": self.terms,
            "parties": self.parties,
            "timestamp": self.timestamp,
            "is_executed": self.is_executed,
            "execution_result": self.execution_result,
        }

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_contracts = []

    def add_contract(self, contract):
        self.pending_contracts.append(contract)

    def mine_contracts(self):
        if not self.pending_contracts:
            raise Exception("No contracts to mine.")
        for contract in self.pending_contracts:
            contract.execute()
            self.chain.append(contract.to_dict())
        self.pending_contracts = []

    def get_chain(self):
        return self.chain

    def get_contract(self, contract_id):
        for contract in self.chain:
            if contract['contract_id'] == contract_id:
                return contract
        return None

class ContractManager:
    def __init__(self):
        self.blockchain = Blockchain()

    def create_contract(self, terms, parties):
        contract_id = self.generate_contract_id(terms, parties)
        contract = SmartContract(contract_id, terms, parties)
        self.blockchain.add_contract(contract)

    def generate_contract_id(self, terms, parties):
        unique_string = f"{terms}{parties}{datetime.now()}"
        return hashlib.sha256(unique_string.encode()).hexdigest()

    def mine_pending_contracts(self):
        self.blockchain.mine_contracts()

    def view_contract(self, contract_id):
        return self.blockchain.get_contract(contract_id)

    def get_all_contracts(self):
        return self.blockchain.get_chain()

def save_contracts_to_file(filename, contracts):
    with open(filename, 'w') as f:
        json.dump(contracts, f, indent=4)

def load_contracts_from_file(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def main():
    manager = ContractManager()

    # Load existing contracts from a file
    existing_contracts = load_contracts_from_file('contracts.json')
    for contract_data in existing_contracts:
        contract = SmartContract(contract_data['contract_id'], contract_data['terms'], contract_data['parties'])
        manager.blockchain.chain.append(contract_data)

    while True:
        print("1. Create a new smart contract")
        print("2. Mine pending contracts")
        print("3. View a smart contract")
        print("4. View all contracts")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            terms = input("Enter the terms of the contract: ")
            parties = input("Enter the parties involved, separated by commas: ").split(',')
            manager.create_contract(terms, parties)
            print("Contract created and added to pending contracts.")
        
        elif choice == '2':
            try:
                manager.mine_pending_contracts()
                print("Pending contracts have been mined.")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '3':
            contract_id = input("Enter the contract ID: ")
            contract = manager.view_contract(contract_id)
            if contract:
                print("Contract details:", contract)
            else:
                print("Contract not found.")
        
        elif choice == '4':
            contracts = manager.get_all_contracts()
            print("All contracts:")
            for contract in contracts:
                print(contract)

        elif choice == '5':
            save_contracts_to_file('contracts.json', manager.blockchain.chain)
            print("Contracts saved to file. Exiting.")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()