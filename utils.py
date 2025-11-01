import json
from typing import Dict, List, Tuple

def calculate_balance_denominations(balance_amount: float, available_denominations: List[float]) -> Dict[float, int]:
    """Calculate denominations needed for balance using greedy algorithm"""
    sorted_denoms = sorted(available_denominations, reverse=True)
    denominations_dict = {}
    remaining = balance_amount
    
    for denom in sorted_denoms:
        if remaining >= denom:
            count = int(remaining / denom)
            denominations_dict[denom] = count
            remaining = round(remaining - (count * denom), 2)
    
    return denominations_dict

def denominations_to_json(denoms_dict: Dict[float, int]) -> str:
    """Convert denominations dict to JSON string"""
    return json.dumps(denoms_dict)

def json_to_denominations(json_str: str) -> Dict[float, int]:
    """Convert JSON string to denominations dict"""
    if not json_str:
        return {}
    return json.loads(json_str)

def format_denominations(denoms_dict: Dict[float, int]) -> str:
    """Format denominations for display"""
    if not denoms_dict:
        return "No denominations"
    
    parts = []
    for denom in sorted(denoms_dict.keys(), reverse=True):
        count = denoms_dict[denom]
        if count > 0:
            parts.append(f"{int(denom)} x {count}")
    
    return ", ".join(parts) if parts else "No denominations"

def generate_bill_number(bill_id: int) -> str:
    """Generate bill number"""
    return f"BILL-{bill_id:06d}"
