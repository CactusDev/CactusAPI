package resource

import (
	"encoding/json"
	"errors"
	"net/http"

	"github.com/cactusdev/cactusapi/driver"
	"github.com/cactusdev/cactusapi/model"
	"github.com/cactusdev/cactusapi/util"
	"github.com/manyminds/api2go"
)

var log = util.GetLogger()

// PermitResource keeps track of the information required for accessing the permit information
type PermitResource struct {
	PermitStorage *driver.Storage
}

// FindAll returns all values in the database for the PermitResource, satisfying the api2go source interface
func (s PermitResource) FindAll(r api2go.Request) (api2go.Responder, error) {

	var result []model.Permit

	permits, err := s.PermitStorage.GetAll()
	if err != nil {
		log.Error(err)
	}

	for _, permit := range permits {
		marshalled, _ := json.Marshal(permit)
		appended := model.Permit{}
		err = json.Unmarshal(marshalled, &appended)
		if err != nil {
			// TODO: Add stuff to handle errors
			log.Error(err)
		}

		result = append(result, appended)
	}

	return &Response{Res: result}, nil
}

// FindOne returns a single permit from the database based on ID
func (s PermitResource) FindOne(ID string, r api2go.Request) (api2go.Responder, error) {
	log.Debug(ID)
	permit, err := s.PermitStorage.GetOne(ID)
	if err != nil {
		log.Error(err)
		return &Response{}, api2go.NewHTTPError(err, err.Error(), http.StatusNotFound)
	}

	marshalled, _ := json.Marshal(permit)
	result := model.Permit{}
	err = json.Unmarshal(marshalled, &result)
	if err != nil {
		// TODO: Add stuff to handle errors
		log.Error(err)
	}

	return &Response{Res: result}, nil
}

// GetOne returns a single permit from the database based on ID
func (s PermitResource) GetOne(ID string) (api2go.Responder, error) {
	permit, err := s.PermitStorage.GetOne(ID)
	if err != nil {
		log.Error(err)
		return &Response{}, api2go.NewHTTPError(err, err.Error(), http.StatusNotFound)
	}

	marshalled, _ := json.Marshal(permit)
	result := model.Permit{}
	err = json.Unmarshal(marshalled, &result)
	if err != nil {
		// TODO: Add stuff to handle errors
		log.Error(err)
	}

	return &Response{Res: result}, nil
}

// Create method satisfies the api2go.DataSource interface
func (s PermitResource) Create(obj interface{}, r api2go.Request) (api2go.Responder, error) {
	// Check that the object supplied has the proper info to fill a model.Permit
	permit, ok := obj.(model.Permit)
	if !ok {
		return &Response{}, api2go.NewHTTPError(errors.New("Invalid instance given"), "Invalid instance given", http.StatusBadRequest)
	}

	id, err := s.PermitStorage.Insert(permit)
	if err != nil {
		// Log the error and return an HTTP error
		log.Error(err)
		return &Response{}, api2go.NewHTTPError(err, err.Error(), http.StatusInternalServerError)
	}
	permit.ID = id

	return &Response{Res: permit, Code: http.StatusCreated}, nil
}

// Delete implements deletion of resources, satisfying api2go.DataSource interface
func (s PermitResource) Delete(id string, r api2go.Request) (api2go.Responder, error) {
	// Check if there is even a permit with that ID
	err := s.PermitStorage.Delete(id)
	// Either way there should be no content, so return that & err, which will be nil if the record was properly deleted
	return &Response{Code: http.StatusNoContent}, err
}

// Update implements the updating of a resource, satisfying api2go.DataSource interface
func (s PermitResource) Update(obj interface{}, r api2go.Request) (api2go.Responder, error) {
	return &Response{Code: http.StatusOK}, nil
}
