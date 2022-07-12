# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

#TODO: WIP

from __future__ import annotations

import datetime
from dataclasses import asdict, dataclass, is_dataclass
from typing import MutableMapping, MutableSequence, Tuple

from valio import Validator, email_pattern


class EdgeQLValidator(Validator):

    def __set_name__(self, owner, name):
        super(EdgeQLValidator, self).__set_name__(owner=owner, name=name)
        if getattr(owner, "create", None) is None:
            setattr(owner, "create", '')
        required = None 
        reassign = None 
        min_value = None
        max_value = None 
        min_length = None 
        max_length = None 
        pattern = None
        in_choice = None
        constraint = None

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

        if any([reassign is not None and not reassign, min_length, max_length, min_value, max_value, pattern, in_choice]):
            constraint = True 
             
        annotation_name = self.annotation.__name__ if not isinstance(self.annotation, str) else self.annotation
        
        owner.create += f"type {owner.__name__}" + " {" if owner.create == '' else ''

        if owner.create.endswith("\n\t}\n}") or owner.create.endswith("\n}"):
            owner.create = owner.create[:-2]

        if not is_dataclass(self.annotation):
            if required:
                owner.create += f"\n\trequired property {name} -> {annotation_name};" 
            else:
                owner.create += f"\n\tproperty {name} -> {annotation_name};" 
        else:
            if required:
                owner.create += f"\n\trequired link {name} -> {annotation_name};" 
            else:
                owner.create += f"\n\tlink {name} -> {annotation_name};"

        if constraint:
            owner.create += "\n\t{"

        owner.create += '''\n\t\tconstraint exclusive;''' if not reassign and reassign is not None else ''
        owner.create += f'''\n\t\tconstraint min_value({min_value});''' if min_value and min_value is not None else ''
        owner.create += f'''\n\t\tconstraint max_value({max_value});''' if max_value and max_value is not None else ''
        owner.create += f'''\n\t\tconstraint min_len_value({min_length});''' if min_length and min_length is not None else ''
        owner.create += f'''\n\t\tconstraint max_len_value({max_length});''' if max_length and max_length is not None else ''
        owner.create += f'''\n\t\tconstraint regexp({pattern});''' if pattern and pattern is not None else ''
        owner.create += f'''\n\t\tconstraint one_of({in_choice});''' if in_choice and in_choice is not None else ''
        if constraint:
            owner.create += "\n\t}"
        owner.create += "\n}"

    
@dataclass
class User(object):
    create = ''
    created_at: datetime.datetime = EdgeQLValidator(logger=False, debug=True, required=True, reassign=False, default=datetime.datetime.now)
    updated_at: datetime.datetime = EdgeQLValidator(logger=False, debug=True, reassign=True, default=datetime.datetime.now)
    name: str = EdgeQLValidator(logger=False, required=True, reassign=False, debug=True, min_length=4)
    email_id: str = EdgeQLValidator(logger=False, debug=True, pattern=email_pattern)
    


@dataclass
class SocialMedia(object):
    media_host: str = EdgeQLValidator(logger=False, debug=True)
    media_handle: str = EdgeQLValidator(logger=False, debug=True)


@dataclass
class Account(object):
    users: User = EdgeQLValidator(logger=False, debug=True)
    media: SocialMedia = EdgeQLValidator(logger=False, debug=True)
    
    
# if __name__ == '__main__':
    # print(User(name='qq22'))
    # print(Account.create)
    # user1 = Account(title="User1")
