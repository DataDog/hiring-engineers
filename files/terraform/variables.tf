variable "aws_region" {
  type        = "string"
  description = "The AWS region to create things in."
}

variable "instance_type" {
  type        = "string"
  description = "AWS instance type"
}

variable "vpc_security_group_ids" {
  type        = "string"
  description = "Target VPC security group where resources will be defined within."
}