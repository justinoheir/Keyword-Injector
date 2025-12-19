---
id: "081"
slug: "karpenter---a-new-way-to-manage-kubernetes-node"
title: "Karpenter \- A New Way to Manage Kubernetes Node Groups"
word_count: 942
themes: ["terraform", "genai", "tutorial", "kubernetes", "aws", "containers"]
extraction_date: "2025-12-19"
content_hash: "59495e892afd"
---

# Karpenter \- A New Way to Manage Kubernetes Node Groups

## Introduction

One of the most common discussions that happen when adopting Kubernetes is around autoscaling. You can autoscale your workloads horizontally or vertically, but the main challenge has always been the nodes.

The hypervisor doesn’t have visibility into what the container is actually consuming in a virtual machine, nor is it aware of the workload resource requirements, and without that information the cloud provider can’t reliably handle the node autoscaling. The solution was to let something that does have that information handle it, and so we have the Cluster Autoscaler.

The Cluster Autoscaler automatically adjusts the size of an autoscaling group (ASG), when a pod failed to run in the cluster due to insufficient resources, or when nodes in the cluster are underutilized for a set period of time, and their pods can fit into other existing nodes.

Looking at the above description, it seems like the Cluster Autoscaler is just fine, and in most cases it is, but what if you need a new type of node that isn’t available yet in your cluster’s nodegroups?

Most organizations will have their clusters deployed using some kind of infrastructure as code tool like Terraform or AWS Cloudformation, which means that updates to this codebase will be necessary when changing the node groups. Configuring details and restrictions of these node groups is not always a straightforward process either.

New nodes can also take a while to be available to Kubernetes, and once they are available you might still run into racing conditions scheduling pods into these nodes.

Recently, AWS released Karpenter to address these issues and bring a more native approach to managing your cluster nodes.

Let’s take a look at how both solutions work, current pros and cons.

## Cluster Autoscaler and Karpenter

How does the Cluster Autoscaler work?

• We deploy a workload to the cluster

• Kubernetes scheduler could not find a node that will fit our pod

• Pod is marked as Pending and Unschedulable

• Cluster Autoscaler looks for pods in a Pending state

• It increases the ASG desired count if the pending pods do not fit in the current nodes

• The ASG creates a new instance

• Instance joins the cluster

• Kubernetes scheduler finds the new node and, if the pod fits in it, assigns the pod to it

## Cluster Autoscaler and Karpenter

So the Cluster Autoscaler doesn’t really deal with the nodes themselves, it just adjusts the AWS ASG and lets AWS take care of everything else on the infrastructure side, and relies on the Kubernetes scheduler to assign the pod to a node.

While this works, it can introduce a number of failure modes, like a racing condition having a pod being assigned to your new node before your old pod, triggering the whole loop again and leaving your pod pending for a longer period.

What about Karpenter?

Karpenter does not manipulate ASGs, it handles the instances directly. Instead of creating code to deploy a new node group, then target your workload to that group, you just deploy your workload, and Karpenter will create an EC2 instance that matches your constraints, if it has a matching Provisioner. A Provisioner in Karpenter is a manifest that describes a node group. You can have multiple Provisioners for different needs, just like node groups.

Ok, if its like node groups, what is the advantage? The catch is in the way that Karpenter works. Let’s do the same exercise we did for the Cluster Autoscaler, but now with Karpenter.

• We deploy a workload to the cluster

• Kubernetes scheduler could not find a node that will fit our pod

• Pod is marked as Pending and Unschedulable

• Karpenter evaluates the resources and constraints of the Unschedulable pods against the available Provisioners and creates matching EC2 instances

• Instance(s) joins the cluster

• Karpenter immediately binds the pods to the new node(s) without waiting for the Kubernetes scheduler

## Cluster Autoscaler and Karpenter

Just by not relying on ASGs and handling the nodes itself, it cuts on the time needed to provision a new node, as it doesn’t need to wait for the ASG to respond to a change in its sizing, it can request a new instance in seconds.

In our tests, a pending pod got a node created for it in 2 seconds, and was running in about 1 minute in average, versus 2 to 5 minutes with the Cluster Autoscaler.

The possible racing condition we talked about before, is not possible in this model as the pods are immediately assigned to the new nodes.

Other interesting things the Provisioner can do is setting a ttl for empty nodes, so a node that has no pods, other than DaemonSet pods, is terminated when the ttl is reached.

It can also ensure nodes are current by enforcing a ttl for the nodes in general, meaning a node is recycled once the ttl is reached.

Ok\! So Karpenter is great, let’s dump the Cluster Autoscaler\! Not so fast\! There is one feature that Karpenter is missing from Cluster Autoscaler, which is rebalancing nodes, the later can drain a node when its utilization falls under a certain threshold and its pods fit in other nodes.

## Talk is Cheap\! Show me the demo\!

Let’s get this running\! We’re following the getting started guide from karpenter.sh with a couple twists.

At the time this post was written Karpenter 0.5.2 was the latest version available.

First the good old warning for all demo code.

WARNING\! This code is for use in testing only, broad permissions are given to Kar