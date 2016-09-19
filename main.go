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

	userStorage, _ := driver.Initialize("localhost:28015", "api", "users")

	api.AddResource(model.User{}, resource.UserResource{UserStorage: userStorage})

	log.Info("Listening on :" + strconv.Itoa(port))
	handler := api.Handler().(*httprouter.Router)

	handler.GET("/v1/user/:id", routes.GetUser)

	http.ListenAndServe(fmt.Sprintf(":%d", port), handler)
}
