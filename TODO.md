# Individual TODOs

* TODO **1** Unit tests
* ~~TODO **2** Implement token-based authentication/limited scope access~~ "Done" 12/20/16 in 4765bde98de8e5292efa420979c80961fce91283 - will definitely be tweaked down the road
* ~~TODO **3** Check for duplicate userId on trust endpoint~~ Done, not sure why this was here
* ~~TODO **4** Fix PATCH implementation to allow for partial editing~~ Done 12/12/16 in b59737b14e8c419d128d820f0d82673380fa4270
* ~~TODO **5** Fix createdAt "cannot be formatted as datetime"~~ - tentatively fixed as of 12/?/16 in f88616ccc07840c5e5b593eff4d1103d2f31b034
* ~~TODO **6** Figure out how to use underscore_case for fields - dump_to="newName" works, but it's got all sorts of issues~~ - Later
* ~~TODO **7** Implement cross-platform regex for checking valid tokens.~~ Done 12/23/16 in e4a1c7fea0562c39f1c29431e229a43ced979e0a
* ~~TODO **8** Move repetitive kwargs parsing into function/decorator~~ Done 12/12/16 in efc24be29eba5543b2a98fe42aa770dc3591dee7
* ~~TODO **9** Implement allowing URL args OR JSON, not forcing JSON ~~ Done 12/20/16 in 4765bde98de8e5292efa420979c80961fce91283
* ~~TODO **10** Implement %COUNT%~~ Done 12/24/16
* ~~TODO **11** Rewrite specification to match style throughout~~ Not an actual API TODO, but still good to do
* ~~TODO **12** Minify logging of request URL to make console easier to read~~ Ignore this, not actually needed
* ~~TODO **13** Implement response sorting/limiting on all endpoints~~ Done 12/24/16 in 2b1e943ddf33e63257f85731a86e3ad78ef45fcd (will be implementing sorting later)
* ~~TODO **14** Implement user creation because that's required for configs~~ Confirmed done. Unknown date/commit
* ~~TODO **15** Don't allow aliases to be created if the aliased command doesn't exists~~ Done 12/22/16 in aad3d5d4f5025dff4e2a5b7ebe2fe09a4bd981a1
* ~~TODO **16** Aliases should be removed when the aliased command gets removed~~ Done 12/22/16 in aad3d5d4f5025dff4e2a5b7ebe2fe09a4bd981a1
* ~~TODO **17**: Check auth token for validity based on datetime~~ Done 12/24/16 in 2d60236a631b041d68765f5bc524a77e9eeae1c6
* ~~TODO **18**: Implement rate-limiting on endpoints~~ Done 12/24/16 in 2d60236a631b041d68765f5bc524a77e9eeae1c6, will need to be thoroughly tested by unit tests
* Make sure the token exists as a user in the API, otherwise give a 403 because user doesn't exist
* Figure out what happened to createdAt key
* ~~Add command name to repeats~~

# Grouped TODOs

* Unit tests
  * Commands
  * Quotes
  * Tickets
  * Trusts
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

# Later TODOs

* Figure out how to use underscore_case for fields - dump_to="newName" works, but it's got all sorts of issues
* Implement response sorting
* Write API reference w/ standard style and up to date stuff
* Sphinx documentation
