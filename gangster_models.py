from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Gangster:
    """Represents a gangster in the family"""
    name: str
    role: str
    weapon: str
    reputation: int = 50
    id: Optional[int] = None
    contracts_completed: int = 0
    join_date: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'weapon': self.weapon,
            'reputation': self.reputation,
            'contracts_completed': self.contracts_completed,
            'join_date': self.join_date.isoformat()
        }

@dataclass
class Contract:
    """Represents a job or contract for the family"""
    target: str
    reward: int
    difficulty: str  # Easy, Medium, Hard
    gangster_id: Optional[int] = None
    id: Optional[int] = None
    completed: bool = False
    completion_date: Optional[datetime] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'target': self.target,
            'reward': self.reward,
            'difficulty': self.difficulty,
            'gangster_id': self.gangster_id,
            'completed': self.completed,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None
        }

@dataclass
class Loot:
    """Represents money or valuables collected"""
    amount: int
    source: str
    gangster_id: Optional[int] = None
    id: Optional[int] = None
    date_collected: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'source': self.source,
            'gangster_id': self.gangster_id,
            'date_collected': self.date_collected.isoformat()
        }