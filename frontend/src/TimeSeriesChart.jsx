import React, { useEffect, useState } from "react";
// import { TimeSeriesServiceClient } from "./generated/timeseries_grpc_web_pb";
// import { StreamRequest } from "./generated/timeseries_pb";
import proto from "./generated/timeseries_pb";
const StreamRequest = proto.StreamRequest;

import proto2 from "./generated/timeseries_grpc_web_pb";
const TimeSeriesServiceClient = proto2.TimeSeriesServiceClient;
const TimeSeriesChart = () => {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const client = new TimeSeriesServiceClient("http://0.0.0.0:8000"); // Adjust this to your gRPC-Web proxy address
    //const request2 = new StreamRequest();
    const request = new StreamRequest();
    request.setLimit(100);

    const stream = client.streamTimeSeriesData(request, {});

    stream.on("data", (response) => {
      setLoading(false);
      setData((prevData) => {
        const newData = [
          ...prevData,
          {
            id: response.getId(),
            time: response.getTime(),
          },
        ];
        return newData.slice(-100); // Keep only the last 100 items
      });
    });

    stream.on("error", (err) => {
      console.error("Error:", err);
      setError(`Stream error: ${err.message}`);
      setLoading(false);
    });

    stream.on("end", () => {
      console.log("Stream ended");
      setLoading(false);
    });

    return () => stream.cancel();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h2>Time Series Data</h2>
      <ul>
        {data.map((item, index) => (
          <li key={index}>
            ID: {item.id}, Time: {item.time}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TimeSeriesChart;
