# About API Titan Works

Today, every company is a software company; we use software every day; consider Uber, which is merely an app. BIND DNS, Postfix, Apache, Dovecot, and many more are over 20 years old and are still actively used in industry today. Almost all of these software setups have been automated by directly altering configuration files with automation tools such as Ansible, Puppet, and others. While sysadmins have some relief due to the idempotent nature of these tools, they are required to repeat the configurations as many times as they like. If something goes wrong, it is exceptionally difficult to debug because the same software is configured in so many different ways across Linux distributions, the default OS on which these pieces of software are running. There is no certainty that misconfiguration will not occur. There is no certainty that a misconfiguration would compromise security or performance.There is no certainty that a misconfiguration would compromise security or performance.

If we can create a well-defined HTTP APIS for managing and configuring this widely used software, we will be able to address all of the issues raised above. To deal with these pieces of software, everyone must learn a single unified and secure API, which will make their lives easier.

At API Titan Works, we aim to create a global community of API developers and experts who are passionate about the open source software model in order to make our vision a reality.

## Why  BIND First

## A DNS lookup is the first step in almost every Internet connection.

There is a DNS lookup to resolve a DNS name to an IP address before your mail server sends an email or before your web browser displays a web page. Watch Eddy Winstead of ISC's [DNS Fundamentals presentation](https://www.youtube.com/watch?v=oeceM-R8DVU&feature=emb_logo) or read [A Warm Welcome to DNS](https://powerdns.org/hello-dns/) by Bert Hubert of PowerDNS.

## BIND 9 on the Internet

BIND is used successfully in a wide range of applications, including publishing the (DNSSEC-signed) DNS root zone and many top-level domains, hosting providers who publish very large zone files with many small zones, enterprises with both internal (private) and external zones, and service providers with large resolver farm.

## PyDNS API

This project aims to create a REST API for [BIND DNS](https://www.isc.org/bind/), the Internet's de-facto DNS software, using [dnspython](https://www.dnspython.org/), a DNS toolkit for Python Programming Language. It is useful for queries, zone transfers, dynamic updates, nameserver testing, and a variety of other tasks.

### ```dnspython``` provides both high and low level DNS access. 

- The high level classes search for data by name, type, and class and return an answer set. 

- The low-level classes allow for the manipulation of DNS zones, messages, names, and records directly. Almost every RR type is supported.

dnspython was initially created at [Nominum](https://www.nominum.com)where to test DNS nameservers.

## Inspired by 

While we in search for  the tool kit for developing this API we have inspired by [this great project](https://gitlab.com/jaytuck/bind-rest-api) where it has used FastAPI Python  framework to develop an API for BIND DNS. 

## About FastAPI 

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>

---

**Documentation**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Source Code**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

The key features are:

* **Fast**: Very high performance, on par with **NodeJS** and **Go** (thanks to Starlette and Pydantic). [One of the fastest Python frameworks available](#performance).
* **Fast to code**: Increase the speed to develop features by about 200% to 300%. *
* **Fewer bugs**: Reduce about 40% of human (developer) induced errors. *
* **Intuitive**: Great editor support. <abbr title="also known as auto-complete, autocompletion, IntelliSense">Completion</abbr> everywhere. Less time debugging.
* **Easy**: Designed to be easy to use and learn. Less time reading docs.
* **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.
* **Robust**: Get production-ready code. With automatic interactive documentation.
* **Standards-based**: Based on (and fully compatible with) the open standards for APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (previously known as Swagger) and <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* estimation based on tests on an internal development team, building production applications.</small>

## Core Feature of PyDNS API

This is a BIND DNS API that supports the following core functions and others:

* It can  export a BIND  zone file to a JSON  file
* It utilises the HTTP GET method to locate a specific DNS record.
* It utilises the HTTP PUT  method to replace or update a DNS record
* It utilises the HTTP DELETE method for deleting a DNS record
* It safeguards the API Key. 
* Ii offers an audit log for 'apikey' to 'DNS changes.'
* It makes use of the [acme.sh](https://acme.sh) tool kit to generate LetsEncrypt certificates via the API.
* It can be installed in a Docker container to make it easier to run in any environment that supports Docker
* Auto-generated API documents



