output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer."
  value       = aws_lb.main.dns_name
}

output "alb_arn" {
  description = "ARN of the Application Load Balancer."
  value       = aws_lb.main.arn
}

output "alb_zone_id" {
  description = "Zone ID of the Application Load Balancer."
  value       = aws_lb.main.zone_id
}

output "odoo_instance_ids" {
  description = "IDs of the Odoo EC2 instances."
  value       = [for instance in aws_instance.odoo_app : instance.id]
}

output "odoo_instance_private_ips" {
  description = "Private IP addresses of the Odoo EC2 instances."
  value       = [for instance in aws_instance.odoo_app : instance.private_ip]
}

output "odoo_instance_public_ips" {
  description = "Public IP addresses of the Odoo EC2 instances (if they have one)."
  value       = [for instance in aws_instance.odoo_app : instance.public_ip]
}

output "nginx_instance_ids" {
  description = "IDs of the Nginx EC2 instances."
  value       = [for instance in aws_instance.nginx_proxy : instance.id]
}

output "nginx_instance_private_ips" {
  description = "Private IP addresses of the Nginx EC2 instances."
  value       = [for instance in aws_instance.nginx_proxy : instance.private_ip]
}

output "nginx_instance_public_ips" {
  description = "Public IP addresses of the Nginx EC2 instances."
  value       = [for instance in aws_instance.nginx_proxy : instance.public_ip]
}

output "rds_endpoint_address" {
  description = "Endpoint address of the RDS PostgreSQL instance."
  value       = var.deploy_managed_db_service ? aws_db_instance.main_postgres[0].address : "N/A (PostgreSQL on EC2)"
}

output "rds_endpoint_port" {
  description = "Endpoint port of the RDS PostgreSQL instance."
  value       = var.deploy_managed_db_service ? aws_db_instance.main_postgres[0].port : "N/A (PostgreSQL on EC2)"
}

output "rds_db_name" {
  description = "Database name of the RDS PostgreSQL instance."
  value       = var.deploy_managed_db_service ? aws_db_instance.main_postgres[0].db_name : var.postgres_db_name # Fallback to var if on EC2
}

output "postgres_ec2_instance_ids" {
  description = "IDs of the EC2 instances hosting PostgreSQL (if not using RDS)."
  value       = var.deploy_managed_db_service ? [] : [for instance in aws_instance.postgres_ec2 : instance.id]
}

output "postgres_ec2_instance_private_ips" {
  description = "Private IP addresses of EC2 instances hosting PostgreSQL (if not using RDS)."
  value       = var.deploy_managed_db_service ? [] : [for instance in aws_instance.postgres_ec2 : instance.private_ip]
}

output "backup_s3_bucket_id" {
  description = "ID (name) of the S3 bucket for backups."
  value       = aws_s3_bucket.backups.id
}

output "backup_s3_bucket_arn" {
  description = "ARN of the S3 bucket for backups."
  value       = aws_s3_bucket.backups.arn
}

output "vpc_id" {
  description = "ID of the VPC."
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets."
  value       = [for subnet in aws_subnet.public : subnet.id]
}

output "private_subnet_ids" {
  description = "IDs of the private subnets."
  value       = [for subnet in aws_subnet.private : subnet.id]
}

output "ec2_instance_role_arn" {
  description = "ARN of the IAM role for EC2 instances."
  value       = aws_iam_role.ec2_instance_role.arn
}

output "ec2_instance_profile_arn" {
  description = "ARN of the IAM instance profile for EC2 instances."
  value       = aws_iam_instance_profile.ec2_instance_profile.arn
}

output "alb_security_group_id" {
  description = "ID of the ALB Security Group."
  value       = aws_security_group.alb_sg.id
}

output "nginx_security_group_id" {
  description = "ID of the Nginx Security Group."
  value       = aws_security_group.nginx_sg.id
}

output "odoo_security_group_id" {
  description = "ID of the Odoo Security Group."
  value       = aws_security_group.odoo_sg.id
}

output "postgres_security_group_id" {
  description = "ID of the PostgreSQL Security Group."
  value       = aws_security_group.postgres_sg.id
}