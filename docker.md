## Attempt to install Docker
I wanted to try and integrated Docker with Datadog. Here was my thought process.
 
I have used Docker once in a project, but never really understood how it really works. I understand at a high level, but I’ve never been able to instinctively know how to set a docker container. 

The first step I did was google “How to install docker on mac”, 
I also googled TutorialsPoint Docker and both provided me with the next step, 
which was to install docker with homebrew.

![Install Docker with Homebrew](a/raw/b/screenshots/docker-screenshots/brew-install-docker.png)

I then managed to stumble upon this article. https://docs.docker.com/docker-for-mac/, which made me look up the versions for docker, docker-compose, and docker-machine. I didn’t have docker-compose. So I managed to just do brew install docker-compose to install it. 

Once I finished, I have all 3 of these and am ready for the next step.

![Docker Versions](a/raw/b/screenshots/docker-screenshots/docker-version.png)

As I continue going through the article, I try and run the hello world docker container.

docker run hello-world and docker run -d -p 80:80 --name webserver nginx

However, when I run both commands, I get this error message. "Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?”
![Attempt to Login](a/raw/b/screenshots/docker-screenshots/logging-in-docker.png)

### Having trouble running docker ps here
![Docker PS](a/raw/b/screenshots/docker-screenshots/installing-docker.png)

So I googled it and I encounter this post https://stackoverflow.com/questions/44084846/cannot-connect-to-the-docker-daemon-on-macos

So I proceed to do brew cask install docker and open the Docker app. 

So the reason why I encountered the error "Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?” was because I wasn’t signed in. 

When I run docker run hello-world, I get this message "unauthorized: incorrect username or password.” So I proceed to google again. 

The reason I get this warning is because of this post here in github. https://github.com/docker/hub-feedback/issues/935

#### Signing into Docker Cloud to get access!
![Signing In Docker](a/raw/b/screenshots/docker-screenshots/docker-cloud.png)
I managed to run docker login and insert my username and password and now it works!

So now I run $ docker run -d -p 80:80 --name webserver nginx and I get something returning in my browser!

#### Running hello-world on my Docker
![Hello World](a/raw/b/screenshots/docker-screenshots/hello-world.png)


I continue running through the documentation and I learn that whenever you spin up a server, it gets saved onto your history of containers. Running docker container ls shows the containers that are currently being spun up, running docker container ls -a shows the history of previous running containers.

There are also “image” commands. Based on this stack overflow post, https://stackoverflow.com/questions/23735149/what-is-the-difference-between-a-docker-image-and-a-container. I know that a running instance of an image is a container.

Based on these 2 findings, I know when I should look at an image and when I should look at a container.

#### Reflection for Part I:  
I learned what Docker is by toying around with it in my terminal and googling stack overflow items.! I know that Docker is used as an easier way to setup a virtual environment which is what we are doing in step 1 anyways. So instead of having to setup Vagrant or VMware, Docker actually does everything in the cloud and you can spin up your servers by running docker commands like this one "docker run -d -p 80:80 --name webserver nginx”

So the next step for me is to find a way to run my python flask server onto docker! 

![Nginx](a/raw/b/screenshots/docker-screenshots/nginx.png)

## Part II
Now I go here https://docs.datadoghq.com/integrations/docker_daemon/.
And I am trying to integrate Docker into my data-dog agent.
One issue that I am encountering is adding the user running the Agent to docker’s group. In Mac OS, I get a usermod command not found. As I continue googling/stack overflowing, I see that usermod is for Linux commands. 

I proceed to google around for workarounds here. I spend at least an hour and I put this path on pause. 

#### Picture of Docker Integration from Datadog
![Docker Integration](a/raw/b/screenshots/docker-screenshots/datadog-docker.png)



#### Posts to help me debug usermod
https://superuser.com/questions/60150/is-there-a-usermod-equivalent-in-terminal-for-os-x-10-6-1  

https://superuser.com/questions/615146/unix-usermod-command-not-found/615165#615165

https://superuser.com/questions/214004/how-to-add-user-to-a-group-from-mac-os-x-command-line

Understanding dscl was like opening a can of worms for me at this point. 


