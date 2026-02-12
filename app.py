from flask import Flask, render_template, request, jsonify, redirect, url_for
from gangster_database import GangsterDatabase
from gangster_utils import GangsterUtils
from gangster_models import Gangster, Contract, Loot
import json

app = Flask(__name__)
db = GangsterDatabase()
utils = GangsterUtils()

@app.route('/')
def index():
    """Home page - shows all gangsters and their operations"""
    gangsters = db.get_all_gangsters()
    contracts = db.get_active_contracts()
    total_loot = db.get_total_loot()
    
    # Get gangster stats
    gangster_stats = []
    for gangster in gangsters:
        stats = utils.calculate_gangster_stats(gangster)
        gangster_stats.append(stats)
    
    return render_template('index.html', 
                          gangsters=gangsters, 
                          contracts=contracts,
                          gangster_stats=gangster_stats,
                          total_loot=total_loot)

@app.route('/api/gangsters', methods=['GET'])
def get_gangsters():
    """API endpoint to get all gangsters"""
    gangsters = db.get_all_gangsters()
    return jsonify([gangster.to_dict() for gangster in gangsters])

@app.route('/api/gangsters', methods=['POST'])
def add_gangster():
    """Add a new gangster"""
    data = request.json
    gangster = Gangster(
        name=data['name'],
        role=data['role'],
        weapon=data['weapon'],
        reputation=data.get('reputation', 50)
    )
    db.add_gangster(gangster)
    return jsonify({'success': True, 'gangster': gangster.to_dict()})

@app.route('/api/contracts', methods=['POST'])
def add_contract():
    """Add a new contract"""
    data = request.json
    contract = Contract(
        target=data['target'],
        reward=data['reward'],
        difficulty=data['difficulty'],
        gangster_id=data.get('gangster_id')
    )
    db.add_contract(contract)
    return jsonify({'success': True, 'contract': contract.to_dict()})

@app.route('/api/contracts/<int:contract_id>/assign', methods=['POST'])
def assign_contract(contract_id):
    """Assign a contract to a gangster"""
    data = request.json
    gangster_id = data['gangster_id']
    
    success = db.assign_contract(contract_id, gangster_id)
    if success:
        gangster = db.get_gangster(gangster_id)
        contract = db.get_contract(contract_id)
        
        # Calculate loot based on difficulty and gangster reputation
        loot_amount = utils.calculate_loot(contract.reward, gangster.reputation)
        loot = Loot(amount=loot_amount, source=f"Contract: {contract.target}", gangster_id=gangster_id)
        db.add_loot(loot)
        
        # Update gangster reputation
        gangster.reputation += utils.calculate_reputation_gain(contract.difficulty)
        db.update_gangster(gangster)
        
        return jsonify({'success': True, 'loot': loot_amount})
    
    return jsonify({'success': False}), 400

@app.route('/api/contracts/<int:contract_id>', methods=['DELETE'])
def delete_contract(contract_id):
    """Delete a contract"""
    db.delete_contract(contract_id)
    return jsonify({'success': True})

@app.route('/api/gangsters/<int:gangster_id>', methods=['DELETE'])
def delete_gangster(gangster_id):
    """Delete a gangster"""
    db.delete_gangster(gangster_id)
    return jsonify({'success': True})

if __name__ == '__main__':
    # Initialize with some sample data
    db.init_sample_data()
    app.run(debug=True)