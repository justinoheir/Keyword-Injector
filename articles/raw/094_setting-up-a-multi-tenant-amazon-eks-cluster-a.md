---
id: "094"
slug: "setting-up-a-multi-tenant-amazon-eks-cluster-a"
title: "Setting up a Multi-tenant Amazon EKS cluster: a few things to consider"
word_count: 1869
themes: ["company-news", "data-analytics", "genai", "tutorial", "kubernetes", "aws", "containers", "security"]
extraction_date: "2025-12-19"
content_hash: "7e1dddef76e8"
---

# Setting up a Multi-tenant Amazon EKS cluster: a few things to consider

## Introduction

OpsGuru prides itself in heavy use of cloud-native technology, and Kubernetes is often the primary platform of choice to run containerized workloads. Because of its flexibility and support on bare metal, virtual machines and across all major cloud providers, Kubernetes has become the most popular container orchestration platform. The nature of the workloads have also changed: instead of being the advocated platform only for simple stateless workloads, Kubernetes is now also used for databases, machine learning workflows and a variety of complex applications.

Ever since Amazon EKS has been made Generally Available since 2018 (and it has just been made available in Canada. Yay\!), it has been noted as the first choice of running Kubernetes workloads on AWS. Hosting a Kubernetes platform on your own is complex, expensive and dubious in business value. In most cases, Amazon EKS — the managed Kubernetes services provided by AWS — is the unassailable choice to manage Kubernetes workloads on AWS.

Amazon EKS can be especially attractive to the needs of a multi-tenant service, because the Kubernetes orchestration layer supports running drastically different workloads on the same server and therefore increasing the density on the Amazon EC2 instances. However, in order to run a SaaS application on Amazon EKS, the hygiene and security concerning multi-tenant data and access have to be considered carefully. The following are a few points that any SaaS service should consider at using Amazon EKS to run their services.

## Each tenant should have its own namespace

Namespace is essential in a multi-tenant EKS cluster, where it can be used as logical boundaries separating tenants. Such boundaries are further fortified by security and policy constructs such as role-based access control (RBAC) and resource quotas (discussed below). The goal is to limit the blast radius by ensuring that only resources within the same namespace can access each other, that external entities (e.g. a user) can only access the objects when specific access to the namespace is granted. Once properly set up, the tenants of different namespaces should be protected from each other, similar to how resources in different AWS accounts are protected from each other.

## Soft Isolation via ResourceQuota to avoid erosion of resources by noisy tenants

Other than resource isolation from each other, namespaces can be used to ensure resources (CPU, memory, storage … ) are fairly shared instead of being monopolised by workloads in particular namespaces. The ResourceQuota object can be used to limit the total consumption of CPU, memory, storage and number of objects of all processes within the namespace (and therefore a tenant based on the 1:1 namespace/tenant mapping). To expand on the same idea, ResourceQuota can also be used to prioritise regular and premium tenants based on the agreements made with the SaaS provider. Meanwhile, to ensure resource sharing within a namespace, LimitRange is a handy object to make sure no container can run away with resources, and the globally defined PriorityClass objects can be used to assign available resources based on the priority of the workloads.

## Hard Isolation via enforcing 1:1 mapping between instance groups and tenants

In the above scenario, the pods for multiple tenants share the same Amazon EC2 instances that run as nodes in the same Amazon EKS clusters. In a scenario where harder separations are needed e.g. completely separate groups of Amazon EC2 node groups, the mechanism of taint,tolerations and nodeSelector can be used to achieve that.

tenant=A:NoSchedule kubectl label nodes node1 tenant=A

As an example, consider a number of nodes that should only execute workloads from tenant A. The first step is to “taint” those nodes with a key/value pair and assign proper labels to it

This taint will ensure only pods with the key/value pair (tenant,A) can run the node. The label is used to help tenant A workloads identify where they should run. While taint and label look similar, they serve different purposes.

Meanwhile, the workloads should satisfy the taint requirement by containing the toleration

\- key: “tenant” value: “A” effect: “NoSchedule”

To ensure that the workload will only run on the dedicated nodes, nodeSelector needs to be used as well, leveraging the labels that have been set earlier.

nodeSelector: tenant: A

With the use of tolerations and taints, one can assign the workloads of namespace/tenant A with the proper tolerations to only nodes associated with tenant A (that are all tainted accordingly). The same toleration and taints can be applied to workloads of other talents. As a result, workloads are spread to different node groups (which are often autoscaling groups), sharing therefore only the control plane. This is a handy way to easily capture instance costs associated with tenants because billing reports with tenant-based tags on the instances is straightforward.

While the above is an ideal scenario to perform hard isolation by separating nodes used by tenants, extraneous security measures will then need to be considered to avoid malicious workloads trying to run workloads on node groups associated with other tenants. A ValidatingAdmissionWebhook is one way to ensure only pods that have expected tolerations are permitted. In fact, the CNCF project Open Policy Agent (OPA) is a good tool to support exactly that. Here is an AWS blog on how to get OPA started on Amazon EKS.

## Integrate Amazon IAM to AWS EKS Cluster to control cluster access

