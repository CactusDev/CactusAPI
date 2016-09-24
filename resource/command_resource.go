package resource

import (
	"encoding/json"
	"errors"
	"net/http"

	"github.com/cactusbot/cactusapi/driver"
	"github.com/cactusbot/cactusapi/model"
	"github.com/cactusbot/sepal/util"
	"github.com/manyminds/api2go"
)

// CommandResource keeps track of the information required for accessing the user information
type CommandResource struct {
	CommandStorage *driver.Storage
}

// FindAll returns all values in the database for the UserResource, satisfying the api2go source interface
func (s CommandResource) FindAll(r api2go.Request) (api2go.Responder, error) {
	var result []model.Command

	commands, err := s.CommandStorage.GetAll()
	if err != nil {
		util.GetLogger().Error(err)
	}

	for _, command := range commands {
		log.Info("COMMAND")
		log.Info(command)
		marshalled, _ := json.Marshal(command)
		appended := model.Command{}
		err = json.Unmarshal(marshalled, &appended)
		if err != nil {
			// TODO: Add stuff to handle errors
			util.GetLogger().Error(err)
		}

		result = append(result, appended)
	}

	return &Response{Res: result}, nil
}

// FindOne returns a single user from the database based on ID
func (s CommandResource) FindOne(ID string, r api2go.Request) (api2go.Responder, error) {
	command, err := s.CommandStorage.GetOne(ID)
	if err != nil {
		util.GetLogger().Error(err)
		return &Response{}, api2go.NewHTTPError(err, err.Error(), http.StatusNotFound)
	}

	marshalled, _ := json.Marshal(command)
	result := model.Command{}
	err = json.Unmarshal(marshalled, &result)
	if err != nil {
		// TODO: Add stuff to handle errors
		util.GetLogger().Error(err)
	}

	return &Response{Res: result}, nil
}

// GetOne returns a single user from the database based on ID
func (s CommandResource) GetOne(ID string) (api2go.Responder, error) {
	user, err := s.CommandStorage.GetOne(ID)
	if err != nil {
		util.GetLogger().Error(err)
		return &Response{}, api2go.NewHTTPError(err, err.Error(), http.StatusNotFound)
	}

	marshalled, _ := json.Marshal(user)
	result := model.Command{}
	err = json.Unmarshal(marshalled, &result)
	if err != nil {
		// TODO: Add stuff to handle errors
		util.GetLogger().Error(err)
	}

	return &Response{Res: result}, nil
}

// Create method satisfies the api2go.DataSource interface
func (s CommandResource) Create(obj interface{}, r api2go.Request) (api2go.Responder, error) {
	command, ok := obj.(model.Command)
	if !ok {
		return &Response{}, api2go.NewHTTPError(errors.New("Invalid instance given"), "Invalid instance given", http.StatusBadRequest)
	}

	id, err := s.CommandStorage.Insert(command)
	if err != nil {
		util.GetLogger().Error(err)
		return &Response{}, api2go.NewHTTPError(err, err.Error(), http.StatusInternalServerError)
	}
	command.ID = id

	return &Response{Res: command, Code: http.StatusCreated}, nil
}

// Delete implements deletion of resources, satisfying api2go.DataSource interface
func (s CommandResource) Delete(id string, r api2go.Request) (api2go.Responder, error) {
	err := s.CommandStorage.Delete(id)
	return &Response{Code: http.StatusNoContent}, err
}

// Update implements the updating of a resource, satisfying api2go.DataSource interface
func (s CommandResource) Update(obj interface{}, r api2go.Request) (api2go.Responder, error) {
	return &Response{Code: http.StatusOK}, nil
}
