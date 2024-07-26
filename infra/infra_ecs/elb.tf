# resource "aws_alb" "load_balancer" {
#   name               = "fiap-elb"
#   internal           = false
#   load_balancer_type = "application"
<<<<<<< HEAD
#   security_groups    = ["sg-03773f25129fe387c"]
#   subnets = ["subnet-096f32102466e631f", "subnet-089dfee703f076258", "subnet-0587620277dc78ef2"]
=======
#   security_groups    = ["sg-06c4bc1940ca31ed7"]
#   subnets = ["subnet-06b1d975cacf99ebd","subnet-0b0a05319e716de21","subnet-01c15112138f84647"]
>>>>>>> baf1322c4d16117df1cd0e5c4acad097447a0379

# }


# resource "aws_alb_listener" "front_end" {
#   load_balancer_arn = aws_alb.load_balancer.id
#   port              = 8080
#   protocol          = "HTTP"

#   default_action {
#     target_group_arn = aws_alb_target_group.target_group.id
#     type             = "forward"
#   }
# }

# resource "aws_alb_target_group" "target_group" {
#   name        = "fiap-target-group"
#   port        = 8080
#   protocol    = "HTTP"
#   vpc_id      = "vpc-0224055d409e21a66"
#   target_type = "ip"

#   health_check {
#     healthy_threshold   = "3"
#     interval            = "60"
#     protocol            = "HTTP"
#     matcher             = "200"
#     timeout             = "10"
#     path                = "/health"
#     unhealthy_threshold = "3"
#   }
# }
