package driver

import (
	"errors"
	"regexp"

	"github.com/cactusdev/cactusapi/util"

	rethink "gopkg.in/dancannon/gorethink.v2"
)

var log = util.GetLogger()
var emptyMap map[string]interface{}

// Storage stores the information required for a DB query
type Storage struct {
	DB        string
	Address   string
	Table     string
	Session   *rethink.Session
	Secondary string
}

// Initialize the RethinkDB session
func Initialize(address string, db string, table string, secondary string) (*Storage, error) {
	session, err := rethink.Connect(rethink.ConnectOpts{
		Address:  address,
		Database: db,
	})
	if err != nil {
		log.Error(err)
	}

	storage := Storage{
		DB:        db,
		Address:   address,
		Table:     table,
		Session:   session,
		Secondary: secondary,
	}

	return &storage, err
}

func getUUIDValidator(text string) bool {
	r := regexp.MustCompile("^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[8|9|aA|bB][a-f0-9]{3}-[a-f0-9]{12}$")
	return r.MatchString(text)
}

// Exists checks if a certain record already exists based on the map given
func (s Storage) Exists(compare interface{}) (bool, map[string]interface{}, error) {
	res, err := rethink.Table(s.Table).Filter(compare).Run(s.Session)
	defer res.Close()

	if err != nil {
		log.Error(err)
		return false, nil, err
	}

	response := make(map[string]interface{})
	err = res.One(&response)

	if err == rethink.ErrEmptyResult {
		log.Error(err)
		return false, nil, nil
	} else if err != nil {
		log.Error(err)
		return false, nil, err
	}

	return len(response) > 0, response, err
}

// GetOne Retrieve a single record from the table supplied, based on an ID
func (s Storage) GetOne(id string) (map[string]interface{}, error) {

	var res *rethink.Cursor
	var err error

	if getUUIDValidator(id) {
		res, err = rethink.Table(s.Table).Get(id).Run(s.Session)
	} else {
		res, err = rethink.Table(s.Table).Filter(rethink.Row.Field(s.Secondary).Eq(id)).Run(s.Session)
	}

	defer res.Close()
	if err != nil {
		log.Error(err)
	}

	response := make(map[string]interface{})

	err = res.One(&response)
	if err != nil {
		log.Error(err)
	}

	return response, err
}

// GetAll Retrieve all records from the table supplied
func (s Storage) GetAll() ([]map[string]interface{}, error) {
	res, err := rethink.Table(s.Table).Run(s.Session)
	defer res.Close()
	if err != nil {
		log.Error(err)
	}

	var response []map[string]interface{}

	err = res.All(&response)
	if err != nil {
		log.Error(err)
	}

	if err == rethink.ErrEmptyResult {
		return response, nil
	}

	return response, err
}

// GetMultiple Retrieve multiple records from the table supplied
func (s Storage) GetMultiple(limit int) ([]map[string]interface{}, error) {
	res, err := rethink.Table(s.Table).Limit(limit).Run(s.Session)
	defer res.Close()
	if err != nil {
		log.Error(err)
	}

	var response []map[string]interface{}

	err = res.All(&response)
	if err != nil {
		log.Error(err)
	}

	if err == rethink.ErrEmptyResult {
		return response, nil
	}

	return response, err
}

// Insert inserts new data into the database
func (s Storage) Insert(obj interface{}) (string, error) {
	result, err := rethink.Table(s.Table).Insert(obj).RunWrite(s.Session)
	if err != nil {
		log.Error(err)
		return "", err
	}

	return result.GeneratedKeys[0], nil
}

// Delete removes a record from the database based on ID
func (s Storage) Delete(id string) error {
	response, err := s.GetOne(id)
	if len(response) != 0 {
		_, err = rethink.Table(s.Table).Filter(response).Delete().Run(s.Session)
		if err != nil {
			log.Error(err)
			return err
		}
	}

	return nil
}

// Update allows editing of records
// FIXME - Make this work in regards to actually editing a resource
func (s Storage) Update(obj interface{}, id string) ([]map[string]interface{}, error) {
	log.Debug(id)
	res, err := s.GetOne(id)
	if err != nil {
		log.Error(err)
		return nil, err
	}

	log.Debug(res)
	log.Debug(obj)

	if len(res) != 0 {
		resource, err := rethink.Table(s.Table).Get(res["id"]).Run(s.Session)
		_, err = rethink.Table(s.Table).Get(res["id"]).Update(obj).RunWrite(s.Session)
		if err != nil {
			log.Error(err)
			return nil, err
		}
	} else {
		return nil, errors.New("Requested endpoint does not exist")
	}

	var response []map[string]interface{}

	res, err = s.GetOne(id)
	if err != nil && err != rethink.ErrEmptyResult {
		log.Error(err)
		return nil, err
	} else if err == rethink.ErrEmptyResult {
		response = append(response, res)
		return response, nil
	}

	return response, nil
}
