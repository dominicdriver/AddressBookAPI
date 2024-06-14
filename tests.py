from api import AddressBookAPI, AddressBookRecord
from record import AddressBookRecordEncoder, AddressBookRecordDecoder
import unittest
import json


class TestAPI(unittest.TestCase):
    ADDRESS_BOOK_FILE_PATH = "test_address_book.json"

    @classmethod
    def setUpClass(cls):
        cls.api = AddressBookAPI(cls.ADDRESS_BOOK_FILE_PATH)

    def setUp(self):
        self.setup_database()

    def setup_database(self):
        """Clears out the database and adds a few example records"""
        test_records = [
            AddressBookRecord("David", "Platt", "01913478234", "david.platt@corrie.co.uk"),
            AddressBookRecord("Jason", "Grimshaw", "01913478123", "jason.grimshaw@corrie.co.uk"),
            AddressBookRecord("Ken", "Barlow", "019134784929", "ken.barlow@corrie.co.uk"),
            AddressBookRecord("Rita", "Sullivan", "01913478555", "rita.sullivan@corrie.co.uk")
        ]

        with open(self.ADDRESS_BOOK_FILE_PATH, "w") as database_file:
            json.dump(test_records, database_file, indent=4, cls=AddressBookRecordEncoder)

    def read_records_from_database(self):
        with open(self.ADDRESS_BOOK_FILE_PATH) as database_file:
            return json.load(database_file, cls=AddressBookRecordDecoder)
        
    def add_record_to_database(self, record: AddressBookRecord):
        records = self.read_records_from_database()
        records.append(record)

        with open(self.ADDRESS_BOOK_FILE_PATH, "w") as database_file:
            json.dump(records, database_file, indent=4, cls=AddressBookRecordEncoder)

    def test_add_single_record(self):
        record_to_add = AddressBookRecord("Chesney", "Brown", "01913606138", "chesney.brown@corrie.co.uk")
        self.api.add_record(record_to_add)

        database_records = self.read_records_from_database()

        self.assertIn(record_to_add, database_records)

    def test_add_multiple_records(self):
        records_to_add = [
            AddressBookRecord("Chesney", "Brown", "01913606138", "chesney.brown@corrie.co.uk"),
            AddressBookRecord("Sharon", "Watts", "01895532162", "sharon.watts@ee.com"),
            AddressBookRecord("Jean", "Slater", "01895643379", "jean.slater@ee.co.uk")
        ]

        for record in records_to_add:
            self.api.add_record(record)

        database_records = self.read_records_from_database()

        for record in records_to_add:
            self.assertIn(record, database_records)

    def test_edit_record(self):
        new_phone_number = "01913633216"
        record_to_edit = AddressBookRecord("Chesney", "Brown", "01913606138", "chesney.brown@corrie.co.uk")
        edited_record = AddressBookRecord("Chesney", "Brown", new_phone_number, "chesney.brown@corrie.co.uk")

        self.add_record_to_database(record_to_edit)
        self.api.edit_record(record_to_edit, new_phone=new_phone_number)

        records_after_edit = self.read_records_from_database()

        self.assertIn(edited_record, records_after_edit)
        self.assertNotIn(record_to_edit, records_after_edit)

    def test_delete_specific_record(self):
        record_to_delete = AddressBookRecord("Chesney", "Brown", "01913606138", "chesney.brown@corrie.co.uk")

        self.add_record_to_database(record_to_delete)
        self.api.delete_specfic_record(record_to_delete)

        records_after_delete = self.read_records_from_database()

        self.assertNotIn(record_to_delete, records_after_delete)

    def test_delete_matching_records(self):
        test_records = [
            AddressBookRecord("Phil", "Mitchell", "01895521739", "phil.mitchell@ee.co.uk"),
            AddressBookRecord("Billy", "Mitchell", "01895521732", "billy.mitchell@ee.co.uk")
        ]

        for record in test_records:
            self.add_record_to_database(record)

        self.api.delete_matching_records(last_name="Mitchell")

        records_after_delete = self.read_records_from_database()

        for record in test_records:
            self.assertNotIn(record, records_after_delete)

    def test_list_records(self):
        database_records = self.read_records_from_database()
        api_records = self.api.list_records()

        self.assertListEqual(database_records, api_records)

    def test_search_records(self):
        search_first_name = "Billy"

        test_records = [
            AddressBookRecord("Billy", "Mayhew", "01913763249", "billy.mayhew@corrie.co.uk"),
            AddressBookRecord("Billy", "Mitchell", "01895521732", "billy.mitchell@ee.co.uk")
        ]

        for record in test_records:
            self.add_record_to_database(record)
        
        found_records = self.api.search_records(first_name=search_first_name)

        self.assertListEqual(test_records, found_records)


if __name__ == "__main__":
    unittest.main()
