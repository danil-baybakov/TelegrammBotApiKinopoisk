from api_database.common.model import db, ParamsStorage, History
from peewee import IntegrityError
from typing import TypeVar, Optional, Any
from datetime import datetime

A = TypeVar("A", ParamsStorage, History)


class InterfaceApiDatabase:

    @classmethod
    def get_param_storage_by_cid(cls, model: A, cid: int) -> Optional[A]:
        try:
            with db.atomic():
                return model.get(model.cid == cid)
        except Exception:
            pass

    @classmethod
    def get_history(cls, model: A, cid: int | None = None, limit: int = 10) -> list[A]:
        with db.atomic():
            where = model.cid == cid if cid is not None else True
            result = model.select().where(where).limit(limit).order_by(model.timestamp.desc())
        return [item for item in result]

    @classmethod
    def set_param_storage_by_cid(cls,
                                 model: A,
                                 cid: int,
                                 command: str | None = None,
                                 genre: str | None = None,
                                 limit: int | None = None,
                                 order: int | None = None,
                                 min_rating: float | None = None,
                                 max_rating: float | None = None,
                                 timestamp: datetime | None = None
                                 ) -> Optional[bool]:
        with (db.atomic()):
            try:
                if model == ParamsStorage:
                    params = cls.get_param_storage_by_cid(model=model, cid=cid)
                    if params is None:
                        with db.atomic():
                            model.insert(cid=cid).execute()
                            params = cls.get_param_storage_by_cid(model=model, cid=cid)
                    if command is not None:
                        params.command = command
                    if genre is not None:
                        params.genre = genre
                    if limit is not None:
                        params.limit = limit
                    if order is not None:
                        params.order = order
                    if min_rating is not None:
                        params.min_rating = min_rating
                    if max_rating is not None:
                        params.max_rating = max_rating
                    if timestamp is None:
                        params.timestamp = datetime.now()
                    else:
                        params.timestamp = timestamp
                    params.save()
                else:
                    with db.atomic():
                        if timestamp is None:
                            timestamp = datetime.now()
                        model.insert(
                            cid=cid,
                            command=command,
                            genre=genre,
                            limit=limit,
                            order=order,
                            min_rating=min_rating,
                            max_rating=max_rating,
                            timestamp=timestamp
                        ).execute()
                return True
            except IntegrityError as ex:
                return

    @classmethod
    def delete_param_storage_by_cid(cls, model: A, cid: int) -> Optional[bool]:
        with db.atomic():
            params = cls.get_param_storage_by_cid(model=model, cid=cid)
            if params is None:
                return
            params.delete_instance()
            params.save()
            return True


if __name__ == "__main__":
    ...
