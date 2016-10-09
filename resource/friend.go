package resource

import (
	"encoding/json"
	"errors"
	"net/http"

	"github.com/cactusdev/cactusapi/driver"
	"github.com/cactusdev/cactusapi/model"
	"github.com/cactusdev/sepal/util"
	"github.com/manyminds/api2go"
)

// FriendResource keeps track of the information required for accessing the user information
type FriendResource struct {
	FriendStorage *driver.Storage
}

// FindAll find all values in the database for the friends
func (s FriendResource) FindAll(r api2go.Request) (api2go.Responder, error) {
	var result []model.Friend

	friends, err := s.FriendStorage.GetAll()
	if err != nil {
		util.GetLogger().Error(err)
	}

	for _, friend := range friends {
		marshalled, _ := json.Marshal(friend)
		appended := model.Friend{}
		err = json.Unmarshal(marshalled, &appended)
		if err != nil {
			util.GetLogger().Error(err)
		}

		result = append(result, appended)
	}

	return &Response{Res: result}, nil
}

// GetOne returns a single friend from the database
func (s FriendResource) GetOne(id string) (api2go.Responder, error) {
	friend, err := s.FriendStorage.GetOne(id)
	if err != nil {
		util.GetLogger().Error(err)
		return &Response{}, api2go.NewHTTPError(err, err.Error(), http.StatusNotFound)
	}

	marshalled, _ := json.Marshal(friend)
	result := model.Friend{}
	err = json.Unmarshal(marshalled, &result)
	if err != nil {
		util.GetLogger().Error(err)
	}

	return &Response{Res: result}, nil
}

// FindOne returns a single user from the database based on ID
func (s FriendResource) FindOne(id string, r api2go.Request) (api2go.Responder, error) {
	quote, err := s.FriendStorage.GetOne(id)
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
func (s FriendResource) Create(obj interface{}, r api2go.Request) (api2go.Responder, error) {
	quote, ok := obj.(model.Quote)
	if !ok {
		return &Response{}, api2go.NewHTTPError(errors.New("Invalid instance given"), "Invalid instance given", http.StatusBadRequest)
	}

	id, err := s.FriendStorage.Insert(quote)
	if err != nil {
		util.GetLogger().Error(err)
		return &Response{}, api2go.NewHTTPError(err, err.Error(), http.StatusInternalServerError)
	}
	quote.ID = id
	return &Response{Res: quote, Code: http.StatusCreated}, nil
}

// Delete implements deletion of resources, satisfying api2go.DataSource interface
func (s FriendResource) Delete(id string, r api2go.Request) (api2go.Responder, error) {
	err := s.FriendStorage.Delete(id)
	return &Response{Code: http.StatusNoContent}, err
}

// Update implements the updating of a resource, satisfying api2go.DataSource interface
func (s FriendResource) Update(obj interface{}, r api2go.Request) (api2go.Responder, error) {
	return &Response{Code: http.StatusOK}, nil
}
