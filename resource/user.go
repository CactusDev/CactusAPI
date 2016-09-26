package resource

import (
	"encoding/json"
	"errors"
	"net/http"

	"github.com/CactusDev/CactusAPI/driver"
	"github.com/CactusDev/CactusAPI/model"
	"github.com/CactusDev/CactusAPI/util"
	"github.com/manyminds/api2go"

	rethink "gopkg.in/dancannon/gorethink.v2"
)

var log = util.GetLogger()

// UserResource keeps track of the information required for accessing the user information
type UserResource struct {
	UserStorage *driver.Storage
}

// FindAll returns all values in the database for the UserResource, satisfying the api2go source interface
func (s UserResource) FindAll(r api2go.Request) (api2go.Responder, error) {

	var result []model.User

	users, err := s.UserStorage.GetAll()
	if err != nil {
		log.Error(err)
	}

	for _, user := range users {
		log.Info(user)
		marshalled, _ := json.Marshal(user)
		appended := model.User{}
		err = json.Unmarshal(marshalled, &appended)
		if err != nil {
			// TODO: Add stuff to handle errors
			log.Error(err)
		}

		result = append(result, appended)
	}

	return &Response{Res: result}, nil
}

// FindOne returns a single user from the database based on ID
func (s UserResource) FindOne(ID string, r api2go.Request) (api2go.Responder, error) {
	log.Debug(ID)
	user, err := s.UserStorage.GetOne(ID)
	if err != nil {
		log.Error(err)
		return &Response{}, api2go.NewHTTPError(err, err.Error(), http.StatusNotFound)
	}

	marshalled, _ := json.Marshal(user)
	result := model.User{}
	err = json.Unmarshal(marshalled, &result)
	if err != nil {
		// TODO: Add stuff to handle errors
		log.Error(err)
	}

	return &Response{Res: result}, nil
}

// GetOne returns a single user from the database based on ID
func (s UserResource) GetOne(ID string) (api2go.Responder, error) {
	user, err := s.UserStorage.GetOne(ID)
	if err != nil {
		log.Error(err)
		return &Response{}, api2go.NewHTTPError(err, err.Error(), http.StatusNotFound)
	}

	marshalled, _ := json.Marshal(user)
	result := model.User{}
	err = json.Unmarshal(marshalled, &result)
	if err != nil {
		// TODO: Add stuff to handle errors
		log.Error(err)
	}

	return &Response{Res: result}, nil
}

// Create method satisfies the api2go.DataSource interface
func (s UserResource) Create(obj interface{}, r api2go.Request) (api2go.Responder, error) {
	// Check that the object supplied has the proper info to fill a model.User
	user, ok := obj.(model.User)
	if !ok {
		return &Response{}, api2go.NewHTTPError(errors.New("Invalid instance given"), "JSON does not match required model for User", http.StatusBadRequest)
	}

	// Check if the user already exists
	exists, obj, err := s.UserStorage.Exists(obj)

	if err != nil && err != rethink.ErrEmptyResult {
		// Log the error and return an HTTP error
		log.Error(err)
		return &Response{}, api2go.NewHTTPError(err, err.Error(), http.StatusInternalServerError)
	} else if exists {
		// Just return that object, since it already exists
		return &Response{Res: obj, Code: http.StatusOK}, err
	} else {
		// It doesn't already exist, so lets create create the user
		id, err := s.UserStorage.Insert(user)
		if err != nil {
			// Log the error and return an HTTP error
			log.Error(err)
			return &Response{}, api2go.NewHTTPError(err, err.Error(), http.StatusInternalServerError)
		}
		user.ID = id

		return &Response{Res: user, Code: http.StatusCreated}, nil
	}
}

// Delete implements deletion of resources, satisfying api2go.DataSource interface
func (s UserResource) Delete(id string, r api2go.Request) (api2go.Responder, error) {
	// Check if there is even a user with that ID
	err := s.UserStorage.Delete(id)
	// Either way there should be no content, so return that & err, which will be nil if the record was properly deleted
	return &Response{Code: http.StatusNoContent}, err
}

// Update implements the updating of a resource, satisfying api2go.DataSource interface
func (s UserResource) Update(obj interface{}, r api2go.Request) (api2go.Responder, error) {
	return &Response{Code: http.StatusOK}, nil
}
