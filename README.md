# OpenMetadata on Azure (Demo/Test) via Terraform

## What this creates
- Resource Group
- VNet + Subnet
- NSG restricting inbound access to your CIDR
- Public IP + NIC
- Ubuntu VM
- Docker + Docker Compose
- OpenMetadata quickstart stack (official compose from pinned release)
- Terraform-generated SSH keypair written locally

## Prerequisites
- Terraform >= 1.5
- Azure CLI authenticated (`az login`)
- Sufficient Azure subscription permissions

## Usage

1. Create `terraform.tfvars`:

```hcl
allowed_cidr = "203.0.113.10/32" # Replace with YOUR public IP/CIDR
location     = "westeurope"
prefix       = "omdemo"
# optional:
# openmetadata_release = "1.11.9-release"
