variable "region" {
  description = "Please Enter AWS Region to deploy Server"
  type        = string
  default     = "eu-north-1"
}

variable "instance_type" {
  description = "Enter Instance Type"
  type        = string
  default     = "t3.micro"
}

variable "allow_ports" {
  description = "List of Ports to open for server"
  type        = list
  #default     = ["80", "443", "22"]
}

variable "busket_name" {
  description = "Enter busket_name"
  type        = string
  default     = "bucketname90days1"
}