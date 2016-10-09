package util

// IsInSlice checks if a certain key exists in a slice of strings
func IsInSlice(key string, slice []string) bool {
	for _, value := range slice {
		if value == key {
			return true
		}
	}
	// Didn't find it in the key in the slice
	return false
}
