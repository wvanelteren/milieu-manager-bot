from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

class StakeholderType(str, Enum):
    BEDRIJF = "Bedrijf"
    WINKEL = "Winkel"
    HORECA = "Horeca"
    BEWONER = "Bewoner"
    BEVOEGD_GEZAG = "Bevoegd gezag"

class InfluenceLevel(str, Enum):
    HOOG = "Hoog"
    MIDDEL = "Middel"
    LAAG = "Laag"

class ImpactLevel(str, Enum):
    HOOG = "Hoog"
    MIDDEL = "Middel"
    LAAG = "Laag"

class StrategyType(str, Enum):
    INFORMEREN = "Informeren"
    SAMENWERKEN = "Samenwerken"
    MONITOREN = "Monitoren"
    TEVREDEN_HOUDEN = "Tevreden Houden"
    RAADPLEGEN = "Raadplegen"
    ADVISEREN = "Adviseren"
    COPRODUCEREN = "Coproduceren"
    MEEBESLISSEN = "Meebeslissen"
    DELEGEREN = "Delegeren"
    REAGEREN = "Reageren"

class InteractionLevel(str, Enum):
    OMGEVINGSAPP = "Omgevingsapp"
    BEWONERSBRIEF = "Bewonersbrief"
    INLOOPUUR = "Inloopuur"
    KEUKENTAFELGESPREKKEN = "Keukentafelgesprekken"

class ContactInfo(BaseModel):
    adres: str = Field(..., description="Straatnaam en huisnummer van de stakeholder.")
    postcode: str = Field(..., description="Postcode van de stakeholder.")
    email: Optional[str] = Field(None, description="Emailadres van de stakeholder.")
    telefoon: Optional[str] = Field(
        None, description="Telefoonnummer van de stakeholder."
    )

class Stakeholder(BaseModel):
    stakeholder: str = Field(..., description="Naam van de stakeholder.")
    type: StakeholderType = Field(..., description="Type stakeholder.")
    invloed: InfluenceLevel = Field(..., description="Invloedniveau van de stakeholder.")
    impact: ImpactLevel = Field(
        ..., description="Impactniveau van de stakeholder op het project."
    )
    strategie: List[StrategyType] = Field(
        ..., description="Lijst van communicatiestrategieën voor de stakeholder."
    )
    communicatiemiddel: str = Field(
        ..., description="Het voorkeurscommunicatiemiddel voor de stakeholder."
    )
    frequentie: str = Field(
        ..., description="De frequentie van communicatie met de stakeholder."
    )
    interactieniveau: List[InteractionLevel] = Field(
        ..., description="Gewenste interactieniveaus met de stakeholder."
    )
    # contactgegevens: ContactInfo = Field(
    #     ..., description="Contactinformatie van de stakeholder."
    # )

class StakeholderList(BaseModel):
    stakeholders: List[Stakeholder] = Field(
        ..., description="Lijst van stakeholders"
    )