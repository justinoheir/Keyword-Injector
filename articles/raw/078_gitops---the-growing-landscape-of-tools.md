---
id: "078"
slug: "gitops---the-growing-landscape-of-tools"
title: "GitOps \- The Growing Landscape of Tools"
word_count: 1928
themes: ["gcp", "data-analytics", "genai", "tutorial", "devops", "kubernetes", "azure", "serverless", "aws", "containers", "security"]
extraction_date: "2025-12-19"
content_hash: "fde048ab7c54"
---

# GitOps \- The Growing Landscape of Tools

## Introduction

In an earlier post we have discussed the advent of GitOps, what it is and why it has become so popular. In this post we are going to take a look into a few GitOps offerings. While the first GitOps product has been Weaveworks Cloud in 2017 (if memory serves me right), the landscape has since evolved. While GitOps originally is conceived for Kubernetes deployment, the term has expanded to usage beyond Kubernetes, including deployment onto other platforms and creation of infrastructure. It appears that GitOps is now a term that is interpreted literally: operations driven from Git.

A number of the products have been open-core i.e. core functionalities are open-sourced, while full suite of functionalities are only available based on subscriptions of commercial products. A few examples belonging to this category are Weaveworks Cloud with open-source Flux, CloudBees CI/CD with open-sourced CloudBees Jenkins X distro. A few of them are extended offerings from established products e.g. GitLab with Auto DevOps, GitHub Actions. Meanwhile, a number of open-sourced projects serve as archetype of what a GitOps pipeline should look like.

The survey below by no means captures all the services currently available; it is a sketch of a few offerings. We have explored these projects in particular because they are representatives of the landscape and many are well-known brands. We certainly look forward to other upcoming services that enrich the landscape solving the git-driven CI/CD challenge.

## GitLab Auto DevOps

If GitOps is about using Git as the source of truth of everything, including deployment and configurations, GitLab is certainly strongly behind the message. GitLab is promoting using Git as the enterprise collaboration tool because the mechanism is well-known and well-trusted.

Starting at GitLab 11.0, GitLab has introduced Auto DevOps, which is a suite of 12 features responsible for the range of build, test, static code analytics, dynamic application security testing, dependency scanning, license compliance, container scanning, deployment and monitoring. Though purported to work for infrastructure as well, the GitLab Auto DevOps offering is conceived for containerized applications. Since GitLab 12, Auto DevOps pipeline can be triggered automatically upon detection of the presence of the Dockerfile. The Auto DevOps suite incorporates a number of open-source tools, including Clair for container scanning, Helm for deployment packaging and templating and Prometheus for monitoring.

GitLab Auto DevOps work on Google Kubernetes Engine (GKE) and Amazon Elastic Kubernetes Service (EKS). It also has support for AWS Lambda and Knative running on either GKE and EKS. The full feature set of GitLab Auto DevOps is only available in the GitLab Gold package at $99 per month per user, which includes 50,000 pipeline minutes per month on shared runners.

## CloudBees CI/CD powered by Jenkins X

First announced in early December 2019, CloudBees CI/CD powered by Jenkins X is a hosted solution provided by CloudBees. Jenkins X is used to drive the CI/CD features of the product, while the pipeline coordination mechanism is based on Tekton. Both Jenkins X and Tekton are projects of the Cloud Delivery Foundation, providing continuous delivery features that are vendor-neutral and cloud-native.

Jenkins X is designed to operate on Kubernetes from the ground-up. Jenkins X attempts to provide a platform experience of Kubernetes. User should not be concerned be concerned about the underlying cloud provider (the managed Kubernetes from AWS, Google Cloud, Azure are supported, along with OpenShift, Pivotal, even Minikube and Minishift), it also supports spinning up preview environments as a test before code merges. Jenkins X has a command-line tool “jx” that can instigate multiple API calls to Kubernetes and cloud providers (it reminds of kubectl). A number of addon integration are possible, including Prometheus for monitoring, Istio for service mesh, Ambassador for API gateway and Anchore Engine for container security validation.

However, Jenkins X in CloudBees CI/CD powered by Jenkins X is based on the CloudBees distro of Jenkins X. The specific version of Jenkins is managed by CloudBees and has monthly release cadences. At time of writing, CloudBees Jenkins X distribution only supports GKE. It leverages heavily the concept of build pack, whereby the user will need to define the Dockerfile, Jenkinsfile and helm charts dedicated to the particular application. Build packs are organised based on physical locations of files in the GitHub repository. While the “jx” command-line tool to install Jenkins X functionality into GKE clusters, how addons are supported by the distro and how future addons are going to be made available is not yet well understood.

CloudBees CI/CD has highlighted however a number of features extraneous to the generic Jenkins X distribution. One such feature is the Hashicorp Vault integration, which is noteworthy because secrets management is often the Achilles heel for CI/CD systems, where hard-coded secrets are often stored internally and exposed as environment variables to be accessed during the pipeline actions. Because the CloudBees offering usages Tekton, the Kubernetes operator for pipeline, the Jenkins server component is no longer needed, making pipeline triggering for deployment to even other Kubernetes clusters, much simpler. In fact, automated environment promotion of a build is one of the features CloudBees advertises. The CloudBees CI/CD also promises a rich and intuitive UI for better user experience.

