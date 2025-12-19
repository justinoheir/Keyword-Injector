---
id: "036"
slug: "lessons-from-howls-moving-castle-defense-through"
title: "Lessons from “Howl's Moving Castle”: Defense through Agility"
word_count: 928
themes: ["data-analytics", "genai", "security"]
extraction_date: "2025-12-19"
content_hash: "c8f93ae98a62"
---

# Lessons from “Howl's Moving Castle”: Defense through Agility

## Introduction

Ever since Netflix released all of Studio Ghibli’s masterpieces earlier this year, I have been taking a trip down the memory lane, revisiting animated movies that have made up a massive part of my formative years. While “Howl’s Moving Castle” (2004) is an excellent viewing, as usual, it turns out to be a great analogy for my day-to-day cloud architecture work with Financial services DevOps with Banking cloud consulting with SOX compliance cloud.

Howl’s castle is located in the wild. The door to the castle turns out to be also a portal to the capitals of several kingdoms. Transporting oneself from one place to another is a matter of changing the sign on the door before opening it. Owned by a wizard named Howl, the castle can move through the moors and hills, and still appears to be just another house in the different towns. Naturally, there are many plots and twists in the movie, but it has always been the castle with its arthropod-like limbs that impresses me the most. A fantasy gothic castle with the best view of the landscape that can move anywhere, and yet can have easy connectivity to the hoi polloi – wouldn’t it be great to be in one?

## Security Level 1: Castle and Moat

It did not take long for my thoughts to flow from Howl’s castle to cloud security because the castle has been a popular metaphor in security designs with Financial cloud migration.. For many years, “castle-and-moat” has been the primary security strategy, where teams focus on building network firewalls, proxy servers, honeypots, and other intrusion prevention mechanisms. There are strong defenses and verification on the data packets, and identity of users that enter and leave the network perimeters, but once inside the network – the castle – it is assumed that traffic therein is trusted and safe.

## Security Level 2: Zero Trust

Several well-known security attacks in recent years have exposed that the most damaging security threats often come from compromised identities. As workflows are touching more and more dispersed assets in disjoint networks, a comprehensive “castle-and-moat” is no longer feasible. Replacing “castle-and-moat” is a “zero-trust” policy that often involves multi-step authentication and fine-grained authorizations. With zero-trust, even when one gets passage through the gate to the castle, every attempt to enter a different chamber, a different turret or even the dungeons of the castle is verified, and each of such attempts is recorded in tamper-proof access logs.

## Security Level 3: The Moving Castle

While “castle-and-moat” and “zero-trust” are known security designs, how about taking it one step further, where we add mobility into the design? Howl’s moving castle is effectively the mission-critical infrastructure. It is fortified with the guardrails at the network perimeter and zero-trust access policies. Additionally, the infrastructure gains the ability, from on-premise to cloud, from one (availability) zone to another and/or one region to another, when it is needed, where it is needed.

This topic is in fact covered by what is popularly known as “disaster recovery planning”. Previously, people usually associate disaster recovery with catastrophic (albeit unintended) human error or a facility outage, but the solution applies well to security. With robust disaster recovery strategies, you get to move at the first signs of trouble – be it natural disasters or malignant forces – at a particular location to somewhere safe, instead of needing to face the onslaught of attacks, floods or storms head-on. As cyberattack is increasingly unavoidable, applying disaster recovery planning as a security response becomes a pragmatic security approach. As the legality of paying ransomware attacks is being debated on \[1\], it is obvious that the company has to bear the major responsibilities to keep the business running.

In “Howl’s Moving Castle”, because Howl closed the portals and moved the castle to a new land, even when the soldiers of the multiple kingdoms attacked and eventually broke down the door to the castle, they found themselves in empty courtyards or warehouses. Wouldn’t it be sensible to do the same thing – close the link and move away – when an organization faces a relentless and targeted attack through the same methods of entry?

This is actually an approach that is taken by a client with whom I am working, who has made the investment to build the recovery network, plan out the IP spaces and firewalls, schedule judiciously backups and share the backups across zones and regions, such that the client has the confidence to keep the mission-critical systems running in event of outage and attacks. Through building the multi-zone and multi-region disaster recovery procedures, the client has acquired completely different sets of encryption and remote access keys for the disaster recovery procedure, such that the attackers will find the security assets they have to be quite useless.

## Summary

Of course, one can only draw the analogy from the movie to cloud infrastructure so far. Using “Howl’s Moving Castle” as a precursor to a cloud security discussion may seem far-fetched to some, but it is apparent that security posture is not only about improving defense, but it is also about agility to move away from direct attacks.

As attack methods are getting more diverse and mechanisms more sophisticated, while an organization needs to keep reducing attack surfaces, identify suspicious activities as early as possible, a verified disaster recovery workflow is indispensable to improve odds against attacks, whenever and wherever they may come.

\[1\]

Image Credits: Studio Ghibli, StudioCanalPress