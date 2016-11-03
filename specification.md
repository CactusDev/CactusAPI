# CactusAPI Specification

## How to interact with the api

The API base path is `/api/v1`. This will change over time as our API changes versions, but this is the basic form. All API requests **must** start with that path.

## Responses

All responses from endpoints are returned in JSON form and are [JSON:API](http://jsonapi.org/) compliant.

Regular HTTP codes are in use. If the request completes successfully and is able to return data, then the status code will be `200`. Other results and their respective codes include:

* **`201`** Created:
     * The request has been fulfilled and resulted in a new resource being created.

* **`204`** No Content:
     * The server has fulfilled the request but does not need to return an entity-body, and might want to return updated metainformation.
     * The server has successfully processed the request, but will not be returning any content.

* **`400`** Bad request:
     * The request could not be understood by the server due to malformed syntax.


*    **`404`** Resource not found:
     * There is no API endpoint for that path

     An error object will be returned with more details.

*    **`500`** Internal Server Error:
     * The server encountered an unexpected condition which prevented it from fulfilling the request.Used when there is no more specific error code


## Users

### User Creation

  `PATCH` `/api/v1/user/:username`

   A `PATCH` request to this endpoint must have the following parameters included:
   
   * `email` - The user's email address
   * `provider` - The user's OAuth provider
     * `pid` - User ID from the OAuth provider
     * `userName` - The properly formatted username involving case from the OAuth provider
   * `token` - The user's platform-agnostic token, in string form

### Search for a user
  `GET` `/api/v1/user/:token`

  `GET` `/api/v1/user/:username?service=:service`

  A `GET` request to this endpoint will return a list of all users that the token matches the username provided in the path. Normally will only return a single object.

  Alternatively, you can search by username, but you will also have to provide the service that user is on (Twitch, Beam, etc.)

### Link a new service

  `POST` `/api/v1/user/:token/link?service=:service&source=:channelId`

  To link a new service/platform to an existing account, make a `POST` request to this endpoint, providing the new service in the request parameter `service` and the channel ID on that platform in parameter `channelId`.

## Commands

### Get all commands
  `GET` `/api/v1/user/:token/command`

  A `GET` request to this endpoint will return a list of all commands associated with the token supplied.

### Get an individual command
  `GET` `/api/v1/user/:token/command/:command`

  A `GET` request to this endpoint will return a single command object in response if the command requested exists. If not, or if the user requested does not exist, the API will return no content with the HTTP response code set to `204`.

## Quotes
### Get all quotes
  `GET` `/api/v1/user/:token/quote`

   A `GET` request to this endpoint will return a list of all quotes associated with the token supplied.

### Get an individual quote

  `GET` `/api/v1/user/:token/quote/<int:quote>`

   A `GET` request to this endpoint will return a single quote object in response if the quote requested exists. If not, or if the user requested does not exist, the API will return no content with the HTTP response code set to `204`.

## Trusts

### Get all trusts

  `GET` `/api/v1/user/:token/trust?service=:service`

  A `GET` request to this endpoint will return a list of all trusts associated with the token supplied.
  
  Optionally a request parameter `:service` may be provided to limit the results to trusts specific to that platform.

### Get an individual trust

  `GET` `/api/v1/user/:token/trust/:username?service=:service`

  A `GET` request to this endpoint will return a single trust object in response if the trust requested exists on the supplied service. If not, or if the user requested does not exist, the API will return no content with the HTTP response code set to `204`.

  `:service` may be omitted if the trust requested is universal.

### Creating and editing a trust

  `PATCH` `/api/v1/user/:token/trust/:username?service=:service`

  ***INFO ABOUT PERMIT REQUEST PARAMETERS FOR SHORTER THAN FOREVER TRUST GOES HERE***

  This endpoint will return the newly created trust with HTTP status code `201` if the creation is successful.

  When editing via this endpoint, simply supply any changes wished to be made. If successful, the endpoint will return the modified trust with status code `200`.

  The `:service` request parameter is optional unless you want to create the trust for only a specific platform.

### Remove a trust

  `DELETE` `/api/v1/user/:token/trust/:username?service=:service`

  A `DELETE` request to this endpoint will return nothing with the HTTP status code `204` if the deletion was successful.

  If it fails due to a user being supplied that does not exist, then an error will be returned with what was missing.

  The `:service` request parameter is optional unless you want to remove the trust for only a specific platform.
