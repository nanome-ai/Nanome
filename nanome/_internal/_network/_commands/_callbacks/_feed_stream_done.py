def _feed_stream_done(network, result, request_id):
    network._call(request_id)