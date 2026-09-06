resource "aws_eip" "flask_ip" {

  instance = aws_instance.flask_server.id

  domain = "vpc"

  tags = {
    Name = "flask-eip"
  }
}