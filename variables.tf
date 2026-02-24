variable "prefix" {
  description = "Prefix used for all resource names"
  type        = string
  default     = "omdemo"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "westeurope"
}

variable "admin_username" {
  description = "Admin username for the VM"
  type        = string
  default     = "azureuser"
}

variable "ssh_public_key" {
  description = "SSH public key content (e.g. ~/.ssh/id_ed25519.pub)"
  type        = string
}

variable "vm_size" {
  description = "VM size for OpenMetadata demo. 4 vCPU / 16 GB RAM recommended."
  type        = string
  default     = "Standard_D4s_v5"
}

variable "allowed_ssh_cidr" {
  description = "CIDR allowed to SSH to the VM"
  type        = string
  default     = "0.0.0.0/0"
}

variable "openmetadata_version" {
  description = "OpenMetadata Docker image tag"
  type        = string
  default     = "1.10.4"
}

variable "docker_compose_file_url" {
  description = "Official OpenMetadata docker compose file URL"
  type        = string
  # For demo use, pin to a known version. Adjust as needed.
  default     = "https://raw.githubusercontent.com/open-metadata/OpenMetadata/1.10.4/docker/docker-compose-openmetadata.yml"
}

variable "public_http_port" {
  description = "Port exposed for OpenMetadata UI/API"
  type        = number
  default     = 8585
}
