from record import AddressBookRecord


class AddressBookAPI:
    """Provides methods to interact with the JSON address book database"""
    def __init__(self, database_path: str) -> None:
        self.database_path = database_path

    def add_record(self, new_record: AddressBookRecord) -> AddressBookRecord:
        # TODO
        pass

    def edit_record(self, old_record: AddressBookRecord, edited_record: AddressBookRecord) -> AddressBookRecord:
        # TODO
        pass

    def delete_specfic_record(self, record_to_delete: AddressBookRecord) -> AddressBookRecord:
        # TODO
        pass

    def delete_matching_records(self, first_name: str = "", last_name: str = "",
                       phone: str = "", email: str = "") -> list[AddressBookRecord]:
        # TODO
        pass

    def list_records(self) -> list[AddressBookRecord]:
        # TODO
        pass

    def search_records(self, first_name: str = "", last_name: str = "",
                       phone: str = "", email: str = "") -> list[AddressBookRecord]:
        # TODO
        pass
