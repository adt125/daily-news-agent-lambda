output "lambda_function_name" {
  value = aws_lambda_function.news_lambda.function_name
}

output "lambda_arn" {
  value = aws_lambda_function.news_lambda.arn
}

output "eventbridge_rule_name" {
  value = aws_cloudwatch_event_rule.daily_news_schedule.name
}

output "eventbridge_rule_arn" {
  value = aws_cloudwatch_event_rule.daily_news_schedule.arn
}