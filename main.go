package main

import (
	"net/http"

	"github.com/go-chi/chi"
	"gopkg.in/DataDog/dd-trace-go.v1/ddtrace/tracer"
)

func main() {
	tracer.Start(tracer.WithServiceName("My Service"))
	defer tracer.Stop()

	r := chi.NewRouter()

	r.Get("/", func(w http.ResponseWriter, r *http.Request) {
		span := tracer.StartSpan("web.request", tracer.ResourceName("/"))
		defer span.Finish()
		span.SetTag("http.url", r.URL.Path)
		w.Write([]byte("Entrypoint to the Aplication"))
	})
	r.Get("/api/apm", func(w http.ResponseWriter, r *http.Request) {
		span := tracer.StartSpan("web.request", tracer.ResourceName("/api/apm"))
		defer span.Finish()
		span.SetTag("http.url", r.URL.Path)
		w.Write([]byte("Getting APM Started"))
	})
	r.Get("/api/trace", func(w http.ResponseWriter, r *http.Request) {
		span := tracer.StartSpan("web.request", tracer.ResourceName("/api/trace"))
		defer span.Finish()
		span.SetTag("http.url", r.URL.Path)
		w.Write([]byte("Posting Traces"))
	})

	http.ListenAndServe(":5050", r)
}
