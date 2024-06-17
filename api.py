from record import (AddressBookRecord, AddressBookRecordEncoder, AddressBookRecordDecoder,
                    EMAIL_REGEX, NAME_REGEX, PHONE_REGEX)
from enum import Enum, auto
from typing import Optional
from dataclasses import dataclass
import json
import re


class ResponseCode(Enum):
    OK = auto()
    ALREADY_EXISTS = auto()
    NOT_FOUND = auto()
    INVALID_FIELD = auto()


@dataclass
class Response:
    response_code: ResponseCode
    data: Optional[AddressBookRecord | list[AddressBookRecord]]


class AddressBookAPI:
    """
    Provides methods to interact with the JSON address book database
    All methods return a response code, along with any relevant data
    """
    def __init__(self, database_path: str) -> None:
        self.database_path = database_path

    def add_record(self, new_record: AddressBookRecord) -> Response:
        """
        Adds the provided record to the database.
        Returns the added record on success, or an error if the record already exists
        """
        records = self.list_records().data

        if new_record in records:
            return Response(ResponseCode.ALREADY_EXISTS, None)

        records.append(new_record)

        with open(self.database_path, "w") as database_file:
            json.dump(records, database_file, indent=4, cls=AddressBookRecordEncoder)

        return Response(ResponseCode.OK, new_record)

    def edit_record(self, old_record: AddressBookRecord, new_first_name: str = "", new_last_name: str = "",
                    new_phone: str = "", new_email: str = "") -> Response:
        """
        Edits a record with the provided fields.
        Returns the edited record on success,
        or an error if the record is not found or a new field is invalid
        """
        records = self.list_records().data

        # Check that any new field is valid, return an error if not
        if new_first_name and not re.match(NAME_REGEX, new_first_name):
            return Response(ResponseCode.INVALID_FIELD, new_first_name)

        if new_last_name and not re.match(NAME_REGEX, new_last_name):
            return Response(ResponseCode.INVALID_FIELD, new_last_name)
        
        if new_phone and not re.match(PHONE_REGEX, new_phone):
            return Response(ResponseCode.INVALID_FIELD, new_phone)
        
        if new_email and not re.match(EMAIL_REGEX, new_email):
            return Response(ResponseCode.INVALID_FIELD, new_email)

        # Find the existing record and edit any specificed fields
        for record in records:
            if old_record == record:
                if new_first_name:
                    record.first_name = new_first_name
                if new_last_name:
                    record.last_name = new_last_name
                if new_phone:
                    record.phone = new_phone
                if new_email:
                    record.email = new_email

                with open(self.database_path, "w") as database_file:
                    json.dump(records, database_file, indent=4, cls=AddressBookRecordEncoder)

                return Response(ResponseCode.OK, record)

        return Response(ResponseCode.NOT_FOUND, None)

    def delete_specific_record(self, record_to_delete: AddressBookRecord) -> Response:
        """
        Trys to delete the specified records.
        Returns the record is successful, or an error if the record is not found
        """
        records = self.list_records().data

        try:
            records.remove(record_to_delete)
        except ValueError:
            return Response(ResponseCode.NOT_FOUND, None)

        with open(self.database_path, "w") as database_file:
            json.dump(records, database_file, indent=4, cls=AddressBookRecordEncoder)

        return Response(ResponseCode.OK, record_to_delete)

    def delete_matching_records(self, first_name: str = "", last_name: str = "",
                                phone: str = "", email: str = "") -> Response:
        """
        Deletes records that match the provided fields.
        Returns the deleted records
        """
        records = self.list_records().data
        new_records = records.copy()
        deleted_records = []

        for record in records:
            if ((first_name == "" or first_name == record.first_name)
            and (last_name == "" or last_name == record.last_name)
            and (phone == "" or phone == record.phone)
            and (email == "" or email == record.email)):

                new_records.remove(record)
                deleted_records.append(record)

        with open(self.database_path, "w") as database_file:
            json.dump(new_records, database_file, indent=4, cls=AddressBookRecordEncoder)

        return Response(ResponseCode.OK, deleted_records)

    def list_records(self) -> Response:
        """
        Returns all records in the database
        """
        with open(self.database_path, "r") as database_file:
            return Response(ResponseCode.OK, json.load(database_file, cls=AddressBookRecordDecoder))

    def search_records(self, first_name: str = "", last_name: str = "",
                       phone: str = "", email: str = "") -> Response:
        """
        Returns all records that match the provided fields
        """
        records = self.list_records().data
        found_records = []

        # If no search fields are specified, return an empty list
        if first_name == "" and last_name == "" and phone == "" and email == "":
            return Response(ResponseCode.OK, [])

        for record in records:
            if ((first_name == "" or first_name == record.first_name)
            and (last_name == "" or last_name == record.last_name)
            and (phone == "" or phone == record.phone)
            and (email == "" or email == record.email)):

                found_records.append(record)

        return Response(ResponseCode.OK, found_records)
