---
id: "067"
slug: "kubernetes-development-environment-for-ml-in"
title: "Kubernetes Development Environment for ML in Amazon EKS"
word_count: 603
themes: ["terraform", "gcp", "case-study", "genai", "devops", "kubernetes", "aws"]
extraction_date: "2025-12-19"
content_hash: "e248db9ae7ea"
---

# Kubernetes Development Environment for ML in Amazon EKS

## Background

This client is a company that leverages AI to generate photos for use in the fashion industry. They unite a team of experts with the perfect combination of skills to revolutionize fashion visuals. With vast experience in computer vision, AI, media, and usable enterprise products, they are committed to transforming the fashion industry through the use of synthetic media.

## The Challenge

The client faced several challenges in developing a more efficient and cost-effective development environment for ML. First, their previous solution using GPU instances in GCP was too expensive and slow. Second, they needed a solution that would enable their developers to carry out the development process and training experiments in a more streamlined and efficient way.

## Our Solution

To address these challenges, OpsGuru created a development environment for ML using EKS and GPU instances on Amazon Web Services (AWS). This provided the client with a faster and more efficient development environment than they previously had. The developers were able to SSH into the pods to carry out the development process and could use Kubernetes jobs to carry out training experiments.

OpsGuru used Terraform to create the environment, which helped to automate the process and ensure consistency across the entire environment. This also allowed OpsGuru to deploy the environment quickly and efficiently while minimizing the risk of errors.

OpsGuru proposed building an ML development environment using Terraform to automate the environment creation process, as well as EKS and GPU instances on AWS to provide the necessary infrastructure for training ML models.

To implement the solution, OpsGuru followed the following steps:

Step 1: Use Terraform to automate environment creation

OpsGuru used Terraform to automate the process of creating the ML development environment on AWS. This allowed the client to create and manage the environment in a more efficient and cost-effective way.

Step 2: Set up the EKS cluster

OpsGuru set up an EKS cluster using a combination of managed AWS services and open-source tools. This provided a scalable and reliable platform for running ML workloads.

Step 3: Configure GPU instances

To accelerate the training process and reduce costs, OpsGuru configured GPU instances to be used in the development environment. Thus allowing the client’s development team to train models more quickly and efficiently.

Step 4: Set up a development environment

OpsGuru set up the development environment, including pods and Kubernetes jobs, to enable the development team to carry out ML experiments. The development environment was designed to be flexible and scalable, allowing the team to run multiple experiments in parallel.

## The Result

The project was a success, and the company’s CEO expressed satisfaction with the results, stating, “I really enjoyed working together and very happy with the results”. By leveraging OpsGuru’s expertise in cloud-native technologies and extensive experience with the AWS platform, the company was able to achieve its goal of developing an efficient and cost-effective development environment for ML including:

• A cost-effective and scalable environment by leveraging Terraform automation and utilizing GPU instances on the AWS platform.

• Faster model training times, thus allowing them to iterate more quickly on their AI models.

• A scalable and flexible development environment that could accommodate multiple experiments in parallel.

• The new environment has enabled their developers to work in a more streamlined and efficient manner while avoiding the high costs and slow performance they had experienced in the past.

As a result of this project, the client was able to train its AI models more quickly and cost-effectively, thus gaining a competitive advantage in the fashion industry.