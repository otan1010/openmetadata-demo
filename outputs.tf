output "resource_group_name" {
  value       = azurerm_resource_group.this.name
  description = "Azure Resource Group name."
}

output "public_ip" {
  value       = azurerm_public_ip.this.ip_address
  description = "Public IP of the OpenMetadata VM."
}

output "admin_username" {
  value       = var.admin_username
  description = "Linux admin username."
}

output "openmetadata_url" {
  value       = "http://${azurerm_public_ip.this.ip_address}:${var.openmetadata_port}"
  description = "OpenMetadata URL (reachable only from allowed_cidr, unless using SSH tunnel)."
}

output "local_tunnel_url" {
  value       = "http://localhost:${var.openmetadata_port}"
  description = "URL to use locally when SSH tunnel is established."
}

output "ssh_private_key_local_path" {
  value       = abspath(local_file.ssh_private_key.filename)
  description = "Path to the generated SSH private key."
  sensitive   = true
}

output "ssh_public_key_local_path" {
  value       = abspath(local_file.ssh_public_key.filename)
  description = "Path to the generated SSH public key."
}

output "ssh_command" {
  value       = "ssh -i ${abspath(local_file.ssh_private_key.filename)} ${var.admin_username}@${azurerm_public_ip.this.ip_address}"
  description = "Convenience SSH command."
}

output "ssh_tunnel_command" {
  value       = "ssh -i ${abspath(local_file.ssh_private_key.filename)} -L ${var.openmetadata_port}:localhost:${var.openmetadata_port} ${var.admin_username}@${azurerm_public_ip.this.ip_address}"
  description = "Command to establish an SSH tunnel to OpenMetadata."
}
