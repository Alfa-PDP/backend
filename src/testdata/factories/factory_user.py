from database.models.user import User
from testdata.factories.common_data import user_emails, user_ids, user_phone_numbers, user_telegrams
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
        return "https://cdn0.iconfinder.com/data/icons/user-pictures/100/malecostume-512.png"

    @classmethod
    def build_all(cls) -> list[User]:
        return [
            cls.build(id=user_id, telegram=user_telegram, phone_number=user_phone_number, email=user_email)
            for user_id, user_telegram, user_phone_number, user_email in zip(
                user_ids, user_telegrams, user_phone_numbers, user_emails
            )
        ]
