import json
from typing import List, Dict, Optional
from gangster_models import Gangster, Contract, Loot
from datetime import datetime

class GangsterDatabase:
    """Handles all data storage and retrieval for the gangster operation"""
    
    def __init__(self):
        self.gangsters: Dict[int, Gangster] = {}
        self.contracts: Dict[int, Contract] = {}
        self.loot: Dict[int, Loot] = {}
        self.next_gangster_id = 1
        self.next_contract_id = 1
        self.next_loot_id = 1
    
    def init_sample_data(self):
        """Initialize with some sample gangsters and contracts"""
        # Add sample gangsters
        sample_gangsters = [
            Gangster("Tony 'The Nose' Soprano", "Boss", "Thompson SMG", 95),
            Gangster("Paulie Walnuts", "Enforcer", "Baseball Bat", 75),
            Gangster("Silvio Dante", "Consigliere", "Silenced Pistol", 85),
            Gangster("Christopher Moltisanti", "Soldier", "9mm", 65),
            Gangster("Bobby Baccalieri", "Associate", "Brass Knuckles", 45)
        ]
        
        for gangster in sample_gangsters:
            self.add_gangster(gangster)
        
        # Add sample contracts
        sample_contracts = [
            Contract("Rat Informant", 5000, "Easy"),
            Contract("Rival Bookie", 15000, "Medium"),
            Contract("Disloyal Capo", 50000, "Hard"),
            Contract("Uncooperative Business Owner", 10000, "Easy"),
            Contract("Territory Infringement", 30000, "Medium")
        ]
        
        for contract in sample_contracts:
            self.add_contract(contract)
    
    def add_gangster(self, gangster: Gangster) -> int:
        """Add a new gangster to the family"""
        gangster.id = self.next_gangster_id
        self.gangsters[self.next_gangster_id] = gangster
        self.next_gangster_id += 1
        return gangster.id
    
    def get_gangster(self, gangster_id: int) -> Optional[Gangster]:
        """Get a gangster by ID"""
        return self.gangsters.get(gangster_id)
    
    def get_all_gangsters(self) -> List[Gangster]:
        """Get all gangsters in the family"""
        return list(self.gangsters.values())
    
    def update_gangster(self, gangster: Gangster):
        """Update a gangster's information"""
        if gangster.id in self.gangsters:
            self.gangsters[gangster.id] = gangster
    
    def delete_gangster(self, gangster_id: int):
        """Remove a gangster from the family"""
        if gangster_id in self.gangsters:
            del self.gangsters[gangster_id]
    
    def add_contract(self, contract: Contract) -> int:
        """Add a new contract"""
        contract.id = self.next_contract_id
        self.contracts[self.next_contract_id] = contract
        self.next_contract_id += 1
        return contract.id
    
    def get_contract(self, contract_id: int) -> Optional[Contract]:
        """Get a contract by ID"""
        return self.contracts.get(contract_id)
    
    def get_active_contracts(self) -> List[Contract]:
        """Get all active (not completed) contracts"""
        return [c for c in self.contracts.values() if not c.completed]
    
    def assign_contract(self, contract_id: int, gangster_id: int) -> bool:
        """Assign a contract to a gangster"""
        contract = self.contracts.get(contract_id)
        gangster = self.gangsters.get(gangster_id)
        
        if contract and gangster and not contract.completed:
            contract.gangster_id = gangster_id
            contract.completed = True
            contract.completion_date = datetime.now()
            return True
        return False
    
    def delete_contract(self, contract_id: int):
        """Delete a contract"""
        if contract_id in self.contracts:
            del self.contracts[contract_id]
    
    def add_loot(self, loot: Loot) -> int:
        """Add loot to the collection"""
        loot.id = self.next_loot_id
        self.loot[self.next_loot_id] = loot
        self.next_loot_id += 1
        return loot.id
    
    def get_total_loot(self) -> int:
        """Calculate total loot collected"""
        return sum(loot.amount for loot in self.loot.values())
    
    def get_gangster_loot(self, gangster_id: int) -> List[Loot]:
        """Get all loot collected by a specific gangster"""
        return [loot for loot in self.loot.values() if loot.gangster_id == gangster_id]