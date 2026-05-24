resource "aws_lambda_function" "news_lambda" {
  function_name = var.lambda_function_name
  role          = aws_iam_role.lambda_exec.arn
  handler       = "handler.lambda_handler"
  runtime       = "python3.13"

  filename         = "${path.module}/../../lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/../../lambda.zip")

  timeout     = 60
  memory_size = 512

  environment {
    variables = {
      SES_SENDER     = var.email_sender
      SES_RECEIVER   = var.email_receiver
      SES_RECEIVERS  = length(var.email_receivers) > 0 ? join(",", var.email_receivers) : var.email_receiver
      GOOGLE_API_KEY = var.google_api_key
    }
  }
}
