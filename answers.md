Your answers to the questions go here.

Datadog username: pantsonsteven

##Level 1

1. Current metrics being reported.

2. Bonus Question: The agent is a small bit of code that is run on my hosts. It collects various types of data and sends it to DataDog where I can do wondrous things with it.

3. Submitted: 
curl  -X POST -H "Content-type: application/json" \
> -d '{
>       "title": "Did you hear the news today?",
>       "text": "Oh boy!",
>       "priority": "normal",
>       "tags": ["environment:test"],
>       "alert_type": "info"
>   }' \
> 'https://app.datadoghq.com/api/v1/events?api_key=eaa897b3f1f740b518102ac6de2d1bff'

Received: 
{
    "status": "ok", 
    "event": {
        "priority": "normal", 
        "date_happened": 1407874364, 
        "handle": null, 
        "title": "Did you hear the news today?", 
        "url": "https://app.datadoghq.com/event/jump_to?event_id=2409401106494613851", 
        "text": "Oh boy!", 
        "tags": [
            "environment:test"
        ], 
        "related_event_id": null, 
        "id": 2409401106494613851
    }
}

4. Subject line of alert email: [Metric Alert] Triggered: Free Disk Space below 10.24 GB

##Level 2

1. Load test graph: https://app.datadoghq.com/event/event?id=2409547238278287361

