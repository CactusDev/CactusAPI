package model

// Quote defines the fields for API2Go
type Quote struct {
	ID    string `json:"quoteID"`
	Quote string `json:"quote"`
}

// GetID return the id for the given quote
func (q Quote) GetID() string {
	return q.ID
}

// SetID set the id for the given quote
func (q Quote) SetID(id string) error {
	q.ID = id
	return nil
}
