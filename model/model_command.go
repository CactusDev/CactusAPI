package model

// Command defines the fields for API2Go
type Command struct {
	ID       string `json:"-"`
	Command  string `json:"command"`
	Response string `json:"response"`
	Calls    int    `json:"calls"`
	Channel  string `json:"channel"`
}

// GetID Returns the user's ID to satisfy api2go
func (c Command) GetID() string {
	return c.ID
}

// SetID sets ID of a User object to satisfy the requirement of api2go
func (c *Command) SetID(id string) error {
	c.ID = id
	return nil
}
