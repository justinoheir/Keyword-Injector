---
id: "019"
slug: "deep-learning-based-saas-enablement-on-google"
title: "Deep Learning-based SaaS Enablement on Google Cloud"
word_count: 753
themes: ["gcp", "data-analytics", "case-study", "genai", "devops", "migration", "kubernetes", "containers", "security"]
extraction_date: "2025-12-19"
content_hash: "54ad2f85bbed"
---

# Deep Learning-based SaaS Enablement on Google Cloud

## Introduction

• Customer Success

January 6, 2025

## Background

Founded with the aim of simplifying vehicle inspection, Click-Ins introduces AI-driven automated technology that completely redefines its category. Helping insurance and car companies transition from manual procedures to fast and efficient fact-based processes, Click-Ins provides a user experience that is both simpler and more reliable, for all parties involved. To achieve the highest level of transparency and certainty, Click-Ins has developed a hybrid approach to AI.

Using proprietary simulated data to pre-train AI models, and leveraging multidisciplinary technologies, Click-Ins SaaS cloud solution accurately and consistently recognizes and measures any damage and accurately identifies the affected parts, with no training period. With its highly skilled team of technology, automotive, insurance, and business experts, Click-Ins is headquartered in Israel, with offices and partners in the USA, LatAm, and Europe, providing 24/7 service to customers worldwide.

## The Challenge

Click-Ins has already adopted Google Cloud as a preferred cloud provider, however, their environments have been configured in a traditional, non-cloud-native way with the heavy utilization of manually managed VMs that served their SaaS to the customers. This approach prevented the company from scaling to meet the growing business needs as it required a lot of engineering effort. Seeking to optimize their system, the client enlisted the expertise of the OpsGuru team to redesign their solution from the ground up, enabling their SaaS to leverage the full benefits of modern cloud deployments, including elasticity, resilience, and scalability.

## Our Solution

To gain a better understanding of the highly intricate SaaS architecture, OpsGuru has conducted multiple discovery sessions. The SaaS architecture comprises multiple microservices implemented through gRPC, which require very specific GPU resources to publish, optimize and serve Deep Learning models. After carefully examining the SaaS architecture, the joint OpsGuru, and Click-Ins’ engineering team agreed on the necessary changes to optimize the system. The approach involved the utilization of a state-of-the-art container orchestrator – Kubernetes via fully managed Google Kubernetes Engine (GKE) service with the utilization of multiple node groups that provided performant and cost-optimized computing needed for the compute-heavy workloads. OpsGuru first deployed the Cloud foundation through the Cloud Launchpad (CLP) to achieve the above, enabling Click-Ins to have a secure, reliable, standardized cloud baseline. With the CLP deployed, OpsGuru proceeded to configure the Kubernetes cluster (GKE), and other relevant resources that will be used to orchestrate all of the SaaS components.

Once the Kubernetes cluster was deployed, the team started an optimization of the Deep Learning model workflows. The optimized architecture utilizes Kubernetes, Helm, ArgoCD, Argo Workflows, and multiple cloud-native services managed by Google Cloud to solve all identified issues with the legacy configuration. This allowed for a fully automated model lifecycle, eliminating the need for a semi-manual approach that was prone to human errors and required downtime for the entire platform.

Besides the Deep Learning related components, OpsGuru has also implemented CI/CD for Click-Ins microservices and web components of the SaaS including Rest API, Frontend, and Portal. These components were also deployed within the Kubernetes cluster, utilizing GKE, GCR, and other Google Cloud managed services. All the components utilize OpenTelemetry for complete observability of the platform.

## The Result

Click-Ins was able to seamlessly scale to meet any load required for future business expansion while ensuring cost-optimized, performant, and reliable architecture is utilized.

• Secure Cloud Baseline: Deployment of the Cloud Launchpad ensured Click-Ins would have a rock-solid baseline in the Google Cloud that can be used to run any workloads on the cloud.

• Fully Automated Deep Learning Workflows: Deep Learning workflows are fully automated, ensuring rapid time-to-market model delivery while keeping security, performance, and high availability on the supreme levels

• Container Orchestration: All the workloads are currently orchestrated through Kubernetes, allowing Click-Ins to effectively develop, maintain, and scale for any future demands.

• CI/CD: Implementation of the Continuous Integration and Deployment (CI/CD) pipelines allowed Click-Ins to fully automate the management of application code (e.g. API) all the way to Deep Learning models, providing accelerated integration and deployment of the latest artifacts

Upon completion of the project, OpsGuru provided comprehensive training sessions for the Click-Ins team as well as documentation and operational playbooks for the newly designed systems. The training and documentation included the operational guidance of the newly built environment, Google Cloud configuration, and deployment, among other topics.