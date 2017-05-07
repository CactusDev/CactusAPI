# Individual TODOs

* TODO Unit tests
* ~~TODO Implement token-based authentication/limited scope access~~ "Done" 12/20/16 in 4765bde98de8e5292efa420979c80961fce91283 - will definitely be tweaked down the road
* ~~TODO Check for duplicate userId on trust endpoint~~ Done, not sure why this was here
* ~~TODO Fix PATCH implementation to allow for partial editing~~ Done 12/12/16 in b59737b14e8c419d128d820f0d82673380fa4270
* ~~TODO Fix createdAt "cannot be formatted as datetime"~~ - tentatively fixed as of 12/?/16 in f88616ccc07840c5e5b593eff4d1103d2f31b034
* ~~TODO Figure out how to use underscore_case for fields - dump_to="newName" works, but it's got all sorts of issues~~ - Later
* ~~TODO Implement cross-platform regex for checking valid tokens.~~ Done 12/23/16 in e4a1c7fea0562c39f1c29431e229a43ced979e0a
* ~~TODO Move repetitive kwargs parsing into function/decorator~~ Done 12/12/16 in efc24be29eba5543b2a98fe42aa770dc3591dee7
* ~~TODO Implement allowing URL args OR JSON, not forcing JSON~~ Done 12/20/16 in 4765bde98de8e5292efa420979c80961fce91283
* ~~TODO Implement %COUNT%~~ Done 12/24/16
* ~~TODO Rewrite specification to match style throughout~~ Not an actual API TODO, but still good to do
* ~~TODO Minify logging of request URL to make console easier to read~~ Ignore this, not actually needed
* ~~TODO Implement response sorting/limiting on all endpoints~~ Done 12/24/16 in 2b1e943ddf33e63257f85731a86e3ad78ef45fcd (will be implementing sorting later)
* ~~TODO Implement user creation because that's required for configs~~ Confirmed done. Unknown date/commit
* ~~TODO Don't allow aliases to be created if the aliased command doesn't exists~~ Done 12/22/16 in aad3d5d4f5025dff4e2a5b7ebe2fe09a4bd981a1
* ~~TODO Aliases should be removed when the aliased command gets removed~~ Done 12/22/16 in aad3d5d4f5025dff4e2a5b7ebe2fe09a4bd981a1
* ~~TODO Check auth token for validity based on datetime~~ Done 12/24/16 in 2d60236a631b041d68765f5bc524a77e9eeae1c6
* ~~TODO Implement rate-limiting on endpoints~~ Done 12/24/16 in 2d60236a631b041d68765f5bc524a77e9eeae1c6, will need to be thoroughly tested by unit tests
* ~~TODO Make sure the token exists as a user in the API, otherwise give a 403 because user doesn't exist~~
* ~~TODO Repeats done by repeat alias instead of numeric ID~~
* ~~TODO Make repeats "editable" to change time~~
* ~~TODO Figure out what happened to createdAt key~~
* ~~TODO Add command name to repeats~~
* TODO Make `PATCH` for quotes only edit, not create
* ~~TODO Change X-Auth-JWT to X-Auth-Key~~
* ~~TODO Convert list in auth key to bits/hex strings~~
* ~~TODO Make aliases endpoint have proper type "alias" not "aliase"~~
* ~~TODO DB migration tool~~
* TODO Implement soft deletion (if deletedAt key == None then not "deleted", otherwise "deleted" at epoch timestamp)
* TODO Fix 500 KeyError "id" when creating command - Source is app/util/helpers/response.py:104, need to find solution. Caused by missing keys in creation JSON on creation.
* TODO Implement append

# Grouped TODOs

* Unit tests
  * ~~Commands~~
  * ~~Quotes~~
  * ~~Trusts~~
  * ~~Users~~
  * ~~Aliases~~
  * ~~Repeats~~
  * All tables/users created before tests start then test authentication & run tests as regular user
  * DocTests/documentation for all backend functions
  * Mock RethinkDB responses
  * Tests for 404/400 responses
  * Test commands return nothing for command that exists for different user
  * Create records and store IDs outside of tests
  * Models/Schemas:
    * Validation
    * Import/Export
  * util:
    * OAuth ... somehow
    * helpers:
      * decorators
      * resource
      * response
      * rethink

  * Rate limiting
  * Tables and users have to be created before tests can occur
  * Resources aren't 100% removed from DB until end of test (specifically commands, because they're needed in later tests)

# Later TODOs

* Figure out how to use underscore_case for fields - dump_to="newName" works, but it's got all sorts of issues
* Implement response sorting
* Write API reference w/ standard style and up to date stuff
* Sphinx documentation
