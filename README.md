Telemetry server
================

Information
-----------

Simple telemetry server which assepts POST requests with json and saves json
data to local files newline separated.

Configuration
-------------

Example configuration are provided by upstream.

* `[server]` section:
    * `address` - address to bind, string
    * `port` - port to bind, integer
    * `request_path` - path for requests, string

Telemetry is splitted by groups, each group should have own configuration section
named as `[group:group_name]`, e.g. `[group:sample]`. The following configuration
allowed inside group:

* `database_filename` - database file name to store telemetry. Additional variables
  comes from request (e.g. `api`, `type`) and from this group are allowed. E.g.:
  `sample-db-api-v{api}.db`

API
---

* `HEAD /`
    * defined responses:
      ```
      $ curl -I http://localhost:8080

      HTTP/1.0 200 OK
      Server: BaseHTTP/0.6 Python/3.5.2
      Date: Thu, 01 Jan 1970 00:00:00 GMT
      Content-Type: application/json
      ```
* `GET /`
    * no headers required
    * no payload required
    * defined responses:
      ```
      $ curl -i http://localhost:8080

      HTTP/1.0 501 Not Implemented
      Server: BaseHTTP/0.6 Python/3.5.2
      Date: Thu, 01 Jan 1970 00:00:00 GMT
      Content-Type: application/json

      {"message": "not implemented"}
      ```
* `POST /:request_path`
    * headers: `Content-Type: application/json`
    * payload should be dictionary or list of dictionary. Each dictionary should
      have the following keys:
        * `api` - telemetry API version
        * `type` - telemetry type matches to known names
        * `metadata` - any metadata inside as json which will be saved to file

      Any other keys will be ignored.
    * defined responses:
      ```
      $ curl -H 'Content-Type: application/json' -d '{"type": "example", "api": 0, "metadata": {"key":"value"}}' -i http://localhost:8080/

      HTTP/1.0 200 OK
      Server: BaseHTTP/0.6 Python/3.5.2
      Date: Thu, 01 Jan 1970 00:00:00 GMT
      Content-Type: application/json

      {"message": "saved"}
      ```

      ```
      $ curl -H 'Content-Type: application/json' -d '{"type": "example", "api": 0, "metadata": {"key":"value"}}' -i http://localhost:8080/invalid_path

      HTTP/1.0 404 Not Found
      Server: BaseHTTP/0.6 Python/3.5.2
      Date: Thu, 01 Jan 1970 00:00:00 GMT
      Content-Type: application/json
      ```

      ```
      $ curl -H 'Content-Type: invalid_type' -d '{"type": "example", "api": 0, "metadata": {"key":"value"}}' -X POST -i http://localhost:8080

      HTTP/1.0 415 Unsupported Media Type
      Server: BaseHTTP/0.6 Python/3.5.2
      Date: Thu, 01 Jan 1970 00:00:00 GMT
      Content-Type: application/json
      ```

      ```
      $ curl -H 'Content-Type: application/json' -d '{"somekey": "somevalue"}' -i http://localhost:8080

      HTTP/1.0 400 Bad Request
      Server: BaseHTTP/0.6 Python/3.5.2
      Date: Thu, 01 Jan 1970 00:00:00 GMT
      Content-Type: application/json

      {"message": "invalid payload"}
      ```

      ```
      $ curl -H 'Content-Type: application/json' -d '{"somekey": broken_json}' -X POST -i http://localhost:8080

      HTTP/1.0 500 Internal Server Error
      Server: BaseHTTP/0.6 Python/3.5.2
      Date: Fri, 01 Jan 1970 00:00:00 GMT
      Content-Type: application/json
      ```
