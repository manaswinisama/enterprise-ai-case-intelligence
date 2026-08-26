from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Process(Base):
    __tablename__ = "processes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    department = Column(String(100), nullable=True)
    activities = Column(Text, nullable=True)

    analysis = relationship(
        "ProcessAnalysis",
        back_populates="process",
        cascade="all, delete-orphan"
    )


class ProcessAnalysis(Base):
    __tablename__ = "process_analyses"

    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(Integer, ForeignKey("processes.id"), nullable=False)

    ai_opportunity = Column(String(50))
    automation_potential = Column(String(50))
    human_involvement = Column(String(100))

    benefits = Column(Text)
    risks = Column(Text)
    technology = Column(Text)

    priority_score = Column(Float)
    reasoning = Column(Text)

    process = relationship(
        "Process",
        back_populates="analysis"
    )