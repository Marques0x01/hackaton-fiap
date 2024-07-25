provider "aws" {
  region = "us-east-2"
}

data "aws_ecr_repository" "existing" {
  name = "agenda_suspeita"
}

resource "aws_ecr_repository" "agenda_suspeita" {
  count = length(data.aws_ecr_repository.existing) == 0 ? 1 : 0

  name = "agenda_suspeita"

  image_scanning_configuration {
    scan_on_push = true
  }

  image_tag_mutability = "MUTABLE"

  lifecycle_policy {
    policy = <<EOF
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Keep last 30 images",
      "selection": {
        "tagStatus": "any",
        "countType": "imageCountMoreThan",
        "countNumber": 30
      },
      "action": {
        "type": "expire"
      }
    }
  ]
}
EOF
  }
}
