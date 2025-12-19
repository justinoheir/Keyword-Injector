---
id: "079"
slug: "gitops---why-is-it-relevant-now"
title: "GitOps \- Why is it Relevant Now?"
word_count: 1082
themes: ["terraform", "genai", "devops", "kubernetes", "aws", "containers"]
extraction_date: "2025-12-19"
content_hash: "e23b866b50a5"
--- with Microservices consulting with Serverless architecture.

# GitOps \- Why is it Relevant Now?

## Introduction

Recently there seems to be a lot of talk about GitOps. This impression is certainly reinforced by the sessions and booths during KubeCon San Diego late 2019\. Regardless of the discipline or services, GitOps was the keyword that was constantly repeated. Despite a very branded beginning of the word (Weaveworks, with full credits, has done a great job promoting the concept), it seems to have quickly become a standard. As OpsGuru spends a lot of time working with clients implementing Day2Ops, including managing CI/CD and processes enabling cloud-native workloads, GitOps is such a relevant topic that it needs a deeper look.

## What is GitOps?

When Weaveworks first promoted the term GitOps, it was largely pointing to using Git as the source of truth for Kubernetes manifests and resource configurations. An automated pipeline is set up to run through the validation, test and deployment actions. As a result of the setup, the pipeline is triggered whenever the triggering event (e.g. pull request issued, successful merge to the production branch) is fired. The pre-configured workflows — including necessary tests and validations — generally lead to API calls to the targeted Kubernetes clusters, resulting in, for example, rollout of new versions of applications and services, creation of a new namespace to support a new tenant. The key is that no manual intervention is necessary.

Because Git is the standard option to store source code (including codified configurations), and any DevOps practices will mandate automated pipelines, the GitOps is the logical marriage of source code and automation pipeline. In fact, GitOps is only a slight extension from the infrastructure as code paradigm. After all, the next logical stage for codified infrastructure is a standardised workflow, and what more can be standardised than a predefined automated workflow?

One implicit requirement for GitOps, however, is declarative infrastructure. Declarative code is superior to procedural code because it is idempotent. Because declarative code only specifies desired state of the system post-application, the same desired state is valid regardless of the current state of the system. Kubernetes resources are declarative by nature, infrastructure-as-code tools such as Terraform and CloudFormation are also declaration-driven. Declarative infrastructure is popular because delegating the just-in-time action plan to the controllers of the respective resources is a lot more scalable and manageable. The alternative of determining all the applicable decision flows and execution paths of complex systems is simply not viable.

Figure 1: A typical GitOps pipeline: Git triggers the workflow, resulting in “kubectl apply” at a Kubernetes cluster

## Why GitOps now?

The premise of GitOps is not different from the drivers of CI/CD, namely

• Need for speed: one of the differentiation for Docker and containers is speed, especially when compared to bare-metal servers and virtual machines. The advantage of speedy deployments requires however a process that is equally speedy. The need for speed goes hand in hand with the need for transparency — transparent code leads to quicker knowledge transfer and therefore increases confidence and quality.

• Need for repeatability: one of the primary drivers of using version control is repeatability — that the same software/configuration can be regenerated using the same code. As declarative (and implicitly idempotent) infrastructure and configuration is the expected norm, the code and instructions of the same version are expected to bring up the exact infrastructure, regardless of when the code is executed.

• Need for a single source of truth: this is where Git shines over other version control mechanisms. What can be more convenient than using a version control system that allows developers to collaborate while keeping track of all the divergences and correlations? Git is accessible, it builds on a storage mechanism that is well-known and well-adopted by the majority of developers. Until another version control mechanism is introduced (blockchain\!\!), Git is the binary-based version control that is as good as cemented for most purposes.

• Need for reliability with auditability: having Kubernetes manifests stored in a source code is the first step to reliability, but a proven and reliable mechanism to verify, apply and track the changes is also critical as part of the insurance to the credibility of the process. A standardized workflow that applies the changes is a lot more credible than an engineer being able to get the change and apply manually using “kubectl.”

As such, why is it suddenly so popular? Arguably, it is because of the current features of the Kubernetes ecosystem.

The popularity of Kubernetes-targeted, opinionated CI/CD solutions from different vendors is not only an indicator of the popularity of Kubernetes, but it is also a signal of the need to introduce a platform-as-a-service experience that is thus far largely lacking in Kubernetes.

While Kubernetes grows in its feature set, Kubernetes user experience in the core project is still an area that lags behind the platform. The kubernetes/dashboard project has been attempting to fill the gap. However, a UI that assumes users to have relatively intimate knowledge of the container orchestration platform is still a high entry barrier to most developers whose primary concern is the administration of individual workloads instead of the cluster. Kubernetes is the primary choice of container orchestration, but it does not fulfil the user requirements on looking for a platform-as-a-service experience.

OpenShift arguably is the first product that identifies the need to address the platform-as-a-service gap for the Kubernetes experience. However, while RedHat continuously and heavily contributes to upstream Kubernetes, one cannot help but wonder about the potential divergence between OpenShift and Kubernetes. The slew of products emerging in the market aims to provide a packaged platform-as-a-service experience, including CI/CD, container registry, container scanning services. They aim to strongly reinforce the native Kubernetes platform by providing an experience that abstracts from the complexities of the platform.

In the next two weeks, we are going to explore a number of services available that answer the GitOps needs and compare the features and promises of a number of GitOps hosted services. We are also going to deep-dive into one such offering and examine how it can be incorporated to simplify some CI/CD pipeline setup.

Are you interested in learning how OpsGuru implements CI/CD, Day2Ops and how GitOps aligns with Day2Ops in a solution that works for you? We’d love to discuss a workflow that is customised to your needs\!

info@opsguru.com