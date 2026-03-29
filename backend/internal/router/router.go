package router

import (
	"net/http"
	"wordlehunter/internal/handlers/status"
)

// Creates a new router
func NewRouter() *http.ServeMux {
	r := http.NewServeMux()

	// !!! Add API routes here
	status.AddRoutes(r)

	return r
}

// Creates a new router wrapped in logging middleware
//
// See [loggingMiddleware]
func NewLoggingRouter() http.Handler {
	return loggingMiddleware(NewRouter())
}
