variable "region" {
  description = "Region to use"
  default = "eu-east-1"
}
variable "subnet1" {
  description = "First subnet for EKS Cluster"
  default = "null"
}

variable "subnet2" {
  description = "Second subnet for EKS Cluster"
  default = "null"
}

variable "cluster_name" {
  default = "example"
  type    = "string"
}

variable "instance_type" {
  description = "Instance type to use"
  default = "t3.small"
}