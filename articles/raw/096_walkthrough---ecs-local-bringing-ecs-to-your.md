---
id: "096"
slug: "walkthrough---ecs-local-bringing-ecs-to-your"
title: "Walkthrough \- ECS Local: Bringing ECS to your local environment"
word_count: 1720
themes: ["company-news", "data-analytics", "genai", "tutorial", "devops", "kubernetes", "serverless", "aws", "containers", "security"]
extraction_date: "2025-12-19"
content_hash: "648391f4fb32"
---

# Walkthrough \- ECS Local: Bringing ECS to your local environment

## Introduction

As someone who works with AWS on a day-to-day basis, It’s important to stay up to date with all the changes and new features of the different services on the platform. That’s how one recent announcement caught my eye – the new capability of local testing of ECS.

I am particularly interested in ECS local testing because it is a feature that bridges a known gap. In recent years, containers have become increasingly popular. Without a doubt Kubernetes has been the leading standard for containers deployment. Whilst Kubernetes is feature-rich and powerful, it attracts users because the same Kubernetes can be run locally on a developer’s desktop.

When developing a feature, I want to be able to test it as quickly and quietly as possible. A tool that allows me to perform rapid and quiet testing while I am trying to figure things out is very helpful. Being able to deploy onto Kubernetes means that I can test the same manifests locally, making sure that all changes can be tested before the deployments are scrutinized by my peers and potentially impact shared resources, it gives me confidence that I am not wasting my teams’ resources and time.

ECS was first announced in 2013 and has been the go-to tool for containers orchestration on AWS (as evidenced by the number of new features on the public containers roadmap). While others can get on the heated — and even religious — debate on the virtue of Kubernetes vs ECS, the straightforwardness of ECS, the tight and intuitive integration of ECS with the other AWS features, is very attractive. For someone who is heavily leveraging AWS, and needs some container orchestration for part of workloads, more often than not ECS is sufficient.

Until now, it has been challenging to encourage developers to work closely with ECS, because developers cannot test their work unless they deploy directly onto AWS ECS clusters that are running on AWS. Prior to this release, it is necessary to raise an ECS cluster on AWS and test the task definitions on the cloud to verify ECS workloads. Whilst this makes sense for feature integration and performance testing, it is a significant entry barrier for early development. Not every developer will have direct access to ECS resources, and to follow through with the CI/CD workflow for every minute change tends to be too slow for feedback. To workaround the overhead, developers often choose to develop with docker-compose, and leave the ECS testing for a later state. This delay can make deployments more error-prone and ECS more difficult to adopt. With the new feature, the barrier for ECS adoption seems to be significantly reduced.

The new ECS feature supports testing of network modes, secrets, volumes and credentials without the requirement of launching an ECS Task or an ECS Service on AWS and doing everything locally on the work-station. This is achieved by ecs-cli, which is a wrapper of Docker and Docker Compose that simulates a fully functional ECS environment via a special container. With this wrapper, the user can locally get mock endpoints and resources available to test tasks and verify application functionality.

## Pre-requisites

The usual tools associated with a container-based development environment still apply; namely, Docker and Docker Compose. On top of that; installing ecs-cli command line tool.

Valid AWS credentials are required too:

• Install Docker: 

• Install Docker Compose: 

• Install AWS ecs-cli: 

• Export your AWS ACCESS KEY and AWS SECRET KEY to Environment variables:

For this walkthrough, I have created several ECR Repositories:

export AWS\_ACCESS\_KEY\_ID=xxxxxxxxxxxxxxxxxx export AWS\_SECRET\_ACCESS\_KEY=yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy export AWS\_DEFAULT\_REGION=us-west-1

In each repository, there are several images e.g. app2

The same images are accessible on the command line with ecs-cli command line tool. For example, the following will list the available images, along with respective metadata.

ecs-cli images

In order to pull the images from the ECR to my workstation I need AWS credentials and Docker authentication with the remote repository. The following command will initiate and perform login from my local machine to ECR

$(aws ecr get-login \--no-include-email \--region us-west-1)

Before local execution of ECS takes place, I need to define the run-time parameters for the containers, such as the memory and CPU requirements and the ports opened. This is done in the ECS task definition. While the task definitions need to be created on AWS initially, I can download the task definition as JSON file to my local machine or use remote task definitions for local testing. For my test application (app-main), I have already created several versions of a task definition on ECS.

## The ecs-cli Walkthrough

