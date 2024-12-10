from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column


class Base(DeclarativeBase):
	pass


class User(Base):
	__tablename__ = 'users'

	id: Mapped[int] = mapped_column(primary_key=True)
	notes: Mapped[list['Note']] = relationship(back_populates='user')
	folders: Mapped[list['Folder']] = relationship(back_populates='user')
	message_id: Mapped[int] = mapped_column(nullable=True)


class Folder(Base):
	__tablename__ = 'folders'

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(default='Unnamed folder')
	notes: Mapped[list['Note']] = relationship(back_populates='folder')
	folded: Mapped[bool] = mapped_column(default=True)
	folders: Mapped[list['Folder']] = relationship(back_populates='parent')

	parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey('folders.id'))
	parent: Mapped[Optional['Folder']] = relationship(back_populates='folders', remote_side='Folder.id')

	user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
	user: Mapped['User'] = relationship(back_populates='folders')


class Note(Base):
	__tablename__ = 'notes'

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(default='Unnamed note')
	description: Mapped[str] = mapped_column(nullable=True)

	folder_id: Mapped[int] = mapped_column(ForeignKey('folders.id'), nullable=True)
	folder: Mapped[Optional['Folder']] = relationship(back_populates='notes')

	user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
	user: Mapped['User'] = relationship(back_populates='notes')
