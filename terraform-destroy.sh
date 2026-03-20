#!/bin/bash
# This script destroys the infrastructure provisioned by Terraform.
# chmod +x terraform-destroy.sh - required
cd "$(dirname "$0")/infastructure/terraform"
terraform destroy -auto-approve
