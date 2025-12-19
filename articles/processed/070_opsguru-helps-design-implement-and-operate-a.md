---
id: "070"
slug: "opsguru-helps-design-implement-and-operate-a"
title: "OpsGuru helps design, implement and operate a multi-regional platform on AWS"
word_count: 398
themes: ["terraform", "data-analytics", "case-study", "genai", "devops", "migration", "serverless", "aws"]
extraction_date: "2025-12-19"
content_hash: "56d2ae022108"
---

# OpsGuru helps design, implement and operate a multi-regional platform on AWS

## Introduction

• Customer Success

January 6, 2025

## Background

The Vancouver-based company under consideration is a well-established mining company with a strong financial foundation. Focusing on gold production, the company manages a diverse portfolio of mines across the Americas. The organization is constantly exploring ways to produce gold in a efficient, sustainable and sociably responsible manner.

## The Challenge

The company pursues a high growth and high yield strategy, which is sustained by close oversight on asset transactions, material costs and operational expenditure. Such sensitive business data is stored in the different ERP systems across the different regions with Financial services AWS with Banking modernization... It is essential to keep its mission-critical ERP systems secure and available to promote the company’s continued success. Meanwhile, because of the ERP systems are set up and maintained by regional teams using different technologies, sharing a uniform architecture and standardized operating procedures is extremely challenging.

## Our Solution

OpsGuru was engaged to design, implement and operate a multi-regional platform on AWS, which would host mission-critical ERP systems and potentially other assets and support workloads to be operated using a standardized playbook.

The platform was developed using infrastructure as code (Terraform), such that new regions to support multi-region resilience could be easily added. However, migrating the ERP systems to AWS on the newly created platform was only the first step; it was more even important to ensure system availability through data backup, system monitoring, rapid responses. A full resilience workflow was deployed leveraging AWS Backup, Amazon CloudWatch, Amazon Lambda. All the workflows were executed in internal network contained within AWS VPC. DevOps best practices were also followed by setting up isolated environments emulating production, such that the full workflow could be tested before production adoption.

## The Result

As a result of the engagement, OpsGuru enabled the company to migrate already two of the largest ERP systems onto AWS. The resilience procedures have been tested for both of the systems. The runbooks and records of the resilience tests were instrumental for the company to pass third-party independent review, such that the company remained in good standing. The streamlined workflow also grew confidence in the different teams of the company. New workloads are currently being elaborated to support further AWS adoption, and to take advantage of the resilient and cost-effective designs.

## 

• Customer Success