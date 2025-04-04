from pydantic import BaseModel, model_validator
from app.schemas.enums import FolioCategoryEnum

CATEGORIES = [category.value for category in FolioCategoryEnum]

class FolioBase(BaseModel):
    name: str
    category: FolioCategoryEnum
    subcategory: str

    @model_validator(mode="after")
    def validate_combination(self) -> "FolioBase":
        name = self.name
        category = self.category
        subcategory = self.subcategory

        if name is None or name == "":
            raise ValueError("Name cannot be empty")
        if len(name) > 50:
            raise ValueError("Name cannot exceed 50 characters")
        if category is None or category == "":
            raise ValueError("Category cannot be empty")
        if category not in CATEGORIES:
            raise ValueError(f"Invalid category: {category}")
        if len(subcategory) > 50:
            raise ValueError("Subcategory cannot exceed 50 characters")
        
        return self

class FolioCreate(FolioBase):
    pass

class FolioRead(FolioBase):
    model_config = {
        "from_attributes": True
    }
