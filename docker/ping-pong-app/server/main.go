package main

import (
	"context"
	"log"
	"net"

	pb "github.com/abruneau/hiring-engineers/docker/server/proto"
	"github.com/ilyakaznacheev/cleanenv"
	"google.golang.org/grpc"
	grpctrace "gopkg.in/DataDog/dd-trace-go.v1/contrib/google.golang.org/grpc"
	"gopkg.in/DataDog/dd-trace-go.v1/ddtrace/tracer"
)

// Config load config from file or environment variables
type Config struct {
	Port string `env:"PORT" env-default:"50051"`
}

type server struct{}

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

func (s *server) Ping(ctx context.Context, in *pb.Request) (*pb.Response, error) {
	log.Printf("Received Ping: %v", in.GetMessage())
	return &pb.Response{Message: "Pong " + in.GetMessage()}, nil
}

func (s *server) Pong(ctx context.Context, in *pb.Request) (*pb.Response, error) {
	log.Printf("Received Pong: %v", in.GetMessage())
	return &pb.Response{Message: "Ping " + in.GetMessage()}, nil
}

func main() {
	tracer.Start()
	defer tracer.Stop()

	lis, err := net.Listen("tcp", ":"+cfg.Port)

	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	si := grpctrace.StreamServerInterceptor(grpctrace.WithServiceName("grpc-pingpong-server"))
	ui := grpctrace.UnaryServerInterceptor(grpctrace.WithServiceName("grpc-pingpong-server"))
	s := grpc.NewServer(grpc.StreamInterceptor(si), grpc.UnaryInterceptor(ui))

	pb.RegisterPingPongServer(s, &server{})
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
