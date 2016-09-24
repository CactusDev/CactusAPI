package model

// User struct defines the fields for api2go to send
type User struct {
	ID        string      `json:"-"`
	Confirmed string      `json:"confirmedAt"`
	Active    bool        `json:"active"`
	Email     string      `json:"email"`
	Roles     []string    `json:"roles"`
	Channels  interface{} `json:"channels"`
	Username  string      `json:"username"`
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
