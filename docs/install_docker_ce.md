# How To Install Docker CE on Ubuntu 22.04|20.04|18.04

Follow the steps in this article to install Docker CE on the Ubuntu 22.04|20.04|18.04 Linux distribution. Docker Engine is a container runtime engine that lets you package your applications and their dependencies into a standardized unit for software development and distribution.

Docker containers, as you may know, wrap a piece of software in a complete filesystem that contains everything it needs to run: code, runtime, system tools, system libraries - anything that can be installed on a server. This ensures that it will always run the same way, regardless of the environment.

## Step 1: Update the System

```
sudo apt -y update
```
## Step 2: Install basic dependencies

There are a few dependencies that must be met before we can configure Docker repositories and install packages. Install them in your terminal by typing the following commands.

```
 sudo apt -y install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
```
