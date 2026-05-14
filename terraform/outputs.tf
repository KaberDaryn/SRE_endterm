output "instance_public_ip" {
  description = "Public IP address of the SRE VM"
  value       = aws_instance.sre_vm.public_ip
}

output "instance_id" {
  description = "EC2 Instance ID"
  value       = aws_instance.sre_vm.id
}

output "services_urls" {
  description = "URLs for all deployed services"
  value = {
    frontend      = "http://${aws_instance.sre_vm.public_ip}:5000"
    user_api      = "http://${aws_instance.sre_vm.public_ip}:5001"
    product_api   = "http://${aws_instance.sre_vm.public_ip}:5002"
    order_api     = "http://${aws_instance.sre_vm.public_ip}:5003"
    notification  = "http://${aws_instance.sre_vm.public_ip}:5004"
    payment_api   = "http://${aws_instance.sre_vm.public_ip}:5005"
    prometheus    = "http://${aws_instance.sre_vm.public_ip}:9090"
    grafana       = "http://${aws_instance.sre_vm.public_ip}:3000"
    nginx         = "http://${aws_instance.sre_vm.public_ip}:8081"
  }
}
