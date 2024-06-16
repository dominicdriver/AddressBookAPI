from api import AddressBookAPI
from record import AddressBookRecord
from typing import Annotated
from fastapi import FastAPI, Body
import uvicorn

ENDPOINTS = {
    "add_record": "/add_record",
    "edit_record": "/edit_record",
    "delete_specific_record": "/delete_record",
    "delete_matching_record": "/delete_matching_record",
    "list_records": "/list_records",
    "search_records": "/search_records"
}

ADDRESS_BOOK_FILE_PATH = "address_book.json"
    
class FastAPIWrapper:
    """
    A wrapper that contains an instance of FastAPI and the API used to interact with the database
    """
    def __init__(self, database_file_path: str):
        self.app = FastAPI()
        self.api = AddressBookAPI(database_file_path)

        self.app.add_api_route(ENDPOINTS["add_record"], endpoint=self.add_record_endpoint, methods=["POST"])
        self.app.add_api_route(ENDPOINTS["edit_record"], endpoint=self.edit_record_endpoint, methods=["POST"])
        self.app.add_api_route(ENDPOINTS["delete_specific_record"], endpoint=self.delete_specific_record_endpoint, methods=["DELETE"])
        self.app.add_api_route(ENDPOINTS["delete_matching_record"], endpoint=self.delete_matching_record_endpoint, methods=["DELETE"])
        self.app.add_api_route(ENDPOINTS["list_records"], endpoint=self.list_records_endpoint, methods=["GET"])
        self.app.add_api_route(ENDPOINTS["search_records"], endpoint=self.search_records_endpoint, methods=["GET"])

    def add_record_endpoint(self, record_to_add: AddressBookRecord):
        api_result = self.api.add_record(record_to_add)

        return api_result
    
    def edit_record_endpoint(self, record_to_edit: AddressBookRecord, new_first_name: Annotated[str, Body()] = "",
                             new_last_name: Annotated[str, Body()] = "", new_phone: Annotated[str, Body()] = "",
                             new_email: Annotated[str, Body()] = ""):
        api_result = self.api.edit_record(record_to_edit, new_first_name, new_last_name,
                                          new_phone, new_email)

        return api_result

    def delete_specific_record_endpoint(self, record_to_delete: AddressBookRecord):
        api_result = self.api.delete_specfic_record(record_to_delete)

        return api_result
    
    def delete_matching_record_endpoint(self, first_name: Annotated[str, Body()] = "", last_name: Annotated[str, Body()] = "",
                                        phone: Annotated[str, Body()] = "", email: Annotated[str, Body()] = ""):
        api_result = self.api.delete_matching_records(first_name, last_name, phone, email)

        return api_result
    
    def search_records_endpoint(self, first_name: Annotated[str, Body()] = "", last_name: Annotated[str, Body()] = "",
                                phone: Annotated[str, Body()] = "", email: Annotated[str, Body()] = ""):
        api_result = self.api.search_records(first_name, last_name, phone, email)

        return api_result

    def list_records_endpoint(self):
        api_result = self.api.list_records()

        return api_result


fast_api = FastAPIWrapper(ADDRESS_BOOK_FILE_PATH)

if __name__ == "__main__":
    uvicorn.run(fast_api.app)
