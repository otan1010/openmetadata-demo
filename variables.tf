variable "prefix" {
  description = "Prefix for Azure resource names."
  type        = string
  default     = "omdemo"
}

variable "location" {
  description = "Azure region."
  type        = string
  default     = "westeurope"
}

variable "admin_username" {
  description = "Linux admin username for the VM."
  type        = string
  default     = "azureuser"
}

variable "allowed_cidr" {
  description = "CIDR allowed to access SSH and OpenMetadata (e.g. 203.0.113.10/32)."
  type        = string

  validation {
    condition     = can(cidrhost(var.allowed_cidr, 0))
    error_message = "allowed_cidr must be a valid CIDR block, e.g. 203.0.113.10/32."
  }
}

variable "vm_size" {
  description = "Azure VM size (demo/test)."
  type        = string
  default     = "Standard_D4s_v5"
}

variable "ssh_private_key_output_path" {
  description = "Local path where Terraform will write the generated private key."
  type        = string
  default     = "./.ssh/openmetadata-demo-id_rsa"
}

variable "openmetadata_port" {
  description = "OpenMetadata UI/API port exposed on the VM."
  type        = number
  default     = 8585
}

variable "openmetadata_release" {
  description = "Pinned OpenMetadata GitHub release tag for quickstart compose."
  type        = string
  default     = "1.11.9-release"
}

variable "tags" {
  description = "Tags to apply to Azure resources."
  type        = map(string)
  default = {
    environment = "demo"
    purpose     = "openmetadata-test"
    managed-by  = "terraform"
  }
}
