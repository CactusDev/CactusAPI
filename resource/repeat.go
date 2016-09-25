package resource

import (
	"encoding/json"
	"errors"
	"net/http"

	"github.com/CactusDev/CactusAPI/driver"
	"github.com/CactusDev/CactusAPI/model"
	"github.com/CactusDev/CactusAPI/util"
	"github.com/manyminds/api2go"
)

var log = util.GetLogger()

// RepeatResource keeps track of the information required for accessing the Repeat information
type RepeatResource struct {
	RepeatStorage *driver.Storage
}

// FindAll returns all values in the database for the RepeatResource, satisfying the api2go source interface
func (s RepeatResource) FindAll(r api2go.Request) (api2go.Responder, error) {

	var result []model.Repeat

	repeats, err := s.RepeatStorage.GetAll()
	if err != nil {
		log.Error(err)
	}

	for _, repeat := range repeats {
		marshalled, _ := json.Marshal(repeat)
		appended := model.Repeat{}
		err = json.Unmarshal(marshalled, &appended)
		if err != nil {
			// TODO: Add stuff to handle errors
			log.Error(err)
		}

		result = append(result, appended)
	}

	return &Response{Res: result}, nil
}

// FindOne returns a single Repeat from the database based on ID
func (s RepeatResource) FindOne(ID string, r api2go.Request) (api2go.Responder, error) {
	Repeat, err := s.RepeatStorage.GetOne(ID)
	if err != nil {
		log.Error(err)
		return &Response{}, api2go.NewHTTPError(err, err.Error(), http.StatusNotFound)
	}

	marshalled, _ := json.Marshal(Repeat)
	result := model.Repeat{}
	err = json.Unmarshal(marshalled, &result)
	if err != nil {
		// TODO: Add stuff to handle errors
		log.Error(err)
	}

	return &Response{Res: result}, nil
}

// GetOne returns a single Repeat from the database based on ID
func (s RepeatResource) GetOne(ID string) (api2go.Responder, error) {
	Repeat, err := s.RepeatStorage.GetOne(ID)
	if err != nil {
		log.Error(err)
		return &Response{}, api2go.NewHTTPError(err, err.Error(), http.StatusNotFound)
	}

	marshalled, _ := json.Marshal(Repeat)
	result := model.Repeat{}
	err = json.Unmarshal(marshalled, &result)
	if err != nil {
		// TODO: Add stuff to handle errors
		log.Error(err)
	}

	return &Response{Res: result}, nil
}

// Create method satisfies the api2go.DataSource interface
func (s RepeatResource) Create(obj interface{}, r api2go.Request) (api2go.Responder, error) {
	// Check that the object supplied has the proper info to fill a model.Repeat
	Repeat, ok := obj.(model.Repeat)
	if !ok {
		return &Response{}, api2go.NewHTTPError(errors.New("Invalid instance given"), "Invalid instance given", http.StatusBadRequest)
	}

	id, err := s.RepeatStorage.Insert(Repeat)
	if err != nil {
		// Log the error and return an HTTP error
		log.Error(err)
		return &Response{}, api2go.NewHTTPError(err, err.Error(), http.StatusInternalServerError)
	}
	Repeat.ID = id

	return &Response{Res: Repeat, Code: http.StatusCreated}, nil
}

// Delete implements deletion of resources, satisfying api2go.DataSource interface
func (s RepeatResource) Delete(id string, r api2go.Request) (api2go.Responder, error) {
	// Check if there is even a Repeat with that ID
	err := s.RepeatStorage.Delete(id)
	// Either way there should be no content, so return that & err, which will be nil if the record was properly deleted
	return &Response{Code: http.StatusNoContent}, err
}

// Update implements the updating of a resource, satisfying api2go.DataSource interface
func (s RepeatResource) Update(obj interface{}, r api2go.Request) (api2go.Responder, error) {
	return &Response{Code: http.StatusOK}, nil
}
