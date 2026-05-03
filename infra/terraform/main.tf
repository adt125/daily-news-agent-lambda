resource "aws_lambda_function" "news_lambda" {
  function_name = var.lambda_function_name
  role          = aws_iam_role.lambda_exec.arn

  package_type = "Image"

  image_uri = "575108925992.dkr.ecr.ap-south-1.amazonaws.com/daily-news-agent:latest"

  timeout     = 60
  memory_size = 512
  architectures = ["x86_64"]
  environment {
    variables = {
      SES_SENDER     = var.email_sender
      SES_RECEIVER   = var.email_receiver
      GOOGLE_API_KEY = var.google_api_key
    }
  }
}