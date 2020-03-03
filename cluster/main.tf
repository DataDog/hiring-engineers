# Configure the AWS Provider
provider "aws" {
  version = "~> 2.45"
  region  = "${var.region}"
}

# IAM Roles & Policies for eks_cluster
resource "aws_iam_role" "cluster-assume-role" {
  name = "eks-datadog-cluster"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "datadog-AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = "${aws_iam_role.cluster-assume-role.name}"
}

resource "aws_iam_role_policy_attachment" "datadog-AmazonEKSServicePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
  role       = "${aws_iam_role.cluster-assume-role.name}"
}

# IAM Roles & Policies for eks_node_group
resource "aws_iam_role" "datadog-ng" {
  name = "eks-datadog-node-group"

  assume_role_policy = jsonencode({
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })
}

resource "aws_iam_role_policy_attachment" "datadog-AmazonEKSWorkerNodePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.datadog-ng.name
}

resource "aws_iam_role_policy_attachment" "datadog-AmazonEKS_CNI_Policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.datadog-ng.name
}

resource "aws_iam_role_policy_attachment" "datadog-AmazonEC2ContainerRegistryReadOnly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.datadog-ng.name
}



# Cloudwatch Logging
resource "aws_cloudwatch_log_group" "datadog-cluster" {
  name              = "/aws/eks/${var.cluster_name}/cluster"
  retention_in_days = 7
}





# EKS Cluster
resource "aws_eks_cluster" "datadog" {
  name                      = "${var.cluster_name}"
  role_arn                  = "${aws_iam_role.cluster-assume-role.arn}"
  enabled_cluster_log_types = ["api", "audit"]

  vpc_config {
    subnet_ids = ["${var.subnet1}", "${var.subnet2}"]
  }

  # Ensure that IAM Role permissions are created before and deleted after EKS Cluster handling.
  # Otherwise, EKS will not be able to properly delete EKS managed EC2 infrastructure such as Security Groups.
  depends_on = [
    "aws_iam_role_policy_attachment.datadog-AmazonEKSClusterPolicy",
    "aws_iam_role_policy_attachment.datadog-AmazonEKSServicePolicy",
    "aws_cloudwatch_log_group.datadog-cluster"
  ]
  
  provisioner "local-exec" {
    command = "aws eks --region ${var.region} update-kubeconfig --name ${var.cluster_name}"
  }

  provisioner "local-exec" {
    command = "kubectl apply -f kubernetes/dd-daemonset.yaml"
  }
}

# EKS Node Group
resource "aws_eks_node_group" "datadog" {
  cluster_name      = aws_eks_cluster.datadog.name
  node_group_name   = "${var.cluster_name}-node-group"
  node_role_arn     = aws_iam_role.datadog-ng.arn
  instance_types    = ["${var.instance_type}"]
  subnet_ids        = ["${var.subnet1}", "${var.subnet2}"]

  scaling_config {
    desired_size = 2
    max_size     = 2
    min_size     = 1
  }

  # Ensure that IAM Role permissions are created before and deleted after EKS Node Group handling.
  # Otherwise, EKS will not be able to properly delete EC2 Instances and Elastic Network Interfaces.
  depends_on = [
    aws_iam_role_policy_attachment.datadog-AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.datadog-AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.datadog-AmazonEC2ContainerRegistryReadOnly,
  ]
}
