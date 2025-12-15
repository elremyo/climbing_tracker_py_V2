"""
Calculs de statistiques pour une voie spécifique.
"""
from datetime import datetime

class RouteStatsService:
    """Service de calcul des stats d'une voie"""
    
    @staticmethod
    def get_route_stats(route_attempts):
        """
        Calcule toutes les stats d'une voie.
        
        Args:
            route_attempts: liste des tentatives de la voie
            
        Returns:
            dict avec {
                'total': int,
                'success_count': int,
                'success_rate': float,
                'first_attempt_date': str,
                'last_attempt_date': str
            }
        """
        if not route_attempts:
            return {
                'total': 0,
                'success_count': 0,
                'success_rate': 0,
                'first_attempt_date': None,
                'last_attempt_date': None
            }
        
        success_count = sum(1 for a in route_attempts if a["success"])
        success_rate = (success_count / len(route_attempts)) * 100
        
        oldest = min(route_attempts, key=lambda a: a["date"])
        newest = max(route_attempts, key=lambda a: a["date"])
        
        return {
            'total': len(route_attempts),
            'success_count': success_count,
            'success_rate': success_rate,
            'first_attempt_date': oldest["date"],
            'last_attempt_date': newest["date"]
        }
    
    @staticmethod
    def get_progression_timeline(route_attempts):
        """
        Retourne les tentatives triées par date pour affichage timeline.
        Plus récentes en haut.
        
        Args:
            route_attempts: liste des tentatives
            
        Returns:
            liste triée par date décroissante
        """
        return sorted(route_attempts, key=lambda a: a["date"], reverse=True)