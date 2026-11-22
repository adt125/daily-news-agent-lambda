variable "lambda_function_name" {
  default = "daily-news-agent"
}

variable "email_sender" {}
variable "email_receiver" {
  default = ""
}
variable "email_receivers" {
  type    = list(string)
  default = []
}
variable "google_api_key" {}
