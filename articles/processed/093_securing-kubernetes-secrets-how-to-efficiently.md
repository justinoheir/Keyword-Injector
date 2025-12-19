---
id: "093"
slug: "securing-kubernetes-secrets-how-to-efficiently"
title: "Securing Kubernetes secrets: How to efficiently secure access to etcd and protect your secrets"
word_count: 442
themes: ["data-analytics", "genai", "tutorial", "kubernetes", "containers", "security"]
extraction_date: "2025-12-19"
content_hash: "200d92670d80"
---

# Securing Kubernetes secrets: How to efficiently secure access to etcd and protect your secrets

## Securing Kubernetes secrets: How to efficiently secure access to etcd and protect your secrets

Etcd is a distributed, consistent and highly-available key value store used as the Kubernetes backing store for all cluster data, making it a core component of every K8s deployment with Financial services cloud consulting SOX compliance.

Due to its central role etcd may contain sensitive information related to access of the deployed services and their associated components, such as database credentials, CA keys, LDAP logins credentials it is a premium target for malicious attacks.

Historically, in traditional, non-containerised environments, this data was NOT stored in such a centralised manner as credentials were usually under an ownership of a specific team that was responsible for maintaining a certain component of the stack: the DB access credentials, for example, were known only to the DBA team, CA keys have been in the hands of few selected System Administrators etc.

With K8s, the required approach is notably different as credentials are now kept within a single central place (etcd), which, if not properly hardened, can lead to serious security breaches as the attacker may now create fake certificates, access databases and applications.

Managing and hardening your secrets becomes even more critical with tools such as Helm and Tiller; these tools allow you to install (or redeploy) an entire K8s based datacenter within minutes and they constantly interact with etcd.

The Center for Internet Security (CIS) came up with this publicly available document providing guidance on how to properly harden and secure your Kubernetes cluster.

The only single recommendation CIS provides regarding hardening etcd is using TLS:

## Encrypting Secret Data at Rest

Starting with K8s 1.7 (and etcd v3) you can encrypt resources inside etcd using several different algorithms. At the very least, you should encrypt all your secrets. It is especially true if you are using Helm as a lot of Helm charts require LDAP or DB credentials to be directly made available in the ConfigMaps.

The encryption follows a very simple rule:

encrypt using the first provider defineddecrypt after locating a functional provider at checking each provider in the order the providers are defined

To implement the full workflow, it is necessary to add the experimental-encryption-provider-config flag to the apiserver

Define the EncryptionConfig config file (place the content in /etc/kubernetes/pki/encryption-config.yaml)

Within the file, the resources.resources field is an array of Kubernetes resource names that should be encrypted. The providers array is an ordered list of the possible encryption providers.

Enable experimental-encryption-provider-config in the kube-apiserver. Edit /etc/kubernetes/manifests/kube-apiserver.yaml and add:

Restart the apis