import base64
from functools import cache

from database.models.user import User
from testdata.factories.common_data import user_ids
from testdata.factories.factory_base import BaseSQLAlchemyFactory


class UserFactory(BaseSQLAlchemyFactory[User]):
    @classmethod
    def name(cls) -> str:
        return cls.__faker__.first_name()

    @classmethod
    def family_name(cls) -> str:
        return cls.__faker__.last_name()

    @classmethod
    def middle_name(cls) -> str:
        return cls.__faker__.language_name()

    @classmethod
    def position(cls) -> str:
        return cls.__faker__.job()

    @classmethod
    def avatar(cls) -> str:
        return cls._get_avatar()

    @classmethod
    @cache
    def _get_avatar(cls) -> str:
        with open("src/testdata/avatar.png", "rb") as image_file:
            base64_bytes = base64.b64encode(image_file.read())
            return base64_bytes.decode()

    @classmethod
    def build_all(cls) -> list[User]:
        return [cls.build(id=user_id) for user_id in user_ids]
