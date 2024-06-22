import type * as grpc from '@grpc/grpc-js';
import type { MessageTypeDefinition } from '@grpc/proto-loader';

import type { TimeSeriesServiceClient as _timeseries_TimeSeriesServiceClient, TimeSeriesServiceDefinition as _timeseries_TimeSeriesServiceDefinition } from './timeseries/TimeSeriesService';

type SubtypeConstructor<Constructor extends new (...args: any) => any, Subtype> = {
  new(...args: ConstructorParameters<Constructor>): Subtype;
};

export interface ProtoGrpcType {
  timeseries: {
    StreamRequest: MessageTypeDefinition
    TimeSeriesData: MessageTypeDefinition
    TimeSeriesService: SubtypeConstructor<typeof grpc.Client, _timeseries_TimeSeriesServiceClient> & { service: _timeseries_TimeSeriesServiceDefinition }
  }
}

