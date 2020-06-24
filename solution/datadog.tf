# Extract our credentials from the GOOGLE_CREDENTIALS environment variable
data "external" "credentials" {
  program = ["bash", "./assets/import_creds.sh"]
}

# Create a new Datadog - Google Cloud Platform integration
resource "datadog_integration_gcp" "awesome_gcp_project_integration" {
  project_id     = data.external.credentials.result.project_id
  private_key_id = data.external.credentials.result.private_key_id
  private_key    = data.external.credentials.result.private_key
  client_email   = data.external.credentials.result.client_email
  client_id      = data.external.credentials.result.client_id
}