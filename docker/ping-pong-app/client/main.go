package main

import (
	"context"
	"log"
	"math/rand"
	"strconv"
	"time"

	pb "github.com/abruneau/hiring-engineers/docker/client/proto"
	"github.com/ilyakaznacheev/cleanenv"
	"google.golang.org/grpc"
)

// Config load config from file or environment variables
type Config struct {
	Address   string `env:"ADDRESS" env-default:"localhost:50051"`
	NBRequest int    `env:"NB_REQUEST" env-default:"10"`
}

var (
	cfg Config
)

func init() {
	err := cleanenv.ReadEnv(&cfg)
	if err != nil {
		help, _ := cleanenv.GetDescription(&cfg, nil)
		log.Println(help)
		log.Fatalf("failed to parse config: %v", err)
	}
}

func main() {

	nb := rand.New(rand.NewSource(99))

	// Set up a connection to the server.
	conn, err := grpc.Dial(cfg.Address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	log.Println("Connected to server")
	defer conn.Close()

	c := pb.NewPingPongClient(conn)

	ctx := context.Background()

	log.Printf("Starting loop with %v requests", cfg.NBRequest)
	for i := 0; i < cfg.NBRequest/2; i++ {
		log.Printf("Round %v", i)
		r, err := c.Ping(ctx, &pb.Request{Message: strconv.Itoa(i)})
		if err != nil {
			log.Fatalf("could not ping: %v", err)
		}

		log.Printf("Received: %s", r.GetMessage())

		time.Sleep(time.Duration(nb.Intn(1000)) * time.Millisecond)

		r, err = c.Pong(ctx, &pb.Request{Message: strconv.Itoa(i)})
		if err != nil {
			log.Fatalf("could not ping: %v", err)
		}
		time.Sleep(time.Duration(nb.Intn(1000)) * time.Millisecond)
		log.Printf("Received: %s", r.GetMessage())
	}
}
