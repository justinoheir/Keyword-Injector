---
id: "050"
slug: "top-10-misconceptions-around-migrating-hadoop-to"
title: "Top 10 Misconceptions around Migrating Hadoop to the Cloud"
word_count: 1621
themes: ["terraform", "gcp", "data-analytics", "case-study", "genai", "tutorial", "devops", "migration", "azure", "aws", "security"]
extraction_date: "2025-12-19"
content_hash: "dc7278c8f648"
---

# Top 10 Misconceptions around Migrating Hadoop to the Cloud

## Introduction

• Big Data

Lots of mid-size companies and Enterprises want to leverage the Cloud for their Data Processing requirements for obvious reasons such as: agility, scalability, pay as you go model etc.

But the reality shows that migrating a production, Petabyte scale, multi-component Data Processing pipeline from on-prem to the Cloud is never an easy task. With the sheer amount of different services (Hadoop, Hive, Yarn, Spark, Kafka, Zookeeper, Jupyter, Zeppelin to name just a few) and conceptual environment differences, it’s easy to get lost and succumb to one of many pitfalls.

In this article, I will present some common misconceptions and tips on how to make your on-prem to Cloud migration smoother and potentially save you some pain. I will use AWS as a reference but of course, all the mentioned is valid for other providers like GCP and Azure which offer similar solutions.

## \#1 — Copying data to the Cloud is easy

Transferring several PB’s of data into Public Cloud Object Store such as S3 (which will be used as your Data Lake) is not as trivial as it sounds and can quickly become extremely cumbersome and time-consuming process.

Despite the fact that numerous solutions (both open-source and commercial) exist out there, I haven’t really found one solution that covers all my needs (transfer, data integrity & verification, reports).

Usually, a good strategy is to break the data transfer task into two phases;

If a certain portion of the data is relatively static (or rolling in a reasonably slow pace) a good idea will be to use a solution like AWS Snowball to copy a good portion of your data to a physical device — usually, such device will be plugged into your DC and when the copy process is done will be physically transferred to AWS DC’s and uploaded to your S3 bucket. Keep in mind that several Snowballs might be required — so your data will be sharded between them. After the major portion of the data was transferred and uploaded to the object store, use a Direct Connect uplink to the cloud provider in order to fill the remaining gaps (a variety of methods can be used here, for example: scheduled Hadoop DistCP’s or Kafka Mirroring). Both of these methods have their own issues: DistCP requires pretty serious tuning and continuous scheduling, also not all versions of DistCP allow you to blacklist/whitelist objects. Kafka MirrorMaker requires a lot of tuning and visibility (metrics export via JMX) in order to be able to measure its throughput, lag and overall stability.

Verification of that data in the Cloud object store is even harder and in certain cases requires some custom tooling. For example, a custom Data Catalogue with object name hashes or something similar.

## \#2 — “Cloud is just another DC, things should work the same”

What once behaved well in the on-prem world might not work as expected in the Cloud.

The best example for this would be Zookeeper and Kafka, where the ZK client library caches the resolved ZK server addresses for its entire lifetime, this is obviously a huge deal for Cloud deployments which are sometimes ephemeral in their nature and requires custom workarounds, such as static ENI’s for the ZK server instances.

From the performance perspective, it’s a good idea to perform a series of NFT’s (non-functional tests) on the Cloud infrastructure to see whether the instances and storage layer you chose suffices your workloads. Remember the environment is multi-tenant so it’s possible that “noisy neighbours” will steal some of your precious capacity.

## \#3 — “Object Store can replace HDFS 100%”

Separating the compute layer from the storage layer sounds like a great idea, but with great power comes great responsibility.

In most cases, the object store is eventually consistent (with the exception of Google Cloud Storage which claims to have strong consistency), which means that it can be used for both raw and processed data input as well as for final results output.

However, it cannot be used as a temporary storage, that require multi node access where HDFS is still required.

## \#4 — “Deployment of Cloud Infrastructure is just a couple of clicks in the UI”

While this might be true for a small, very early stage, test environment, you will probably want a reliable and repetitive method of provisioning your infrastructure via code. You also probably want to have multiple environments (Dev, QA, Prod). Tools like CloudFormation and Terraform can do the job, however, their learning curve is not always trivial. You will find yourself re-factoring and re-writing the code-base multiple times.

