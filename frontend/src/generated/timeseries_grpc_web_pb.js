// Import necessary modules
import { MethodDescriptor } from "grpc-web";
import {
  StreamRequest,
  TimeSeriesData,
  TimeSeriesService,
} from "./timeseries_pb"; // Adjust path

// Define constants
const SERVICE = {
  STREAM_TIME_SERIES_DATA: {
    methodName: "StreamTimeSeriesData",
    service: TimeSeriesService,
    requestStream: false,
    responseStream: true,
    requestType: StreamRequest,
    responseType: TimeSeriesData,
  },
};

// Define client class
export class TimeSeriesServiceClient {
  constructor(hostname, credentials, options) {
    this.hostname = hostname;
    this.credentials = credentials;
    this.options = options;
  }

  // Method to stream time series data
  streamTimeSeriesData(request, metadata, callback) {
    const methodInfo = SERVICE.STREAM_TIME_SERIES_DATA;
    const methodDescriptor = new MethodDescriptor(
      `/${methodInfo.service.serviceName}/${methodInfo.methodName}`,
      methodInfo.methodType,
      methodInfo.requestType,
      methodInfo.responseType,
      methodInfo.requestStream,
      methodInfo.responseStream
    );

    return grpc.invokeStreaming(
      this.hostname + methodDescriptor.path,
      {
        request: request,
        host: this.hostname,
        metadata: metadata || {},
        transport: this.options.transport,
      },
      this.credentials,
      methodDescriptor,
      callback
    );
  }
}
