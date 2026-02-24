output "resource_group_name" {
  value       = azurerm_resource_group.this.name
  description = "Azure Resource Group name."
}

output "public_ip" {
  value       = azurerm_public_ip.this.ip_address
  description = "Public IP of the OpenMetadata VM."
}

output "openmetadata_url" {
  value       = "http://localhost:${var.openmetadata_port}"
  description = "URL to use locally when SSH tunnel is established."
}

output "ssh_tunnel_command" {
    value = "ssh -i ${abspath(var.ssh_private_key_output_path)} -L 8585:localhost:8585 -L 8080:localhost:8080 ${var.admin_username}@${azurerm_public_ip.this.ip_address}"
    #value       = "ssh -i \"${abspath(var.ssh_private_key_output_path)}\" -L 8585:localhost:8585 -L 8080:localhost:8080 \"${var.admin_username}@${azurerm_public_ip.this.ip_address}\""
  description = "One-line SSH tunnel command for OpenMetadata (8585) and Airflow (8080)."
}

output "ssh_public_key_local_path" {
  value       = abspath(local_file.ssh_public_key.filename)
  description = "Path to the generated SSH public key."
}
