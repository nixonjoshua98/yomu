from sqlalchemy.orm import Query, sessionmaker

from .data_entities import Story


class DataRepository:
    def __init__(self, session_maker: "sessionmaker"):
        self._session_maker: sessionmaker = session_maker

    def add(self, source: "Story"):
        with self._session_maker.begin() as session:
            session.add(source)

    def update(self, source: "Story"):
        with self._session_maker.begin() as session:
            linked_story: Story = (
                session.query(Story).filter(Story.id == source.id).first()
            )

            linked_story.update(source)

    def delete(self, source: "Story"):
        with self._session_maker.begin() as session:
            session.query(Story).filter(Story.id == source.id).delete()

    def get_stories_with_status(self, status: int, readable_only: bool = False):
        with self._session_maker.begin() as session:
            query: Query = session.query(Story).filter(Story.status == status)

            if readable_only:
                query = query.filter(Story.latest_chapter > Story.latest_chapter_read)

            ls = query.all()

            session.expunge_all()

        return ls

    def get_readable_stories(self) -> list["Story"]:
        with self._session_maker.begin() as session:
            ls = (
                session.query(Story)
                .filter(Story.status == 0 or Story.status == 2)
                .filter(Story.latest_chapter > Story.latest_chapter_read)
                .all()
            )

            session.expunge_all()

        return ls

    def get(self, id_: int):
        with self._session_maker.begin() as session:
            linked_story: Story = session.query(Story).filter(Story.id == id_).first()

            session.expunge_all()

        return linked_story

    def get_all(self):
        with self._session_maker.begin() as session:
            ls = session.query(Story).all()

            session.expunge_all()

        return ls
