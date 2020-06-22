package api

import (
	"database/sql"
	"log"

	"github.com/gin-gonic/gin"
)

type API struct {
	db *sql.DB
}

func NewAPI(db *sql.DB) *API {
	return &API{db: db}
}

func (a *API) HandleLastFiveTweets(ctx *gin.Context) {
	log.Println("Received request for last five tweets")
	rows, err := a.db.Query("SELECT text FROM tweets ORDER BY id DESC LIMIT 5")
	if err != nil {
		log.Println(err.Error())
		ctx.JSON(500, gin.H{"error": err.Error()})
		return
	}
	defer rows.Close()
	var tweetText string
	tweets := []string{}

	for rows.Next() {
		if err := rows.Scan(&tweetText); err != nil {
			ctx.JSON(500, gin.H{"error": err.Error()})
			return
		} else {
			tweets = append(tweets, tweetText)
		}
	}
	ctx.JSON(200, gin.H{"data": tweets})
}
