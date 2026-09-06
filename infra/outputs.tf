output "ec2_public_ip" {
  value = aws_eip.flask_ip.public_ip
}

output "ec2_public_dns" {
  value = aws_instance.flask_server.public_dns
}

output "instance_id" {
  value = aws_instance.flask_server.id
}