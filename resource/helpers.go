package resource

import (
	"fmt"

	"github.com/manyminds/api2go"

	rethink "gopkg.in/dancannon/gorethink.v2"
)

// CheckEmpty checks if the error is a ErrEmptyResult, indicating no more rows and returns the proper HTTPError
func CheckEmpty(err error, resource string, ID string) api2go.HTTPError {
	if err == rethink.ErrEmptyResult {
		errMsg := fmt.Sprintf("No such %s %s", resource, ID)
		return api2go.NewHTTPError(err, errMsg, 404)
	}
	// It's not an ErrEmptyResult, so return a 500
	log.Error(err)
	return api2go.NewHTTPError(err, err.Error(), 500)
}
