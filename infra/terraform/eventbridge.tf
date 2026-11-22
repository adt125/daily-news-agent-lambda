resource "aws_cloudwatch_event_rule" "daily_news_schedule" {
  name                = "daily-news-trigger"
  schedule_expression = "cron(30 2 * * ? *)" # 8 AM IST
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.daily_news_schedule.name
  target_id = "lambda"
  arn       = aws_lambda_function.news_lambda.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.news_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_news_schedule.arn
}