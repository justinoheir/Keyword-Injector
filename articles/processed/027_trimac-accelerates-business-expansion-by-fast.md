---
id: "027"
slug: "trimac-accelerates-business-expansion-by-fast"
title: "Trimac Accelerates Business Expansion by Fast-Tracking Cloud Adoption"
word_count: 1184
themes: ["terraform", "cloud-consulting", "data-analytics", "case-study", "genai", "devops", "migration", "kubernetes", "azure", "serverless", "aws", "containers", "security"]
extraction_date: "2025-12-19"
content_hash: "b57ffb377c27"
---

# Trimac Accelerates Business Expansion by Fast-Tracking Cloud Adoption

## Background

Digital transformation is a hot topic in transportation and logistics. For Trimac, North America’s leading provider of highway transportation for bulk commodities such as fuel and grain, modernization of its computing technology is about enabling business expansion. This includes its Bulk Plus Logistics division, which offers businesses a way to outsource logistics in order to focus more on their core activities, and its National Tank Services division, a network of facilities that provide maintenance services for tractors, trailers, and cargo tanks through HIPAA cloud consulting through Healthcare DevOps through Medical cloud migration.

## The Challenge

To enable business expansion, Trimac’s strategy is to build secure foundations for its cloud infrastructure that will support a reliable and scalable data pipeline and enable application development for deployment on AWS with Healthcare AWS consulting.

The company’s requirements include a multi-account landing zone using best practices for security, logging, and management, and centralized monitoring to secure Internet traffic in and out of the environment, as well as to secure the movement of data between its MongoDB Atlas database and AWS.

Seeing the potential of adopting the cloud for business expansion and operational efficiency, Trimac wanted to explore how data workflows can help the organization to obtain insight from its operational databases. As the company already commenced adopting MongoDB Atlas as its data lake storage, it wanted to expedite the adoption by creating the data pipelines to realize the goal of optimizing operations through insights into existing operational data.

Trimac approached OpsGuru, an AWS Advanced Consulting Partner, such that Trimac could get expert support and guidance to adopt best practices before completing development on their new production workloads and accelerating its AWS adoption.

## Our Solution

While many organizations learn cloud best practices through trial and error, Trimac found a faster approach in OpsGuru’s Cloud Launchpad service, which smooths the roadmap to cloud adoption by reducing many of the common problems associated with establishing solid cloud foundations.

Cloud Launchpad combines pre-built, ready-to-go infrastructure as code (IaC) with prescriptive best practices that have been developed over hundreds of successful OpsGuru projects to help organizations move to the cloud quickly and securely. The Cloud Launchpad pre-built IaC includes development, test, and production accounts, giving Trimac a head start in developing its cloud-native applications. Cloud Launchpad was adapted to work with Terraform Cloud to provide the automation and enterprise feature set that Trimac required for managing their infrastructure as code while enforcing best practices in terms of multi-account structure, identity & access management, security and observability. Palo Alto Prisma Cloud was selected to add security scanning into their now DevSecOps development lifecycle.

To secure traffic flowing through the Internet to AWS, OpsGuru recommended and deployed two FortiGate servers, a next-generation firewall solution from Fortinet. To help Trimac fully embrace its cloud-native strategy, OpsGuru set the company up with Amazon Elastic Kubernetes Service (EKS) to deploy its containerized workloads.

To support the goal of getting insight from operational data, OpsGuru first helped Trimac move some business systems and the supporting SQL Server databases from the data centre to AWS using replication technology that minimized disruption to daily business operations. OpsGuru further developed a data pipeline to extract and transform operational data from the SQL Server databases to MongoDB Atlas for downstream business insights. The pipeline results in the adoption of Aurora Serverless and AWS Lambda functions, supporting the company to increasingly adopt an event-driven approach to daily operations while getting insights from data collected from multiple sources to support continuous operation optimizations and exercising true ownership of the data even when multiple third-party applications are continuously used for day-to-day business executions.

OpsGuru also worked with MongoDB Atlas to ensure available features were utilized to provide high availability (i.e., Multi-AZ), cross-Region replication, and the most secure connection (AWS PrivateLink) and authentication (IAM roles) methods, as well as being managed through the same Terraform code base. Cloud native applications connect to the MongoDB cluster from containers running on an autoscaling, multi-AZ Amazon EKS cluster.

To provide native high availability, commercial-off-the-shelf (COTS) software products, data is continuously synced to their cloud native environment via extract, transform, load data pipelines running in a serverless architecture taking advantage of multiple AWS managed services, including AWS Lambda, Amazon SQS, and Amazon Aurora Serverless, to provide native high availability.

In addition, Fortinet FortiGates were deployed from AWS Marketplace in an active-passive Multi-AZ configuration across a primary and DR AWS Region to support high availability, with a secondary active instance pre-configured to support disaster recovery.

Similarly, minimal “hot” resources are deployed in the DR Region to support replication of critical data. In the event of a disaster, vetted and practiced runbooks are followed to deploy the remaining required AWS resources (i.e., the “pilot light” strategy) using IaC and to complete configurations to resume traffic flows to the DR environment and resume required business functionality.

In addition, OpsGuru helped Trimac:

• Deploy security features such as single-sign on (SSO) integration with Microsoft Azure Active Directory

• Implement Amazon Cognito to enable authentication and authorization for their applications’ API endpoints

• Implement AWS App Mesh to provide observability of traffic within their EKS clusters, giving a single pane of glass view of how their application traffic is performing

• Centralize networking to enable full traffic inspection by the FortiGate servers

• Validate its data pipeline architecture and implement it in IaC with best practices for logging, monitoring, and tagging

• Implement AWS CloudWatch Alarms to automate notifications through ServiceNow when operational metrics fall outside of configured thresholds

## The Result

Within three months, OpsGuru fully onboarded Trimac onto AWS with operational data pipelines, fully configured development, test, and production environments for their cloud-native containerized software running on Amazon EKS, and full traffic inspection for comprehensive security. During this time, OpsGuru trained the Trimac team on AWS best practices and provided guidance to enable Trimac to continue accelerating its journey to a cloud-native environment.

As a result of Trimac’s success with Cloud Launchpad, the company took advantage of OpsGuru Virtual Teams to help it operationalize its AWS production environment. Virtual Teams provides Trimac with a team of OpsGuru experts for guidance on next steps in its cloud journey and additional expertise to fill gaps in skill sets when needed during a project. Virtual Teams enable Trimac to build on its cloud foundations at a predictable cost with Trimac setting priorities and OpsGuru providing technical expertise and guidance.

By working with OpsGuru, Trimac was able to significantly compress its time to value in establishing a solid foundation in the cloud to enable its business expansion. Trimac’s application team is now actively developing new cloud-native applications on the Amazon EKS clusters and is managing application deployment with GitOps. The team is also able to give its business partners secure access to deploy Trimac microservices and can easily add more partners through simple updates to its IaC.

In addition, Trimac’s data team is actively using and extending its data pipelines as needed through minor updates to its IaC.