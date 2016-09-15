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
 
 DA: This confirms that the server loads and runs the trained model successfully!
 
 You can do a Cntrl-C on the server terminal to stop the server. ps -ef will tell you if the server is running or not. 
 
 
17. Running other models: Download the model, build and export it - bazel-bin it
  
  Export Inception model in container (see  :https://tensorflow.github.io/serving/serving_inception if req) 
  
  17.a: root@dfa56cdad66b:/kardir/serving# curl -O http://download.tensorflow.org/models/image/imagenet/inception-v3-2016-03-01.tar.gz
  
  17.b: tar xzf inception-v3-2016-03-01.tar.gz
  
  17.c: bazel-bin/tensorflow_serving/example/inception_export --checkpoint_dir=inception-v3 --export_dir=inception-export

  (Will see: WARNING:tensorflow:tf.op_scope(values, name, default_name) is deprecated, use tf.name_scope(name, default_name, values)
  Successfully loaded model from inception-v3/model.ckpt-157585 at step=157585.
  Successfully exported model to inception-export)
  
  
18. Once the model is there, start the server: 

  /kardir/serving# bazel-bin/tensorflow_serving/model_servers/tensorflow_model_server --port=9000 --model_name=inception --model_base_path=inception-export       
  
  Output: tensorflow_serving/model_servers/main.cc:171] Running ModelServer at 0.0.0.0:9000 ...
  
19. Now that the server is running, you can use a client to send requests and get responses from the server 

  bazel-bin/tensorflow_serving/example/inception_client --server=localhost:9000 --image=/kardir/visionPics/snowdogs.jpg  (Examples similar to this: http://ouralaskanadventures.com/wp-content/uploads/2015/04/Sled-Dogs.jpg) 
  
  bazel-bin/tensorflow_serving/example/inception_client --server=localhost:9000 --image=/kardir/visionPics/street.jpg
  
  Output: 
  
   *******
  
  D0915 17:50:30.040548009    8674 ev_posix.c:101]             Using polling engine: poll

 outputs {
  key: "classes"
  value {
    dtype: DT_STRING
    tensor_shape {
      dim {
        size: 1
      }
      dim {
        size: 5
      }
    }
    string_val: "dogsled, dog sled, dog sleigh"
    string_val: "Eskimo dog, husky"
    string_val: "Siberian husky"
    string_val: "malamute, malemute, Alaskan malamute"
    string_val: "snowmobile"
  }
 }
 outputs {
  key: "scores"
  value {
    dtype: DT_FLOAT
    tensor_shape {
      dim {
        size: 1
      }
      dim {
        size: 5
      }
    }
    float_val: 9.57605266571
    float_val: 7.05985927582
    float_val: 5.23411989212
    float_val: 2.50853919983
    float_val: 2.42705345154
  }
}

  E0915 17:50:38.418339608    8674 chttp2_transport.c:1810]    close_transport: {"created":"@1473961838.418305549","description":"FD shutdown","file":"src/core/lib/iomgr/ev_poll_posix.c","file_line":427}

 ********
  
  
  

  



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







