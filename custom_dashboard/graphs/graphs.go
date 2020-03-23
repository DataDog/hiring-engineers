package graphs

import datadog "github.com/zorkian/go-datadog-api"

func customeMetricGraph() datadog.Graph {
	gd := &datadog.GraphDefinition{}
	gd.SetViz("timeseries")

	r := gd.Requests
	gd.Requests = append(r, datadog.GraphDefinitionRequest{
		Query:   datadog.String("avg:my_metric{*}"),
		Stacked: datadog.Bool(false),
	})

	return datadog.Graph{
		Title:      datadog.String("Custom Metric"),
		Definition: gd,
	}
}

func databaseAnomalyGraph() datadog.Graph {
	gd := &datadog.GraphDefinition{}
	gd.SetViz("timeseries")

	r := gd.Requests
	gd.Requests = append(r, datadog.GraphDefinitionRequest{
		Query:   datadog.String("anomalies(avg:mongodb.opcounters.queryps{*}, 'basic', 2, direction='above', alert_window='last_15m', interval=60, count_default_zero='true')"),
		Stacked: datadog.Bool(false),
	})

	return datadog.Graph{
		Title:      datadog.String("Mongo Read requests per second"),
		Definition: gd,
	}
}

func customMetricRollup() datadog.Graph {
	gd := &datadog.GraphDefinition{}
	gd.SetViz("query_value")

	r := gd.Requests
	gd.Requests = append(r, datadog.GraphDefinitionRequest{
		Query:   datadog.String("avg:my_metric{*}.rollup(sum, 3600)"),
		Stacked: datadog.Bool(false),
	})

	return datadog.Graph{
		Title:      datadog.String("My Metric sum of all points in the past hour"),
		Definition: gd,
	}

}

// Create builds a list of Graph
func Create() []datadog.Graph {
	graphs := []datadog.Graph{}
	graphs = append(graphs, customeMetricGraph())
	graphs = append(graphs, databaseAnomalyGraph())
	graphs = append(graphs, customMetricRollup())

	return graphs
}
