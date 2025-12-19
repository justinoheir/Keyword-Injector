---
id: "010"
slug: "the-current-state-of-kubernetes-on-aws-kubernetes"
title: "The Current State of Kubernetes on AWS: Kubernetes Security, Scalability, Performance Engineering & More, Part 2"
word_count: 1109
themes: ["data-analytics", "genai", "devops", "migration", "kubernetes", "aws", "security"]
extraction_date: "2025-12-19"
content_hash: "b02095442318"
---

# The Current State of Kubernetes on AWS: Kubernetes Security, Scalability, Performance Engineering & More, Part 2

## Introduction

In the first part of our two-part post on the current state of Kubernetes in AWS, we discussed how Kubernetes can help you handle stateful workloads with persistent data storage and standardize your application and data engineering approaches. We also shared how different AWS services can support Kubernetes cluster management.

In the second part of this post, we’re diving into topics like Kubernetes security, Kubernetes scalability, next-level cloud economy, performance engineering, and more to further unpack the current state of Kubernetes in AWS.

## Kubernetes Security

Security is a pervasive topic, it is present at every layer of the stack and AWS makes it easier all the way.

Either running on EKS, EKS-A or even on EC2, you can authenticate using the standard authentication service in AWS, IAM. Users and roles can authenticate against the cluster and then be mapped to a series of RBAC roles that will scope out their access level to the cluster.

If your workloads need access to AWS resources, IAM Roles for Service Accounts (IRSA) has your back, allowing you to create IAM roles that trust a Kubernetes service account, securely providing credentials to workloads.

You can consume secrets from the AWS SSM Parameter Store, AWS Secrets Manager directly from those services (see the previous paragraph on IRSA), or through integrations like External Secrets, or even mounting them as volumes using the Secrets Store CSI driver.

Network Policies can manage access to your workloads by labels and IP addresses, but if you need your workload to be part of a security group, you can attach one to your pods thanks to the AWS VPC CNI driver.

## Kubernetes Scalability

In order to leverage Kubernetes and scale to handle thousands or millions of customers for your application stack, autoscaling your workloads is a big requirement.

Like we briefly mentioned in the Working Backwards section, Kubernetes allows you to handle scaling of your workloads in different ways.

By default, a properly set up cluster will monitor metrics for each workload running, like memory and CPU utilization, which can then be leveraged for scaling your workloads.

Horizontal Pod Autoscaling (HPA), will handle scaling replicas of your workloads. For applications that can handle more traffic by simply running more copies, it’s the perfect fit.

Vertical Pod Autoscaling (VPA), will increase the resource reservations for a running workload, instead of increasing the amount of replicas, which is the perfect fit for applications that scale by having more resources available. This is usually the case with legacy applications.

Now CPU and Memory might not be the best way to scale your application, you might need more replicas according to the size of some message queue, or more resources according to the number of requests you’re getting. To scale based on custom metrics there are several projects available to add this functionality into Kubernetes, from which Keda is one of the most comprehensive, allowing you to scale based on a series of data sources.

## Cost-effective / Next-Level Cloud Economy

AWS Savings Plans and Reserved Instances continue to be extremely popular with the Kubernetes community. When leveraging these for Kubernetes, make sure to properly prepare your cluster’s node groups according to your workload’s needs, and also leverage Spot Instances as much as possible.

You should also have the AWS Node Termination Handler to help your nodes terminate gracefully whenever a disruption event occurs. Trust us, people cry without this 😀

## Performance Engineering

We often help customers through challenges related to performance and troubleshooting at scale. Observability is critical, so leveraging monitoring tools like Thanos and Prometheus are critical, if not ISVs that specialize in Kubernetes such as Fairwinds Insights.

Collecting metrics is easy, making sense of them requires insight into how all the Kubernetes components work and interact with each other and the AWS infrastructure. To help make sense of this sea of data we can use Grafana, or Amazon Managed Grafana, to visualize it through dashboards, bringing together data from Prometheus/Thanos, Cloudwatch and a series of other data sources.

## Skills Development

Last, but definitely not least, is the whole area of skills development.

Our recommended prerequisite at OpsGuru for Solutions Architects and Cloud Engineers who have an interest in learning more about Kubernetes and already have foundational or Associate / Professional certifications on AWS is to get hands-on experience with local distributions and set a path towards Linux Foundation certification.

If you’re already familiar with core cloud computing concepts, a great start is by setting a path towards achieving the recently released Kubernetes and Cloud Native Associat (KCNA) certification.

From there, you can select your path towards any of the 3 core Kubernetes certs, depending on your interest and degree of specialization.

• Certified Kubernetes Administrator (CKA)

• Certified Kubernetes Application Developer (CKAD)

• Certified Kubernetes Security Specialist (CKS)

## Conclusion

AWS provides managed Kubernetes services in the cloud, which can be extended to on-premises environments with EKS Anywhere. With the wide support across cloud, hybrid and on-premise, Kubernetes is the perfect answer to portability and flexibility across vendors and geographies.

In conclusion, the Kubernetes on AWS ecosystem continues to grow on a daily basis, so keep learning and keep trying new things\! We encourage you to reach out if you have any questions, or are looking to accelerate your projects with Kubernetes enablement support.

Are you interested in working with leading-edge technologies? OpsGuru is always looking for highly skilled engineers and architects. Visit our careers page to find the role that’s right for you.

Interested to learn more? Check out part 1 of The Current State of Kubernetes on AWS: Kubernetes Security, Scalability, Performance Engineering & More

## Written by:

Fernando Battistella, Principal Architect at OpsGuru – Fernando has over two decades of experience in IT, with the last six years architecting cloud-native solutions for companies of all sizes. Specialized in Kubernetes and the Cloud Native ecosystem, he has helped multiple organizations design, build, migrate, operate and train their teams in cloud-native technologies and platforms.

Bill Hunka, Account Executive at OpsGuru – Bill has over 15 years of sales and business development experience supporting customers across Canada and the Western US. After spending 10 years at a Vancouver-based SaaS security leader, Bill pivoted to work with HPC and scale-out customers with focused industry vertical solutions. Over the past 5 years with his head in the “Clouds”, he’s built his skills by diving deep with his customers’ data-driven initiatives, helping to plan out migrations at scale, and driving DevOps-focused transformations.