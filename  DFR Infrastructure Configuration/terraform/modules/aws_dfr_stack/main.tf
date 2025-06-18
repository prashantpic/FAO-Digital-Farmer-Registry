data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_secretsmanager_secret_version" "db_password" {
  count     = var.deploy_managed_db_service ? 1 : 0
  secret_id = var.postgres_db_password_secret_arn
}

locals {
  az_count             = length(var.availability_zones) > 0 ? length(var.availability_zones) : 2 # Default to 2 AZs if not specified
  availability_zones   = length(var.availability_zones) > 0 ? var.availability_zones : slice(data.aws_availability_zones.available.names, 0, local.az_count)
  vpc_name             = "${var.country_code}-${var.environment_name}-dfr-vpc"
  s3_bucket_backup_name = "${var.backup_s3_bucket_name_prefix}-${var.country_code}-${var.environment_name}"
  common_tags = {
    Environment = var.environment_name
    Project     = "DFR"
    Country     = var.country_code
    ManagedBy   = "Terraform"
  }
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(local.common_tags, {
    Name = local.vpc_name
  })
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id

  tags = merge(local.common_tags, {
    Name = "${local.vpc_name}-igw"
  })
}

resource "aws_subnet" "public" {
  count                   = local.az_count
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = local.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = merge(local.common_tags, {
    Name   = "${local.vpc_name}-public-subnet-${count.index + 1}"
    Tier   = "Public"
  })
}

resource "aws_subnet" "private" {
  count             = local.az_count
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = local.availability_zones[count.index]

  tags = merge(local.common_tags, {
    Name   = "${local.vpc_name}-private-subnet-${count.index + 1}"
    Tier   = "Private"
  })
}

resource "aws_eip" "nat" {
  count = local.az_count # One NAT Gateway per AZ for resilience
  domain = "vpc" # Changed from "vpc" = true to domain = "vpc" for Terraform 0.13+ syntax

  tags = merge(local.common_tags, {
    Name = "${local.vpc_name}-nat-eip-${count.index + 1}"
  })
}

resource "aws_nat_gateway" "nat" {
  count         = local.az_count
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = merge(local.common_tags, {
    Name = "${local.vpc_name}-nat-gw-${count.index + 1}"
  })

  depends_on = [aws_internet_gateway.gw]
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = merge(local.common_tags, {
    Name = "${local.vpc_name}-public-rt"
  })
}

resource "aws_route_table_association" "public" {
  count          = local.az_count
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table" "private" {
  count  = local.az_count
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat[count.index].id
  }

  tags = merge(local.common_tags, {
    Name = "${local.vpc_name}-private-rt-${count.index + 1}"
  })
}

resource "aws_route_table_association" "private" {
  count          = local.az_count
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

# Security Groups
resource "aws_security_group" "alb_sg" {
  name        = "${local.vpc_name}-alb-sg"
  description = "Allow HTTP/HTTPS traffic to ALB"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${local.vpc_name}-alb-sg"
  })
}

resource "aws_security_group" "nginx_sg" {
  name        = "${local.vpc_name}-nginx-sg"
  description = "Allow HTTP/HTTPS from ALB and SSH"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }

  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }

  ingress {
    description = "Allow SSH from bastion/admin (Update CIDR)"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # FIXME: Restrict this to specific IPs
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${local.vpc_name}-nginx-sg"
  })
}

resource "aws_security_group" "odoo_sg" {
  name        = "${local.vpc_name}-odoo-sg"
  description = "Allow Odoo ports from Nginx and SSH"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Odoo HTTP"
    from_port       = 8069
    to_port         = 8069
    protocol        = "tcp"
    security_groups = [aws_security_group.nginx_sg.id]
  }
  
  ingress {
    description     = "Odoo Longpolling"
    from_port       = 8072 
    to_port         = 8072
    protocol        = "tcp"
    security_groups = [aws_security_group.nginx_sg.id]
  }

  ingress {
    description = "Allow SSH from bastion/admin (Update CIDR)"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # FIXME: Restrict this to specific IPs
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${local.vpc_name}-odoo-sg"
  })
}

resource "aws_security_group" "postgres_sg" {
  name        = "${local.vpc_name}-postgres-sg"
  description = "Allow PostgreSQL port from Odoo SG"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.odoo_sg.id]
  }
  
  # If Postgres is on EC2, allow SSH
  ingress {
    count       = var.deploy_managed_db_service ? 0 : 1
    description = "Allow SSH from bastion/admin (Update CIDR) - for EC2 Postgres"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # FIXME: Restrict this to specific IPs
  }


  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${local.vpc_name}-postgres-sg"
  })
}

