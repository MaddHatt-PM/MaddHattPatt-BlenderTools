ORGANIZER = "Organizer"
TOOLS = "Tools"
LOWPOLY = "Low_Poly"
MIDPOLY = "Mid_Poly"
HIGHPOLY = "High_Poly"

SUF_LOW = "_low"
SUF_MID = "_mid"
SUF_HIGH = "_high"

def coll_to_suffix(input:str):
    if input == LOWPOLY:
        return SUF_LOW
        
    if input == MIDPOLY:
        return SUF_MID

    if input == HIGHPOLY:
        return SUF_HIGH