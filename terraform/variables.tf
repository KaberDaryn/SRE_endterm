variable "project_name" {
  description = "Project name"
  type        = string
  default     = "sre-assignment6"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "VM size used for vertical scaling"
  type        = string
  default     = "t3.medium"
}

variable "allowed_ssh_cidr" {
  description = "Allowed CIDR block for SSH access"
  type        = string
  default     = "0.0.0.0/0"
}
