provider "aws" {
  region = "us-east-2"
}

resource "aws_ecr_repository" "agenda_suspeita" {
  name = "agenda_suspeita"

  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}

output "ecr_repository_url" {
  value = aws_ecr_repository.agenda_suspeita.repository_url
}
