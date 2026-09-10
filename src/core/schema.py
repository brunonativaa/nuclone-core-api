from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):

    model_config = ConfigDict(

        # Mapeia diretamente modelos do SQLAlchemy (antigo orm_mode)
        from_attributes=True,
        populate_by_name=True,  # Permite preencher campos por nome ou alias
        str_strip_whitespace=True,  # Remove espaços extras no início/fim de strings
        use_enum_values=True,  # Converte Enums automaticamente para seus valores nativos
    )
