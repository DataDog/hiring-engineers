# Datadog tech exercise variables file

variable "project_id" {
  description = "Your Google Cloud Platform project id. You can find this at the top of the page on the Google Cloud Console. You must have the Compute Engine API enabled for your project in order for this Terraform code to function."
}

variable "region" {
  description = "The GCP region where you want to build infrastructure."
  default     = "us-central1"
}

variable "zone" {
  description = "The GCP zone where you want to build infrastructure."
  default     = "us-central1-a"
}

variable "dogname" {
  description = "Name for your VM instance"
  default     = "astro"
}

variable "machine_type" {
  description = "GCP machine size. Examples: g1-small, f1-micro"
  default     = "g1-small"
}

variable "subnet_prefix" {
  description = "The address prefix to use for the subnet."
  default     = "10.0.10.0/24"
}

variable "dd_api_key" {
  description = "Your Datadog API key. We strongly recommend storing this as environment variable DD_API_KEY."
}