package main
import (
    "fmt"
    "net/http"
)
func defaultHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello world!")
}
func main() {
    http.HandleFunc("/", defaultHandler)
    http.ListenAndServe(":8080", nil)
}