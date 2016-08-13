Code View server
================

[![Build Status](https://travis-ci.org/code-view/server.svg?branch=master)](https://travis-ci.org/code-view/server)
 
Backend of [code-view.io](https://code-view.io/) &ndash; service for streaming code.

Development
-----------

Install dependencies with:

```
pip install -r requirements.txt
```

Run server with:

```
python -m code_view.main
```

Run tests with:

```
py.test
```

Usage
-----

Run server:

```
docker run codeview/server
```

API
---

Session object:

```
{
    id: str,
    secureToken: str,
    fileName: str,
    text: str,
    selectionStartLine: int,
    selectionStartColumn: int,
    selectionEndLine: int,
    selectionEndColumn: int
}
```

Endpoints:

* `POST`:`/api/session/` &ndash; create new streaming session (accepts empty object);
* `PUT`:`/api/session/{id}/` &ndash; update streaming session;
* `GET`:`/api/session/{id}/` &ndash; get streaming session;
* `WS`:`/channel/session/{id}/` &ndash; subscribe to streaming session.

License MIT
-----------
