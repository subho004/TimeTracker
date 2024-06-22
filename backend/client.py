import grpc
import logging
import time
from timeseries_pb2 import StreamRequest
from timeseries_pb2_grpc import TimeSeriesServiceStub

# gRPC server address
SERVER_ADDRESS = 'localhost:50051'

def stream_time_series_data():
    # Establish a connection to the gRPC server
    channel = grpc.insecure_channel(SERVER_ADDRESS)
    stub = TimeSeriesServiceStub(channel)

    # Create a stream for receiving TimeSeriesData messages
    response = stub.StreamTimeSeriesData(StreamRequest(start_timestamp=0, end_timestamp=int(time.time()), limit=677500))

    # Iterate over the stream and log each received data item
    for data_item in response:
        logging.info(f"Received data: {data_item}")

def run():
    logging.basicConfig(level=logging.INFO)
    stream_time_series_data()

if __name__ == '__main__':
    run()
