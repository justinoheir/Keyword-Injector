---
id: "029"
slug: "when-isolation-and-silos-are-good-data-stores-in"
title: "When Isolation and Silos are good: Data stores in a multi-tenant solution"
word_count: 1772
themes: ["terraform", "data-analytics", "genai", "kubernetes", "serverless", "aws", "containers", "security"]
extraction_date: "2025-12-19"
content_hash: "c2d6b16dc531"
---

# When Isolation and Silos are good: Data stores in a multi-tenant solution

## Introduction

We have explored earlier in this post on a number of points to consider in setting up a multi-tenant Amazon EKS cluster. However, while it is important to safeguard multi-tenancy on the application cluster, it is equally important — in fact, arguably more so — to safeguard multi-tenancy for data stores.

AWS offers a comprehensive portfolio of data stores, making it a very compelling choice for a SaaS offering platform with Financial services DevOps with Banking cloud consulting with SOX compliance cloud.... However, securing and isolating these data stores in a multi-tenant, highly regulated environment brings its own set of challenges.

## Multi-tenancy on Datastores

At managing multi-tenant data, “silo” is the goal. Here are a few reasons that support clear tenant-based data partitioning in a multi-tenant SaaS solution with Financial cloud migration with PCI DSS cloud consulting.

## Cross-tenant access should generally be denied

Data security is a high priority topic in a SaaS solution – not only for protection against external entities but also for security between tenants. Even in the case of inter-tenant collaboration, cross-tenant data access needs to be strictly controlled and monitored, and access should be granted based on business logic rather than direct datastore access.

## Different Encryption and Security Requirements required by Industry Standards

Depending on the industry, the tenants may be subject to different compliance standards. Some require data encryption with a clearly mandated frequency of encryption key rotation, while other standards require tenant-specific encryption keys instead of shared keys. By clearly identifying data assets associated with individual tenants, the different encryption and security controls as required by different compliance standards can be applied to individual tenants only as needed.

## Clear Performance Tuning based on the Tenant Subscription

While tenants follow the same general workflow as offered by the SaaS provider, each tenant may sign up to different sets of features and performance thresholds based on the tier the tenant is in. In a tiered pricing model, some tenants are willing to pay for high volumes of usage, while non-paying customers often have lower performance expectations. As a SaaS provider, it is necessary to monitor the usage of individual tenants and ensure the adherence to the performance promised by the service-level agreement. This does not only ensure that the resources are not monopolised by tenants but also supports clearer identification of up-sell opportunities.

## Easy Data Management

As the SaaS service grows, the number of tenants grows while some tenants will inadvertently decide to adopt other services. When a tenant unsubscribes from a SaaS offering, the tenant may expect the data to be fully exported and the historical data be deleted permanently from the SaaS solution. Given “right to erasure” is one of the key protections in the European Union (EU) General Data Protection Regulation (GDPR), a SaaS provider needs to support that by clearly identify data assets of individual tenants for proper lifecycle management.

## Techniques to Address Multi-tenancy on Datastores

It should be emphasised that there is no “one rule to fit all” at setting up tenant datastore silos because each solution will need to address its particular requirements.

A comprehensive solution depends on factors like service-level agreements with the tenants, read/write access patterns, compliance and regulatory requirements, and last by not least; costs. There are a number of data partitioning and isolation techniques that should be considered based on the requirements. Let us demonstrate the methods using a relational database such as Amazon Aurora.

## Tenant-id based data partitions on shared database and instances

In this case, a table is shared amongst the tenants, but the individual tenant data is separated and identifiable by a tenant\_id key.

The authorization happens on the actual relational database via the “row-level security” feature. Access of the application is based on an access policy that takes the tenant identity into account.

• It is cost-efficient.

• Authorization is enforced on the database level. It implies that there will be more than one authorization mechanism in the solution leveraging both AWS IAM and individual database policies.

• Custom application logic has to be developed for a microservice to make sure it is aware of tenant-id.

• No guardrails against potential “tenant noise” – service-level agreement based on tiers of tenants cannot be enforced.

• AWS CloudTrail cannot be used to keep track of access actions, because authorizations happen on the database level. Applications will need to compensate by logging the pertinent information extraneously instead for troubleshooting and tracking.

## Data schema isolation on shared instances

In this case, the tenancy is still shared on the instance level. However, the data siloing happens on the database level. This makes AWS IAM authentication and authorization possible.

• It is cost-efficient.

• AWS IAM is solely responsible for the authentication and authorization mechanism.

• Because AWS IAM is in charge of access, the full audit trail is available on AWS CloudTrail without adjusting the logging on individual applications.

• Because the underlying database instances are still shared by the tenants, it is not possible to defend against potential “noisy tenants”; service-level agreement based on still tiers of tenants cannot be enforced.

