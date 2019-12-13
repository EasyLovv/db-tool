import sqlalchemy as sa
from .base import Base


class Patient(Base):
    __tablename__ = "patients"
    # __table_args__ = {"schema": "public"}

    id = sa.Column(sa.Integer(), autoincrement=True, primary_key=True)
    source_id = sa.Column(sa.String(100), nullable=False)
    birth_date = sa.Column(sa.Date(), nullable=True)
    gender = sa.Column(sa.String(100), nullable=True)
    race_code = sa.Column(sa.String(100), nullable=True)
    race_code_system = sa.Column(sa.String(100), nullable=True)
    ethnicity_code = sa.Column(sa.String(100), nullable=True)
    ethnicity_code_system = sa.Column(sa.String(100), nullable=True)
    country = sa.Column(sa.String(100), nullable=True)
