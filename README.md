# Amity

Amity is a simple room allocator written in Python. It provides a minimal set
of models and controllers that can be used to manage offices, living spaces and
people.

## Requirements

* Python >= 3.11
* The dependencies listed in `requirements.txt`

## Installation

Create a virtual environment and install the dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running tests

The project uses `pytest`. Execute the following command from the repository
root to run all tests:

```bash
pytest -q
```

All tests should pass and you should see output similar to:

```
23 passed in <time>s
```

## Project layout

* `app/` – source code containing the models and controllers
* `app/tests/` – unit tests for the application logic
* `tests/` – additional unit tests
* `designs/` – design documentation

## License

This project is provided for educational purposes.
