# Outputs file
output "dog_url" {
  description = "Public URL for the Dog App."
  value = "http://${google_compute_instance.doghouse.network_interface.0.access_config.0.nat_ip}"
}

output "z_instructions" {
  value = <<-EOM

    #####################################################################
    Your SSH key has been created in the current directory as dogkey.pem.

    You can SSH into your machine using the following commands:
    
    chmod 600 dogkey.pem
    ssh -i dogkey.pem ubuntu@${google_compute_instance.doghouse.network_interface.0.access_config.0.nat_ip}
    #####################################################################
    EOM
}