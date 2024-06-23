import grpc
import logging
import time
import json
from timeseries_pb2 import StreamRequest
from timeseries_pb2_grpc import TimeSeriesServiceStub

# gRPC server address
SERVER_ADDRESS = 'localhost:50051'

def stream_time_series_data():
    # Establish a connection to the gRPC server
    channel = None
    while channel is None:
        try:
            channel = grpc.insecure_channel(SERVER_ADDRESS)
            logging.info("Connected to server")
        except Exception as e:
            logging.error(f"Failed to connect to server: {e}")
            time.sleep(1)  # Retry after 1 second

    stub = TimeSeriesServiceStub(channel)

    # Create a stream for receiving TimeSeriesData messages
    response = stub.StreamTimeSeriesData(StreamRequest(start_timestamp=0, end_timestamp=int(time.time()), limit=677500))

    # Prepare a list to store received data
    received_data = []

    # Iterate over the stream and log each received data item
    for data_item in response:
        # Example assuming data_item has fields id, time, and various EEG_*_REF fields
        data_dict = {
            'id': data_item.id,
            'time': data_item.time,
            'EEG_CZ_REF': data_item.EEG_CZ_REF,
            'EEG_P4_REF': data_item.EEG_P4_REF,
            'EEG_ROC_REF': data_item.EEG_ROC_REF,
            'EEG_T2_REF': data_item.EEG_T2_REF,
            'EEG_T3_REF': data_item.EEG_T3_REF,
            'EEG_O1_REF': data_item.EEG_O1_REF,
            'EEG_P3_REF': data_item.EEG_P3_REF,
            'EEG_FZ_REF': data_item.EEG_FZ_REF,
            'EEG_F8_REF': data_item.EEG_F8_REF,
            'EEG_A1_REF': data_item.EEG_A1_REF,
            'EEG_F4_REF': data_item.EEG_F4_REF,
            'EEG_EKG1_REF': data_item.EEG_EKG1_REF,
            'EEG_LOC_REF': data_item.EEG_LOC_REF,
            'EEG_T1_REF': data_item.EEG_T1_REF,
            'EEG_T4_REF': data_item.EEG_T4_REF,
            'EEG_C4_REF': data_item.EEG_C4_REF,
            'EEG_T5_REF': data_item.EEG_T5_REF,
            'EEG_A2_REF': data_item.EEG_A2_REF,
            'EEG_FP2_REF': data_item.EEG_FP2_REF,
            'EEG_FP1_REF': data_item.EEG_FP1_REF,
            'EEG_F3_REF': data_item.EEG_F3_REF,
            'EEG_T6_REF': data_item.EEG_T6_REF,
            'EEG_PZ_REF': data_item.EEG_PZ_REF,
            'EEG_F7_REF': data_item.EEG_F7_REF,
            'EEG_O2_REF': data_item.EEG_O2_REF
        }
        
        received_data.append(data_dict)

        # Serialize data to JSON and write to file after each item (or adjust as needed)
        with open('streamed_data.json', 'w') as f:
            json.dump(received_data, f, indent=2)  # Pretty print with indentation

        logging.info(f"Received data: {data_dict}")

def run():
    logging.basicConfig(level=logging.INFO)
    stream_time_series_data()

if __name__ == '__main__':
    run()
