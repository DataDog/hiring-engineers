  /* EC2 Things */

provider "aws" {
  region = "${var.region}"
}

/* Security Group */
resource "aws_security_group" "demo" {
  name_prefix = "demo-security-group"
  vpc_id = "${var.vpc_id}"

  tags = {
    Name = "demo-security-group"
  }
}

/* Security Group Ingress */
resource "aws_security_group_rule" "incoming" {
  type = "ingress"
  from_port = 22
  to_port = 22
  protocol = "tcp"
  cidr_blocks = ["11.22.33.44/32"]

  security_group_id = "${aws_security_group.demo.id}"
}

/* Security Group Egress */
resource "aws_security_group_rule" "outgoing" {
  type = "egress"
  from_port = 0
  to_port = 65535
  protocol = "-1"
  cidr_blocks = ["0.0.0.0/0"]

  security_group_id = "${aws_security_group.demo.id}"
}

/* EC2 Instance */
resource "aws_instance" "demo" {
  ami = "${var.image_id}"
  instance_type = "${var.instance_type}"
  associate_public_ip_address = true
  ebs_optimized = false
  key_name = "${var.key_name}"
  count = 1

  root_block_device {
   volume_size = 16
   volume_type = "gp2"
 }

  tags {
    Name = "demo"
  }
  vpc_security_group_ids = [ "${aws_security_group.demo.id}" ]
}
