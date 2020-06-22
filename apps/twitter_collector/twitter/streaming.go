package twitter

import (
	"context"
	"database/sql"
	"fmt"
	"log"

	twitterapi "github.com/dghubble/go-twitter/twitter"
	"github.com/dghubble/oauth1"
	"gopkg.in/DataDog/dd-trace-go.v1/ddtrace/tracer"
)

type TwitterStreamingClient struct {
	db      *sql.DB
	client  *twitterapi.Client
	streams []*twitterapi.Stream
}

func NewTwitterStreamingClient(db *sql.DB, consumerKey, consumerSecret, accessToken, accessSecret string) *TwitterStreamingClient {
	oauthConfig := oauth1.NewConfig(consumerKey, consumerSecret)
	oauthToken := oauth1.NewToken(accessToken, accessSecret)
	oauthClient := oauthConfig.Client(oauth1.NoContext, oauthToken)

	twitterClient := twitterapi.NewClient(oauthClient)

	return &TwitterStreamingClient{
		db:      db,
		client:  twitterClient,
		streams: []*twitterapi.Stream{},
	}
}

func (c *TwitterStreamingClient) Start() error {
	filter := twitterapi.StreamFilterParams{
		StallWarnings: twitterapi.Bool(true),
		Track:         []string{"#love"},
	}
	stream, err := c.client.Streams.Filter(&filter)
	if err != nil {
		return err
	}
	c.streams = append(c.streams, stream)

	fmt.Println("Listening for Tweets about #love...")
	demux := twitterapi.NewSwitchDemux()
	demux.Tweet = c.handleTweet
	go demux.HandleChan(stream.Messages)
	return nil
}

func (c *TwitterStreamingClient) Stop() {
	for _, stream := range c.streams {
		stream.Stop()
	}
}

func (c *TwitterStreamingClient) handleTweet(tweet *twitterapi.Tweet) {
	span, ctx := tracer.StartSpanFromContext(
		context.Background(),
		"save-tweet-to-database",
		tracer.SpanType("database-insert"),
		tracer.ResourceName("handleTweet"),
	)
	log.Printf(
		"Handling tweet %s dd.trace_id=%d dd.span_id=%d",
		tweet.IDStr,
		span.Context().TraceID(),
		span.Context().SpanID(),
	)
	_, err := c.db.ExecContext(
		ctx,
		"INSERT INTO tweets(id, userid, username, created_at, text, full_text) values($1, $2, $3, $4, $5, $6)",
		tweet.ID, tweet.User.IDStr, tweet.User.Name, tweet.CreatedAt, tweet.Text, tweet.FullText,
	)
	if err != nil {
		log.Println(err.Error())
	}
	span.Finish(tracer.WithError(err))
}
