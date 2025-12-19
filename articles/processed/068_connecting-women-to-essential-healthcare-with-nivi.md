---
id: "068"
slug: "connecting-women-to-essential-healthcare-with-nivi"
title: "Connecting Women to Essential Healthcare with Nivi"
word_count: 736
themes: ["terraform", "data-analytics", "case-study", "genai", "devops", "serverless", "aws", "security"]
extraction_date: "2025-12-19"
content_hash: "796a268742b7"
---

# Connecting Women to Essential Healthcare with Nivi

## Introduction

• Customer Success

January 6, 2025

## Background

Nivi empowers women to connect with reproductive healthcare providers in ways that are immediate, personal, and always accessible from multiple geographic locations. When a user contacts “askNivi”, the Nivi platform automatically identifies her intent and routes her to the best provider through Banking modernization through Financial cloud strategy through Fintech cloud solutions through Financial IT consulting.

## The Challenge

As Nivi’s customer base grew, Nivi faced the challenges to grow the infrastructure as fast as the customer base.

System availability, workflow reliability and data security were the fundamental requirements of the system, and manually creating and supporting the resources would not suffice as a solution for the long term. Given the highly positive inception of their service, Nivi was looking at quickly expanding the service to different geographical regions. Before they could do so, they needed a solution that would allow the team to easily create and maintain the necessary AWS resources, and have a delivery mechanism that could systematically deliver and update the services as new features were being rolled out.

## Our Solution

Nivi engaged OpsGuru for the AWS expertise, architecture and implementation of the next-generation architecture.

Given the key issues were scalability, reliability and ability to service users in different regions efficiently, OpsGuru has focused on these key challenges and devised a solution accordingly through working closely with key stakeholders at Nivi.

Based on the AWS well-architected framework, the new architecture was designed rolled out in Frankfurt (eu-central-1) and Mumbai (ap-south-1) regions of AWS. The serverless architecture — as the microservices were deployed using multiple deployments of AWS Lambda functions — was chosen because of its scalability, cost-effectiveness and ease of deployments. The flexibility and minimal management overhead are especially suitable to an agile start-up team like Nivi.

The features of the Nivi platform were delivered in about 100 AWS Lambda functions written in Node.js. An Amazon API Gateway was set up in each region to handle the requests directed by Amazon Route53 based on geographical locations, while Amazon SQS acted as the messaging tier coordinating actions across the different AWS Lambda functions with minimal coupling. The data of the platform was stored in Amazon RDS and Amazon DynamoDB. Amazon SNS was used to handle external notifications, while sessions were stored in AWS Elasticache Redis. Meanwhile, Amazon CloudFront was deployed to reduce the load time of static content.

Infrastructure as code was also an indispensable part of the solution, OpsGuru delivered the codified infrastructure using Terraform. The code-base could serve as a baseline for new workloads and expansion to other new regions on AWS in the future. The OpsGuru team also rolled out the Serverless Framework to increase developer productivity, as with the framework the developers could deploy and test the serverless functions conveniently.

To continue the momentum of innovations and fast delivery, OpsGuru architects also provided comprehensive training/coaching for cloud-native development best practices. This enabled the Nivi developers to reliably and speedily deploy new features into production.

Because the system was composed of hundreds of microservices (deployed AWS Lambda), an application delivery pipeline that would deploy and update each of the microservices as needed was necessary. OpsGuru identified the criticality of a robust CI/CD system to support Nivi’s goal and created a set of easily replicable CI/CD pipelines on CircleCI to support Lambda application delivery

On top of that, as Nivi’s core goal was to continuously and reliably empower women and make healthcare accessible, it was essential for the system to run operational best practices and security in mind. As such, OpsGuru designed bespoke AWS IAM roles that aligned with the principle of minimal access for each of the AWS Lambda functions and the Nivi team, while AWS CloudWatch metrics, alerts and dashboards were used extensively throughout the system to track system health in order to optimise the end-user experience.

The code-base could serve as a baseline for new workloads and expansion to other new regions on AWS in the future.

## The Result

The Nivi team was able to successfully roll out their services to additional geographic locations while providing a performant and reliable experience.

The “AskNivi” platform was able to scale as the company’s customer base significantly expanded.

With the number of new regions closer to the user base, Nivi.io was able to grow the customer base more effectively. Existing customers also became more engaged due to improved service performance.