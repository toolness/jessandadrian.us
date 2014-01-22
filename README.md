## Requirements

* Python 2.7
* [pip and virtualenv](http://stackoverflow.com/q/4324558)

## Quick Start

```
virtualenv venv

# On Windows, replace the following line with 'venv\Scripts\activate'.
source venv/bin/activate

pip install -r requirements.txt
python manage.py runserver
```

## Environment Variables

**Note:** When an environment variable is described as representing a
boolean value, if the variable exists with *any* value (even the empty
string), the boolean is true; otherwise, it's false.

**Note:** When running `manage.py runserver`, the following environment
variables are given default values: `SECRET_KEY`, `DEBUG`, `PORT`, `ORIGIN`.

* `SECRET_KEY` is a large random value.
* `DEBUG` is a boolean value that indicates whether debugging is enabled
  (this should always be false in production).
* `PORT` is the port that the server binds to.
* `ORIGIN` is the origin of the server, as it appears
  to users. If `DEBUG` is enabled, this defaults to
  `http://localhost:PORT`. Otherwise, it must be defined.
