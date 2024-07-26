provider "aws" {
  region = "us-east-2"
}

data "aws_ecr_repository" "agenda_suspeita" {
  name = "agenda_suspeita"
}

data "aws_ecs_cluster" "agenda_suspeita_cluster" {
  cluster_name = "agenda_suspeita_cluster"
}

# Cria uma nova IAM Role com um nome diferente
resource "aws_iam_role" "ecsTaskExecutionRole" {
  name = "ecsTaskExecutionRoleNew"

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
    subnets          = [aws_subnet.public.id]
    security_groups  = [aws_security_group.sg.id]
    assign_public_ip = true
  }
}

resource "aws_security_group" "sg" {
  name        = "allow_http"
  description = "Allow HTTP inbound traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}
