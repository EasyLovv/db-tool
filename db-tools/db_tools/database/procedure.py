import sqlalchemy as sa
from .base import Base


class Procedure(Base):
    __tablename__ = "procedures"
    # __table_args__ = {"schema": "public"}

    id = sa.Column(sa.Integer(), autoincrement=True, primary_key=True)

    source_id = sa.Column(sa.String(100), nullable=False)
    patient_id = sa.Column(sa.ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    encounter_id = sa.Column(sa.ForeignKey("encounters.id", ondelete="CASCADE"), nullable=True)

    procedure_date = sa.Column(sa.Date(), nullable=False)

    type_code = sa.Column(sa.String(100), nullable=False)
    type_code_system = sa.Column(sa.String(100), nullable=False)
