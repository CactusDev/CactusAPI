package util

import "github.com/Sirupsen/logrus"

var log = logrus.New()

// InitLogger Initialize a new logger and return said logger.
func InitLogger(debug bool) *logrus.Logger {
	log.Formatter = new(logrus.TextFormatter)

	if debug {
		log.Level = logrus.DebugLevel
	} else {
		log.Level = logrus.InfoLevel
	}
	log.WithFields(logrus.Fields{"debug": debug}).Info("Logger initialized.")

	return log
}

// GetLogger Return a reference of the logger
func GetLogger() *logrus.Logger {
	return log
}
