// Original file: timeseries.proto

import type * as grpc from '@grpc/grpc-js'
import type { MethodDefinition } from '@grpc/proto-loader'
import type { StreamRequest as _timeseries_StreamRequest, StreamRequest__Output as _timeseries_StreamRequest__Output } from '../timeseries/StreamRequest';
import type { TimeSeriesData as _timeseries_TimeSeriesData, TimeSeriesData__Output as _timeseries_TimeSeriesData__Output } from '../timeseries/TimeSeriesData';

export interface TimeSeriesServiceClient extends grpc.Client {
  StreamTimeSeriesData(argument: _timeseries_StreamRequest, metadata: grpc.Metadata, options?: grpc.CallOptions): grpc.ClientReadableStream<_timeseries_TimeSeriesData__Output>;
  StreamTimeSeriesData(argument: _timeseries_StreamRequest, options?: grpc.CallOptions): grpc.ClientReadableStream<_timeseries_TimeSeriesData__Output>;
  streamTimeSeriesData(argument: _timeseries_StreamRequest, metadata: grpc.Metadata, options?: grpc.CallOptions): grpc.ClientReadableStream<_timeseries_TimeSeriesData__Output>;
  streamTimeSeriesData(argument: _timeseries_StreamRequest, options?: grpc.CallOptions): grpc.ClientReadableStream<_timeseries_TimeSeriesData__Output>;
  
}

export interface TimeSeriesServiceHandlers extends grpc.UntypedServiceImplementation {
  StreamTimeSeriesData: grpc.handleServerStreamingCall<_timeseries_StreamRequest__Output, _timeseries_TimeSeriesData>;
  
}

export interface TimeSeriesServiceDefinition extends grpc.ServiceDefinition {
  StreamTimeSeriesData: MethodDefinition<_timeseries_StreamRequest, _timeseries_TimeSeriesData, _timeseries_StreamRequest__Output, _timeseries_TimeSeriesData__Output>
}
