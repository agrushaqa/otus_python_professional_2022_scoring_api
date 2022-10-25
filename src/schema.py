from abc import abstractmethod
from weakref import WeakKeyDictionary

from config import Config
from validator_birthday import ValidatorBirthday
from validator_client_ids import ValidatorClientIds
from validator_date import ValidatorDate
from validator_email import ValidatorEmail
from validator_gender import ValidatorGender
from validator_phone import ValidatorPhone


class ParseSchema(type):
    def __new__(cls, name, bases, dct):
        klass_attr = {}
        attrs = ((name, value) for name, value in dct.items() if
                 not name.startswith('__'))
        for i in attrs:
            if hasattr(i[1], "__dict__"):
                klass_attr[i[0]] = i[1].__dict__
        dct["list_attr"] = klass_attr
        return super().__new__(cls, name, bases, dct)


class Field(object):
    def __init__(self):
        self.data = WeakKeyDictionary()

    def __get__(self, instance, cls):
        return self.data.get(instance)

    def __set__(self, instance, value):
        if "nullable" in self.__dict__.keys():
            if self.nullable is False:
                if value is None:
                    raise ValueError("None value")
        self.data[instance] = self._validator(value)

    def __delete__(self, instance):
        raise AttributeError("Can't delete attribute")

    @staticmethod
    @abstractmethod
    def _validator(value): pass


class CharField(Field):
    def __init__(self, required, nullable, group=None):
        self.required: bool = required
        self.nullable: bool = nullable
        self.group: int = group
        super().__init__()

    @staticmethod
    def _validator(value):
        return value


class ArgumentsField(Field):
    def __init__(self, required, nullable):
        self.required: bool = required
        self.nullable: bool = nullable
        super().__init__()

    @staticmethod
    def _validator(value):
        if type(value) is not dict:
            raise ValueError(f"invalid type: {type(value)}")
        return value


class EmailField(CharField):

    @staticmethod
    def _validator(value):
        ValidatorEmail(value)
        return value


class PhoneField(Field):
    def __init__(self, required, nullable, group=None):
        self.required: bool = required
        self.nullable: bool = nullable
        self.group: int = group
        super().__init__()

    @staticmethod
    def _validator(value):
        ValidatorPhone(value)
        return value


class DateField(Field):
    def __init__(self, required, nullable, group=None):
        self.required: bool = required
        self.nullable: bool = nullable
        self.group: int = group
        super().__init__()

    @staticmethod
    def _validator(value):
        ValidatorDate(value)
        return value


class BirthDayField(Field):
    def __init__(self, required, nullable, group=None):
        self.required: bool = required
        self.nullable: bool = nullable
        self.group: int = group
        super().__init__()

    @staticmethod
    def _validator(value):
        ValidatorBirthday(value)
        return value


class GenderField(Field):
    def __init__(self, required, nullable, group=None):
        self.required: bool = required
        self.nullable: bool = nullable
        self.group: int = group
        super().__init__()

    @staticmethod
    def _validator(value):
        ValidatorGender(value)
        return value


class ClientIDsField(Field):
    def __init__(self, required, nullable, group=None):
        self.required: bool = required
        self.nullable: bool = nullable
        self.group: int = group
        super().__init__()

    @staticmethod
    def _validator(value):
        ValidatorClientIds(value)
        return value


class ClientsInterestsRequest(metaclass=ParseSchema):
    client_ids = ClientIDsField(required=True, nullable=False)
    date = DateField(required=False, nullable=True)


class OnlineScoreRequest(metaclass=ParseSchema):
    first_name = CharField(required=False, nullable=True, group='fio')
    last_name = CharField(required=False, nullable=True, group='fio')
    email = EmailField(required=False, nullable=True, group='phone-email')
    phone = PhoneField(required=False, nullable=True, group='phone-email')
    birthday = BirthDayField(required=False, nullable=True, group='day-gender')
    gender = GenderField(required=False, nullable=True, group='day-gender')


class MethodRequest(metaclass=ParseSchema):
    account = CharField(required=False, nullable=True)
    login = CharField(required=True, nullable=True)
    token = CharField(required=True, nullable=True)
    arguments = ArgumentsField(required=True, nullable=True)
    method = CharField(required=True, nullable=False)

    @property
    def is_admin(self):
        return self.login == Config().admin_login
