from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationInfo


# TODO: clase PrestamoEntrada (BaseModel) con las 6 variables del modelo, con sus rangos (ver enunciado).
#       Debe rechazar campos que no existan.

class PrestamoEntrada(BaseModel):

    model_config = ConfigDict(extra='forbid')


    edad: int = Field(ge=18, le=75, description="Edad del solicitante")

    ingresos_mensuales: float = Field(gt=0, description="Ingresos mensuales del solicitante")

    importe_prestamo: float = Field(gt=0, description="Importe del préstamo solicitado")

    plazo_meses: int = Field(ge=6, le=84, description="Meses para pagar el préstamo")

    antiguedad_laboral_anios: int = Field(ge=0, le=50, description="Años trabajados")
    #no puede ser mayor que edad - 16

    impagos_previos: int = Field(ge=0, le=20, description="Número de impagos previos")


# TODO: field_validator (con classmethod) para antiguedad_laboral_anios: no puede ser incoherente con la edad.

    #ejecutamos siempre para "revisar" antiguedad_laboral_anios
    @field_validator("antiguedad_laboral_anios", mode='after')
    @classmethod
    def validar_antiguedad(cls,value, info:ValidationInfo):

        edad = info.data.get("edad")

        if value > edad - 16:
            raise ValueError(f"La antiguedad laboral no puede ser mayor que la edad-16."
                             f"Antiguedad laboral: {value}, "
                             f"Edad: {edad}")
        else:
            return value

# TODO: clase PrediccionSalida con probabilidad_impago (entre 0 y 1) y decision (aprobar, revisar o rechazar).

class PrediccionSalida(BaseModel):

    model_config = ConfigDict(extra='forbid')

    probabilidad_impago: float = Field(ge=0, le=1)

    decision: Literal["aprobar", "revisar", "rechazar"]
