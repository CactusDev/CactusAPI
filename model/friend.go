package model

// Friend defines the fields for API2Go
type Friend struct {
	ID       string `json:"-"`
	Username string `json:"string"`
}

// GetID return the id for the given friend
func (f Friend) GetID() string {
	return f.ID
}

// SetID set the id for the given friend
func (f Friend) SetID(id string) error {
	f.ID = id
	return nil
}
