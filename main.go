package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strconv"

	"github.com/cactusbot/cactusapi/driver"
	"github.com/cactusbot/cactusapi/model"
	"github.com/cactusbot/cactusapi/resource"
	"github.com/cactusbot/cactusapi/util"

	"github.com/julienschmidt/httprouter"

	"github.com/manyminds/api2go"
)

type config struct {
	Host  string
	Port  string
	Table string
}

func main() {
	var log = util.InitLogger(true)

	file, err := os.Open("config.json")
	if err != nil {
		log.Error("The config file does not exist.")
		log.Error("Creating...")

		err := util.CopyFile("config-template.json", "config.json")
		if err != nil {
			log.Error(err)
			log.Fatal("There was an error copying the config template.")
		}
		log.Info("Copy finished!")
		log.Info("Verify the options in there, and restart.")
		return
	}

	decoder := json.NewDecoder(file)
	conf := config{}
	err = decoder.Decode(&conf)
	if err != nil {
		log.Fatal(err)
	}

	port := 8000
	api := api2go.NewAPI("v1")

	userStorage, err := driver.Initialize(conf.Host+":"+conf.Port, conf.Table, "users", "userName")
	if err != nil {
		log.Fatal(err)
	}

	commandStorage, err := driver.Initialize(conf.Host+":"+conf.Port, conf.Table, "commands", "name")
	if err != nil {
		log.Fatal(err)
	}

	api.AddResource(model.User{}, resource.UserResource{UserStorage: userStorage})
	api.AddResource(model.Command{}, resource.CommandResource{CommandStorage: commandStorage})

	log.Info("Listening on :" + strconv.Itoa(port))
	handler := api.Handler().(*httprouter.Router)

	http.ListenAndServe(fmt.Sprintf(":%d", port), handler)
}