ecs-cli for local testing have only 4 subcommands for now:

## Launching a Task

The following command will locally launch a Docker container based on a task definition:

ecs-cli local up \--task-def-remote app-main:6

app-main is the name of the task-definition and 6 is the revision of the task definition – If the version is omitted, the latest version will be used.

Trying out with the latest version of my task definition.

and voilà\!

ecs-cli local up

did a few things:

1\. Wrote docker-compose.ecs-local.yaml file

2\. Wrote an additional docker-compose.ecs-local.override.yml file

3\. Created local network ecs-local-network for containers

4\. Pulled Image amazon/amazon-ecs-local-container-endpoints

5\. Used docker-compose binary to start the relevant containers as described in our Task Definition

6\. Pulled a corresponding Image of the relevant container from ECR

7\. Created Container ecslocal-lab\_app-main\_1

## Examining the Running Task

ECS Local uses the Docker Compose installed on the local machine to create network for containers and provision those containers. The information is captured at the generated docker-compose.ecs-local.yaml file. The ecs-local.yaml file acts as the local counterpart of the task definition that is stored on AWS.

Content of docker-compose.ecs-local.yml

Another file docker-compose.ecs-local.override.yml created is used to define a single container that emulates how credentials are exposed to a running container.

Content of docker-compose.ecs-local.override.yml

At examining the running processes with ecs-cli, I can see that my test application is running.

ecs-cli local ps \--all

docker ps \--all

However, if I repeat the above using native docker command, an additional container running alongside the application container is found:

The abstracted amazon-ecs-local-container-endpoints container is essentially a mock service that simulates AWS endpoints with configured ECS Task IAM Role in the task definition.

The above also shows that the application container is running on port 32771 and forwarding traffic to port 80 on the container itself. Port 80 is open because it is defined as such in the task definition.

With this set-up, I can now access the container in two ways,

Via Local network IP address by running

docker network inspect ecs-local-network

and

curl

Via the assigned Port on the local machine by running

ifconfig

to get our local IP address in network ecs-local-network

then calling against the address and assigned port

curl 169.254.170.1:32771

The container in concern is a trivial example for a container, therefore testing it is straightforward. But imagine a complex task where multiple containers are running, instead of needing to emulate the task definition locally with a docker-compose (which would be thrown away once the troubleshooting is done) there is now an AWS provided tool that translates the task definition to something that can run locally, therefore bridging some of the difficulty of making ECS usable beyond AWS.

## Stopping the Task

Once I have my local troubleshooting of ECS, I can stop all running containers and delete local network quite easily by another ecs-cli local command:

ecs-cli local down \--all

## Observations and Musings

When I first heard about ECS local testing, I thought that AWS was stepping into the right direction, to make ECS more accessible to developers. When AWS published ECS CLI a few years ago, it seemed to be following the precedents set by competitors such as Heroku, to make the containers deployment an easy one-step process. The unenviable position for ECS, however, is that while it is not as complex Kubernetes, it is not as straightforward as other developer-friendly services such as Elastic Beanstalk. ECS appears after all, to be targeting infrastructure teams to run containers easily without the complexity, but it lacks the intuitiveness for developers to adopt it readily and enthusiastically. The local testing option of ECS appears to be an attempt to draw developers closer to the service, by emulating the environment locally, and therefore supporting local work and experiment.

It may be too early to give a full verdict to the ECS local testing functionality. As the prerequisites for ECS local are still heavily based on the cloud e.g. task definitions on ECS and containers being uploaded already to ECR, it is still arguably not ready for developers who are completely new to the containers ecosystem. However, it is certainly useful to gain some local understanding of the inner workings of ECS. I look forward to new features being introduced with the local tool, and maybe examples on how to best leverage it.

It is noteworthy that ecs-cli can be used for Fargate development as well. As Fargate is the serverless version of ECS, and is expected to marry the best of containers (in terms of duration, flexibility of resource allocations) and serverless (in terms of simplicity and lack of cluster management), perhaps ecs-local is another way to approach a serverless future.

## Conclusion

We have seen that ecs-cli local is a useful wrapper for Docker and Docker Compose, which you can leverage to quickly and efficiently test your ECS Task Definition configurations locally without actually deploying your task to a remote ECS Cluster.

This enables quick and more efficient development & test cycles and is overall a great addition to the evolving AWS ECS ecosystem.

Interested in hearing more about our containers expertise?

Contact us at info@opsguru.com

– Written by Denis Astahov