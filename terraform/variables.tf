/* Variables */

variable "environment" {
  type = "string"
  default = "demo"
}

variable "region" {
  type = "string"
  default = "us-east-2"
}

variable "image_id" {
  type = "string"
  default = "ami-6693b703"
}

variable "instance_type" {
  type = "string"
  default = "t2.small"
}

variable "vpc_id" {
  type = "string"
  default = "vpc-6acb3703"
}

variable "key_name" {
  type = "string"
  default = "areyouthekeymaster"
}

variable "datadog_api_key" {
  type = "string"
  default = "SECRET_API_KEY_GOES_HERE"
}

variable "datadog_app_key" {
  type = "string"
  default = "SECRET_APP_KEY_GOES_HERE"
}
