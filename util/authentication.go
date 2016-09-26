package util

import (
	"fmt"

	"github.com/CactusDev/CactusAPI/driver"

	"golang.org/x/crypto/bcrypt"
)

// EncryptPassword encrypt a password
func EncryptPassword(password string) string {
	hash, _ := bcrypt.GenerateFromPassword([]byte(password), 10)

	return string(hash)
}

// ComparePassword compare a user's password
func ComparePassword(password string, user string) string {
	storage, err := driver.Initialize("localhost:28015", "api", "users", "name")

	fmt.Println(storage.GetUser(user))
	if err != nil {
		log.Fatal(err)
	} // if err := bcrypt.CompareHashAndPassword(password, )
	return ""
}
