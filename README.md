git clone https://github.com/otan1010/openmetadata-demo.git
cd .\openmetadata-demo\

vim .\terraform.tfvars

```
allowed_cidr = "111.222.333.444/32" # Replace with YOUR public IP/CIDR
location     = "westeurope"
prefix       = "omdemo"
# optional:
# openmetadata_release = "1.11.9-release"
```

az login #Choose correct username and then the correct subscription to build resources in

terraform init
terraform plan -out tfplan
terraform apply .\tfplan

Establish an ssh tunnel #See ssh_tunnel_command output

Likely credentials:
Open Metadata
Username: admin@open-metadata.org
Password: admin

Airflow/ingestion
Username: admin
Password: admin
