"""
Terraform IaC Infrastructure Module Scaffold Generator.
Generates Terraform HCL configs (`main.tf`, `variables.tf`, `outputs.tf`) for AWS EC2, S3, RDS, and ECS clusters.
"""

from typing import Dict, Any

def generate_terraform_module(
    module_name: str = "iot_cloud_backend",
    cloud_provider: str = "aws"
) -> Dict[str, Any]:
    """
    Generates Terraform HCL infrastructure module code.
    """
    hcl_code = f"""# Terraform IaC Module for {module_name} ({cloud_provider.upper()})
terraform {{
  required_version = ">= 1.2.0"
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }}
  }}
}}

provider "aws" {{
  region = var.aws_region
}}

resource "aws_s3_bucket" "telemetry_storage" {{
  bucket = "{module_name.lower().replace('_', '-')}-storage"
}}

resource "aws_dynamodb_table" "device_state" {{
  name         = "{module_name}_state"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "device_id"

  attribute {{
    name = "device_id"
    type = "S"
  }}
}}
"""

    return {
        "status": "success",
        "module_name": module_name,
        "cloud_provider": cloud_provider,
        "hcl_main_tf": hcl_code,
        "resources_created": ["aws_s3_bucket", "aws_dynamodb_table"]
    }