## Database instance isolation per tenant

1\. Database instance isolation per tenant

In this case, we have a complete tenant-based database and instance isolation. This solution is by far the most secure and reliable amongst the options because on top of the AWS IAM and AWS CloudTrail audit features there is also complete tenant isolation.

• Both authentication & authorization are managed by AWS IAM.

• The full audit trail is available on CloudTrail because AWS IAM is responsible for access control.

• Complete noise isolation per tenant.

• The total costs will be higher because of the database and instance isolation between tenants.

## How Applications can access the multi-tenant data

Being able to store the data in a tenancy isolation model that aligns with business requirements is essential, but regardless of methods, it is important to ensure the applications can access the data accordingly.

Fortunately, if you are using primarily AWS IAM for access control (as illustrated in both data schema and full instance isolations earlier), most of the work is already done. AWS IAM can be readily used by applications to access the data associated with the current tenant. Let us walk through this in the example Amazon EKS.

In EKS, pod-level IAM access can be achieved by using OpenID Connect (OIDC) identity provider together with Kubernetes service account annotations, as it enables an exchange of JWT with STS to offer the applications temporary access to relevant cloud resources. With this approach, no extended permission to the underlying Amazon EKS worker nodes is required. Instead, you can scope only the IAM permissions to the service account associated with the pods, based on the actual permissions the application (running as part of the pod) requires. Other than fine-grained control of permissions based on the applications/pods, another immediate advantage is the ability to have audit trail since each API call by an EKS pod will be logged by AWS CloudTrail to satisfy auditing needs.

The IAM integration, therefore, supports a comprehensive “tenant-aware” authorization system that fronts the access to the data stores. This adds another level of security as we do not blindly rely on database connection strings (that only controls access via authentication).

## Example: Amazon EKS accessing a multi-tenanted AWS DynamoDB table

To further illustrate the multi-tenant access, let us take a look at how an application running Amazon EKS can access a multi-tenanted Amazon DynamoDB. Often, multi-tenancy on Amazon DynamoDB is implemented on the table-level (i.e. table and tenant are in a 1:1 relationship). The following AWS IAM policy (called ‘‘aws-dynamodb-tenant1-policy”) illustrates this access pattern, where all data is associated with Tenant1.

{ "Version": "2012-10-17", "Statement": \[ { "Sid": "Tenant1", "Effect": "Allow", "Action": "dynamodb:\*", "Resource": "arn:aws:dynamodb:${region}-${account\_id}:table/Tenant1" } \] }

Next, we need to associate this role with an EKS cluster service account leveraging OpenID.

eksctl utils associate-iam-oidc-provider \--name my-cluster \--approve \--region ${region} eksctl create iamserviceaccount \--name tenant1-service-account \--cluster my-cluster \--attach-policy-arn arn:aws:iam::xxxx:policy/aws-dynamodb-tenant1-policy \--approve \--region ${region}

To leverage the newly created service account ‘‘tenant1-service-account”, the pod definition will contain the necessary “serviceAccountName” specification.

apiVersion: v1 kind: Pod metadata: name: my-pod spec: serviceAccountName: tenant1-service-account containers: \- name: tenant1 …

While the IAM service account and the IAM policy is tenant-specific, static, and managed by configuration management tools such as Terraform and Ansible, the pod specification can be more dynamically configured. If you are using a templating engine like Helm (note: Helm supports lot more functionalities beyond that, templating is only one of its key features), the “serviceAccountName” can be set as a variable and set to the corresponding tenant-based service account depending on the deployment. It implies that each tenant will have its own dedicated deployment of the same application — in fact, each tenant should have its own dedicated namespace where the tenant-specific applications are running (a point much belaboured in the previous post).

Similar examples can be drawn using Amazon Aurora Serverless, Amazon Neptune and Amazon S3 buckets. However, because of the length and the details involved, we will address the discussion in future posts.

## Summary

At creating a SaaS offering, it is important to consider carefully how data is accessed based on the different storage, encryption, performance and management requirements from the tenants. We have examined a few ways to partition data and showcased that there is no unified approach for data multi-tenancy. The advantage of running multi-tenant workloads on AWS is the availability of AWS IAM, which can be used to simplify tenant-based data access control and how applications can access the data dynamically based on the tenant.

Naturally, this blog only offers a high-level overview of a number of considerations and solutions. As every workload is different, some generic patterns are preferred over others, a comprehensive solution needs to be carefully designed after analysing applicable factors and anticipated requirements.

If you’re considering hosting your SaaS service on AWS and are looking for opportunities to improve on cost efficiencies or revise the security posture – We’d like to learn more about your use case and work with you to build a solution that suits your needs\!

Simply reach out to info@opsguru.com

Written by: Paul Podolny & Mency Woo