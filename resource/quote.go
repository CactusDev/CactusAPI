package resource

import (
	"encoding/json"
	"errors"
	"net/http"

	"github.com/CactusDev/CactusAPI/driver"
	"github.com/CactusDev/CactusAPI/model"
	"github.com/CactusDev/sepal/util"
	"github.com/manyminds/api2go"
)

// QuoteResource keeps track of the information required for accessing the user information
type QuoteResource struct {
	QuoteStorage *driver.Storage
}

// FindAll returns all values in the database for the QuoteResource, satisfying the api2go source interface
func (s QuoteResource) FindAll(r api2go.Request) (api2go.Responder, error) {
	var result []model.Quote

	quotes, err := s.QuoteStorage.GetAll()
	if err != nil {
		util.GetLogger().Error(err)
	}

	for _, quote := range quotes {
		marshalled, _ := json.Marshal(quote)
		appended := model.Quote{}
		err = json.Unmarshal(marshalled, &appended)
		if err != nil {
			util.GetLogger().Error(err)
		}

		result = append(result, appended)
	}

	return &Response{Res: result}, nil
}

// FindOne returns a single user from the database based on ID
func (s QuoteResource) FindOne(id string, r api2go.Request) (api2go.Responder, error) {
	quote, err := s.QuoteStorage.GetOne(id)
	if err != nil {
		util.GetLogger().Error(err)
		return &Response{}, api2go.NewHTTPError(err, err.Error(), http.StatusNotFound)
	}

	marshalled, _ := json.Marshal(quote)
	result := model.Quote{}
	err = json.Unmarshal(marshalled, &result)
	if err != nil {
		util.GetLogger().Error(err)
	}

	return &Response{Res: result}, nil
}

// GetOne returns a single user from the database based on ID
func (s QuoteResource) GetOne(id string) (api2go.Responder, error) {
	quote, err := s.QuoteStorage.GetOne(id)
	if err != nil {
		util.GetLogger().Error(err)
		return &Response{}, api2go.NewHTTPError(err, err.Error(), http.StatusNotFound)
	}

	marshalled, _ := json.Marshal(quote)
	result := model.Quote{}
	err = json.Unmarshal(marshalled, &result)
	if err != nil {
		util.GetLogger().Error(err)
	}

	return &Response{Res: result}, nil
}

// Create satisfies the api2go.DataSource interface
func (s QuoteResource) Create(obj interface{}, r api2go.Request) (api2go.Responder, error) {
	quote, ok := obj.(model.Quote)
	if !ok {
		return &Response{}, api2go.NewHTTPError(errors.New("Invalid instance given"), "Invalid instance given", http.StatusBadRequest)
	}

	id, err := s.QuoteStorage.Insert(quote)
	if err != nil {
		util.GetLogger().Error(err)
		return &Response{}, api2go.NewHTTPError(err, err.Error(), http.StatusInternalServerError)
	}
	quote.ID = id
	return &Response{Res: quote, Code: http.StatusCreated}, nil
}

// Delete implements deletion of resources, satisfying api2go.DataSource interface
func (s QuoteResource) Delete(id string, r api2go.Request) (api2go.Responder, error) {
	err := s.QuoteStorage.Delete(id)
	return &Response{Code: http.StatusNoContent}, err
}

// Update implements the updating of a resource, satisfying api2go.DataSource interface
func (s QuoteResource) Update(obj interface{}, r api2go.Request) (api2go.Responder, error) {
	return &Response{Code: http.StatusOK}, nil
}
