from typing import List

def determine_base_strategy(invloed: str, impact: str) -> str:
    """Determine the base strategy based on influence and impact levels."""
    if impact in ["MIDDEL", "HOOG"] and invloed == "LAAG":
        return "Informeren"
    elif impact == "HOOG" and invloed == "HOOG":
        return "Samenwerken"
    elif impact == "LAAG" and invloed == "LAAG":
        return "Monitoren"
    elif impact == "LAAG" and invloed in ["MIDDEL", "HOOG"]:
        return "Tevreden Houden"
    return "Informeren"  # Default fallback

def determine_interaction_levels(impact: str, invloed: str) -> List[str]:
    """Determine appropriate interaction levels based on impact and influence."""
    interaction_levels = ["Omgevingsapp", "Bewonersbrief"]
    
    if impact == "HOOG":
        interaction_levels.append("Inloopuur")
        if invloed == "HOOG":
            interaction_levels.append("Keukentafelgesprekken")
    
    return interaction_levels
