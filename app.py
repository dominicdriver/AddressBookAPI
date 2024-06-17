from api import AddressBookAPI, ResponseCode
from record import AddressBookRecord
from typing import Annotated
from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse
import uvicorn

ENDPOINTS = {
    "add_record": "/add_record",
    "edit_record": "/edit_record",
    "delete_specific_record": "/delete_record",
    "delete_matching_records": "/delete_matching_records",
    "list_records": "/list_records",
    "search_records": "/search_records"
}

ADDRESS_BOOK_FILE_PATH = "address_book.json"


class FastAPIWrapper:
    """
    A wrapper that contains an instance of FastAPI and the API used to interact with the database
    """
    def __init__(self, database_file_path: str) -> None:
        self.app = FastAPI(title="Address Book API")
        self.api = AddressBookAPI(database_file_path)

        self.app.add_api_route(ENDPOINTS["add_record"], endpoint=self.add_record_endpoint, methods=["POST"])
        self.app.add_api_route(ENDPOINTS["edit_record"], endpoint=self.edit_record_endpoint, methods=["POST"])

        self.app.add_api_route(ENDPOINTS["delete_specific_record"], endpoint=self.delete_specific_record_endpoint, methods=["DELETE"])
        self.app.add_api_route(ENDPOINTS["delete_matching_records"], endpoint=self.delete_matching_records_endpoint, methods=["DELETE"])
        
        self.app.add_api_route(ENDPOINTS["list_records"], endpoint=self.list_records_endpoint, methods=["GET"])

        # Ideally this would use GET, but some web browsers do not allow GET requests with a (json) body
        self.app.add_api_route(ENDPOINTS["search_records"], endpoint=self.search_records_endpoint, methods=["POST"])

    def add_record_endpoint(self, record_to_add: AddressBookRecord) -> JSONResponse:
        api_result = self.api.add_record(record_to_add)

        match api_result.response_code:
            case ResponseCode.ALREADY_EXISTS:
                return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                                    content={"msg": "Record already in database"})
            case ResponseCode.OK:
                return api_result.data

    def edit_record_endpoint(self, record_to_edit: AddressBookRecord, new_first_name: Annotated[str, Body()] = "",
                             new_last_name: Annotated[str, Body()] = "", new_phone: Annotated[str, Body()] = "",
                             new_email: Annotated[str, Body()] = "") -> JSONResponse:
        api_result = self.api.edit_record(record_to_edit, new_first_name, new_last_name,
                                          new_phone, new_email)
        
        match api_result.response_code:
            case ResponseCode.NOT_FOUND:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                    content={"msg": "Record not found"})
            case ResponseCode.INVALID_FIELD:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                    content={"msg": f"Invalid value: {api_result.data}"})
            case ResponseCode.OK:
                return api_result.data

    def delete_specific_record_endpoint(self, record_to_delete: AddressBookRecord) -> JSONResponse:
        api_result = self.api.delete_specific_record(record_to_delete)

        match api_result.response_code:
            case ResponseCode.NOT_FOUND:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                    content={"msg": "Record not found"})
            case ResponseCode.OK:
                return api_result.data

    def delete_matching_records_endpoint(self, first_name: Annotated[str, Body()] = "",
                                         last_name: Annotated[str, Body()] = "",
                                         phone: Annotated[str, Body()] = "", email: Annotated[str, Body()] = ""
                                        ) -> list[AddressBookRecord]:
        api_result = self.api.delete_matching_records(first_name, last_name, phone, email)

        match api_result.response_code:
            case ResponseCode.OK:
                return api_result.data

    def search_records_endpoint(self, first_name: Annotated[str, Body()] = "", last_name: Annotated[str, Body()] = "",
                                phone: Annotated[str, Body()] = "", email: Annotated[str, Body()] = ""
                                ) -> list[AddressBookRecord]:
        api_result = self.api.search_records(first_name, last_name, phone, email)

        match api_result.response_code:
            case ResponseCode.OK:
                return api_result.data

    def list_records_endpoint(self) -> list[AddressBookRecord]:
        api_result = self.api.list_records()
        
        match api_result.response_code:
            case ResponseCode.OK:
                return api_result.data


fast_api = FastAPIWrapper(ADDRESS_BOOK_FILE_PATH)

if __name__ == "__main__":
    uvicorn.run(fast_api.app)
