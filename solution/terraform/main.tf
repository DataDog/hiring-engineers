provider "aws" "default" {
  region = "${var.default_tags["region"]}"
}

# let's restrict our security group with just my ip
variable "my_ip" {}

variable "dd_api_key" {}

variable "default_tags" {
  type = "map"
  default = {
    region        = "us-west-2"
    datadog-agent = "true"
  }
}

variable "instance_data" {
  type    = "map"
  default = {
    count    = 1
    model    = "t2.nano"
    # 137112412989 <- amazon linux, 099720109477 <- ubuntu
    owners   = "137112412989,099720109477"
    ami_name = "amzn-ami-hvm-2016.09.1.20170119-x86_64-gp2"
    #ami_name = "ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-20170414"
  }
}

data "aws_ami" "service_ami" {
  most_recent = true
  owners      = ["${split(",", var.instance_data["owners"])}"]

  filter {
    name      = "name"
    values    = ["${var.instance_data["ami_name"]}"]
  }
}

data "template_file" "init" {
  template = <<EOF
#!/bin/bash

DD_API_KEY=$${dd_api_key} bash -c "\
  $(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"

sed -i 's,^# collect_ec2_tags.*,collect_ec2_tags: yes,' /etc/dd-agent/datadog.conf

service datadog-agent restart

EOF

  vars {
    dd_api_key = "${var.dd_api_key}"
  }

}

resource "aws_key_pair" "dd-example-key" {
  key_name   = "dd-example-key"
  public_key = "${file("secret.pub")}"
}

resource "aws_security_group" "app" {
  name_prefix = "dd-example-sg-"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${var.my_ip}/32"]
	}

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_role" "app" {
  name_prefix     = "dd-example-role-"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "app" {
  name       = "dd-example-attachment"
  roles      = ["${aws_iam_role.app.name}"]
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"
}

resource "aws_iam_instance_profile" "app" {
  name_prefix = "dd-example-instance-profile-"
  roles       = ["${aws_iam_role.app.id}"]
}

resource "aws_instance" "app" {
  count                  = "${var.instance_data["count"]}"
  ami                    = "${data.aws_ami.service_ami.id}"
  instance_type          = "${var.instance_data["model"]}"
  key_name               = "${aws_key_pair.dd-example-key.key_name}"
  vpc_security_group_ids = ["${aws_security_group.app.id}"]
  tags                   = "${merge(var.default_tags, map("Name", "dd-example-${count.index}"))}"

  user_data              = "${data.template_file.init.rendered}"
  iam_instance_profile   = "${aws_iam_instance_profile.app.id}"
}

output "public_ips" {
  value = ["${aws_instance.app.*.public_ip}"]
}
