terraform {
  backend "s3" {
    bucket         = "mybucket"
    key            = "myky/terraform.tfstate"
    region         = "myregion"
    dynamodb_table = "shared-terraform-lock-table"
  }
}
