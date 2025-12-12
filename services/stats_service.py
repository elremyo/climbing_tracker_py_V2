"""
Calculs de statistiques pour le dashboard.
"""
from collections import Counter
from datetime import datetime
from utils.constants import GRADES

class StatsService:
    """Service de calcul des statistiques"""
    
    @staticmethod
    def calculate_success_rate(attempts):
        """Calcule le taux de réussite global"""
        if not attempts:
            return 0
        successful = sum(1 for a in attempts if a["success"])
        return (successful / len(attempts)) * 100
    
    @staticmethod
    def get_most_attempted_route(attempts, routes):
        """Trouve la voie la plus tentée"""
        if not attempts:
            return None, 0
        
        route_counter = Counter(a["route_id"] for a in attempts)
        most_common_route_id, count = route_counter.most_common(1)[0]
        route = next((r for r in routes if r["id"] == most_common_route_id), None)
        return route, count
    
    @staticmethod
    def get_hardest_completed_route(attempts, routes):
        """Trouve la voie la plus difficile réussie"""
        successful_attempts_with_routes = []
        
        for a in attempts:
            if a["success"]:
                route = next((r for r in routes if r["id"] == a["route_id"]), None)
                if route:
                    successful_attempts_with_routes.append((a, route))
        
        if not successful_attempts_with_routes:
            return None, None
        
        sorted_attempts = sorted(
            successful_attempts_with_routes,
            key=lambda item: GRADES.index(item[1]["grade"]) if item[1]["grade"] in GRADES else -1,
            reverse=True
        )
        
        return sorted_attempts[0]
    
    @staticmethod
    def calculate_grade_stats(attempts, routes):
        """Calcule les stats par niveau de difficulté"""
        grade_stats = {}
        
        for grade in GRADES:
            grade_attempts = []
            for a in attempts:
                route = next((r for r in routes if r["id"] == a["route_id"]), None)
                if route and route.get("grade") == grade:
                    grade_attempts.append(a)
            
            if grade_attempts:
                total = len(grade_attempts)
                successful = sum(1 for a in grade_attempts if a["success"])
                rate = (successful / total) * 100
                grade_stats[grade] = (total, successful, rate)
        
        return grade_stats