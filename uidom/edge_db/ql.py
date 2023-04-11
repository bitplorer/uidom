# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from dataclasses import dataclass, is_dataclass

# TODO: WIP
from datetime import datetime
from typing import get_args

from valio import (
    BOOL,
    CHOICE,
    DATE_TIME_DELTA,
    DEBUG,
    DEFAULT,
    DOC,
    INT,
    NAME,
    PATTERN,
    STR,
    VALUE,
    TypeValidator,
    Validator,
    email_pattern,
)


class EdgeQLValidator(Validator):
    exclusive: BOOL = TypeValidator(logger=False, debug=True)

    def __init__(
        self,
        default: DEFAULT = None,
        name: NAME = None,
        doc: DOC = None,
        required: BOOL = None,
        pattern: PATTERN = None,
        reassign: BOOL = None,
        multiple_of: VALUE = None,
        min_value: VALUE = None,
        value: VALUE = None,
        max_value: VALUE = None,
        gt: VALUE = None,
        eq: VALUE = None,
        lt: VALUE = None,
        min_length: INT = None,
        length: INT = None,
        max_length: INT = None,
        expire_after: DATE_TIME_DELTA = None,
        expire_on: DATE_TIME_DELTA = None,
        expire_before: DATE_TIME_DELTA = None,
        in_choice: CHOICE = None,
        not_in_choice: CHOICE = None,
        has_attributes: list[STR] = None,
        task_interval: INT = None,
        cache_task: BOOL = True,
        debug: DEBUG = None,
        cache_validation: BOOL = None,
        enable_async: BOOL = None,
        allow_validation: BOOL = True,
        exclusive: BOOL = None,
        **kwargs,
    ):

        self.exclusive = exclusive

        super().__init__(
            default=default,
            name=name,
            doc=doc,
            required=required,
            pattern=pattern,
            reassign=reassign,
            multiple_of=multiple_of,
            min_value=min_value,
            value=value,
            max_value=max_value,
            gt=gt,
            eq=eq,
            lt=lt,
            min_length=min_length,
            length=length,
            max_length=max_length,
            expire_after=expire_after,
            expire_on=expire_on,
            expire_before=expire_before,
            in_choice=in_choice,
            not_in_choice=not_in_choice,
            has_attributes=has_attributes,
            task_interval=task_interval,
            cache_task=cache_task,
            debug=debug,
            cache_validation=cache_validation,
            enable_async=enable_async,
            allow_validation=allow_validation,
            **kwargs,
        )

    def __set_name__(self, owner, name):
        super(EdgeQLValidator, self).__set_name__(owner=owner, name=name)
        if getattr(owner, "create", None) is None:
            setattr(owner, "create", "")

        abstract = None
        exclusive = None
        required = None
        reassign = None
        min_value = None
        max_value = None
        min_length = None
        max_length = None
        pattern = None
        in_choice = None
        default = None
        constraint = None
        try:
            Meta = getattr(owner, "Meta", None)
            abstract = getattr(Meta, "abstract", None)
        except:
            pass

        try:
            exclusive = self.exclusive
        except KeyError as ke:
            pass

        try:
            required = self.required
        except KeyError as ke:
            pass

        try:
            reassign = self.reassign
        except KeyError as ke:
            pass

        try:
            min_value = self.min_value
        except KeyError as ke:
            pass

        try:
            max_value = self.max_value
        except KeyError as ke:
            pass

        try:
            min_length = self.min_length
        except KeyError as ke:
            pass

        try:
            max_length = self.max_length
        except KeyError as ke:
            pass

        try:
            pattern = self.pattern
        except KeyError as ke:
            pass

        try:
            in_choice = self.in_choice
        except KeyError as ke:
            pass

        try:
            default = self.default
        except KeyError as ke:
            pass

        if any(
            [
                exclusive,
                reassign is not None and not reassign,
                min_length,
                max_length,
                min_value,
                max_value,
                pattern,
                in_choice,
                default,
            ]
        ):
            constraint = True

        args = get_args(owner.__annotations__[name])
        if any(args):
            if any(get_args(args[0])):
                annotation_name = get_args(args[0])[0].__name__
            else:
                annotation_name = args[0].__name__
        else:
            annotation_name = (
                self.annotation.__name__
                if not isinstance(self.annotation, str)
                else self.annotation
            )

        owner.create += (
            f"{'abstract ' if abstract is not None and abstract else ''}type {owner.__name__}"
            + " {"
            if owner.create == ""
            else ""
        )

        if owner.create.endswith("\n\t};\n}") or owner.create.endswith("\n}"):
            owner.create = owner.create[:-2]

        if not is_dataclass(owner.__annotations__[name] if not any(args) else args[0]):
            if required:
                owner.create += (
                    f"\n\trequired property {name} -> {annotation_name};"
                    if not any(args)
                    else f"\n\trequired multi property {name} -> array<<{annotation_name}>>;"
                )
            else:
                owner.create += (
                    f"\n\tproperty {name} -> {annotation_name};"
                    if not any(args)
                    else f"\n\tmulti property {name} -> array<<{annotation_name}>>;"
                )
        else:
            if required:
                owner.create += (
                    f"\n\trequired link {name} -> {annotation_name};"
                    if not any(args)
                    else f"\n\trequired multi link {name} -> {annotation_name};"
                )
            else:
                owner.create += (
                    f"\n\tlink {name} -> {annotation_name};"
                    if not any(args)
                    else f"\n\tmulti link {name} -> {annotation_name};"
                )

        if constraint:
            if owner.create.endswith(";"):
                owner.create = owner.create[:-1]
            owner.create += "\n\t{"

        owner.create += (
            """\n\t\tconstraint exclusive;"""
            if exclusive is not None and exclusive
            else ""
        )
        owner.create += (
            """\n\t\treadonly := true;"""
            if not reassign and reassign is not None
            else ""
        )
        owner.create += (
            f"""\n\t\tconstraint min_value({min_value});"""
            if min_value and min_value is not None
            else ""
        )
        owner.create += (
            f"""\n\t\tconstraint max_value({max_value});"""
            if max_value and max_value is not None
            else ""
        )
        owner.create += (
            f"""\n\t\tconstraint min_len_value({min_length});"""
            if min_length and min_length is not None
            else ""
        )
        owner.create += (
            f"""\n\t\tconstraint max_len_value({max_length});"""
            if max_length and max_length is not None
            else ""
        )
        owner.create += (
            f"""\n\t\tconstraint regexp({pattern});"""
            if pattern and pattern is not None
            else ""
        )
        owner.create += (
            f"""\n\t\tconstraint one_of({in_choice});"""
            if in_choice and in_choice is not None
            else ""
        )
        if not self.annotation is datetime:
            owner.create += (
                f"""\n\t\tdefault := {self.default if not callable(self.default) else self.default.__qualname__};"""
                if default is not None
                else ""
            )
        else:
            if self.default in [datetime.now, datetime.utcnow]:
                owner.create += f"""\n\t\tdefault := datetime_current()"""

        if constraint:
            owner.create += "\n\t}"

        owner.create += "\n}"


