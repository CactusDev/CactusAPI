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

* **`500`** Internal Server Error:
  * The server encountered an unexpected condition which prevented it from fulfilling the request.
  * Used when there is no more specific error code
   
* **`404`** Resource not found:

  * There is no API endpoint for that path
    
    An error object will be returned with more details.


## Commands

 * ### Get all commands
     `GET` `/api/v1/user/:token/command`

      A `GET` request to this endpoint will return a list of all commands associated with the token supplied.

 * ### Get an individual command

    `GET` `/api/v1/user/:token/command/:command`

     A `GET` request to this endpoint will return a single command object in response if the command requested exists. If not, or if the user requested does not exist, the API will return no content with the HTTP response code set to `204`.

 * ### Creating and editing a command

      `PATCH` `/api/v1/user/:token/command/:name`
      A `PATCH` request to this endpoint must have the following parameters included:
    
    *  `response` - **Optional if editing, required for command creation**
         The command's response
    
    *  `level` - **Optional, defaults to `0`**
         Sets the user level requirement to run the command.
       * `0` - Accessible by ALL users
       * `1` - Channel Moderator Only
       * `2` - Channel Owner Only
       * `3` - Channel Subscriber Only
    
    This endpoint will return the newly created command with HTTP status code `201` if the command is created.
    
    When editing via this endpoint, simply supply any changes wished to be made. If successful, the endpoint will return the newly changed command with status code `200`.
    
 * ### Remove a command
      `DELETE` `/api/v1/user/:token/command/:command`
    
    A `DELETE` request to this endpoint will return nothing with the HTTP status code `204` if the deletion was successful.
    
    If it fails due to a token or command being supplied that does not exist, then an error will be returned with what was missing.

## Quotes

* ### Get all quotes
    `GET` `/api/v1/user/:token/quote`

     A `GET` request to this endpoint will return a list of all quotes associated with the username supplied.

* ### Get an individual quote

    `GET` `/api/v1/user/:token/quote/:quoteId`

    A `GET` request to this endpoint will return a single quote object in response if the quote requested exists. If not, or if the user requested does not exist, the API will return no content with the HTTP response code set to `204`.


 * ### Creating and editing a quote
      `PATCH` `/api/v1/user/:token/quote/:quoteId`
      A `PATCH` request to this endpoint must have the following parameters included:

    * `quote` - **Required**
      The quote's content (text)

      This endpoint will return the newly created quote with HTTP status code `201` if the quote is created.

    When editing via this endpoint, simply supply any changes wished to be made. If successful, the endpoint will return the newly changed quote with status code `200`.

 * ### Remove a quote
      `DELETE` `/api/v1/user/:token/quote/quoteId`

    A `DELETE` request to this endpoint will return nothing with the HTTP status code `204` if the deletion was successful.

    If it fails due to a token or quote ID being supplied that does not exist, then an error will be returned with what was missing.

## Trusts

* ### Get all trusts

    `GET` `/api/v1/user/:token/trust`

     A `GET` request to this endpoint will return a list of all trusts associated with the channel supplied.

    **Optional Parameters**:

    * `service` - A comma-separated string representing the platform(s) you want to limit the trusts returned to

* ### Get an individual trust

    `GET` `/api/v1/user/:token/trust/:username`

    A `GET` request to this endpoint will return a single trust object in response if the trust requested exists. If not, or if the user requested does not exist, the API will return no content with the HTTP response code set to `204`.

    **Optional Parameters**:

    - `service` - A comma-separated string representing the platform(s) you want to limit the trusts returned to.

* ### Creating and editing a trust

    `PATCH` `/api/v1/user/:token/trust/:username`

    ***INFO ABOUT PERMIT REQUEST PARAMETERS FOR SHORTER THAN FOREVER PERMITS***

    This endpoint will return the newly created resource with HTTP status code `201` if the creation is successful.

    When editing via this endpoint, simply supply any changes wished to be made. If successful, the endpoint will return the newly changed resource with status code `200`.

* ### Remove a trust

    `DELETE` `/api/v1/channel/:token/trust/:username`

    A `DELETE` request to this endpoint will return nothing with the HTTP status code `204` if the deletion was successful.

    If it fails due to a channel being supplied that does not exist, then an error will be returned with what was missing.

    **Optional Parameters**:

    - `service` - A comma-separated string representing the platform(s) you want to remove the trusts from.
