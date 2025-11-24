#!/usr/bin/env python3
"""
Test simple des validations @validates
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Mock minimal pour éviter les dépendances Flask/SQLAlchemy
class MockModel:
    def __init__(self):
        self._validates = {}
    
    def validates(self, *fields):
        def decorator(func):
            for field in fields:
                self._validates[field] = func
            return func
        return decorator
    
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if hasattr(self, '_validates') and name in self._validates:
            try:
                result = self._validates[name](self, name, value)
                super().__setattr__(name, result)
            except Exception as e:
                print(f"✗ Validation error for {name}: {e}")
                raise

# Mock des requêtes
class MockQuery:
    def get(self, id):
        # Simuler quelques données de test
        if id == 'PLA001':
            return type('Plateforme', (), {
                'id_pla': 'PLA001', 'cout_exploi_jour': 100.5,
                'jours_av_mainte': 30, 'inter_mainte': 365
            })()
        elif id == 'B001':
            return type('Budget', (), {'id_budg': 'B001', 'valeur': 10000.0})()
        elif id == 'C001':
            return type('Campagne', (), {
                'id_camp': 'C001', 'date_deb_camp': '2025-09-11', 'duree': 2
            })()
        return None
    
    def filter_by(self, **kwargs):
        # Retourner un objet avec méthode all()
        return self
    
    def all(self):
        # Simuler des résultats vides pour les tests simples
        return []
    
    def count(self):
        # Pour les requêtes count()
        return 0

# Patcher les imports
import monApp.models as models
models.db = MockModel()
models.validates = MockModel().validates

# Mock des classes de requête
models.Habilitation.query = MockQuery()
models.Plateforme.query = MockQuery()
models.Personnel.query = MockQuery()
models.Campagne.query = MockQuery()
models.Budget.query = MockQuery()
models.SpecialiserEn.query = MockQuery()
models.Necessiter.query = MockQuery()
models.Participer.query = MockQuery()

# Mock timedelta
import datetime
models.timedelta = datetime.timedelta

def test_participer():
    print("=== Test Participer ===")
    try:
        part = models.Participer('PER001', 'C001')
        print("✓ Participer créé sans erreur")
    except Exception as e:
        print(f"Erreur: {e}")

def test_campagne():
    print("\n=== Test Campagne ===")
    try:
        camp = models.Campagne('C002', 5, '2025-10-01', 'PLA001', 'B001')
        print("✓ Campagne créée sans erreur")
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    test_participer()
    test_campagne()
    print("\n=== Tests terminés ===")