In earlier paragraphs, I have focused the discussion from the resource perspective, but good multi-tenant practice on Amazon EKS is heavily dependent on good security posture too. The first and foremost security practice on Amazon EKS — particularly for a multi-tenant cluster — is role-based access control, which can be tightly integrated with Amazon IAM.

At setting up RBAC on Kubernetes, the first thing to understand is the difference between cluster-roles and roles. While cluster-role may be convenient because it is applicable to the entire cluster (a reason why many beginner tutorials of Kubernetes default cluster-admin role because of its simplicity), it is highly discouraged in a multi-tenant setup. If any entities need access to a tenanted-namespace, the namespace-specific roles should be used instead (in fact, it can be argued that it is better to set up similar roles across each of the tenanted namespaces than to set up a cross-namespace cluster role for the same functionality). AWS IAM can be easily mapped to a role in the EKS cluster. AWS has provided clear documentation on the different ways to map AWS IAM credentials to an EKS cluster-role or (namespace-specific role).

## Integrate AWS IAM to EKS workloads to enforce AWS resource access

AWS IAM roles are not only useful for controlling the objects in the Amazon EKS cluster, but it is necessary to control access from workloads to AWS. The usual security practice of applying AWS IAM roles to the underlying Amazon EC2 instances is insufficient because they need to include all permissions necessary to support all actions that will take place on the nodes, namely the access of all possible workloads across all tenants. In a pool of worker nodes that can run workloads of multiple tenants, it is not possible to implement tenant-specific IAM policies on the Amazon EC2 instances. In fact, even in a single-tenanted cluster, IAM roles on the Amazon EC2 nodes are inadequate as a security construct because it requires to be a super-set of all permissions needed.

Since September 2019, AWS IAM has added support for EKS workloads on the pod level. This is done by first mapping namespace-specific service accounts to AWS IAM roles, then associate the service accounts with the individual pods. By doing so, you are not only using AWS IAM to control access to AWS resources by the workloads running on the EKS cluster, but also ensuring such workloads only have access to the tenant-specific resources. For example, often Amazon S3 buckets are used to store permanent data, and tenant-specific data can be stored under specific paths in the same bucket. By assigning IAM permissions to each pod running on the EKS clusters, you can ensure that there is no unintended cross-tenant data access to the data in the AWS S3 buckets, as each pod can be assigned access only associated with the tenant the pod is running with (A side note: the recent announcement of Amazon S3 Access Points look especially attractive for multi-tenant workloads).

## Control Communications via Network Policies

Network policies are used to control ingress and egress permissions based on multiple criteria. For a multi-tenant EKS set up that maps tenants to namespaces, namespaceSelector and podSelector can be used to limit cross-namespace communications and even communications amongst different pods within the same namespace.

Suppose there is a namespace tenantA already set up, and there is a label associated with it that is in the form of

kubectl label namespace/tenant-a tenant=a

The following example is a network policy that allows only same-namespace traffic within the tenantA namespace getting to pods with labels “app:api”

apiVersion: networking.k8s.io/v1 kind: NetworkPolicy metadata: name: same-namespace-only namespace: tenant-a spec: podSelector: matchLabels: app: api policyTypes: \- ingress \- egress ingress: \- from: \- namespaceSelector: matchLabels: tenant: a egress: \- to: \- namespaceSelector: matchLabels: tenant: a

## Pod-Host Access Control to Double Assurance on Multi-tenant Security

While PodSecurityPolicy is intended to limit access to the underlying EC2 instances in an Amazon EKS cluster, by the same token it can be used to limit access the shared resources in the EC2 instances in a multi-tenant cluster.

By not using pod-security policy, you are essentially implementing

apiVersion: policy/v1beta1 kind: PodSecurityPolicy metadata: name: privileged annotations: seccomp.security.alpha.kubernetes.io/allowedProfileNames: '\*' spec: privileged: true allowPrivilegeEscalation: true allowedCapabilities: \- '\*' volumes: \- '\*' hostNetwork: true hostPorts: \- min: 0 max: 65535 hostIPC: true hostPID: true runAsUser: rule: 'RunAsAny' seLinux: rule: 'RunAsAny' supplementalGroups: rule: 'RunAsAny' fsGroup: rule: 'RunAsAny'

It is easy to discern, by observing all permissions granted in the volumes stanza, what security pitfalls the default policy pose. In a scenario where pods from multiple namespaces/tenants are sharing the underlying resources of the Amazon EC2 instances, not locking down access from the pod to host can mean inadvertently exposing data across tenants, if the data is stored/cached in the associated volumes.

## Summary

The above is by no means a comprehensive set of rules to set up multi-tenants on Amazon EKS. However, as Amazon EKS is becoming a popular choice for hosting multi-tenant services, it is important to consider how to properly apply the resource and security boundaries between tenants to ensure functionality for the service. Amazon EKS presents many exciting possibilities — especially with the increasing maturity of persistence data management.

Are you interested in learning more about using Amazon EKS to run your multi-tenant solution?

Are you wondering about other architectural design patterns applicable to multi-tenant solution on AWS? The OpsGuru team is ready to work with you to adopt the cloud and to optimise your workloads. Let us have a chat info@opsguru.com.

Written by: Mency Woo