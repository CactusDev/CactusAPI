package routes

import (
	"fmt"
	"net/http"

	"github.com/cactusbot/CactusAPI/driver"
	"github.com/cactusbot/CactusAPI/model"
	"github.com/cactusbot/api2go/jsonapi"
	"github.com/julienschmidt/httprouter"
)

// GetCommand get an individual command and send it to the client requesting it
func GetCommand(w http.ResponseWriter, r *http.Request, params httprouter.Params) {
	connection, _ := driver.Initialize("localhost:28015", "api", "command")

	command, _ := connection.GetOne(params.ByName("command"))

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
