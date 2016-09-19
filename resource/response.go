package resource

// Response struct implements api2go.Responder
type Response struct {
	Res  interface{}
	Code int
}

// Metadata is simply here to satisfy the requirements of api2go.Responder
func (r Response) Metadata() map[string]interface{} {
	return map[string]interface{}{}
}

// Result returns the JSON/interface of the response
func (r Response) Result() interface{} {
	return r.Res
}

// StatusCode returns the HTTP status code for the response
func (r Response) StatusCode() int {
	return r.Code
}
