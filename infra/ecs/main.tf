provider "aws" {
  region = "us-east-2"
}

data "aws_ecr_repository" "agenda_suspeita" {
  name = "agenda_suspeita"
}

data "aws_ecs_cluster" "agenda_suspeita_cluster" {
  cluster_name = "agenda_suspeita_cluster"
}

data "aws_vpc" "main" {
  id = "vpc-0a2df8074681f79f3"
}

data "aws_subnet" "public_subnets" {
  ids = [
    "subnet-001113aebb3a0086f",
    "subnet-0379b250a6d6affdb",
    "subnet-0fe974589b952abe5"
  ]
}

data "aws_security_group" "allow_http" {
  id = "sg-04f14be79d56e0c51"
}

resource "aws_ecs_task_definition" "agenda_suspeita_task" {
  family                   = "agenda_suspeita"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = aws_iam_role.ecsTaskExecutionRole.arn
  cpu                      = "256"
  memory                   = "512"

  container_definitions = jsonencode([
    {
      name      = "agenda_suspeita"
      image     = "${data.aws_ecr_repository.agenda_suspeita.repository_url}:latest"
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "agenda_suspeita_service" {
  name            = "agenda_suspeita_service"
  cluster         = data.aws_ecs_cluster.agenda_suspeita_cluster.id
  task_definition = aws_ecs_task_definition.agenda_suspeita_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = data.aws_subnet.public_subnets.ids
    security_groups  = [data.aws_security_group.allow_http.id]
    assign_public_ip = true
  }
}

resource "aws_iam_role" "ecsTaskExecutionRole" {
  name = "ecsTaskExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Effect = "Allow"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  role       = aws_iam_role.ecsTaskExecutionRole.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}
