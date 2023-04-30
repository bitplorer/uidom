# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import asyncio
import typing
import uuid
from dataclasses import dataclass
from datetime import datetime, time
from enum import Enum, IntEnum
from pathlib import Path
from uuid import UUID

import valio
from tortoise import Model, Tortoise

from uidom import dom, elements

valio.Validator.register(Model)


class ModelValidator(valio.Validator):
    annotation = typing.Union[Model, None]


class ModelField(valio.Field):
    validator = ModelValidator


@dataclass
class Queries(object):
    model_field = ModelField(logger=True, debug=True)
    model: typing.Type[Model] = model_field.validator

    async def all(self):
        return await self.model.all()

    async def only(self, *field_names):
        return await self.model.all().only(*field_names)

    async def get(self, field: str, value=None):
        field = {f"{field}": value}
        value = await self.model.filter(**field).get()
        return value

    async def create(self, **kwargs):
        return await self.model.create(**kwargs)

    async def update(self, field: str, value=None, **kwargs):
        field = {f"{field}": value}
        value = await self.model.filter(**field).update(**kwargs)
        return value

    async def delete(self, field: str, value=None):
        field = {f"{field}": value}
        await self.model.filter(**field).delete()

    async def gt(self, field: str, value=None):
        field = f"{field}__gt"
        return await self.get(field=field, value=value)

    async def lt(self, field: str, value=None):
        field = f"{field}__lt"
        return await self.get(field=field, value=value)

    async def contains(self, field: str, value=None):
        field = f"{field}__contains"
        return await self.get(field=field, value=value)


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(db_url="sqlite://db.sqlite3", modules={"models": ["__main__"]})
    # Generate the schema
    await Tortoise.generate_schemas()


async def query(q):
    await init()
    value = await asyncio.gather(q)
    await Tortoise.close_connections()
    return value


