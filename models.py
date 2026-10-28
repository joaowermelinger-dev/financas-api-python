from sqlalchemy.orm import DeclarativeBase, declarative_base, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)