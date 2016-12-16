# Individual TODOs

* TODO **1** Unit tests
* TODO **2** Implement token-based authentication/limited scope access
* TODO **3** Check for duplicate userId on trust endpoint
* ~~TODO **4** Fix PATCH implementation to allow for partial editing~~ Done 12/12/16 in b59737b14e8c419d128d820f0d82673380fa4270
* ~~TODO **5** Fix createdAt "cannot be formatted as datetime"~~ - tentatively fixed as of 12/?/16 in f88616ccc07840c5e5b593eff4d1103d2f31b034
* TODO **6** Figure out how to use underscore_case for fields - dump_to="newName" works, but it's got all sorts of issues
* TODO **7** Implement cross-platform regex for checking valid tokens.
* ~~TODO **8** Move repetitive kwargs parsing into function/decorator~~ Done 12/12/16 in efc24be29eba5543b2a98fe42aa770dc3591dee7
* TODO **9** Implement allowing URL args OR JSON, not forcing JSON (decorator)
* TODO **10** Implement %COUNT%
* TODO **11** Rewrite specification to match style throughout
* TODO **12** Minify logging of request URL to make console easier to read
* TODO **13** Implement response sorting/limiting on all endpoints
~~* TODO **14** Implement user creation because that's required for configs~~ Confirmed done. Unknown date/commit

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
