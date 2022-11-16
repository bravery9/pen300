https://docker-curriculum.com/

to test whether the docker is working correctly
`docker run hello-world`

pulling a container
`docker pull busybox`

you can check the downloaded images using

```
└─# docker images      
REPOSITORY    TAG       IMAGE ID       CREATED         SIZE
busybox       latest    bc01a3326866   2 weeks ago     1.24MB
hello-world   latest    feb5d9fea6a5   13 months ago   13.3kB
gcc           4.9       1b3de68a7ff8   5 years ago     1.37GB

```

```
# docker run busybox echo "hello from busybox"
hello from busybox

```

to check the current running containers

`docker ps`

to checking previously run container

`docker ps -a`

we can interact with the docker container using 
`docker run -it busybox sh`

each time docker creates a new system alltogether.

after running docker consumes memory so all the containers can be removed by

`└─# docker rm $(docker ps -a -q -f status=exited)`

or `docker container prune`

`docker rmi`

## running a web app

`docker run --rm -it prakhar1989/static-site`

Since the image doesn't exist locally, the client will first fetch the image from the registry and then run the image. 


Lets create a command such that we can run docker run to publish ports

```
docker run -d -P --name static-site prakhar1989/static-site
```

to check the exposed ports

```
docker port static-site
```

```
└─# docker port static-site                                    
443/tcp -> 0.0.0.0:49153
443/tcp -> :::49153
80/tcp -> 0.0.0.0:49154
80/tcp -> :::49154
```

we can go to http://localhost:49154

we can give a custom port also

`docker run -p 8080:80 prakhar1989/static-site`

## Creating our own image

To see the images available offline

`docker images`

we can pull a specific version of docker image

`docker pull ubuntu:18.04`

creating an image of flask app

`git clone https://github.com/prakhar1989/docker-curriculum.git`
`cd docker-curriculum/flask-app`

create a Dockerfile

```Dockerfile
FROM python:3.8

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# define the port number the container should expose
EXPOSE 5000

# run the command
CMD ["python", "./app.py"]
```

`docker build -t yourusername/catnip .`

`docker run -p 8888:5000 yourusername/catnip`

`docker login`

`docker push yourusername/catnip`

`docker run -p 8888:5000 yourusername/catnip`

It has further instructions to create docker instances and uploading into amazon and docker compose etc.

I liked the tree command

```
┌──(root㉿kali)-[~/docker-curriculum]
└─# tree flask-app 
flask-app
├── app.py
├── Dockerfile
├── Dockerrun.aws.json
├── requirements.txt
└── templates
    └── index.html
```

To search for a particular container

`docker search havoc`

## Approaches to creating docer

1. create docker then install anaconda - anaconda so that we can install packages without polluting the entier environment

2. or install anaconda then create a docker image

3. or create new docker container

https://docs.docker.com/engine/reference/commandline/create/

creating your own instance would take a lot of time and installation of packages

4. instead we can use preinstalled docker instances

`docker pull ubuntu`

https://www.linode.com/docs/guides/create-tag-and-upload-your-own-docker-image/

`docker run --name havoc_test_server -it ubuntu:latest bash`

if you find no internet then we can also try

`systemctl restart docker`

trying to run commands to set up docker


```
root@faad191a73d6:/# history
    1  apt update
    2  ping
    3  apt install iputils
    4  apt install build-essential
    5  sudo add-apt-repository ppa:deadsnakes/ppa
    6  add-apt-repository ppa:deadsnakes/ppa
    7  apt install software-properties-common
    8  apt update
    9  add-apt-repository ppa:deadsnakes/ppa
   10  apt update
   11  sudo apt install python3.10 python3.10-dev
   12  apt install python3.10 python3.10-dev
   13  history
   14  git clone https://github.com/HavocFramework/Havoc.git
   15  apt install git
   16  git clone https://github.com/HavocFramework/Havoc.git
   17  cd Havoc/Client
   18  make
   19  apt install make
   20  make
   21  ls -al
   22  rm -rf Build
   23  make
   24  cmake .
   25  wget https://github.com/Kitware/CMake/releases/download/v3.25.0-rc4/cmake-3.25.0-rc4-linux-aarch64.sh
   26  apt install wget
   27  wget https://github.com/Kitware/CMake/releases/download/v3.25.0-rc4/cmake-3.25.0-rc4-linux-aarch64.sh
   28  chmod cmake-3.25.0-rc4-linux-aarch64.sh 
   29  chmod +x cmake-3.25.0-rc4-linux-aarch64.sh 
   30  ./cmake-3.25.0-rc4-linux-aarch64.sh 
   31  cd ..
   32  ls -al
   33  cd Havoc/
   34  ls -al
   35  cd Client
   36  ls -al
   37  cmake
   38  make
   39  cat makefile
   40  sed -i 's/cmake/cmake-3.25.0-rc4-linux-aarch64/g' makefile
   41  cat makefile
   42  make
   43  cd cmake-3.25.0-rc4-linux-aarch64
   44  ls -al
   45  cd bin
   46  ls -al
   47  pwd
   48  cd ..
   49  history
```











