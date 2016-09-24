package util

import "io/ioutil"

// CopyFile copy a file from a src to a destination.
func CopyFile(src, dst string) (err error) {
	data, err := ioutil.ReadFile(src)
	if err != nil {
		return err
	}
	err = ioutil.WriteFile(dst, data, 0644)
	if err != nil {
		return err
	}
	return nil
}
