from dataclasses import dataclass, asdict
import json


@dataclass
class AddressBookRecord:
    """Holds information about an entry in the address book"""
    first_name: str
    last_name: str
    phone: str
    email: str


class AddressBookRecordEncoder(json.JSONEncoder):
    """Encodes an AddressBookRecord into JSON by converting it to a dictionary"""
    def default(self, obj):
        if isinstance(obj, AddressBookRecord):
            return asdict(obj)
        return super().default(obj)


class AddressBookRecordDecoder(json.JSONDecoder):
    """Decodes a JSON object into an AddressBookRecord object"""
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        return AddressBookRecord(**obj)
