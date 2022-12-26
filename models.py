from sqlalchemy import Column, Integer, Text

from db import Base


class OlxOrderModel(Base):
    __tablename__ = "olx_orders"

    id = Column(Integer, primary_key=True)
    url = Column(Text)
    price = Column(Text)
    device_name = Column(Text)
    seller_name = Column(Text)
    description = Column(Text)
    phone_number = Column(Text)


class KolesaOrderModel(Base):
    __tablename__ = "kolesa_orders"

    id = Column(Integer, primary_key=True)
    url = Column(Text)
    price = Column(Text)
    item_name = Column(Text)
    description = Column(Text)
    phone_number = Column(Text)
