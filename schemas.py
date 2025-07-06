from pydantic import BaseModel
class Cosmetics_input(BaseModel):
    texture: str
    spf : str
    finish : str
    skin_type : str
    coverage : str
    usage_ease : str
    active_ingredients : str
    application : str
    base_color : str
    has_shades : str
    durability : str
    volume_ml : str
    container_type : str
    brand : str
    country_of_origin : str
class skin_care_input(BaseModel):
    product_type: str
    color_options: str
    skin_type: str
    spf: str
    uv_protection_uva: str
    uv_protection_uvb: str
    volume_g: str
    suitable_for: str
    age_group: str
    application_area: str
    active_ingredients: str
    features: str
    container_type: str
    brand: str
    brand_origin: str
    manufacturer: str
    country_of_manufacture: str
    other_features: str
    ingredients: str