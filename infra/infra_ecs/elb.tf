resource "aws_alb" "load_balancer" {
  name               = "fiap-elb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = ["sg-04f14be79d56e0c51"]
  subnets = ["subnet-001113aebb3a0086f", "subnet-0379b250a6d6affdb", "subnet-0fe974589b952abe5"]

}


resource "aws_alb_listener" "front_end" {
  load_balancer_arn = aws_alb.load_balancer.id
  port              = 8080
  protocol          = "HTTP"

  default_action {
    target_group_arn = aws_alb_target_group.target_group.id
    type             = "forward"
  }
}

resource "aws_alb_target_group" "target_group" {
  name        = "fiap-target-group"
  port        = 8080
  protocol    = "HTTP"
  vpc_id      = "vpc-0a2df8074681f79f3"
  target_type = "ip"

  health_check {
    healthy_threshold   = "3"
    interval            = "30"
    protocol            = "HTTP"
    matcher             = "200,301"
    timeout             = "10"
    path                = "/api-docs"
    unhealthy_threshold = "3"
  }
}
