from dataclasses import dataclass, asdict
from typing import Any, Annotated
from pydantic import StringConstraints
import json

# From https://www.regular-expressions.info/email.html
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


@dataclass
class AddressBookRecord:
    """Holds information about an entry in the address book"""
    first_name: Annotated[str, StringConstraints(pattern=r"[a-zA-Z]+")]
    last_name: Annotated[str, StringConstraints(pattern=r"[a-zA-Z]+")]
    phone: Annotated[str, StringConstraints(pattern=r"\d+")]
    email: Annotated[str, StringConstraints(pattern=EMAIL_REGEX)]


class AddressBookRecordEncoder(json.JSONEncoder):
    """Encodes an AddressBookRecord into JSON by converting it to a dictionary"""
    def default(self, obj) -> dict | Any:
        if isinstance(obj, AddressBookRecord):
            return asdict(obj)
        return super().default(obj)


class AddressBookRecordDecoder(json.JSONDecoder):
    """Decodes a JSON object into an AddressBookRecord object"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj) -> AddressBookRecord:
        return AddressBookRecord(**obj)
