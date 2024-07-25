provider "aws" {
  region = "us-east-2"
}

resource "aws_ecs_cluster" "agenda_suspeita_cluster" {
  name = "agenda_suspeita_cluster"
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.agenda_suspeita_cluster.name
}
