package main

import (
	"fmt"
	"net/http"
	"strconv"

	"github.com/cactusbot/cactusapi/driver"
	"github.com/cactusbot/cactusapi/model"
	"github.com/cactusbot/cactusapi/resource"
	"github.com/cactusbot/cactusapi/util"

	"github.com/julienschmidt/httprouter"

	"github.com/manyminds/api2go"
)

func main() {
	var log = util.InitLogger(true)

	port := 8000
	api := api2go.NewAPI("v1")

	userStorage, err := driver.Initialize("rpiawesomeness.me:20815", "cactus", "users", "userName")
	if err != nil {
		log.Fatal(err)
	}
	commandStorage, err := driver.Initialize("rpiawesomeness.me:20815", "cactus", "commands", "name")
	if err != nil {
		log.Fatal(err)
	}

	api.AddResource(model.User{}, resource.UserResource{UserStorage: userStorage})
	api.AddResource(model.Command{}, resource.CommandResource{CommandStorage: commandStorage})

	log.Info("Listening on :" + strconv.Itoa(port))
	handler := api.Handler().(*httprouter.Router)

	http.ListenAndServe(fmt.Sprintf(":%d", port), handler)
}
