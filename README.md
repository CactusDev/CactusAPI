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

## Commands

  * ### Get all commands
    `GET` `/api/v1/user/<string:username>/command`

	   A `GET` request to this endpoint will return a list of all commands associated with the username supplied.

  * ### Get an individual command
    `GET` `/api/v1/user/<string:username>/command/<string:command>`

	A `GET` request to this endpoint will return a **single** command object in response if the command requested exists. If not, or if the user requested does not exist, the API will return no content with the HTTP response code set to `204`.

  * ### Creating and editing a command
    `PATCH` `/api/v1/user/<string:username>/command/<string:command>`
	A `PATCH` request to this endpoint must have the following parameters included:

	* `response` - **Optional if editing, required for command creation**
	  The command's response

	* `level` - **Optional, defaults to `0`**
	  Sets the user level requirement to run the command.
	   * `0` - Accessible by ALL users
	   * `1` - Channel Moderator Only
	   * `2` - Channel Owner Only
	   * `3` - Channel Subscriber Only

    This endpoint will return the newly created command with HTTP status code `201` if the command is created.

	When editing via this endpoint, simply supply any changes wished to be made. If successful, the endpoint will return the newly changed command with status code `200`.

  * ### Remove a command
    `DELETE` `/api/v1/user/<string:username>/command/<string:command>`

	A `DELETE` request to this endpoint will return nothing with the HTTP status code `204` if the deletion was successful.

	If it fails due to a username or command being supplied that does not exist, then an error will be returned with what was missing.

## Quotes

  * ### Get all quotes
    `GET` `/api/v1/user/<string:username>/quote`

	   A `GET` request to this endpoint will return a list of all quotes associated with the username supplied.

  * ### Get an individual quote
    `GET` `/api/v1/user/<string:username>/quote/<int:quote>`

	A `GET` request to this endpoint will return a **single** quote object in response if the quote requested exists. If not, or if the user requested does not exist, the API will return no content with the HTTP response code set to `204`.

  * ### Creating and editing a quote
    `PATCH` `/api/v1/user/<string:username>/quote/<string:quote>`
	A `PATCH` request to this endpoint must have the following parameters included:

	* `quote` - **Required**
	  The quote's content (text)

    This endpoint will return the newly created quote with HTTP status code `201` if the quote is created.

	When editing via this endpoint, simply supply any changes wished to be made. If successful, the endpoint will return the newly changed quote with status code `200`.

  * ### Remove a quote
    `DELETE` `/api/v1/user/<string:username>/quote/<int:quote>`

	A `DELETE` request to this endpoint will return nothing with the HTTP status code `204` if the deletion was successful.

	If it fails due to a username or quote ID being supplied that does not exist, then an error will be returned with what was missing.

## Friends

  * ### Get all quotes
    `GET` `/api/v1/channel/<string:channel>/friend`

	   A `GET` request to this endpoint will return a list of all friends associated with the channel supplied.

  * ### Get an individual friend
    `GET` `/api/v1/channel/<string:channel>/friend/<string:friend>`

	A `GET` request to this endpoint will return a **single** friend object in response if the friend requested exists. If not, or if the user requested does not exist, the API will return no content with the HTTP response code set to `204`.

  * ### Creating and editing a friend
    `PATCH` `/api/v1/channel/<string:channel>/friend/<string:friend>`
	A `PATCH` request to this endpoint does not require any paramters, as friends are permanent.

    This endpoint will return the newly created friend with HTTP status code `201` if the friend is created.

	When editing via this endpoint, simply supply any changes wished to be made. If successful, the endpoint will return the newly changed friend with status code `200`.

  * ### Remove a friend
    `DELETE` `/api/v1/channel/<string:channel>/friend/<string:friend>`

	A `DELETE` request to this endpoint will return nothing with the HTTP status code `204` if the deletion was successful.

	If it fails due to a channel being supplied that does not exist, then an error will be returned with what was missing.
