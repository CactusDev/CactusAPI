package model

// User struct defines the fields for api2go to send
type User struct {
	ID       string   `json:"-"gorethink:",omitempty"`
	Active   bool     `json:"active"gorethink:"active"`
	Email    string   `json:"email"gorethink:"email"`
	Roles    []string `json:"-"gorethink:"roles"`
	Channels []string `json:"channels"gorethink:"channels"`
	Username string   `json:"username"gorethink:"username"`
}

// GetID Returns the user's ID to satisfy api2go
func (u User) GetID() string {
	return u.ID
}

// SetID sets ID of a User object to satisfy the requirement of api2go
func (u *User) SetID(id string) error {
	u.ID = id
	return nil
}
