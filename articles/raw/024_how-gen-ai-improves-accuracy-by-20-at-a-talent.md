---
id: "024"
slug: "how-gen-ai-improves-accuracy-by-20-at-a-talent"
title: "How Gen AI Improves Accuracy by 20% at a Talent Acquisition Platform"
word_count: 601
themes: ["data-analytics", "case-study", "genai", "tutorial", "aws", "security"]
extraction_date: "2025-12-19"
content_hash: "7c0d971b861b"
---

# How Gen AI Improves Accuracy by 20% at a Talent Acquisition Platform

## Background

The talent acquisition and recruitment industry is essential for building a company’s workforce, focusing on efficiently and accurately matching candidates to roles. This process is time-sensitive, as delays can increase costs and lead to missed opportunities. Accurate matching is crucial to enhance productivity and reduce turnover, making it a key strategic function in competitive markets.

## The Challenge

The 50-person private software company in Toronto has focused on providing a web-based SaaS talent acquisition platform to solve this problem by creating private talent pools for hiring fleets of contractors and providing a direct sourcing experience where candidates can view jobs and directly apply for jobs and talent acquisition specialists to communicate with candidates and manage the hiring processes seamlessly. However, as the volume of resumes keeps increasing and the job descriptions of the roles get more diverse, new solutions need to be explored to provide that timely and seamless experience.

That explains why the company is interested in leveraging language processing capabilities to solve the problem. Working with OpsGuru, the company identified three use cases that GenAI can significantly enhance. They are (a) using GenAI to enhance the clarity, conciseness and compliance of job descriptions (b) summarizing results from the data instantly and (c) ingesting job applicants’ resumes into vectors to more efficiently identify the fit of candidates and job postings.

## Our Solution

As with any new technology, OpsGuru first started with a rapid proof of concept (POC) to validate the technology stack. After validating the POC, which consisted of a vector database and a few agents, the company rapidly committed to productization because of the apparent value of the solution. This led to a complete redesign of the workflow and resources to ensure the performance and validity of the job-matching process, as well as the security of sensitive personal information.

For the production system, multiple agents were set up to break down queries and send the relevant parts to the respective resume, job posting and company intelligent agent, such that the document can be indexed into summary, embedding and question indices to facilitate overall performance and accuracy of semantic search. The end-to-end workflow leverages Claude on Amazon Bedrock as the foundation model and Weaviate as the vector database.

## The Result

The AWS best practices of data protection using Amazon KMS encryption, Amazon S3 as raw data storage, and AWS IAM for access control have been adopted. At the same time, special care has been taken to ensure ethical guidelines and governance are incorporated: benchmark tests using frameworks such as BLEU and ROUGE have been included to measure the performance of the natural language processing workflows. A growing set of referenceable data has been included in the testing process to regularly measure the fairness and basis of the matching and summarization. Human-in-the-loop feedback has also been used to provide feedback on the accuracy of the process – it has been found in the early rounds of testing that the Gen AI solution has introduced at least a 20% improvement of accuracy compared with the previous workflows, not to mention the improvement in the time taken to analyze resumes, job descriptions and find matching candidates to the job posts.

At the end of the implementation, OpsGuru also conducted knowledge transfer sessions to ensure the company has full ownership of the solution. As a result, the company is confident that they can shepherd the productized solution and grow the solution with more use cases along with the rapidly growing Gen AI technologies.

##