It’s usually a good idea to integrate it with a CI/CD flow that will include a pre-deployment verification stage (pre-flight tests) and smoke tests, which is also not always trivial.

## \#5 — “Visibility on Cloud is easy — I’ll just use ${SaaS\_name}”

Clear visibility (logging, monitoring) of both of your old & new environments is crucial for a successful migration.

Sometimes this becomes non-trivial due to the fact that different systems are used in the two environments, for example; Prometheus and ELK are used on-prem and NewRelic and Sumologic are used in the Cloud.

Even if a SaaS solution is used for both of the environments (which can get costly at scale), there is an effort with exporting and processing the application metrics, for example extracting JMX metrics from the apps, setting up aggregations and dashboards, creating alerts etc.

## \#6 — “Cloud just scales indefinitely”

Users are often excited to hear about feature such as Auto Scaling Groups and think they can easily apply them on their data processing platforms; while in some cases it’s relatively trivial (for example EMR worker nodes without HDFS), in other cases, where persistent storage is involved — it’s not and sometimes requires quite a significant effort (for example Kafka brokers).

Before shifting traffic to your cloud infrastructure, it’s usually a good idea to check the current resource limits (number of instances, disks etc) and pre-warm the load balancers; without that your serving capacity can be limited and can be easily avoided.

Last but not least, it’s worth remembering that as scalable as cloud is, the depth the budget has its boundaries 😉

## \#7 — “I will just lift and shift my infra as-is”

While it’s usually a good strategy to avoid potential vendor lock-in and rely on proprietary data stores (such as DynamoDB), it’s a good idea to leverage services that are API compatible, for example using Amazon RDS for Hive Metastore DB is probably a good idea.

EMR is another good example, no need to re-invent the wheel here, just keep in mind that heavy customization of EMR might be required via post-installation scripts (tunables such as heap sizes, 3rd party jar’s, UDF’s, security addons) etc.

In case of EMR it’s also worth mentioning that there is still no HA available for the master node (NameNode, YARN ResourceManager etc), so it’s up to you to architect your pipelines to be able to tolerate a failure and adjust to more ephemeral state.

## \#8 — “I will just port my Hadoop/Spark jobs to the Cloud”

This is where things get complicated. For a successful job migration you will need to have clear visibility into your business logic and pipelines; from initial ingestion of RAW data to meaningful, distilled aggregations. It gets even more complicated where the results of pipeline X and pipeline Y are inputs of pipeline Z. These flows and interdependencies have to be clearly mapped (a DAG chart might be a good idea) with all the components involved. Only after this mapping, you will be able to effectively start moving your analytical pipelines keeping the business SLA.

## \#9 — “Cloud will reduce operational expense and staff”

While it can happen that operations with owned hardware will require more personnel for physically supporting on-premise resources, with cloud the personnel will still need to respond to business needs — development, operations support, troubleshoot, plan the expense, and also tool up (find/develop tools) your new infrastructure.

Eventually, someone in your organization must possess the knowledge of what you have, how it operates. This means a higher skill-set of personnel, which are not trivial to hire. So while the \# of Operation people may slightly decrease, you may still find yourself paying the same price if not more.

Another noticeable item is service/licensing fees (for example EMR), which can become costly, at scale. Without careful planning/modelling, you will find very quickly that you’re paying more for the actual service license rather than the compute resources you’re using.

## \#10 — “Cloud will finally allow us to have No-Ops”

“No-Ops” is a great buzzword coined to a situation when a business can totally opt-out of the operational expertise of 3rd party service. For some companies’ needs, it is satisfactory to have pretty thin operations teams, unfortunately, this is totally untrue for Data-Intensive companies.

You will still require someone to integrate and duck-tape all the systems, benchmark these systems, automate provisioning, provide meaningful visibility and respond to alerts, the role of Data Operations simply shifts to the higher stacks and by no means disappears\!

To conclude, while migration of your Data Processing pipelines to the Cloud can obviously bring multiple undeniable benefits, the migration process has to be thoroughly planned and executed with all of the above points taken into account. Plan ahead and don’t get caught unprepared.