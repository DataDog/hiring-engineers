provider "aws" {
  access_key    = "${var.access_key}"
  secret_key    = "${var.secret_key}"
}   
   
resource "aws_instance" "Datadog_Tech_Example" {
  ami                         = "ami-cd0f5cb6"
  instance_type               = "t2.large"
  associate_public_ip_address = true
  key_name                    = "DD_Testing"
  vpc_security_group_ids = [
      "sg-033ebf73"
  ]

  tags {
    Name = "Datadog_Tech_Example"
  }

  provisioner "local-exec" {
    command = "sleep 120; ANSIBLE_HOST_KEY_CHECKING=False AWS_ACCESS_KEY=${var.access_key} AWS_SECRET_KEY=${var.secret_key} ansible-playbook /Users/hack/dd_solution_engineer/ansible/Tasks/main.yml -u ubuntu --private-key /Users/hack/.ssh/DD_Testing.pem -i '${aws_instance.Datadog_Tech_Example.public_ip},'"
  }
}