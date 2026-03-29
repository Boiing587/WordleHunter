package main

import (
	"log"
	"net/http"
	"wordlehunter/internal/router"
	"wordlehunter/internal/utils"
)

func main() {
	r := router.NewLoggingRouter()
	log.Printf("Starting API %s on port %s", utils.API_VERSION, utils.PORT)
	log.Fatal(http.ListenAndServe(":"+utils.PORT, r))

}
