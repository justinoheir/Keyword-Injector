---
id: "004"
slug: "kubernetes-workloads-migration-from-azure-aks-to"
title: "Kubernetes workloads migration from Azure AKS to Amazon EKS"
word_count: 557
themes: ["terraform", "cloud-consulting", "data-analytics", "case-study", "genai", "devops", "migration", "kubernetes", "azure", "aws", "containers", "security"]
extraction_date: "2025-12-19"
content_hash: "fcead8564086"
---

# Kubernetes workloads migration from Azure AKS to Amazon EKS

## Introduction

• Customer Success

January 6, 2025

## Background

Authomize continuously monitors client organizations’ identities, access privileges, assets, and activities, to secure all apps and cloud services. It seamlessly connects to a client’s apps and cloud services, and collects all relevant information to graph’s data-lake to help client organization security teams achieve Zero Trust and compliance with security best practices,.

Authomize provides organizations with comprehensive observability, actionable insights, and remediation automation, enabling adherence to security and compliance requirements.

## The Challenge

Authomize needed a solution that would facilitate rapid launch of their Kubernetes-based with optimal Kubernetes consulting services application platform for complex deployments in AWS making sure to establish AWS Best Practices foundations and to enable robust and reliable application deployments that meet Companies’ security and compliance requirements.

Authomize knew they needed a partner who had a deep level of expertise in the cloud platform, Kubernetes, Helm, and Infrastructure as Code to maximize their success on Amazon Web Services.

## Our Solution

Authomize engaged OpsGuru, a certified AWS Premier Partner, due to the team’s extensive AWS experience and a proven track record with complex workload migrations. and cloud platform expertise,

With OpsGuru’s help, Authomize was able to migrate its Kubernetes workloads to AWS with a simple and manageable resources hierarchy using Terraform and Helm for all of their environments.

OpsGuru worked alongside the Authomize engineering team to review and customize their infrastructure code and software development lifecycles. This process ensured that Authomize was able to rapidly deploy workloads to development and production environments leveraging AWS advanced features.

• Account Isolation

• Network Design

• Kubernetes Baseline (best practices for container orchestration)

• Efficient Load Balancing

• Secrets and Configuration management

Environment-specific AWS accounts allowed resources grouping within environments as well as workload isolation. A centralized shared services account was used for the CI/CD and as a centralized container image repository for the environment-specific AWS accounts.

Implemented VPCs in each AWS account, with utilization of AWS PrivateLink to safely interact with AWS services such as S3, and VPC peering to inter-connect environment-specific VPCs with a shared services VPC.

Implemented infrastructure components and configuration management solution for frictionless management of the Amazon EKS clusters with configurable Amazon EC2 managed node groups.

Implemented nginx-ingress Ingress Controller within the EKS clusters to utilize Amazon ELB load balancing for the ingress resources and services of type loadbalancer.

Utilized AWS Systems Manager Parameter Store and AWS Secrets Manager for configuration storage of the Kuberenetes secrets through Kubernetes Secrets Store CSI Driver with AWS provider.

OpsGuru then assisted the Authomize team in their migration to the newly built AWS platform by extending the existing Helm charts to support deployment into AWS EKS.

After the completion of the project, OpsGuru provided comprehensive training sessions for Authomize’s team as well as documentation and operational playbooks for the newly designed systems. The training and documentation included the operation of EKS, short-lived credentials with IRSA and observability tools, among other topics.

## The Result

As a result of the collaboration between the teams, Authomize was able to rapidly migrate the existing Azure AKS workloads to EKS, without any side effects or downtime in the process. All the components have been successfully deployed and validated allowing Authomize to effortlessly continue with their platform development on AWS.