There are a number of unknown at the time of writing because CloudBees CI/CD powered by Jenkins X is still in preview. Feature-wise, it has potential to be like OpenShift with its own ecosystem of support of many tools; it appears that it can be integrated with other pieces of tools (e.g. Clair or Anchore Engine that is supported natively in Jenkins X). We look forward to more information — including pricing, support and introduction of new services — and actually testing the service out.

## Weaveworks Weave Cloud

When Weaveworks first promoted the term GitOps, it was in concert with the advent of the Weave Cloud service. The core technology of Weave Cloud CI/CD — Flux — has become a CNCF sandbox project in August 2019\. Flux is also a Kubernetes operator, it has the advantage of not needing to grant extraneous access to a CI system because Weave Cloud adheres to the essence of using Git as the single source of truth and collaboration workspace.

Unlike later comers such as GitLab Auto DevOps and CloudBees CI/CD powered by Jenkins X, Weave Cloud focuses on the delivery and monitoring capability for Kubernetes clusters. It assumes the container is already built and stored somewhere accessible — the tutorials Weave Cloud use Travis CI for build and quay.io for container registry needs.

Because of the Flux CD origin, “fluxctl” is the command-line tool that can be used to manage a workload, which is defined by the version of the image used in a pod (thus can be a deployment, daemonset, stateset and cronjob) and the targeted cluster. Deployment on Weave Cloud is triggered based on changes in the monitored container repository. By monitoring the container repository instead of the Git directly, it implies that Weave Cloud only expects the Kubernetes manifests to be made available in the Git repository instead of actual application source code. The Flux operator deployed onto Kubernetes clusters will monitor for the manifests on Git and compare it against the previous deployments stored in memcached deployed on the cluster, and deployment is triggered if a difference is discerned and when deployments policies allows.

Weave Cloud also assumes the manifest files are directly stored in the Git repository pointing to the versioned container image i.e. Weave Cloud does not support templating engines like Helm to dynamically resolve the manifests. Weave Cloud effectively takes a simplistic yet intuitive approach to Kubernetes deployment. It can be argued that the product is more similar to Spinnaker than a full development platform. Weave Cloud pricing is based on monthly node-seconds, a formula that addresses the ephemeral nature of nodes while supporting the traditional duration-based usage.

## GitHub Actions

Made generally available in November 2019, GitHub Actions is another new-comer into the GitOps landscape. It is easy to compare it against GitLab Auto DevOps, though at the initial release, GitHub actions appears to be a pipeline management tool with optional runners. Users can configure the pipeline based on specific needs or use third-party provided actions to perform specific needs, be it for container validation, testing, deployment, than a diverse platform with many features to support actions in the software delivery life cycles. Given the availability of third-party actions, it is expected that there will be more managed actions, including more in-depth Kubernetes actions, to make GitHub actions more feature-rich and powerful.

GitHub Actions focuses on convenience and easy adaptability. Arguably its simplicity and intuitiveness (as in not that different from other hosted CI/CD offering like CircleCI and TravisCI) can be attractive to its faithful followers who are deeply entrenched in the GitHub ecosystem. GitHub Actions are free for public repositories; for private repositories, the charge is based on minutes, storage or data transfer and associated overage charge after free tier is exhausted.

The OpsGuru team has done a deep-dive on setting up GitHub actions. Stay tuned for the post\!

## Argo CD

It is not a hosted service provided by a vendor (though there are independent vendors providing hosted support), Argo CD is arguably the most popular open-source project implementing GItOps pipeline. Argo CD needs to be mentioned in this post because it is the vendor-neutral archetype that demonstrates what a GitOps pipeline would look like. The continuous delivery mechanism is deployed as an operator onto a Kubernetes cluster, making pipelines a first-class resource in a Kubernetes cluster. The Argo CD Kubernetes controller than continuously monitors running applications and compares the current and desired state as stated in the Git repository. As is expected of any continuous delivery system, it provides a web UI that provides a real-time view of application activity. It supports multiple config management and templating tools including Kustomize, Helm, Jsonnet, and naturally the plain YAML.

## GitOps Engine

We have discussed earlier Weaveworks Cloud, which is based on the open-sourced Flux project and Argo CD above. Flux CD and Argo CD are the open-sourced standard for GitOps pipelines; hence it is very interesting how the two projects are joining forces for a collaboration that attempts to get the best of both worlds. The FAQ of the GitOps Engine project is especially interesting on how implementers of each of the projects can look forward to as a result of the joining of forces. Hopefully we can see a new and comprehensive standard emerging from this collaboration.

## Summary

The landscape of services providing Kubernetes-specific CI/CD pipelines is increasingly rich and competitive. With Kubernetes becoming the winner amongst container orchestrators, the user and platform experience becomes the gap that needs to be addressed to support Kubernetes’ continuous lead. Multiple vendors and projects are providing solutions based on their own interpretation to the needs. When I started off writing this piece, I was aiming to address GitOps as a concept, but it is really exciting to see the different interpretations. I look forward to a write-up on as the landscape evolves.

GitOps is a particular way to implement CI/CD, which is essentially in any manageable deployments. How do you configure your CI/CD? Does GitOps make sense to you? We’d love to hear from you. In our final post, we will look into how to create a pipeline using GitHub Actions.