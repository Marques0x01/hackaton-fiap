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

data "aws_subnet" "subnet1" {
  id = "subnet-001113aebb3a0086f"
}

data "aws_subnet" "subnet2" {
  id = "subnet-0379b250a6d6affdb"
}

data "aws_subnet" "subnet3" {
  id = "subnet-0fe974589b952abe5"
}

data "aws_security_group" "allow_http" {
  id = "sg-04f14be79d56e0c51"
}

data "aws_iam_role" "ecsTaskExecutionRole" {
  name = "ecsTaskExecutionRole"
}

resource "aws_ecs_task_definition" "agenda_suspeita_task" {
  family                   = "agenda_suspeita"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = data.aws_iam_role.ecsTaskExecutionRole.arn
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
    subnets          = [
      data.aws_subnet.subnet1.id,
      data.aws_subnet.subnet2.id,
      data.aws_subnet.subnet3.id
    ]
    security_groups  = [data.aws_security_group.allow_http.id]
    assign_public_ip = true
  }
}

resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  role       = data.aws_iam_role.ecsTaskExecutionRole.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}
