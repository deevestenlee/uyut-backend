from typing import List, Optional from pydantic import BaseModel, Field, ConfigDict
class ProductOptionPublic(BaseModel): model_config = ConfigDict(from_attributes=True)
id: int
name: str
price: int = Field(..., ge=0)
class ProductPublic(BaseModel): model_config = ConfigDict(from_attributes=True)
id: int
title: str
description: Optional[str] = None
image_url: Optional[str] = None
is_spicy: bool
badge: Optional[str] = None
options: List[ProductOptionPublic] = []
class CategoryWithProducts(BaseModel): model_config = ConfigDict(from_attributes=True)
id: int
name: str
sort_order: int
products: List[ProductPublic] = []
class RestaurantSettingsPublic(BaseModel): model_config = ConfigDict(from_attributes=True)
id: int
name: str
currency_symbol: str
phone: Optional[str]
address: Optional[str]
min_order_amount: int
class InitResponse(BaseModel): settings: RestaurantSettingsPublic categories: List[CategoryWithProducts]
class OptionPriceUpdate(BaseModel): price: int = Field(..., ge=0)
class ProductAvailabilityUpdate(BaseModel): is_available: bool
class ProductOptionAdmin(BaseModel): model_config = ConfigDict(from_attributes=True) id: int product_id: int name: str price: int
class ProductAdminShort(BaseModel): model_config = ConfigDict(from_attributes=True) id: int title: str is_available: bool