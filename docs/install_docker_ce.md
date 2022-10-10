# Installing Docker CE on Ubuntu 22.04|20.04|18.04

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

## Step 3: Install Docker CE

Remove any previous versions of Docker and their dependencies.

```
sudo apt remove docker docker-engine docker.io containerd runc
```

**Import Docker repository GPG key:**

```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/docker-archive-keyring.gpg
```

**The Docker CE repository can then be added to Ubuntu.**

```
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

**Finally install Docker CE on Ubuntu22.04|20.04|18.04:**

```
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```

**Add your user account to docker group.\

```
sudo usermod -aG docker $USER
newgrp
```
**NOTE**

During a login session, the ```newgrp``` command is used to change the current group ID. If the - flag is specified, the user's environment will be reinitialized as if the user had logged in; otherwise, the current environment, including the current working directory, will remain unchanged.


**Check the Docker version to ensure proper installation:***

```
docker version
```

## Step 4: Set up Docker Compose.**

Docker Compose must be installed because we will be using it to deploy several containers with our ```bindapi``` container.

We use ```curl``` to install the most recent Compose on your Linux machine.

```
curl -s https://api.github.com/repos/docker/compose/releases/latest | grep browser_download_url  | grep docker-compose-linux-x86_64 | cut -d '"' -f 4 | wget -qi -

```








