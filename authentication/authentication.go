package authentication

import (
	"fmt"
	"log"

	"github.com/cactusdev/cactusapi/driver"

	"golang.org/x/crypto/bcrypt"
)

// TODO: Implement this fully
// TODO: Implement auth tokens?

// EncryptPassword encrypt a password
func EncryptPassword(password string) string {
	hash, _ := bcrypt.GenerateFromPassword([]byte(password), 10)

	return string(hash)
}

// ComparePassword compare a user's password
func ComparePassword(password string, user string) string {
	storage, err := driver.Initialize("localhost:28015", "api", "users", "name")

	fmt.Println(storage.GetOne(user))
	if err != nil {
		log.Fatal(err)
	} // if err := bcrypt.CompareHashAndPassword(password, )
	return ""
}
