resource "aws_alb" "load_balancer" {
  name               = "fiap-elb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = ["sg-0ae6acb0122745c14"]
  subnets = ["subnet-046d8ca90c49da4f6","subnet-012f52a7da18e761c","subnet-0f372ff98bb5233d9"]

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
  vpc_id      = "vpc-0948f5391118dd3ef"
  target_type = "ip"

  # health_check {
  #   healthy_threshold   = "3"
  #   interval            = "60"
  #   protocol            = "HTTP"
  #   matcher             = "200"
  #   timeout             = "10"
  #   path                = "/medicos"
  #   unhealthy_threshold = "3"
  # }
}
