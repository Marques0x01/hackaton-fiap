terraform {
  backend "s3" {
    bucket         = "hackatuun"
    key            = "hackatuun/terraform.tfstate"
    region         = "us-east-1"
    
  }
}
