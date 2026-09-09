from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    relationship
)

from datetime import datetime


DATABASE_URL = "sqlite:///./documents.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(
        String,
        nullable=False
    )

    file_size = Column(Integer)

    total_chunks = Column(Integer)

    status = Column(
        String,
        nullable=False
    )

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete"
    )


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False
    )

    chunk_index = Column(
        Integer,
        nullable=False
    )

    chunk_text = Column(
        Text,
        nullable=False
    )

    document = relationship(
        "Document",
        back_populates="chunks"
    )


Base.metadata.create_all(bind=engine)