class UiMeta(type):
    labels = None
    inputs = None
    fields = None
    buttons = None
    form = None

    INPUT = {
        str: elements.CharInput,
        int: elements.IntegerField,
        float: elements.FloatInput,
        bytes: elements.FileButtonInput,
        bool: elements.CheckboxInput,
        time: elements.DateInput,
        Path: elements.FileButtonInput,
        UUID: elements.CharInput,
        Enum: elements.EnumInput,
        IntEnum: elements.IntegerEnumInput,
    }

    LABEL = {
        str: elements.CharLabel,
        int: elements.IntegerLabel,
        float: elements.FloatLabel,
        bytes: elements.CharLabel,
        bool: elements.BooleanLabel,
        datetime.time: elements.DateLabel,
        Path: elements.CharLabel,
        UUID: elements.CharLabel,
        Enum: elements.EnumLabel,
        IntEnum: elements.EnumLabel,
    }

    CSS = {
        str: {
            "labels": "font-sm font-mono text-md px-2 uppercase",
            "inputs": "px-2 focus:outline-none focus:ring-2 focus:ring-gray-300 rounded-lg "
            "placeholder-gray-400 bg-gray-100",
            "fields": "flex flex-row justify-between space-x-4 m-1 p-2 "
            "rounded-lg shadow-md border-2 border-gray-300 w-full",
        },
        bool: {
            "labels": "font-sm font-mono text-md px-2 uppercase",
            "inputs": "px-2 focus:outline-none focus:ring-2 focus:ring-gray-300 rounded-lg bg-gray-100",
            "fields": "flex flex-row justify-between space-x-2 m-1 p-2 "
            "rounded-lg shadow-md border-2 border-gray-300 w-full",
        },
        "buttons": {
            "save": "flex flex-row bg-green-500 hover:bg-green-400 whitespace-nowrap "
            "text-white m-2 p-2 rounded-lg justify-evenly space-x-2",
            "delete": "flex flex-row border border-red-500 hover:border-red-400 whitespace-nowrap "
            "text-red-500 m-2 p-2 rounded-lg justify-evenly space-x-2",
            "edit": "flex flex-row bg-blue-500 hover:bg-blue-400 whitespace-nowrap "
            "m-2 text-white p-2 rounded-lg justify-evenly space-x-2",
            "buttons": "flex flex-row p-2 m-2 justify-between",
        },
    }

    def __new__(mcs, name, bases, namespaces):
        inputs = dict()
        labels = dict()
        fields = dict()
        _annotations = dict()
        buttons = dict()
        btn_css = mcs.CSS.get("buttons", None)
        meta = namespaces.get("Meta", None)
        model = getattr(meta, "model", None)

        for base in bases:
            for ns, ann in base.__dict__.get("__annotations__", {}).items():
                if ns in getattr(base, "Meta", mcs.Meta).exclude:
                    continue
                _annotations[ns] = ann
                if not issubclass(ann, UIBase):
                    inputs[ns] = mcs.INPUT[ann]
                    labels[ns] = mcs.LABEL[ann]
                else:
                    data = queries(model.all().select_related(ns))
                    labels[ns] = dom.span(f"Choose {ns}")
                    inputs[ns] = dom.select(
                        dom.option(opt, value=str(opt)) for opt in data
                    )
                    edit_btn = dom.SubmitButton(
                        label=f"Edit {ann.__qualname__}",
                        value=f"edit_{ann.__qualname__.lower()}",
                    )
                    edit_btn["class"] = (
                        btn_css.get("edit", "") if btn_css is not None else ""
                    )
                    fields[ns] = dom.div(labels[ns], inputs[ns], edit_btn)

        for ns, ann in namespaces.get("__annotations__", {}).items():
            if ns in getattr(namespaces, "Meta", mcs.Meta).exclude:
                continue
            _annotations[ns] = ann
            if not issubclass(ann, UIBase):
                inputs[ns] = mcs.INPUT[ann]
                labels[ns] = mcs.LABEL[ann]
            else:
                data = asyncio.run(query(model.all().select_related(ns)))
                labels[ns] = dom.span(f"Choose {ns}")
                inputs[ns] = dom.select(
                    dom.option(id=opt.id, value=str(opt)) for opt in data
                )
                edit_btn = dom.SubmitButton(
                    label=f"Edit {ann.__qualname__}",
                    icon=dom.manage_icon,
                    value=f"edit_{ann.__qualname__.lower()}",
                )
                edit_btn["class"] = (
                    btn_css.get("edit", "") if btn_css is not None else ""
                )
                fields[ns] = dom.div(labels[ns], inputs[ns], edit_btn)

        for atr in inputs:
            if not isinstance(inputs[atr], dict):
                if callable(inputs[atr]):
                    atr_name = atr.replace("_", "-")
                    if "_" in atr:
                        atr_label = " ".join(
                            map(lambda x: x.capitalize(), atr.replace("_", " ").split())
                        )
                    else:
                        atr_label = atr.capitalize()
                    css = mcs.CSS.get(_annotations[atr], None)
                    inputs[atr] = inputs[atr](
                        name=atr_name,
                        placeholder=f"Enter {atr_label}",
                        cls=css.get("inputs", "") if css is not None else "",
                    )
                    labels[atr] = labels[atr](
                        label=atr_label,
                        cls=css.get("labels", "") if css is not None else "",
                    )
                    labels[atr]["for"] = inputs[atr]["id"] = atr_name
                    fields[atr] = dom.div(
                        labels[atr],
                        inputs[atr],
                        cls=css.get("fields", "") if css is not None else "",
                    )

        buttons["save"] = dom.SubmitButton(
            label=f"Save {name}", icon=dom.save_icon, value=f"save_{name.lower()}"
        )
        buttons["save"]["class"] = (
            btn_css.get("save", "") if btn_css is not None else ""
        )
        buttons["delete"] = dom.SubmitButton(
            label=f"Delete {name}", icon=dom.delete_icon, value=f"delete_{name.lower()}"
        )
        buttons["delete"]["class"] = (
            btn_css.get("delete", "") if btn_css is not None else ""
        )
        buttons["buttons"] = dom.div(
            buttons["delete"],
            buttons["save"],
            cls=btn_css.get("buttons", "") if btn_css is not None else "",
        )

        form = dom.Form(*fields.values(), buttons["buttons"])
        cls = type.__new__(mcs, name, bases, namespaces)
        setattr(cls, "labels", labels)
        setattr(cls, "inputs", inputs)
        setattr(cls, "fields", fields)
        setattr(cls, "buttons", buttons)
        setattr(cls, "form", form)
        return cls

    class Meta:
        exclude: list = []


