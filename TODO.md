**TODO** *1* Unit tests
**TODO** *2* Implement token-based authentication/limited scope access
**TODO** *3* Check for duplicate userId on trust endpoint
**TODO** *4* Fix PATCH implementation to allow for partial editing
**TODO** *5* Fix createdAt "cannot be formatted as datetime" - hopefully fixed in develop?
**TODO** *6* Figure out how to use underscore_case for fields - dump_to="newName" works, but it's got all sorts of issues
**TODO** *7* Implement cross-platform regex for checking valid tokens.
~~**TODO** *8* Move repetitive kwargs parsing into function/decorator~~ Done 12/12/16
**TODO** *9* Implement allowing URL args OR JSON, not forcing JSON (decorator)
**TODO** *10* Implement %COUNT%
**TODO** *11* Rewrite specification to match style throughout
**TODO** *12* Minify logging of request URL to make console easier to read
**TODO** *13* Implement response sorting/limiting on all endpoints

Unit tests:
    Commands
    Quotes
    Tickets
    Trusts
    Models/Schemas:
        Validation
        Import/Export
    util:
        OAuth ... somehow
        helpers:
            decorators
            resource
            response
            rethink
