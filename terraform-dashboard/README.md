# Create a Dashboard with Terraform 

For this I found it easiest to first explore and build a dashboard in the DataDog web app.  Afterwards I took the settings and built this automation.  

Terraform documentation for Datadog Dashboards are here: 
https://www.terraform.io/docs/providers/datadog/r/dashboard.html

## Apply your dashboard

```
# Set your keys as variables rather than in code 
export DATADOG_API_KEY="<your_api_key>"
export DATADOG_APP_KEY="<your_app_key>"

# Init / Apply the TF automation
terraform init
terraform plan
terraform apply
```


