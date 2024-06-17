# Address Book API

An API for managing a JSON address book, written in Python using FastAPI

## Setup and Running
The API was tested using Python 3.12.
The required modules (along with their dependencies) are:
- fastapi-slim
- uvicorn

To set up a virtual environment with the required modules, run:
```
python -m venv VENV_NAME

(Bash) source VENV_NAME/bin/activate
(Windows) VENV_NAME\Scripts\activate

pip install -r requirements.txt
```

Run `python app.py` to start the API.

The API is accessible from the localhost on port 8000 (`127.0.0.1:8000`)

## Available Endpoints
FastAPI autogenerates documentation for the different endpoints at `http://127.0.0.1:8000/docs`

An overview of the endpoints is below
### GET Endpoints
`/list_records` - Returns a list of all records. No JSON data is sent to this endpoint.

| Response code | JSON data returned |
| ------------- | ------------------ |
| 200           | All records        |

### POST Endpoints
`/add_record` - Adds a new record to the address book, expects JSON data as follow:
```json
{
  "first_name": "First name",
  "last_name": "Last name",
  "phone": "Phone number",
  "email": "Email address"
}
```

| Response code | JSON data returned            |
| ------------- | ------------------            |
| 200           | Added record                  |
| 409           | Record already exists message |
| 422           | Invalid field entry message   |

---
`/edit_record` - Edit an existing record, expects JSON data as follows:
```json
{
  "record_to_edit": {
    "first_name": "First name",
    "last_name": "Last name",
    "phone": "Phone number",
    "email": "Email address"
  },
  "new_first_name": "New first name",
  "new_last_name": "New last name",
  "new_phone": "New phone number",
  "new_email": "New email address"
}
```

Any of the **new** fields can be omitted if they are not to be updated.

| Response code | JSON data returned           |
| ------------- | ------------------           |
| 200           | Newly edited record          |
| 404           | Not found message            |
| 422           | Invalid field entry message  |

---
`/search_records` - Returns a list of all records that match the entered fields, expects JSON data as follows:
```json
{
  "first_name": "First name",
  "last_name": "Last name",
  "phone": "Phone number",
  "email": "Email address"
}
```

Any unused field can be omitted.

| Response code | JSON data returned |
| ------------- | ------------------ |
| 200           | Matching records   |

### DELETE Endpoints

`/delete_record` - Delete an existing record, expects JSON data as follows:
```json
{
  "first_name": "First name",
  "last_name": "Last name",
  "phone": "Phone number",
  "email": "Email address"
}
```

| Response code | JSON data returned |
| ------------- | ------------------ |
| 200           | Deleted record     |
| 404           | Not found message  |

---
`/delete_matching_records` - Delete any record that matches the fields entered, expects JSON data as follows:
```json
{
  "first_name": "First name",
  "last_name": "Last name",
  "phone": "Phone number",
  "email": "Email address"
}
```

Any unused fields can be omitted.

| Response code | JSON data returned  |
| ------------- | ------------------  |
| 200           | Any deleted records |

## Unit Tests
The units tests for the API are in `tests.py`, they are split up into:
- Tests for the internal API which provides methods to interact with the database
- Tests for the different endpoints

To run the unit tests, run `python tests.py`