from pydantic import BaseModel, Field, model_validator

class Chunk(BaseModel):
    id: str
    source: str
    position: int = Field(ge=0)
    text: str
    word_count: int = Field(ge=0)

class Settings(BaseModel):
    size: int = 200
    overlap: int = 40

    @model_validator(mode="after")
    def validate_chunk_settings(self):
        if self.size <=0:
            raise ValueError("Chunk size must be greater than zero.")

        if self.overlap < 0:
            raise ValueError("Overlap cannot be negative.")

        if self.overlap >= self.size:
            raise ValueError("Overlap must be smaller than chunk size.")

        return self