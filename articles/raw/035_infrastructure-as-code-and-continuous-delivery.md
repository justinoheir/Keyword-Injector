---
id: "035"
slug: "infrastructure-as-code-and-continuous-delivery"
title: "Infrastructure as Code and Continuous Delivery Makes Database Development Easy"
word_count: 902
themes: ["devops", "terraform", "data-analytics"]
extraction_date: "2025-12-19"
content_hash: "f0e707d6e893"
---

# Infrastructure as Code and Continuous Delivery Makes Database Development Easy

## Introduction

• DevOps

Infrastructure as Code (IAC), Continuous Integration and Continuous Delivery (CI/CD) are becoming part of the standard pattern for delivering application code into production environments. Unfortunately, this methodology is rarely applied when deploying models for relational databases, often favoring more classic and manual methods that are thought to be safer. This is unfortunate because Infrastructure as Code and Continuous Delivery Makes Database Development easier for the developer and less risky for the business.

Implementing IAC combined with a CI/CD pipeline usually follows a progression from manual, to semi-automated with infrequent releases, to automated with more frequent releases. The common occurrence when CI/CD is applied to database models is to transition from manual to semi-automated but often, the process gets stuck at this stage, never reaching a stage with frequent releases. The cause of this stall will be slightly different for each company, but it is generally fear of losing or corrupting data. Every database developer I know has a war story about a production database mistake they have made that caused data loss or corruption.

Usually, these mistakes have a semi-happy ending where there was some downtime, and the database backup was used to do a full restore, but that is not always the case, and sometimes data is gone forever.

In the postmortems of database events, the common suggestions are to go slower to better understand changes. On the surface, this is a good suggestion, but what “slowing down” means to most companies is to release less frequently. Unfortunately, releasing less often is not going slower, it just feels like it is. If the same number of developers are making roughly the same number of changes and those changes are just being released less often but all at once, that is better characterized as doing nothing broken up by short periods of going very fast. This can create a negative feedback loop where large batches of changes are made all at once to a database model, causing errors, leading to releasing less often, leading to larger batches, and more errors.

## Here are changes you can make to improve your database deployments, and why they help:

• What: make small changes all the way to production. Why: small changes are less complex, they are easier to understand, easier to quickly code review, and if a mistake is made the impact of that mistake should be smaller, thus easier to fix. These changes need to be made all the way to production so we can ensure that all our databases (development, test, and production) are in the same state as well as so that the time between when a change is made and when a change is deployed is minimized so if there is an issue, the developer is still operating in the same context. Example: If you are adding a column and making it not null, do it in multiple steps rather than a single step. First add the column, release, then populate, release, then make not null, release.

• What: Do not combine multiple changes into a single release, each change should get its own release. Why: You want to clearly understand what change each release is making, rolling up multiple releases into a single deployment can make changes to complex to easily understand. As well dependencies and order of operation errors can be introduced when rolling up releases.

• What: Deploy all changes through your entire pipeline(I.E through the development and testing environments). Why: Development and testing environments exist to help catch mistakes before proceeding to production, but we have to make sure we use them. These environments should be combined with manual or automated testing to not just check for syntax and dependency errors, but for logic errors as well.

• What: Never make manual changes to your databases. Why: Manual changes directly in production are one of the easiest ways to make large mistakes quickly. Any manual change you can make should be check in to source code and deployed via a release. This will allow changes to be code reviewed, tested, and validated before entering production. This allows manual changes, even critical ones, to go through the same validation process as normal code, this is the best way to solve problems quickly, rather than making them worse. As well there are some additional benefits that checking in manual changes/fixes allows other developers in the future to see and copy how other problems in the past were resolved.

The steps above may look like they introduce a lot of overhead, but realistically they are just a reversal of most people’s current practices. Rather than doing a lot of work less often, the pattern above is to do a little work more often. As well, mistakes will always happen. This applies to databases just as much as any other software. The best approach you can take is the path that limits impact and increases the chance of a safe fix. The current standard for deploying databases does not do this.

Addendum: As stated above, mistakes will always happen, the pattern above does not remove all mistakes as nothing can, it is important that a disaster recovery strategy exists for when large mistakes happen. If you do not have one for your databases, that should be your highest priority above all else.