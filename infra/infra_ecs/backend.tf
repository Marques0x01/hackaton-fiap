terraform {
  backend "s3" {
    bucket         = "agendaconsultorio"
    key            = "agendaconsultorio/terraform.tfstate"
    region         = "us-east-2"
    
  }
}
