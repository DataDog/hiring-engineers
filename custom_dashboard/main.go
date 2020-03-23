package main

import (
	"log"

	"github.com/abruneau/hiring-engineers/graphs"
	"github.com/ilyakaznacheev/cleanenv"
	datadog "github.com/zorkian/go-datadog-api"
)

// Config load config from file or environment variables
type Config struct {
	APIKey         string `yaml:"api_key" env:"API_KEY"`
	ApplicationKey string `yaml:"application_key" env:"APP_KEY"`
}

var cfg Config
var client *datadog.Client

func init() {
	err := cleanenv.ReadConfig("config.yml", &cfg)
	if err != nil {
		help, _ := cleanenv.GetDescription(&cfg, nil)
		log.Println(help)
		log.Fatalf("failed to parse config: %v", err)
	}

	client = datadog.NewClient(cfg.APIKey, cfg.ApplicationKey)
}

func getCustomDashboard(createGraph func() []datadog.Graph, createVar func() []datadog.TemplateVariable) *datadog.Dashboard {
	return &datadog.Dashboard{
		Title:             datadog.String("My custom Dashboard"),
		Description:       datadog.String("Dashboard created with Datadog API"),
		TemplateVariables: createVar(),
		Graphs:            createGraph(),
		ReadOnly:          datadog.Bool(true),
	}
}

func createVar() []datadog.TemplateVariable {
	tvs := []datadog.TemplateVariable{}

	tvs = append(tvs, datadog.TemplateVariable{
		Name:    datadog.String("Custom Host"),
		Prefix:  datadog.String("host"),
		Default: datadog.String("docker-desktop"),
	})

	return tvs
}

func main() {
	_, err := client.CreateDashboard(getCustomDashboard(graphs.Create, createVar))
	if err != nil {
		log.Fatalf("Creating a dashboard failed: %s", err)
	}
}
