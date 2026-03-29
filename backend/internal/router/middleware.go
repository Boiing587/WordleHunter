package router

import (
	"log"
	"net/http"
)

// Wraps an HTTP handler in logging middleware, logging the URL and method
// of all requests sent to the handler.
//
// Adapted from
// https://dev.to/neelp03/adding-logging-and-error-handling-middleware-to-your-go-api-2f33
func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Printf("Received request: %s %s\n", r.Method, r.URL.Path)
		next.ServeHTTP(w, r)
	})
}
