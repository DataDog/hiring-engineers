package main

import (
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"os/signal"
	"syscall"

	"github.com/gin-gonic/gin"
	"github.com/johnrichter/datadog-se/api"
	"github.com/johnrichter/datadog-se/twitter"
	"github.com/lib/pq"
	_ "github.com/lib/pq"
	sqltrace "gopkg.in/DataDog/dd-trace-go.v1/contrib/database/sql"
	gintrace "gopkg.in/DataDog/dd-trace-go.v1/contrib/gin-gonic/gin"
	"gopkg.in/DataDog/dd-trace-go.v1/ddtrace/tracer"
	"gopkg.in/DataDog/dd-trace-go.v1/profiler"
)

const Version string = "1.0.0"

func main() {
	tracer.Start(
		tracer.WithEnv("development:local"),
		tracer.WithService("twitter_collector"),
		tracer.WithServiceVersion(Version),
		tracer.WithAgentAddr(net.JoinHostPort("172.16.1.12", "8126")),
		tracer.WithAnalytics(true),
	)
	sqltrace.Register("postgres", &pq.Driver{})
	defer tracer.Stop()

	err := profiler.Start(
		profiler.WithAPIKey(os.Getenv("DD_API_KEY")),
		profiler.WithService("twitter_collector"),
		profiler.WithEnv("development:local"),
		profiler.WithTags(fmt.Sprintf("version:%s", Version)),
	)
	if err != nil {
		log.Fatalf(err.Error())
	}
	defer profiler.Stop()

	consumerKey := flag.String("consumerKey", "", "Twitter Consumer Key")
	consumerSecret := flag.String("consumerSecret", "", "Twitter Consumer Secret")
	accessToken := flag.String("accessToken", "", "Twitter Access Token")
	accessSecret := flag.String("accessSecret", "", "Twitter Access Secret")
	flag.Parse()

	if *consumerKey == "" || *consumerSecret == "" || *accessToken == "" || *accessSecret == "" {
		log.Fatalln("Missing Twitter credentials")
	}

	db, err := sqltrace.Open("postgres", "host=172.16.1.11 user=vagrant password=vagrant dbname=postgres")
	if err != nil {
		log.Fatalf(err.Error())
	}

	// Start our Twitter Stream
	span := tracer.StartSpan(
		"start-twitter-streaming-client",
		tracer.SpanType("twitter-stream-initialization"),
		tracer.ResourceName("TwitterStreamingClient"),
	)
	client := twitter.NewTwitterStreamingClient(db, *consumerKey, *consumerSecret, *accessToken, *accessSecret)
	err = client.Start()
	if err != nil {
		log.Fatalf(err.Error())
	}
	span.Finish(tracer.WithError(err))

	// Configure the API
	apiHandler := api.NewAPI(db)
	gin.SetMode(gin.ReleaseMode)
	r := gin.New()
	r.Use(gintrace.Middleware("twitter_collector"))
	r.GET("/tweets/last/5", apiHandler.HandleLastFiveTweets)
	r.Run()

	// Wait to exit until we're told to
	ch := make(chan os.Signal)
	signal.Notify(ch, syscall.SIGINT, syscall.SIGTERM)
	log.Println(<-ch)
	client.Stop()
}
