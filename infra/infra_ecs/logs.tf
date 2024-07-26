# logs.tf

# Set up CloudWatch group and log stream and retain logs for 30 days
resource "aws_cloudwatch_log_group" "fiap_log_group" {
  name              = "/ecs/fiap-app"
  retention_in_days = 30

  tags = {
    Name = "fiap-log-group"
  }
}

resource "aws_cloudwatch_log_stream" "fiap_log_stream" {
  name           = "fiap-log-stream"
  log_group_name = aws_cloudwatch_log_group.fiap_log_group.name
}