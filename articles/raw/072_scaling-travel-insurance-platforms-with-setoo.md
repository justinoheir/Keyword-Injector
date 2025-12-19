---
id: "072"
slug: "scaling-travel-insurance-platforms-with-setoo"
title: "Scaling Travel Insurance Platforms with Setoo"
word_count: 1271
themes: ["data-analytics", "case-study", "genai", "devops", "aws", "containers", "security"]
extraction_date: "2025-12-19"
content_hash: "377608d033c5"
---

# Scaling Travel Insurance Platforms with Setoo

## Introduction

• Customer Success

January 6, 2025

## Background

Setoo’s award-winning insurance-as-a-service platform empowers e-businesses (such as online travel agents, accommodations, ticket sellers, e-commerce) to independently build and distribute personalized, claims-free insurance products. The products are integrated directly into the customer journey to provide a seamless purchasing experience.

## The Challenge

Setoo had identified a business opportunity by streamlining the insurance purchase process.

While a sound business concept was essential, business success also depended on strong execution. Setoo recognised the need to engage trustworthy and dependable partners to bring the concept into fruition.

As Setoo identified Amazon Web Services to be the ideal cloud provider because of the rich features and the maturity of the platform, Setoo needed a partner who could rapidly define and rollout an architecture following cloud best practices and provide the thought leadership necessary on the journey to adopt cloud-native designs. To set it up for success and hyper-growth, Setoo wanted a partner who could take ownership of the infrastructure and build it based on evolving needs, such that the Setoo team could focus on growing the Setoo core products and continuing building its distinct advantages.

## Our Solution

In OpsGuru, Setoo saw the qualities they were looking for in developing the Setoo platform.

OpsGuru identified a number of critical features Setoo required, including rapid delivery and update of systems to deliver features, extensibility in the design such that new features could be easily and quickly added, scalability of the system to service the growing demands, and cost-efficiency to sustain the system while the team expanded to different markets. End-to-end security was indispensable to the workload too.

## Cloud Launchpad – Extensibility, Security and Compliance Readiness

To efficiently deliver a baseline and facilitate team adoption of the AWS platform, OpsGuru deployed the Cloud Launchpad, which featured:

• Account isolation per environment.

• Full AWS API level audit leveraging AWS Cloudtrail shipped to separate Security Escrow account used by security analysts.

• Certificates automatically managed & renewed by AWS Certificate Manager.

• Full encryption at transit and rest leveraging KMS and TLS.

• VPC isolation per environment, with peering configured with shared VPC used to host the shared workloads such as the centralized CI/CD on Jenkins and container repository using Amazon Elastic Container Registry.

The Cloud Launchpad was not only a kickstart toolkit but also a solid foundation that included vulnerability scanning and auditing capabilities. With the foundation in place, Setoo earned the peace of mind knowing that they could focus on further enhancing their platform instead of having to worry about future security features and compliance requirement retrofitting.

## Cloud-Native Application Design

While OpsGuru delivered Cloud Launchpad to create an infrastructure baseline for the Setoo services, it was also important for OpsGuru to support the Setoo team at creating a solution that would take advantage of the design.

Microservices pattern was advocated as a cloud-native design because the modularity of architecture made delivery, testing and release of specific features faster and less challenging, the design pattern also made scaling individual stages of workloads as required by the customers a lot more rapidly and cost-efficient. To that effect, OpsGuru delivered a Spring Boot template, which incorporated best practices for connectivity with databases, queuing systems, configuration and secrets management. By leveraging the template, the Setoo development team was able to confidently deliver new features following a framework that had already been tested and proven working. Multitenancy design was also incorporated in the template, as multi-tenant architecture offered the most efficient use of the infrastructure and standardised access patterns.

An automated CI/CD workflow would make the delivery of the microservices a sustainable process, especially as the number of features and microservices grew. OpsGuru delivered a full-fledged CI/CD system to empower the team with a mechanism to introduce and update the services. Service delivery was not the only goal of the CI/CD system; as sufficient testing needed to run before rolling upgraded services out to all users, OpsGuru also included canary deployment and UI (Selenium) testing in the CI/CD workflows.

## Holistic System Elasticity, High Availability and Resiliency

A cloud platform supporting insurance as a service must consider elasticity, high availability and resiliency.

Service scalability and resilience was achieved by running all stateless applications on AWS Elastic Container Service (ECS) spanning three availability zones for maximum redundancy. Cost-optimized auto-scaling policies leveraging spot instances were implemented for maximum cost efficiency – these helped with supporting workload spikes during high traffic hours while still remaining cost-efficient.

For proactive observability, OpsGuru provided a comprehensive solution which included metrics dashboards and log analysis leveraging AWS CloudWatch as well as distributed application tracing leveraging Zipkin.

The cloud infrastructure delivered by OpsGuru also supported multi-tenancy, as a multi-tenant system could minimise management overhead and utilise the cloud resources more optimally. Armed with the metrics and proactive monitoring, Setoo had the capability to scale the multi-tenanted solutions ahead to ensure no visible impact on end-users.

The initial architecture aside, the entire system was not signed off until OpsGuru and Setoo were able to perform multiple rounds of load tests to ensure performance criteria of elasticity, high availability and resiliency were satisfied.

## Data Insights and Continuous Growth

To support continuous growth, Setoo needed to have insights on the engagement with the system evolved.

After examining the data collected by the Setoo platform, OpsGuru created a workflow to help the team readily report on the data. As the data source was primarily in the Amazon RDS (MySQL) database, AWS Glue ETL processes to retrieve the relevant data and store it in S3 in data-partitioned Parquet format. AWS Glue crawler processes were then run on the S3 data to populate the AWS Glue data catalogs, such that Amazon Athena was deployed to execute specific queries to obtain business insights. Finally, Amazon Quicksight was also set up to connect to AWS Athena, such that charts and dashboards were readily available to make the business insights more accessible.

This foundation enabled Setoo to build a secure system that included vulnerability scanning, auditing capabilities and machine-learning-based threat detection.

## The Result

OpsGuru collaborated with Setoo to create a SaaS platform. A fully compliant and enterprise-grade cloud environment was delivered on day one.

Given the automation of their infrastructure deployments, operational risk had been significantly reduced. All infrastructure and application changes were fully tested and validated in identically configured environments before being promoted into production. Developer velocity was also increased as a result of the automation, which was instrumental in maintaining Setoo’s edge in a competitive market space. Their highly available deployment allowed Setoo to maintain customer satisfaction by making sure customers were always served, even under unexpected circumstances.

• To fully enable the team to use the platform, OpsGuru created Spring Boot templates for the teams to create new microservices more conveniently. A CI/CD pipeline was delivered as well to take advantage of the speed and limitless expandability of the cloud.

• Furthermore, the solution featured easy business data processing. With the data pipeline established to retrieve business insights from the Amazon RDS MySQL data source, near real-time analytics, were readily available through the charts and dashboards on Amazon Quicksight. The Setoo team now could easily analyse the engagement data to design more features feeding into the innovation in the insurance-as-a-service space.

• By providing ample staff training and handover documentation, OpsGuru ensured that Setoo is empowered to continue the enhancement of their platforms and to continue to evolve faster than their competitors.