# IAM Roles
data "aws_iam_policy_document" "ec2_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ec2_instance_role" {
  name               = "${local.vpc_name}-ec2-instance-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role_policy.json

  tags = merge(local.common_tags, {
    Name = "${local.vpc_name}-ec2-instance-role"
  })
}

resource "aws_iam_policy" "ec2_s3_secrets_cw_policy" {
  name        = "${local.vpc_name}-ec2-s3-secrets-cw-policy"
  description = "Policy for EC2 to access S3 for backups, Secrets Manager, and CloudWatch Logs"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ],
        Resource = [
          "arn:aws:s3:::${local.s3_bucket_backup_name}",
          "arn:aws:s3:::${local.s3_bucket_backup_name}/*"
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "secretsmanager:GetSecretValue"
        ],
        Resource = "*" # Consider restricting this to specific secrets
      },
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogStreams"
        ],
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "ec2_policy_attachment" {
  role       = aws_iam_role.ec2_instance_role.name
  policy_arn = aws_iam_policy.ec2_s3_secrets_cw_policy.arn
}

resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "${local.vpc_name}-ec2-instance-profile"
  role = aws_iam_role.ec2_instance_role.name

  tags = merge(local.common_tags, {
      Name = "${local.vpc_name}-ec2-instance-profile"
  })
}

# EC2 Instances (base AMIs for Ansible provisioning)
# Find latest Amazon Linux 2 AMI
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "odoo_app" {
  # count         = var.odoo_instance_count # Assuming a variable for count, default to 1 for now
  count         = 1 
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = var.odoo_instance_type
  subnet_id     = aws_subnet.private[count.index % local.az_count].id # Distribute across private subnets
  vpc_security_group_ids = [aws_security_group.odoo_sg.id]
  iam_instance_profile = aws_iam_instance_profile.ec2_instance_profile.name
  key_name      = var.ec2_key_name # Variable to be added in variables.tf

  tags = merge(local.common_tags, {
    Name = "${local.vpc_name}-odoo-app-${count.index + 1}"
    Role = "odoo-app"
  })
}

resource "aws_instance" "nginx_proxy" {
  # count         = var.nginx_instance_count # Assuming a variable for count, default to 1
  count = 1
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = var.nginx_instance_type
  subnet_id     = aws_subnet.public[count.index % local.az_count].id # Nginx in public for ALB, or private if ALB handles public exposure fully
  vpc_security_group_ids = [aws_security_group.nginx_sg.id]
  iam_instance_profile = aws_iam_instance_profile.ec2_instance_profile.name
  key_name      = var.ec2_key_name # Variable to be added in variables.tf

  tags = merge(local.common_tags, {
    Name = "${local.vpc_name}-nginx-proxy-${count.index + 1}"
    Role = "nginx-proxy"
  })
}

# Database
resource "aws_db_subnet_group" "dfr_db_subnet_group" {
  count      = var.deploy_managed_db_service ? 1 : 0
  name       = "${local.vpc_name}-db-subnet-group"
  subnet_ids = [for subnet in aws_subnet.private : subnet.id]

  tags = merge(local.common_tags, {
    Name = "${local.vpc_name}-db-subnet-group"
  })
}

resource "aws_db_instance" "main_postgres" {
  count                    = var.deploy_managed_db_service ? 1 : 0
  identifier               = "${var.country_code}-${var.environment_name}-dfr-postgres"
  allocated_storage        = var.postgres_allocated_storage
  engine                   = "postgres"
  engine_version           = "15" # Specify desired version
  instance_class           = var.postgres_instance_class
  db_name                  = var.postgres_db_name
  username                 = var.postgres_db_username
  password                 = data.aws_secretsmanager_secret_version.db_password[0].secret_string
  db_subnet_group_name     = aws_db_subnet_group.dfr_db_subnet_group[0].name
  vpc_security_group_ids   = [aws_security_group.postgres_sg.id]
  skip_final_snapshot      = true // Set to false for production
  multi_az                 = false // Set to true for production for HA
  publicly_accessible      = false
  backup_retention_period  = 7 // days, adjust as needed
  storage_encrypted        = true // Recommended

  tags = merge(local.common_tags, {
    Name = "${local.vpc_name}-rds-postgres"
    Role = "database"
  })
}

