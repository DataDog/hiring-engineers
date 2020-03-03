output "endpoint" {
  value = "${aws_eks_cluster.datadog.endpoint}"
}

output "kubeconfig-certificate-authority-data" {
  value = "${aws_eks_cluster.datadog.certificate_authority.0.data}"
}
