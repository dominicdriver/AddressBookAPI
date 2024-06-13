from api import AddressBookAPI
import unittest


class TestAPI(unittest.TestCase):
    ADDRESS_BOOK_FILE_PATH = "address_book.json"

    @classmethod
    def setUpClass(cls):
        cls.api = AddressBookAPI(cls.ADDRESS_BOOK_FILE_PATH)

    def test_add_single_record(self):
        # TODO
        self.fail("Not implemented")

    def test_add_multiple_records(self):
        # TODO
        self.fail("Not implemented")

    def test_edit_record(self):
        # TODO
        self.fail("Not implemented")

    def test_delete_record(self):
        # TODO
        self.fail("Not implemented")

    def test_list_records(self):
        # TODO
        self.fail("Not implemented")

    def test_search_records(self):
        # TODO
        self.fail("Not implemented")


if __name__ == "__main__":
    unittest.main()
