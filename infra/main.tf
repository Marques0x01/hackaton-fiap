provider "aws" {
  region = var.aws_region
}

# Módulo ECR
module "ecr" {
  source = "./infra/ecr"
  
  repository_name = var.repository_name
}

# Módulo ECS Cluster
module "ecs_cluster" {
  source = "./infra/cluster"
  
  cluster_name = var.cluster_name
}

# Módulo ECS Service
module "ecs_service" {
  source = "./infra/ecs"
  
  cluster_name    = module.ecs_cluster.cluster_name
  repository_url  = module.ecr.repository_url
  task_definition = var.task_definition
}

# Variáveis utilizadas no projeto
variable "aws_region" {
  default = "us-east-2"
}

variable "repository_name" {
  default = "agenda_suspeita"
}

variable "cluster_name" {
  default = "agenda-suspeita-cluster"
}

variable "task_definition" {
  description = "The task definition for the ECS service"
}
