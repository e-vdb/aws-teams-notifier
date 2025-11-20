variable "function_name" {
  description = "The name of the Lambda function"
  type        = string
}

variable "function_description" {
  description = "The description of the Lambda function"
  type        = string
}

variable "function_handler" {
  description = "The handler of the Lambda function"
  type        = string
  default = "lambda_function.lambda_handler"
}

variable "function_runtime" {
  description = "The runtime of the Lambda function"
  type        = string
  default = "python3.11"
}

variable "function_memory_size" {
  description = "The memory size of the Lambda function"
  type        = number
  default = 128
}

variable "function_timeout" {
  description = "The timeout of the Lambda function"
  type        = number
  default = 60
}

variable "function_filename" {
  description = "The filename of the Lambda function"
  type        = string
}

variable "role_arn" {
  description = "The ARN of the IAM role for the Lambda function"
  type        = string
}



variable "tags" {
  description = "A map of standardized tags to assign to resources"
  type        = map(string)
}

variable "environment_variables" {
  description = "A map of environment variables to set in the Lambda function"
  type        = map(string)
  default     = {}
}
