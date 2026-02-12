import random
from datetime import datetime
from typing import Dict, Any
from gangster_models import Gangster

class GangsterUtils:
    """Utility functions for gangster operations"""
    
    @staticmethod
    def calculate_loot(reward: int, reputation: int) -> int:
        """Calculate actual loot based on reputation and luck"""
        # Higher reputation means better negotiation = more loot
        multiplier = 0.8 + (reputation / 500)  # 0.8 to 1.0 based on reputation
        base_loot = reward * multiplier
        
        # Add some random variation (luck factor)
        luck_factor = random.uniform(0.9, 1.1)
        
        return int(base_loot * luck_factor)
    
    @staticmethod
    def calculate_reputation_gain(difficulty: str) -> int:
        """Calculate reputation gain based on contract difficulty"""
        difficulty_multipliers = {
            'Easy': 2,
            'Medium': 5,
            'Hard': 10
        }
        return difficulty_multipliers.get(difficulty, 3)
    
    @staticmethod
    def calculate_gangster_stats(gangster: Gangster) -> Dict[str, Any]:
        """Calculate various stats for a gangster"""
        # Success rate is influenced by reputation
        success_rate = min(95, 40 + (gangster.reputation // 2))
        
        # Danger level is based on reputation and contracts completed
        danger_level = min(100, gangster.reputation // 2 + gangster.contracts_completed * 2)
        
        # Value to the family
        family_value = (gangster.reputation * 10) + (gangster.contracts_completed * 50)
        
        return {
            'name': gangster.name,
            'success_rate': success_rate,
            'danger_level': danger_level,
            'family_value': family_value,
            'status': 'Active' if gangster.reputation > 30 else 'On Probation'
        }
    
    @staticmethod
    def generate_gangster_nickname(name: str) -> str:
        """Generate a gangster-style nickname"""
        prefixes = ['Big', 'Little', 'Slick', 'Fast', 'Sly', 'Mad', 'Crazy', 'Silent']
        suffixes = ['The Nose', 'Fingers', 'The Blade', 'Knuckles', 'The Ghost', 'Ace']
        
        if random.choice([True, False]):
            return f"{random.choice(prefixes)} {name.split()[0]}"
        else:
            return f"{name.split()[0]} '{random.choice(suffixes)}'"
    
    @staticmethod
    def assess_contract_difficulty(reward: int) -> str:
        """Assess contract difficulty based on reward amount"""
        if reward < 10000:
            return 'Easy'
        elif reward < 30000:
            return 'Medium'
        else:
            return 'Hard'
    
    @staticmethod
    def format_currency(amount: int) -> str:
        """Format currency in gangster style"""
        if amount >= 1000000:
            return f"${amount/1000000:.1f}M"
        elif amount >= 1000:
            return f"${amount/1000:.1f}K"
        else:
            return f"${amount}"