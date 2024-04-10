from datetime import datetime, timezone

import sqlalchemy as sa
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    WriteOnlyMapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(sa.String(64), unique=True, index=True)
    email: Mapped[str] = mapped_column(sa.String(120), unique=True)
    password_hash: Mapped[str | None] = mapped_column(sa.String(256))

    posts: WriteOnlyMapped["Post"] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return f"<User: {self.username}>"


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(sa.String(140))
    timestamp: Mapped[datetime] = mapped_column(
        index=True, default=lambda: datetime.now(tz=timezone.utc)
    )
    user_id: Mapped[int] = mapped_column(sa.ForeignKey(User.id), index=True)

    author: Mapped[User] = relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"<Post: {self.body}>"
