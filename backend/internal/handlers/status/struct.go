package status

import "time"

type StatusHandler struct {
	StartupTime time.Time
}

type StatusResponse struct {
	Version string `json:"version"`
	Uptime  string `json:"uptime"`
}