@dataclass
class User(object):
    create = ""
    created_at: datetime = EdgeQLValidator(
        logger=False, debug=True, required=True, default=datetime.utcnow
    )
    updated_at: datetime = EdgeQLValidator(
        logger=False, debug=True, reassign=True, default=datetime.utcnow
    )
    name: str = EdgeQLValidator(
        logger=False,
        required=True,
        reassign=False,
        debug=True,
        min_length=4,
        default="Guest",
        exclusive=True,
    )
    email_ids: list[str] | None = EdgeQLValidator(
        logger=False, debug=True, pattern=email_pattern
    )

    class Meta:
        abstract: bool = True


@dataclass
class SocialMedia(object):
    media_host: str = EdgeQLValidator(
        logger=False,
        debug=True,
        pattern=r"^https?://www.|www.\w{2,}.(net|com|edu|app|io|tech|store|biz|in|us|co.in)",
    )
    media_handle: str = EdgeQLValidator(logger=False, debug=True)


@dataclass
class Account(object):
    users: list[User] = EdgeQLValidator(
        logger=False, debug=True, required=True, default=User(name="Guest")
    )
    media: list[SocialMedia] = EdgeQLValidator(logger=False, debug=True)


# if __name__ == "__main__":
#     print(
#         Account(
#             users=[User(name="User-1"), User(name="User-2")],
#             media=[SocialMedia(media_host="www.youtube.com", media_handle="unique1")],
#         )
#     )
#     print(User.create)
