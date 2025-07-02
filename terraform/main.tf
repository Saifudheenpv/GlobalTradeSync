provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "app_server" {
  ami           = "ami-05ffe3c48a9991133" # Amazon Linux 2
  instance_type = "t2.micro"
  security_groups = [aws_security_group.app_sg.name]
  tags = {
    Name = "GlobalTradeSync-Server"
  }
}

resource "aws_security_group" "app_sg" {
  name = "globaltradesync-sg"
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_s3_bucket" "cargo_data" {
  bucket = "globaltradesync-data-2025"
}