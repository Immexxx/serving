Files for using the [Docker](http://www.docker.com) container system.

****************************************************************************
G instructions start ( https://tensorflow.github.io/serving/docker.html  ) : 

Which containers exist? 

We currently maintain the following Dockerfiles:

Dockerfile.devel, which is a minimal VM with all of the dependencies needed to build TensorFlow Serving.

Building a container

run;

docker build --pull -t $USER/tensorflow-serving-devel -f Dockerfile.devel .

Running a container

This assumes you have built the container.

Dockerfile.devel: Use the development container to clone and test the TensorFlow Serving repository.

Run the container;

docker run -it $USER/tensorflow-serving-devel

Clone, configure and test Tensorflow Serving in the running container;

git clone --recurse-submodules https://github.com/tensorflow/serving

cd serving/tensorflow

./configure

cd ..

bazel test tensorflow_serving/...

G instructions end 


****************************************************************************

KAR instructions start: 

1. git clone this_repo 

2. Rename this file to Dockerfile 

3. docker build --pull -t tf_serving . 

4. Output of "docker images" after approx 10 mins: 

  $ docker images

  REPOSITORY                                                          TAG                 IMAGE ID            CREATED              SIZE

  tf_serving                                                        latest              2994115df913        About a minute ago   1.001 GB

  tf_bazel                                                          latest              04efb46c424d        10 days ago          2.738 GB

5. NOTES: This docker container just installs the base image and the dependencies - NOT EVERYTHING THAT YOU NEED 

Run it: 

docker run -it -p 8888:8888 -p 801:801 tf_serving /bin/bash

6. Verify: "docker ps": 

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS        PORTS                   NAMES

dfa56cdad66b        tf_serving          "/bin/bash"         14 seconds ago      Up 13 seconds       0.0.0.0:801->801/tcp,

0.0.0.0:8888->8888/tcp   zen_goldwasser

7. Get the actual code into the repo and then build it

mkdir kardir; cd kardir; git clone --recurse-submodules https://github.com/tensorflow/serving

8. Execute ./configure in /kardir/serving/tensorflow# ./configure 

9. Now you can test it (can build it first?): => /kardir/serving# bazel test tensorflow_serving/... 

10. To build the entire source tree: "bazel build tensorflow_serving/...  "

(This takes about 2 hrs - approx) 

11. 


SNIP

****************************************
Build: (URL: https://tensorflow.github.io/serving/setup) 

TensorFlow Serving uses Bazel to build. Use Bazel commands to build individual targets or the entire source tree.

To build the entire tree, execute:

bazel build tensorflow_serving/...

Binaries are placed in the bazel-bin directory, and can be run using a command like:

./bazel-bin/tensorflow_serving/example/mnist_inference

To test your installation, execute:

bazel test tensorflow_serving/...

****************************************







