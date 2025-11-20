resource "aws_lambda_function" "my_lambda" {
  function_name    = var.function_name
  description      = var.function_description
  runtime          = var.function_runtime
  handler          = var.function_handler
  role             = var.role_arn
  timeout          = var.function_timeout
  filename         = var.function_filename
  memory_size      = var.function_memory_size
  source_code_hash = filebase64sha256(var.function_filename)

  environment {
    variables = var.environment_variables
  }

  tags = var.tags
}
