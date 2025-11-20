

variable "aws_region" {
  type        = string
  description = "AWS region for resources"
  default     = "eu-central-1"
}

variable "owner" {
  type        = string
  description = "Owner of the resources"
}

variable "client" {
  type        = string
  description = "Client of the resources"
  default     = "MyClient"
}

variable "project_name" {
  type        = string
  description = "Project of the resources"
  default     = "MyProject"
}

variable "environment" {
  type        = string
  description = "Environment of the resources"
  default     = "dev"
}
