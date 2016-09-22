package routes

import (
	"fmt"
	"net/http"
	"reflect"

	"github.com/cactusbot/CactusAPI/driver"
	"github.com/cactusbot/CactusAPI/model"
	"github.com/julienschmidt/httprouter"
	"github.com/manyminds/api2go/jsonapi"
)

// GetUser get an individual user and send it to the client requesting it
func GetUser(w http.ResponseWriter, r *http.Request, params httprouter.Params) {
	connection, _ := driver.Initialize("localhost:28015", "api", "users")

	user, _ := connection.GetOne(params.ByName("id"))

	channels := []interface{}{user["channels"]}[0]
	roles := []string{}

	switch reflect.TypeOf(user["roles"]).Kind() {
	case reflect.Slice:
		s := reflect.ValueOf(user["roles"])
		for i := 0; i < s.Len(); i++ {
			roles = append(roles, s.Index(i).Interface().(string))
		}
	}

	userAsStruct := model.User{
		Active:   user["active"].(bool),
		Channels: channels,
		// Confirmed: user["confirmed"].(string),
		Email:    user["email"].(string),
		ID:       user["id"].(string),
		Roles:    roles,
		Username: user["username"].(string),
	}

	json, err := jsonapi.Marshal(userAsStruct)
	if err != nil {
		fmt.Println(err)
	}
	_, _ = w.Write(json)
}
