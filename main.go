package main

import (
	"fmt"
	"net/http"
	"strconv"

	"github.com/cactusbot/CactusAPI/driver"
	"github.com/cactusbot/CactusAPI/model"
	"github.com/cactusbot/CactusAPI/resource"
	"github.com/cactusbot/CactusAPI/routes"
	"github.com/cactusbot/CactusAPI/util"

	"github.com/julienschmidt/httprouter"

	"github.com/manyminds/api2go"
)

func main() {
	var log = util.InitLogger(true)

	port := 8000
	api := api2go.NewAPI("v1")

	userStorage, err := driver.Initialize("localhost:28015", "api", "users")
	if err != nil {
		log.Fatal(err)
	}
	commandStorage, err := driver.Initialize("localhost:28015", "api", "commands")
	if err != nil {
		log.Fatal(err)
	}

	api.AddResource(model.User{}, resource.UserResource{UserStorage: userStorage})
	api.AddResource(model.Command{}, resource.CommandResource{CommandStorage: commandStorage})

	log.Info("Listening on :" + strconv.Itoa(port))
	handler := api.Handler().(*httprouter.Router)

	handler.GET("/v1/user/:id", routes.GetUser)
	handler.GET("/v1/:target/command/:command", routes.GetCommand)

	http.ListenAndServe(fmt.Sprintf(":%d", port), handler)
}
