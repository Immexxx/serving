Files for using the [Docker](http://www.docker.com) container system.

G instructions start: 

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

KAR instructions start: 

1. git clone this_repo 

2. Rename this file to Dockerfile 

3. docker build --pull -t tf_serving . 

4. Output of "docker images" after approx 10 mins: 

$ docker images

REPOSITORY                                                          TAG                 IMAGE ID            CREATED              SIZE

tf_serving                                                        latest              2994115df913        About a minute ago   1.001 GB

tf_bazel                                                          latest              04efb46c424d        10 days ago          2.738 GB

5.





