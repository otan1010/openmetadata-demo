output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "vm_public_ip" {
  value = azurerm_public_ip.pip.ip_address
}

output "ssh_command" {
  value = "ssh ${var.admin_username}@${azurerm_public_ip.pip.ip_address}"
}

output "openmetadata_url" {
  value = "http://${azurerm_public_ip.pip.ip_address}:${var.public_http_port}"
}

output "airflow_url" {
  value = "http://${azurerm_public_ip.pip.ip_address}:8080"
}
