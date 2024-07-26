terraform {
  backend "s3" {
    bucket         = "hackatun"
    key            = "hackatun/terraform.tfstate"
    region         = "us-east-2"
    
  }
}
