package main

import (
	"github.com/DataDog/dd-trace-go/tracer"
	"fmt"
	"github.com/julienschmidt/httprouter"
	"database/sql"
	_ "github.com/lib/pq"
	"log"
	"os/exec"
	"net/http"
	"bytes"
	"strings"
	"encoding/json"
)

const (
	DB_USER = "datadog"
	DB_PASSWORD = "SeIamPUecN3FfVjzdbHmvZNl"
	DB_NAME = "dd_app"
)

type VisitorInfo struct {
	Id int
	Ip string
}

func PostgresStatus(w http.ResponseWriter, r *http.Request, _ httprouter.Params) {
	w.Header().Set("Content-Type", "text/html; charset=utf-8");
	w.Header().Set("Access-Control-Allow-Origin", "*");

	cmd := exec.Command("/usr/bin/datadog-agent", "check", "postgres");
	var out bytes.Buffer;
	cmd.Stdout = &out;
	err := cmd.Run();

	if err != nil {
	    log.Fatal(err);
	}

	fmt.Fprintf(w, "%s\n", strings.Join(strings.Split(out.String(), "\n"), "<br>"));
}

func LogVisitor(w http.ResponseWriter, r *http.Request, _ httprouter.Params) {
	span := tracer.NewRootSpan("web.request", "datadog_demo", "log_visitor");
	defer span.Finish();

	w.Header().Set("Content-Type", "application/json; charset=utf-8");
	w.Header().Set("Access-Control-Allow-Origin", "*");

	dbinfo := fmt.Sprintf("user=%s password=%s dbname=%s sslmode=disable",
	            DB_USER, DB_PASSWORD, DB_NAME);
	db, err := sql.Open("postgres", dbinfo);
	defer db.Close();

	if err != nil {
		panic(err);
	}

	err = db.Ping();

	if err != nil {
		panic(err);
	}

	sqlStatement := `
	INSERT INTO visitors (ip)
	VALUES ($1)`

	_, err = db.Exec(sqlStatement, r.RemoteAddr);

	if err != nil {
		panic(err);
	}

	queryStatement := `
	SELECT a.id, a.ip
	FROM visitors a
	INNER JOIN (
	    SELECT MAX(id) as id
		FROM visitors
	    ) b ON a.id = b.id
	`

	var maxId int;
	var ip string;

	err = db.QueryRow(queryStatement).Scan(&maxId, &ip);


	if err != nil {
		panic(err);
	}

	info := VisitorInfo { maxId, ip };
	obj, err := json.Marshal(info);

	if err != nil {
		panic(err);
	}

	w.Write(obj);

	span.SetMeta("ip", ip);
}

func main() {
	router := httprouter.New();
	router.GET("/postgres_check", PostgresStatus);
	router.GET("/log_visitor", LogVisitor);

	log.Fatal(http.ListenAndServe(":55555", router))
}
