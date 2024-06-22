// Original file: timeseries.proto

import type { Long } from '@grpc/proto-loader';

export interface StreamRequest {
  'startTimestamp'?: (number | string | Long);
  'endTimestamp'?: (number | string | Long);
  'limit'?: (number);
}

export interface StreamRequest__Output {
  'startTimestamp'?: (Long);
  'endTimestamp'?: (Long);
  'limit'?: (number);
}
