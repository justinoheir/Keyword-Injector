---
id: "008"
slug: "the-state-of-kubernetes-in-aws-persistent-data"
title: "The State of Kubernetes in AWS: Persistent Data Storage, Application Engineering and More"
word_count: 1151
themes: ["company-news", "cloud-consulting", "data-analytics", "genai", "devops", "migration", "kubernetes", "aws", "containers", "security"]
extraction_date: "2025-12-19"
content_hash: "a2b94b5beee6"
---

# The State of Kubernetes in AWS: Persistent Data Storage, Application Engineering and More

## Introduction

When it comes to orchestrating containerized workloads, there are several options in the market, with Kubernetes being the most adopted and sought-after solution and container orchestration,.

Here at OpsGuru, we’ve achieved the AWS Service Delivery designation for Amazon Elastic Kubernetes Service (Amazon EKS), recognizing that we have proven success in helping customers architect, deploy, and operate containerized workloads on top of Amazon Kubernetes. We see tremendous opportunity within the Kubernetes ecosystem offered by AWS and we would like to share our real life experience with the community.

As we work with startups and ISVs across the globe, a regular pattern that we help match against is being able to focus their Kubernetes on AWS engineering efforts towards a single release and maintenance process for customers that have clients operating across multiple regions and also being able to operate in non-connected environments.

The choices span from Kubernetes on EC2 to fully managed Amazon EKS and EKS Anywhere (EKS-A, for non-connected environments) or even AWS Outposts.

To start your Kubernetes adoption journey, we “work backwards” by defining “Why Kubernetes?” There are various reasons for a team to adopt it, among them the most common are:

• Standardization: Containers allow applications of all kinds to have the same lifecycle, simplifying operational tasks.

• Scalability: Kubernetes allows you to scale your workloads in a variety of ways like horizontal (replicas) and vertical (resource) scaling based on CPU, memory or custom metrics of any kind.

• Attracting & Retaining Talent: Containerization and Kubernetes are technologies that technical talent looks forward to working with.

Knowing your reasons to adopt Kubernetes will help decide on a path to adoption. While Kubernetes solves a lot of problems, it is also a complex platform in itself and having a partner with deep Kubernetes knowledge by your side is crucial for implementation success. OpsGuru can help you in this journey on AWS with expert Kubernetes consulting and cloud-native infrastructure design.

In this two-part post, we will provide an overview of the current state of Kubernetes in AWS and how you can leverage open-source tools and AWS services in your Kubernetes journey.

## Persistent Data Storage, Ephemeral Workloads

Containers are touted as the perfect solution for ephemeral/stateless workloads, but Kubernetes can also help you handle stateful workloads, allowing you to run legacy applications too.

When needing any kind of storage, stateless workloads will most likely default to using memory or a small space in the host. On the other hand, stateful workloads will need persistent storage.

AWS provides a series of solutions that can be used with Kubernetes, like:

• NFS shares can be handled by Amazon Elastic File System (EFS). EFS provides NFS endpoints with unlimited storage.

• Persistent local storage is provided by Amazon Elastic Block Storage (EBS). These volumes are connected to the instance the container is running on, and if it moves to another host, the disk moves with it.

• Temporary storage can be done in memory or using part of the host’s disk, but if you require faster storage, some AWS instance types have local SSD disks that can also be leveraged.

As long as there is a CSI driver for it, Kubernetes can work with your storage solution, by adopting managed options like the EBS and EFS you can reduce the operational burden on your team.

## Application Engineering / Data Engineering for Machine Learning

Kubernetes can help standardize your approaches to application and data engineering.

Technologies like Kubeflow, a machine learning toolkit, can help you focus on the development tasks while it leverages Kubernetes to handle all the operational ones.

Other tools like Helm can help you facilitate onboarding developers by abstracting the sea of YAML required by Kubernetes into a simple configuration file. If you have a small team of developers also handling operations, CDK8s (an AWS project, recently joined the CNCF) will allow you to use your language of choice to generate Kubernetes manifests for your applications.

These tools can help you rapidly scale the adoption of Kubernetes on your organization by lowering the learning curve.

## Operating Model, Operational Excellence and Site Reliability Engineering

Kubernetes, from the outside, has a high degree of operational complexity to contend with. As you peel back the layers, just like a normal operating model involving VMs, Kubernetes has a lot going on behind the scenes.

Thanks to the tremendous ecosystem of tools that are available, evidenced by the ever-growing CNCF Cloud Native Landscape, you can have all that you need to safely manage Kubernetes clusters, supported by AWS services.

The OpsGuru team has deep experience and expertise with peripheral cluster services, and we help our customers leverage the following solutions:

• Prometheus is the standard for metrics collection in Kubernetes, and it is made even easier to manage with Amazon Managed Service for Prometheus.

• Alertmanager, part of the Prometheus project, can route your alerts to a series of services, including Amazon Simple Notification Service, that in turn can integrate with a series of other AWS or third-party services.

• Thanos is a highly available Prometheus setup, with long-term storage capabilities. Think of Prometheus with nearly infinite metric retention, all backed by Amazon S3.

• Argo CD or Flux for GitOps style application deployment into the clusters, using git repositories, like AWS CodeCommit, as the source of truth for your cluster workloads.

• Fluent Bit to ship all your logs to services like Cloudwatch Logs or ElasticSearch with Amazon OpenSearch Service

• External DNS to automatically create Route 53 entries for your services

Like we said, there are as many tools as there are needs for them, and we could do an entire blog series on just this subject. AWS has several services that can facilitate running and managing Kubernetes clusters and their workloads, from provisioning to observing and managing them.

## Conclusion

AWS provides managed Kubernetes services in the cloud, which can be extended to on-premises environments with EKS Anywhere. With the wide support across cloud, hybrid and on-premises, Kubernetes is the perfect answer to portability and flexibility across vendors and geographies. In The Current State of Kubernetes on AWS – Part 2 we will elaborate on Kubernetes security, scalability, cost-effectiveness, performance engineering and skills development.

OpsGuru has achieved the AWS Service Delivery designation for Amazon EKS, recognizing that OpsGuru has proven success in helping customers architect, deploy, and operate containerized workloads on top of Amazon Kubernetes. To learn more, read our press release.

Are you interested in working with leading-edge technologies? OpsGuru is always looking for highly skilled engineers and architects. Visit our careers page to find the role that’s right for you.

Interested to learn more? Check out part 2 of The Current State of Kubernetes on AWS: Kubernetes Security, Scalability, Performance Engineering & More