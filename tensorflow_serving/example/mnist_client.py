# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

#!/usr/bin/env python2.7

"""A client that talks to tensorflow_model_server loaded with mnist model.

The client downloads test images of mnist data set, queries the service with
such test images to get predictions, and calculates the inference error rate.

Typical usage example:

    mnist_client.py --num_tests=100 --server=localhost:9000
    
    
Kar: 
    Code Flow: 
        result[done] holds the number of test cases executed 
        result[error] holds the number of test cases that had an error 
        result[active] holds the max number of calls you can make concurrently. Set to 1 by default 

"""

import sys
import threading

# This is a placeholder for a Google-internal import.

from grpc.beta import implementations
import numpy
import tensorflow as tf

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
from tensorflow_serving.example import mnist_input_data


tf.app.flags.DEFINE_integer('concurrency', 1,
                            'maximum number of concurrent inference requests')
tf.app.flags.DEFINE_integer('num_tests', 100, 'Number of test images')
tf.app.flags.DEFINE_string('server', '', 'mnist_inference service host:port')
tf.app.flags.DEFINE_string('work_dir', '/tmp', 'Working directory. ')
FLAGS = tf.app.flags.FLAGS


def do_inference(hostport, work_dir, concurrency, num_tests):
  """Tests mnist_inference service with concurrent requests.

  Args:
    hostport: Host:port address of the mnist_inference service.
    work_dir: The full path of working directory for test data set.
    concurrency: Maximum number of concurrent requests.
    num_tests: Number of test images to use.

  Returns:
    The classification error rate.

  Raises:
    IOError: An error occurred processing test data set.
  """
  test_data_set = mnist_input_data.read_data_sets(work_dir).test
  host, port = hostport.split(':')
  channel = implementations.insecure_channel(host, int(port))
  stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
  cv = threading.Condition()
  result = {'active': 0, 'error': 0, 'done': 0}
  def done(result_future, label):
    with cv:
      # Workaround for gRPC issue https://github.com/grpc/grpc/issues/7133
      try:
        exception = result_future.exception()
      except AttributeError:
        exception = None
      if exception:
        result['error'] += 1
        print exception
      else:
        sys.stdout.write('.')
        sys.stdout.flush()
        response = numpy.array(result_future.result().outputs['scores'])
        #argmax => Returns the indices of the maximum values along an axis.
        prediction = numpy.argmax(response)
        if label != prediction:
          result['error'] += 1
      result['done'] += 1
      result['active'] -= 1
      cv.notify()
  for _ in range(num_tests):
    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'mnist'
    image, label = test_data_set.next_batch(1)
    request.inputs['images'].CopyFrom(
        tf.contrib.util.make_tensor_proto(image[0], shape=[1, image[0].size]))
    with cv:
      while result['active'] == concurrency:
        cv.wait()
      result['active'] += 1
    #Kar: Call setup (made) to the server here! 'stub' holds the server config 
    result_future = stub.Predict.future(request, 5.0)  # 5 seconds
    result_future.add_done_callback(
        lambda result_future, l=label[0]: done(result_future, l))  # pylint: disable=cell-var-from-loop
  with cv:
    while result['done'] != num_tests:
      cv.wait()
    return result['error'] / float(num_tests)


def main(_):
  if FLAGS.num_tests > 10000:
    print 'num_tests should not be greater than 10k'
    return
  if not FLAGS.server:
    print 'please specify server host:port'
    return
  error_rate = do_inference(FLAGS.server, FLAGS.work_dir,
                            FLAGS.concurrency, FLAGS.num_tests)
  print '\nInference error rate: %s%%' % (error_rate * 100)


if __name__ == '__main__':
  tf.app.run()
