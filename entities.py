from pydantic import BaseModel, Field
from typing import List, Literal

class Stakeholder(BaseModel):
    naam: str = Field(..., description="Als de stakeholder bewoners zijn, vermeld het bereik van huisnummers; bijv. Bewoners Stikke Hezelstraat 26-84")
    stakeholdertype: List[Literal["Bedrijf", "Winkel", "Horeca", "Bewoner", "Bevoegd gezag", "Gemeente", "Nutsbedrijf", "Hulpdiesnt", "Vuilnisophaaldienst", "Instantie", "School", "Bushalte/Busstation", "Treinstation"]]
    invloed: Literal["Hoog", "Middel", "Laag"]
    impact: Literal["Hoog", "Middel", "Laag"]
    
    strategie: List[Literal[
        "Informeren", "Samenwerken", "Monitoren", "Tevreden Houden",
        "Raadplegen", "Adviseren", "Coproduceren", "Meebeslissen",
        "Delegeren", "Reageren"
    ]] = Field(
        ..., 
        description=(
            "De aanpak voor het betrekken van de stakeholder.: \n"
            "Voeg altijd 'Reageren' toe als strategie\n"
            "Vervolgens, kies uit 1 van de volgende opties op basis van impact en invloed: \n"
            "- Informeren (Invloed = Laag, Impact = Middel of Hoog) \n"
            "- Samenwerken (Invloed = Hoog, Impact = Hoog) \n"
            "- Monitoren (Invloed = Laag, Impact = Laag) \n"
            "- Tevreden Houden (Invloed = Middel of Hoog, Impact = Laag) \n"
            " Tot slot, nu uit de volgende opties op basis van stakeholder type: \n"
            "- Raadplegen (stakeholder type is Gemeente, Nutsbedrijven) \n"
            "- Adviseren (stakeholder type is Gemeente) \n"
            "- Coproduceren (stakeholder type is Gemeente, Nutsbedrijven) \n"
            "- Meebeslissen (stakeholder type is Gemeente, Nutsbedrijven) \n"
            "- Delegeren (stakeholder type is Gemeente) \n"
            "Meerdere strategieën kunnen tegelijk van toepassing zijn."
        )
    )

    # communicatiemiddel: List[str] = Field(
    #     ..., 
    #     description="Een lijst van communicatiemiddelen die worden gebruikt om met de stakeholder te communiceren. Bepaal dit aan de hand van de strategie, invloed en impact. Enkele voorbeelden kunnen zijn: 'Nieuwsbrief', 'Website', 'Social Media', 'Persbericht', 'Workshop', 'Overleg', etc., maar dit blijft open voor dynamische invulling."
    # )

    interactienmethode: List[Literal["Omgevingsapp", "Bewonersbrief", "Inloopuur", "Keukentafelgesprekken"]] = Field(
        ..., 
        description=(
            "Mogelijke interactiemethodes, afhankelijk van invloed en impact: \n"
            "- Omgevingsapp (Invloed = Hoog, Middel of Laag) \n"
            "- Bewonersbrief (Invloed = Hoog, Middel of Laag) \n"
            "- Inloopuur (Invloed = Hoog, Impact = Hoog) \n"
            "- Keukentafelgesprekken (Invloed = Hoog, Impact = Hoog) \n"
            "Meerdere opties zijn mogelijk."
        )
    )

    frequentie: List[str] = Field(
        ..., 
        description="De frequentie van communicatie, zoals 'Maandelijks', 'Per fase', 'Op verzoek', etc. Bepaal dit dynamisch op basis van de stakeholdertype, strategie en interactiemethode."
    )

class StakeholderList(BaseModel):
    stakeholders: List[Stakeholder] = Field(
        ..., 
        description="Lijst van stakeholders. Bewoners worden samengevoegd tot 1 groep stakeholders in de lijst. Andere stakeholders worden apart vermeld in de lijst."
    )