@dataclass
class UIBase(metaclass=UiMeta):
    pass


if __name__ == "__main__":
    import typing
    from dataclasses import dataclass

    import valio
    from tortoise import Model, fields

    from uidom.backend.database.db import queries

    class IDMixin(object):
        id = fields.UUIDField(pk=True)

    class TimeStampMixin(object):
        created_at = fields.DatetimeField(auto_now_add=True)
        updated_at = fields.DatetimeField(auto_now=True)

    class CountryModel(Model, IDMixin, TimeStampMixin):
        country = fields.CharField(max_length=50)

        def __str__(self):
            return f"Country: {str(self.country)}"

        class Meta:
            table = "country"

    class StateModel(Model, IDMixin, TimeStampMixin):
        country = fields.ForeignKeyField(
            model_name="models.CountryModel", related_name="states"
        )
        state = fields.CharField(max_length=50)

        def __str__(self):
            return f"State: {str(self.state)}, {str(self.country)}"

        class Meta:
            table = "state"

    class CityModel(Model, IDMixin, TimeStampMixin):
        state = fields.ForeignKeyField(
            model_name="models.StateModel", related_name="cities"
        )
        city = fields.CharField(max_length=50)

        def __str__(self):
            return f"City: {self.city}, {str(self.state)}"

        class Meta:
            table = "city"

    class LocationModel(Model, IDMixin, TimeStampMixin):
        city = fields.ForeignKeyField(
            model_name="models.CityModel", related_name="locations"
        )
        street_name = fields.CharField(max_length=50)

        class Meta:
            table = "location"

    class UserModel(Model, IDMixin, TimeStampMixin):
        first_name = fields.CharField(max_length=50, blank=True, null=True)
        last_name = fields.CharField(max_length=50, blank=True, null=True)
        photo = fields.BinaryField()

        class Meta:
            table = "user"

    class AccountTypeEnum(str, Enum):
        MANUFACTURER = "manufacturer"
        RETAILER = "retailer"
        WHOLESALER = "wholesaler"
        BROKER = "broker"

    class ProductTypeEnum(str, Enum):
        DIAMOND = "diamond"
        BULLION = "bullion"
        JEWELLERY = "jewellery"
        COLOR_STONE = "color_stone"

    class AccountTypeModel(Model, IDMixin, TimeStampMixin):
        account_type = fields.CharEnumField(enum_type=AccountTypeEnum, unique=True)

        class Meta:
            table = "account_type"

    class ProductTypeModel(Model, IDMixin, TimeStampMixin):
        product_type = fields.CharEnumField(enum_type=ProductTypeEnum, unique=True)

        class Meta:
            table = "product_type"

    class AccountModel(Model, IDMixin, TimeStampMixin):
        email = fields.CharField(max_length=50)
        password = fields.CharField(max_length=80)
        is_active = fields.BooleanField(default=False)
        is_verified = fields.BooleanField(default=False)
        user = fields.ForeignKeyField(
            model_name="models.UserModel", related_name="accounts"
        )
        product_type = fields.ForeignKeyField(
            model_name="models.ProductTypeModel", related_name="accounts"
        )
        account_type = fields.ForeignKeyField(
            model_name="models.AccountTypeModel", related_name="accounts"
        )
        location = fields.ForeignKeyField(
            model_name="models.LocationModel", related_name="accounts"
        )

        class Meta:
            table = "account"

    class Tokens(Model, IDMixin, TimeStampMixin):
        account = fields.ForeignKeyField(model_name="models.Account")

        class Meta:
            table = "token"

    @dataclass
    class ID(object):
        id = valio.UUIDField(default=uuid.uuid4())

        class Meta:
            exclude = ["id"]

    @dataclass
    class TimeStamp(object):
        created_at: time = valio.DateValidator(logger=False, debug=True, default=time())
        updated_at: time = valio.DateValidator(logger=False, debug=True, default=time())

        class Meta:
            exclude = ["created_at", "updated_at"]

    @dataclass
    class Country(UIBase, ID, TimeStamp):
        country_field = valio.StringField(logger=False, max_length=50)
        country: str = country_field.validator

        class Meta:
            model = CountryModel

    valio.Validator.register(Country)  # noqa

    class CountryValidator(valio.Validator):
        annotation = typing.Union[Country, None]

    class CountryField(valio.Field):
        validator = CountryValidator

    @dataclass
    class State(UIBase, ID, TimeStamp):
        country_field = CountryField(logger=False, debug=True)
        state_field = valio.StringField(logger=False, max_length=50)

        country: typing.Union[Country, CountryValidator] = country_field.validator
        state: str = state_field.validator

        class Meta:
            model = StateModel

    valio.Validator.register(State)  # noqa

    class StateValidator(valio.Validator):
        annotation = typing.Union[State, None]

    class StateField(valio.Field):
        validator = StateValidator

    @dataclass
    class City(UIBase, ID, TimeStamp):
        state_field = StateField(logger=False)
        city_field = valio.StringField(logger=False, max_length=50)
        state: State = state_field.validator
        city: str = city_field.validator

        class Meta:
            model = CityModel

    valio.Validator.register(City)  # noqa

    class CityValidator(valio.Validator):
        annotation = typing.Union[City, None]

    class CityField(valio.Field):
        validator = CityValidator

    @dataclass
    class Location(UIBase, ID, TimeStamp):
        city_field = CityField(logger=False)
        street_field = valio.StringField(logger=False)

        city: City = city_field.validator
        street_name = street_field.validator

        class Meta:
            model = LocationModel

    valio.Validator.register(Location)  # noqa

    class LocationValidator(valio.Validator):
        annotation = typing.Union[Location, None]

    @dataclass
    class User(UIBase, ID, TimeStamp):
        first_name: str = valio.StringValidator(logger=False, debug=True)
        last_name: str = valio.StringValidator(logger=False, debug=True)
        photo: Path = valio.PathValidator(logger=False, debug=True)

        class Meta:
            model = UserModel

    valio.Validator.register(User)  # noqa

    class UserValidator(valio.Validator):
        annotation = typing.Union[User, None]

    @dataclass
    class Account(UIBase, TimeStamp):
        email: str = valio.EmailIDValidator(logger=False, debug=True)
        is_active: bool = valio.BooleanValidator(logger=False, debug=True)
        is_verified: bool = valio.BooleanValidator(logger=False, debug=True)
        user: User = UserValidator(logger=False, debug=True)
        account_type: typing.Union[str, Enum, None] = valio.StringEnumField(
            in_choices=AccountTypeEnum, debug=True
        )
        product_type: typing.Union[str, Enum, None] = valio.StringEnumField(
            in_choices=ProductTypeEnum, debug=True
        )
        locations: Location = LocationValidator(logger=False, debug=True)

        class Meta:
            model = AccountModel

    print(Country.form)

    # user_form = Application(Country.form)
    # user_form.link_styles["href"] = "../production_path/static/file/css/styles.css"
    # user_form.save()
