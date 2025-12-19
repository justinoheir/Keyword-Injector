---
id: "069"
slug: "automating-optimizing-best-candidate-hiring"
title: "Automating & Optimizing Best Candidate Hiring Platforms with Perfect"
word_count: 742
themes: ["terraform", "data-analytics", "case-study", "genai", "devops", "migration", "aws", "security"]
extraction_date: "2025-12-19"
content_hash: "3022542f52a3"
---

# Automating & Optimizing Best Candidate Hiring Platforms with Perfect

## Introduction

• Customer Success

January 6, 2025

## Background

Perfect is developing a cutting-edge AI and Big Data solution that is targeting the recruitment market. They are a team of seasoned professionals both in technology and the human resources space, coming from industry-leading companies, and backed by top investors from the local ecosystem.

Their solution allows the end-user to instantly connect with the next-best-hire through features that find candidates who are most likely to join the company, and use contextual data to start meaningful conversations that stand out from the noise.

## The Challenge

Perfect had already adopted Databricks as a primary platform but was limited by a centralized environment that did not allow for the isolation of production and non-production environments or the implementation of user segregation. Additionally, the lack of a declarative approach made it difficult to effectively manage the overall configuration.

Perfect was seeking to optimize and standardize its Databricks environment on AWS through the implementation of best practices for both AWS and Databricks infrastructure resources. This included the establishment of consistent workload environments with no configuration snowflakes, a single source of truth for the desired environment configuration in code, and the ability to declaratively manage Databricks jobs and clusters. The goal was to enable fully automated testing and promotion of features/changes across multiple workload environments, as well as strict access controls between environments and fully automated data replication from production to staging environments.

Additionally, Perfect aimed to improve observability through comprehensive logging and monitoring and to better control and manage overall compute and platform costs.

## Our Solution

Perfect engaged OpsGuru, an AWS Premier Tier Services Partner, due to the team’s extensive AWS and Databricks experience and a proven track record with complex workload migrations. With OpsGuru’s help, Perfect was able to improve its Databricks configuration by fulfilling all of the identified requirements.

OpsGuru identified 4 resource layers that needed to be implemented, in order to achieve efficient scaling and workload isolation requirements:

1\. Infrastructure Layer

• AWS Resources:

• VPC

• Bastion hosts

• Security (IAM, CMK)

• Storage (S3)

• DBMS (RDS)

2\. Bridge Layer

• Database MWS Configuration

• Credentials

• Storage Configuration

• Network

• Databricks Workspace(s)

3\. Configuration Layer

• Resources within the Databricks Workspace

• Cluster Policies

• Instance Pools

• Libraries

• Secrets

• User roles/groups/permissions

• DBFS Mounts

4\. Application Layer

• DBX managed application-specific resources (e.g., Jobs, tables, repos)

All of the layers are managed declaratively in a fully automated manner through Infrastructure as Code (IaC) and CI tools.

Multiple Environments

Different workload environments (e.g., development, staging, production) are managed through multiple instances of the above-defined layers. This approach allows complete isolation and reduces the potential attack surface as the environments have no dependencies on each other and are completely unaware of each other.

IaC allows consistent environment configuration across the whole ecosystem with no manual, snowflake environments.

## The Result

OpsGuru worked alongside the Perfect engineering team to implement the above-presented architecture. This process ensured that Perfect was able to rapidly deploy and promote workloads across fully isolated Databricks environments (workspaces).

• Environment Isolation

Multiple Databricks workspaces allowed engineering teams to frictionlessly manage and promote workloads and their artifacts through different stages.

• Resource layers isolation

Through four identified resource layers, Opsguru helped Perfect to define the separation of concerns across various layers of the architecture, without introducing additional overhead to the engineering teams.

• Declarative architecture

With the effective implementation of the IaC through Terraform with Databricks and AWS providers, Opsguru allowed Perfect to have a single source of truth for the complete architecture, from Databricks to AWS, without any manual steps or snowflake behaviour as before.

• Continuous integration and deployment

Implementation of the IaC allowed Perfect to treat the complete infrastructure the same way as application code, providing them the possibility to implement a fully automated CI/CD process integrated into the existing Git workflows with GitHub Actions.

OpsGuru then assisted the Perfect team in their migration to the newly built Databricks platform by providing the data, configuration migration plan, and execution.

After the completion of the project, OpsGuru provided comprehensive training sessions for the Perfect team as well as documentation and operational playbooks for the newly designed systems. The training and documentation included the operation of the Databricks configuration and environment deployment, AWS configuration, and deployment, among other topics.