resource "aws_alb" "load_balancer" {
  name               = "fiap-elb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = ["sg-06c4bc1940ca31ed7"]
  subnets = ["subnet-06b1d975cacf99ebd","subnet-0b0a05319e716de21","subnet-01c15112138f84647"]

}


# resource "aws_alb_listener" "front_end" {
#   load_balancer_arn = aws_alb.load_balancer.id
#   port              = 8080
#   protocol          = "HTTP"

#   default_action {
#     target_group_arn = aws_alb_target_group.target_group.id
#     type             = "forward"
#   }
# }

resource "aws_alb_target_group" "target_group" {
  name        = "fiap-target-group"
  port        = 8080
  protocol    = "HTTP"
  vpc_id      = "vpc-0d77b7aa0d2922590"
  target_type = "ip"

#   health_check {
#     healthy_threshold   = "3"
#     interval            = "60"
#     protocol            = "HTTP"
#     matcher             = "200"
#     timeout             = "10"
#     path                = "/health"
#     unhealthy_threshold = "3"
#   }
}
