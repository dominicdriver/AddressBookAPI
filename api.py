from record import AddressBookRecord, AddressBookRecordEncoder, AddressBookRecordDecoder
import json


class AddressBookAPI:
    """
    Provides methods to interact with the JSON address book database
    """
    def __init__(self, database_path: str) -> None:
        self.database_path = database_path

    def add_record(self, new_record: AddressBookRecord) -> AddressBookRecord:
        """
        Adds the provided record to the database
        """
        records = self.list_records()

        records.append(new_record)

        with open(self.database_path, "w") as database_file:
            json.dump(records, database_file, indent=4, cls=AddressBookRecordEncoder)

        return new_record

    def edit_record(self, old_record: AddressBookRecord, new_first_name: str = "", new_last_name: str = "",
                    new_phone: str = "", new_email: str = "") -> AddressBookRecord | None:
        """
        Edits a record with the provided fields.
        Returns the edited record on success, or None if the record is not found
        """
        records = self.list_records()

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

                return record

        return None

    def delete_specific_record(self, record_to_delete: AddressBookRecord) -> AddressBookRecord | None:
        """
        Trys to delete the specified records.
        Returns the record is successful, or None otherwise
        """
        records = self.list_records()

        try:
            records.remove(record_to_delete)
        except ValueError:
            return None

        with open(self.database_path, "w") as database_file:
            json.dump(records, database_file, indent=4, cls=AddressBookRecordEncoder)

        return record_to_delete

    def delete_matching_records(self, first_name: str = "", last_name: str = "",
                                phone: str = "", email: str = "") -> list[AddressBookRecord]:
        """
        Deletes records that match the provided fields.
        Returns the deleted records
        """
        records = self.list_records()
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

        return deleted_records

    def list_records(self) -> list[AddressBookRecord]:
        """
        Returns all records in the database
        """
        with open(self.database_path, "r") as database_file:
            return json.load(database_file, cls=AddressBookRecordDecoder)

    def search_records(self, first_name: str = "", last_name: str = "",
                       phone: str = "", email: str = "") -> list[AddressBookRecord]:
        """
        Returns all records that match the provided fields
        """
        records = self.list_records()
        found_records = []

        # If no search fields are specified, return an empty list
        if first_name == "" and last_name == "" and phone == "" and email == "":
            return []

        for record in records:
            if ((first_name == "" or first_name == record.first_name)
            and (last_name == "" or last_name == record.last_name)
            and (phone == "" or phone == record.phone)
            and (email == "" or email == record.email)):

                found_records.append(record)

        return found_records
