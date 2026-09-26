from datetime import datetime 
from typing import Optional, List
from sqlalchemy import String, Integer, Boolean, ForeignKey, Text, DateTime, func from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
class RestaurantSettings(Base): tablename = "restaurant_settings"
id: Mapped[int] = mapped_column(Integer, primary_key=True)
name: Mapped[str] = mapped_column(String(150), nullable=False)
currency_symbol: Mapped[str] = mapped_column(String(8), default="₩", nullable=False)
phone: Mapped[Optional[str]] = mapped_column(String(32))
address: Mapped[Optional[str]] = mapped_column(String(255))
min_order_amount: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
)
class Category(Base): tablename = "categories"
id: Mapped[int] = mapped_column(Integer, primary_key=True)
name: Mapped[str] = mapped_column(String(100), nullable=False)
sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

products: Mapped[List["Product"]] = relationship(
    back_populates="category",
    cascade="all, delete-orphan",
    order_by="Product.id",
)
class Product(Base): tablename = "products"
id: Mapped[int] = mapped_column(Integer, primary_key=True)
category_id: Mapped[int] = mapped_column(
    ForeignKey("categories.id", ondelete="CASCADE"), index=True, nullable=False
)
title: Mapped[str] = mapped_column(String(150), nullable=False)
description: Mapped[Optional[str]] = mapped_column(Text)
image_url: Mapped[Optional[str]] = mapped_column(String(500))
is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
is_spicy: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
badge: Mapped[Optional[str]] = mapped_column(String(32))

category: Mapped["Category"] = relationship(back_populates="products")
options: Mapped[List["ProductOption"]] = relationship(
    back_populates="product",
    cascade="all, delete-orphan",
    order_by="ProductOption.id",
)
class ProductOption(Base): tablename = "product_options"
id: Mapped[int] = mapped_column(Integer, primary_key=True)
product_id: Mapped[int] = mapped_column(
    ForeignKey("products.id", ondelete="CASCADE"), index=True, nullable=False
)
name: Mapped[str] = mapped_column(String(100), nullable=False)
price: Mapped[int] = mapped_column(Integer, nullable=False)

product: Mapped["Product"] = relationship(back_populates="options")
