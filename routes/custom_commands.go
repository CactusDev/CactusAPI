package routes

import (
	"fmt"
	"net/http"

	"github.com/cactusbot/CactusAPI/driver"
	"github.com/cactusbot/CactusAPI/model"
	"github.com/cactusbot/sepal/util"
	"github.com/julienschmidt/httprouter"
	"github.com/manyminds/api2go/jsonapi"
)

// GetCommand get an individual command and send it to the client requesting it
func GetCommand(w http.ResponseWriter, r *http.Request, params httprouter.Params) {
	connection, _ := driver.Initialize("localhost:28015", "api", "command")

	command, err := connection.GetOne(params.ByName("command"))

	if err != nil {
		util.GetLogger().Error(err)
		return
	}

	commandAsStruct := model.Command{
		ID:       command["id"].(string),
		Command:  command["command"].(string),
		Response: command["response"].(string),
		Calls:    command["calls"].(int),
	}

	json, err := jsonapi.Marshal(commandAsStruct)
	if err != nil {
		fmt.Println(err)
	}
	_, _ = w.Write(json)
}
