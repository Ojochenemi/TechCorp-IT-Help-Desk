"""
Mock data for the IT Help Desk System.
Loads sample data from JSON files for tickets, agents, SLA rules, escalations, categories, and satisfaction ratings.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')


def load_json_file(filename):
    """Load data from a JSON file in the data directory."""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r') as f:
        return json.load(f)


tickets = load_json_file('tickets.json')
agents = load_json_file('agents.json')
sla_rules = load_json_file('sla_rules.json')
escalations = load_json_file('escalations.json')
categories = load_json_file('categories.json')
satisfaction_ratings = load_json_file('satisfaction.json')
comments = load_json_file('comments.json')
