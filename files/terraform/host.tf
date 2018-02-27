#tsn - Create the Datadog Host

resource "aws_default_vpc" "default" {
    tags {
        Name = "Default VPC"
    }
}

resource "aws_default_subnet" "default_az1" {
  availability_zone = "us-west-2a"

    tags {
        Name = "Default subnet for us-west-2a"
    }
}

data "aws_security_group" "default" {
  vpc_id = "${aws_default_vpc.default.id}"
  name   = "default"
}

resource "aws_instance" "datadog-host" {
  ami                    = "ami-8b0c12ea"
  instance_type          = "${var.instance_type}"
  key_name               = "datadog"
  subnet_id              = "default_az1"
  vpc_security_group_ids = ["${data.aws_security_group.default.id}"]
  associate_public_ip_address = true

  root_block_device {
    volume_type = "gp2"
    volume_size = "10"
  }

  tags {
    Name      = "datadog-host"
  }
}

output "bot_public_ip" {
  value = "#{aws_instance.datadog-host.public_ip}"
}