# EC2 instance for PostgreSQL container if not using RDS
resource "aws_instance" "postgres_ec2" {
  count         = var.deploy_managed_db_service ? 0 : 1
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = "t3.small" # Example, choose appropriate type
  subnet_id     = aws_subnet.private[0].id # Choose one private subnet
  vpc_security_group_ids = [aws_security_group.postgres_sg.id]
  iam_instance_profile = aws_iam_instance_profile.ec2_instance_profile.name
  key_name      = var.ec2_key_name # Variable to be added in variables.tf

  tags = merge(local.common_tags, {
    Name = "${local.vpc_name}-postgres-ec2-db"
    Role = "postgres-db-container"
  })
}


# Load Balancer
resource "aws_lb" "main" {
  name               = "${local.vpc_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = [for subnet in aws_subnet.public : subnet.id]

  enable_deletion_protection = false // Set to true for production

  tags = merge(local.common_tags, {
    Name = "${local.vpc_name}-alb"
  })
}

resource "aws_lb_target_group" "nginx_http" {
  name        = "${local.vpc_name}-nginx-tg-http"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "instance"

  health_check {
    path                = "/" # Adjust health check path as needed
    protocol            = "HTTP"
    matcher             = "200-399"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
  
  tags = merge(local.common_tags, {
    Name = "${local.vpc_name}-nginx-tg-http"
  })
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_lb_listener" "https" {
  count             = var.ssl_certificate_arn != null ? 1 : 0
  load_balancer_arn = aws_lb.main.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08" # Choose appropriate policy
  certificate_arn   = var.ssl_certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.nginx_http.arn
  }
}

# Attach Nginx instances to Target Group
resource "aws_lb_target_group_attachment" "nginx" {
  # count            = var.nginx_instance_count
  count = 1
  target_group_arn = aws_lb_target_group.nginx_http.arn
  target_id        = aws_instance.nginx_proxy[count.index].id
  port             = 80
}

# Storage (Backups)
resource "aws_s3_bucket" "backups" {
  bucket = local.s3_bucket_backup_name
  # acl    = "private" # Using bucket policy and IAM roles for access control

  tags = merge(local.common_tags, {
    Name = local.s3_bucket_backup_name
    Role = "backup-storage"
  })
}

resource "aws_s3_bucket_acl" "backups_acl" {
  bucket = aws_s3_bucket.backups.id
  acl    = "private"
}


resource "aws_s3_bucket_versioning" "backups_versioning" {
  bucket = aws_s3_bucket.backups.id
  versioning_configuration {
    status = "Enabled" # Or "Suspended"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "backups_encryption" {
  bucket = aws_s3_bucket.backups.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "backups_public_access" {
  bucket = aws_s3_bucket.backups.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "backups_policy" {
  bucket = aws_s3_bucket.backups.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid       = "DenyIncorrectEncryptionHeader",
        Effect    = "Deny",
        Principal = "*",
        Action    = "s3:PutObject",
        Resource  = "${aws_s3_bucket.backups.arn}/*",
        Condition = {
          StringNotEquals = {
            "s3:x-amz-server-side-encryption" = "AES256"
          }
        }
      },
      {
        Sid       = "DenyUnEncryptedObjectUploads",
        Effect    = "Deny",
        Principal = "*",
        Action    = "s3:PutObject",
        Resource  = "${aws_s3_bucket.backups.arn}/*",
        Condition = {
          Null = {
            "s3:x-amz-server-side-encryption" = "true"
          }
        }
      },
      {
        Sid    = "AllowSSLRequestsOnly",
        Effect = "Deny",
        Principal = "*",
        Action = "s3:*",
        Resource = [
            aws_s3_bucket.backups.arn,
            "${aws_s3_bucket.backups.arn}/*"
        ],
        Condition = {
            Bool = {
                "aws:SecureTransport" = "false"
            }
        }
      }
    ]
  })
}

# DNS (Optional)
resource "aws_route53_record" "app_dns" {
  count   = var.domain_name != null && var.route53_zone_id != null ? 1 : 0
  zone_id = var.route53_zone_id
  name    = var.domain_name
  type    = "A"

  alias {
    name                   = aws_lb.main.dns_name
    zone_id                = aws_lb.main.zone_id
    evaluate_target_health = true
  }
}