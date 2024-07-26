terraform {
  backend "s3" {
    bucket         = "hackatin"
    key            = "hackatin/terraform.tfstate"
    region         = "us-east-1"
    
  }
}
