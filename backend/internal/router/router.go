package router

import (
	"net/http"
)

// Creates a new router
func NewRouter() *http.ServeMux {
	r := http.NewServeMux()

	// !!! Add API routes here

	return r
}

// Creates a new router wrapped in logging middleware
//
// See [loggingMiddleware]
func NewLoggingRouter() http.Handler {
	return loggingMiddleware(NewRouter())
}
