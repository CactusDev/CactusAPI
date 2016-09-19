package main

import (
	"fmt"
	"net/http"
	"strconv"

	"github.com/cactusbot/API/driver"
	"github.com/cactusbot/API/model"
	"github.com/cactusbot/API/resource"
	"github.com/cactusbot/API/routes"
	"github.com/cactusbot/API/util"

	"github.com/julienschmidt/httprouter"

	"github.com/manyminds/api2go"
)

func main() {
	var log = util.InitLogger(true)

	port := 8000
	api := api2go.NewAPI("v1")

	userStorage, _ := driver.Initialize("localhost:28015", "api", "users")

	api.AddResource(model.User{}, resource.UserResource{UserStorage: userStorage})

	log.Info("Listening on :" + strconv.Itoa(port))
	handler := api.Handler().(*httprouter.Router)

	handler.GET("/v1/user/:id", routes.GetUser)

	http.ListenAndServe(fmt.Sprintf(":%d", port), handler)
}
