from datetime import datetime

def format_date_fr(date_value):
    """
    Convertit une date ISO (ou datetime) en format français JJ/MM/AA.
    
    Args:
        date_value: string ISO, datetime object, ou date object
        
    Returns:
        string au format "JJ/MM/AA" ou la valeur originale si conversion impossible
    """
    if not date_value:
        return ""
    
    try:
        # Si c'est déjà un datetime/date object
        if hasattr(date_value, "strftime"):
            return date_value.strftime("%d/%m/%y")
        
        # Si c'est un string ISO
        date_obj = datetime.fromisoformat(str(date_value))
        return date_obj.strftime("%d/%m/%y")
    except (ValueError, TypeError):
        # Fallback : retourner tel quel
        return str(date_value)


def format_date_full_fr(date_value):
    """
    Convertit une date en format français complet JJ/MM/AAAA.
    
    Args:
        date_value: string ISO, datetime object, ou date object
        
    Returns:
        string au format "JJ/MM/AAAA"
    """
    if not date_value:
        return ""
    
    try:
        if hasattr(date_value, "strftime"):
            return date_value.strftime("%d/%m/%Y")
        
        date_obj = datetime.fromisoformat(str(date_value))
        return date_obj.strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return str(date_value)
