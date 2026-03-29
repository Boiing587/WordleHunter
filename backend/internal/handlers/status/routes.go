package status

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"
	"wordlehunter/internal/utils"
)

func (s StatusHandler) handler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	response := StatusResponse{
		Version: utils.API_VERSION,
		Uptime:  time.Since(s.StartupTime).Round(time.Second).String(),
	}

	json.NewEncoder(w).Encode(response)
}

func pingHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/plain")
	w.WriteHeader(http.StatusOK)

	fmt.Fprintln(w, "pong")
}

func AddRoutes(r *http.ServeMux) {
	r.HandleFunc(fmt.Sprintf("GET %s", STATUS_ENDPOINT), StatusHandler{StartupTime: time.Now()}.handler)
	r.HandleFunc(fmt.Sprintf("GET %s", PING_ENDPOINT), pingHandler)
}
