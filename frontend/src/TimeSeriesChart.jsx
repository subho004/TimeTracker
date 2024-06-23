import React, { useEffect } from "react";
import { TimeSeriesServiceClient } from "./generated/timeseries_grpc_web_pb"; // Adjust path
import { StreamRequest } from "./generated/timeseries_pb";
function MyComponent() {
  useEffect(() => {
    // Example usage
    const client = new TimeSeriesServiceClient("http://localhost:8080", null, {
      transport: "xhr-streaming",
    });

    const request = new StreamRequest();
    request.setStartTimestamp(Date.now());
    request.setEndTimestamp(Date.now() + 3600 * 1000);
    request.setLimit(100);

    const metadata = { "custom-header-1": "value1" };

    const call = client.streamTimeSeriesData(
      request,
      metadata,
      (error, response) => {
        if (error) {
          console.error("Error:", error);
        } else {
          console.log("Received response:", response.toObject());
        }
      }
    );

    call.on("status", (status) => {
      console.log("Call status:", status);
    });

    return () => {
      call.cancel();
    };
  }, []);

  return (
    <div>
      <h1>React Component Using gRPC-Web</h1>
      {/* Your component JSX */}
    </div>
  );
}

export default MyComponent;
