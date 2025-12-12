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

def format_datetime_fr(datetime_value):
    """
    Convertit un datetime ISO en format français JJ/MM/AA HH:MM.
    
    Args:
        datetime_value: string ISO ou datetime object
        
    Returns:
        string au format "JJ/MM/AA HH:MM"
    """
    if not datetime_value:
        return ""
    
    try:
        if hasattr(datetime_value, "strftime"):
            return datetime_value.strftime("%d/%m/%y %H:%M")
        
        # Parse ISO string avec timezone
        dt_obj = datetime.fromisoformat(str(datetime_value).replace('Z', '+00:00'))
        return dt_obj.strftime("%d/%m/%y %H:%M")
    except (ValueError, TypeError):
        return str(datetime_value)


def format_relative_time(datetime_value):
    """
    Retourne un format relatif (il y a X minutes/heures/jours).
    
    Args:
        datetime_value: string ISO ou datetime object
        
    Returns:
        string au format "il y a X..."
    """
    if not datetime_value:
        return ""
    
    try:
        from datetime import datetime, timezone
        
        if hasattr(datetime_value, "replace"):
            dt_obj = datetime_value
        else:
            dt_obj = datetime.fromisoformat(str(datetime_value).replace('Z', '+00:00'))
        
        # S'assurer que c'est en UTC
        if dt_obj.tzinfo is None:
            dt_obj = dt_obj.replace(tzinfo=timezone.utc)
        
        now = datetime.now(timezone.utc)
        diff = now - dt_obj
        
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return "à l'instant"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"il y a {minutes} min"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"il y a {hours}h"
        elif seconds < 604800:
            days = int(seconds / 86400)
            return f"il y a {days}j"
        else:
            return format_date_fr(dt_obj)
            
    except (ValueError, TypeError):
        return str(datetime_value)