from typing import List, Optional, Literal

from pydantic import BaseModel, Field

class ContactInfo(BaseModel):
    adres: str = Field(..., description="Straatnaam en huisnummer van de stakeholder.")
    postcode: str = Field(..., description="Postcode van de stakeholder.")
    email: Optional[str] = Field(None, description="Emailadres van de stakeholder.")
    telefoon: Optional[str] = Field(
        None, description="Telefoonnummer van de stakeholder."
    )

class Stakeholder(BaseModel):
    naam: str = Field(..., description="Als de stakeholder bewoners zijn, vermeld het bereik van huisnummers; bijv. Bewoners Stikke Hezelstraat 26-84")
    stakeholdertype: Literal["Bedrijf", "Winkel", "Horeca", "Bewoner", "Bevoegd gezag"]
    invloed: Literal["Hoog", "Middel", "Laag"]
    impact: Literal["Hoog", "Middel", "Laag"]
    # strategie: List[Literal[
    #     "Informeren", "Samenwerken", "Monitoren", "Tevreden Houden",
    #     "Raadplegen", "Adviseren", "Coproduceren", "Meebeslissen",
    #     "Delegeren", "Reageren"
    # ]]
    # communicatiemiddel: str
    # frequentie: str
    # interactieniveau: List[Literal["Omgevingsapp", "Bewonersbrief", "Inloopuur", "Keukentafelgesprekken"]]
    # contactgegevens: ContactInfo = Field(
    #     ..., description="Contactinformatie van de stakeholder."
    # )

class StakeholderList(BaseModel):
    stakeholders: List[Stakeholder] = Field(
        ..., description="Lijst van stakeholders. Bewoners worden gezien als 1 groep stakeholders. Bedrijven en andere stakeholders worden apart vermeld."
    )