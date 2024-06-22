// Import the generated protobuf files
import { TimeSeriesServiceClient } from "../generated/timeseries_grpc_pb";
import { StreamRequest } from "../generated/timeseries_pb";

// Create gRPC client instance
const client = new TimeSeriesServiceClient("http://localhost:8000");

// Example function to use the gRPC client
export function fetchData(limit, callback) {
  const request = new StreamRequest();
  request.setLimit(limit);

  client.getData(request, {}, (error, response) => {
    if (error) {
      console.error("Error fetching data:", error.message);
      callback(error, null);
      return;
    }

    console.log("Data received from server:", response.toObject());
    callback(null, response);
  });
}
