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

11. To run tests to verify if things are okay:
  
  bazel test tensorflow_serving/...

  Should output: Executed 45 out of 45 tests: 45 tests pass.

12. /kardir/serving# bazel build //tensorflow_serving/example:mnist_export

(See: https://tensorflow.github.io/serving/serving_basic.html)

Output: 

INFO: Found 1 target...
[0 / 2] BazelWorkspaceStatusAction stable-status.txt
Target //tensorflow_serving/example:mnist_export up-to-date:
  bazel-bin/tensorflow_serving/example/mnist_export
INFO: Elapsed time: 44.046s, Critical Path: 22.72s


13.  /kardir/serving# bazel-bin/tensorflow_serving/example/mnist_export /tmp/mnist_model

  Output: 

training accuracy 0.9092
Done training!
Exporting trained model to /tmp/mnist_model
Done exporting!
root@dfa56cdad66b:/kardir/serving# ls /tmp/mnist_model 


  Result of step 13: "With that, your TensorFlow model is exported and ready to be loaded!"

14. Load Exported Model With Standard TensorFlow Model Server

 /kardir/serving# bazel build //tensorflow_serving/model_servers:tensorflow_model_server
 
 Output:
 
 Target //tensorflow_serving/model_servers:tensorflow_model_server up-to-date:
  bazel-bin/tensorflow_serving/model_servers/tensorflow_model_server
  
15. bazel-bin/tensorflow_serving/model_servers/tensorflow_model_server --port=9000 --model_name=mnist --model_base_path=/tmp/mnist_model/


 /kardir/serving# bazel-bin/tensorflow_serving/model_servers/tensorflow_model_server --port=9000 --model_name=mnist --model_base_path=/tmp/mnist_model/
 
 Output: 
 
 I tensorflow_serving/core/loader_harness.cc:118] Successfully loaded servable version {name: mnist version: 1}
 I tensorflow_serving/model_servers/main.cc:171] Running ModelServer at 0.0.0.0:9000 ...
 I tensorflow_serving/sources/storage_path/file_system_storage_path_source.cc:252] File-system polling update: Servable:{name: mnist version: 1}; Servable path: /tmp/mnist_model/00000001; Polling frequency: 30

16. With the server running, do a "docker exec -i -t dfa56cdad66b /bin/bash" in a new Terminal window - this will drop you into the Docker container on a separate Terminal window 

 Here, build and run the client test script: 
 
 Build: 
 
 /kardir/serving# bazel build //tensorflow_serving/example:mnist_client

 Run: 
 
 /kardir/serving# bazel-bin/tensorflow_serving/example/mnist_client --num_tests=1000 --server=localhost:9000
 
 Output: 
 
 E0914 22:21:55.414200872    7583 chttp2_transport.c:1810]    close_transport: {"created":"@1473891715.414171707","description":"FD shutdown","file":"src/core/lib/iomgr/ev_poll_posix.c","file_line":427}

 Inference error rate: 91.5%


  



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







