

data "template_file" "fiap_app" {
  template = file("./templates/ecs/fiap_app.json.tpl")
}

resource "aws_ecs_task_definition" "app" {
  family             = "fiap-app-task"
  execution_role_arn = aws_iam_role.role.arn
  task_role_arn      = aws_iam_role.role.arn
  network_mode             = "awsvpc"
  
  requires_compatibilities = ["FARGATE"]
  cpu                      = 512
  memory                   = 1024
  container_definitions    = data.template_file.fiap_app.rendered
}

resource "aws_ecs_service" "main" {
  name            = "fiap-service"
  cluster         = aws_ecs_cluster.fiap_app.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    security_groups  = ["sg-06c4bc1940ca31ed7"]
    subnets          = ["subnet-06b1d975cacf99ebd","subnet-0b0a05319e716de21","subnet-01c15112138f84647"]
    assign_public_ip = true
  }

  # load_balancer {
  #   target_group_arn = aws_alb_target_group.target_group.id
  #   container_name   = "fiap-app"
  #   container_port   = 8080
  # }

  # depends_on = [aws_alb_listener.front_end, aws_ecs_task_definition.app]
}
