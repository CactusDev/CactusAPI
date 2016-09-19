package model

import (
	"github.com/cactusbot/API/driver"
	"github.com/cactusbot/API/util"
)

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
func (u User) SetID(id string) error {
	u.ID = id
	return nil
}

// CreateUser create a new user
func (u *User) CreateUser() {
	userStorage, err := driver.Initialize("localhost:28015", "api", "users")
	if err != nil {
		util.GetLogger().Error(err)
	}

	userStorage.Insert(map[string]interface{}{
		"active":       u.Active,
		"confirmed_at": u.Confirmed,
		"email":        u.Email,
		"roles":        u.Roles,
		"channels":     u.Channels,
		"username":     u.Username,
	})
}

// RemoveUser remove a user
func (u *User) RemoveUser() {

}
