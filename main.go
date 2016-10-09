package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"net/http"
	"os"
	"strconv"

	"github.com/Sirupsen/logrus"
	"github.com/cactusdev/cactusapi/driver"
	"github.com/cactusdev/cactusapi/model"
	"github.com/cactusdev/cactusapi/resource"
	"github.com/cactusdev/cactusapi/util"
	"github.com/julienschmidt/httprouter"
	"github.com/manyminds/api2go"

	rethink "gopkg.in/dancannon/gorethink.v2"
)

var log = util.InitLogger(true)

func main() {
	createDB := flag.Bool("create", false, "Create the required RethinkDB database and tables")

	flag.Parse()

	file, err := os.Open("config.json")
	if err != nil {
		log.Error("The config file does not exist.")
		log.Error("Creating...")

		err = util.CopyFile("config-template.json", "config.json")
		if err != nil {
			log.Error(err)
			log.Fatal("There was an error copying the config template.")
		}
		log.Info("Copy finished!")
		log.Info("Verify the options in there, and restart.")
		return
	}

	decoder := json.NewDecoder(file)
	conf := util.Config{}

	err = decoder.Decode(&conf)
	if err != nil {
		log.Fatal(err)
	}
	util.GlobalConfig = conf

	if *createDB {
		dbCreate()
		// Don't continue on to the rest of the program, just creating the DB
		return
	}

	handler, port := initializeAPI(&conf)
	http.ListenAndServe(fmt.Sprintf(":%d", port), handler)
}

func initializeAPI(conf *util.Config) (http.Handler, int) {
	port := 8000
	api := api2go.NewAPI("v1")

	userStorage, err := driver.Initialize(conf.Host+":"+conf.Port, conf.Database, "users", "userName")
	if err != nil {
		log.Fatal(err)
	}

	commandStorage, err := driver.Initialize(conf.Host+":"+conf.Port, conf.Database, "commands", "name")
	if err != nil {
		log.Fatal(err)
	}

	quoteStorage, err := driver.Initialize(conf.Host+":"+conf.Port, conf.Database, "quotes", "name")
	if err != nil {
		log.Fatal(err)
	}

	friendStorage, err := driver.Initialize(conf.Host+":"+conf.Port, conf.Database, "friends", "name")
	if err != nil {
		log.Fatal(err)
	}

	permitStorage, err := driver.Initialize(conf.Host+":"+conf.Port, conf.Database, "permits", "name")
	if err != nil {
		log.Fatal(err)
	}

	repeatStorage, err := driver.Initialize(conf.Host+":"+conf.Port, conf.Database, "repeats", "name")
	if err != nil {
		log.Fatal(err)
	}

	api.AddResource(model.User{}, resource.UserResource{UserStorage: userStorage})
	api.AddResource(model.Command{}, resource.CommandResource{CommandStorage: commandStorage})
	api.AddResource(model.Quote{}, resource.QuoteResource{QuoteStorage: quoteStorage})
	api.AddResource(model.Friend{}, resource.FriendResource{FriendStorage: friendStorage})
	api.AddResource(model.Permit{}, resource.PermitResource{PermitStorage: permitStorage})
	api.AddResource(model.Repeat{}, resource.RepeatResource{RepeatStorage: repeatStorage})

	log.Info("Listening on :" + strconv.Itoa(port))
	handler := api.Handler().(*httprouter.Router)

	return handler, port
}

func dbCreate() {
	log.Info("Connecting to RethinkDB server...")
	session, err := rethink.Connect(rethink.ConnectOpts{
		Address: util.GlobalConfig.Host,
	})
	if err != nil {
		log.Fatal("Errors occured during connection!")
		log.Fatal(err)
	}
	log.Info("Connection succeeded!")
	log.Info("Continuing on to DB creation...")

	// Check if the DB already exists
	res, err := rethink.DBList().Run(session)
	if err != nil {
		log.Fatalln(err)
	}
	var response []string
	res.All(&response)

	exists := util.IsInSlice(util.GlobalConfig.Database, response)
	if !exists {
		// Create the database, then the tables
		wres, err := rethink.DBCreate(util.GlobalConfig.Database).RunWrite(session)
		if err != nil {
			log.Fatalln(err)
		} else {
			log.WithFields(logrus.Fields{
				"database": util.GlobalConfig.Database,
				"info":     wres.TablesCreated,
			}).Info("Database created")
			session.Use(util.GlobalConfig.Database)
		}
	} else {
		session.Use(util.GlobalConfig.Database)
	}

	// Tables to be created
	tables := []string{
		"users",
		"commands",
		"quotes",
		"friends",
		"permits",
		"repeats",
	}

	for _, table := range tables {
		res, err := rethink.TableList().Run(session)
		if err != nil {
			log.Fatalln(err)
		}
		var response []string
		res.All(&response)

		// It's not in the slice, so create the table
		if !util.IsInSlice(table, response) {
			wres, err := rethink.TableCreate(table).RunWrite(session)
			if err != nil {
				log.Fatal(err)
			} else {
				log.WithFields(logrus.Fields{
					"table": table,
					"info":  wres.TablesCreated,
				}).Info("Table created")
			}
		} else {
			log.WithField("table", table).Info("Table already exists")
		}
	}

	log.Info("Successfully created database and tables!")
}
