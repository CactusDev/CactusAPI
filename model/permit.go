package model

// Permit struct defines the fields for api2go to send
type Permit struct {
	ID       string `json:"-"`
	Username string `json:"username"`
	Until    string `json:"until"`
}

// GetID Returns the user's ID to satisfy api2go
func (u Permit) GetID() string {
	return u.ID
}

// SetID sets ID of a User object to satisfy the requirement of api2go
func (u *Permit) SetID(id string) error {
	u.ID = id
	return nil
}
