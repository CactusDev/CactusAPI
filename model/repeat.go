package model

// Repeat struct defines the fields for api2go to send
type Repeat struct {
	ID   string `json:"-"`
	Time string `json:"time"`
	Text string `json:"text"`
}

// GetID Returns the user's ID to satisfy api2go
func (u Repeat) GetID() string {
	return u.ID
}

// SetID sets ID of a User object to satisfy the requirement of api2go
func (u *Repeat) SetID(id string) error {
	u.ID = id
	return nil
}
