import React, { useEffect, useRef, useState } from "react";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";

import grpc from "@grpc/grpc-js";
import { loadSync } from "@grpc/proto-loader";
import { TimeSeriesService } from "./generated/timeseries"; // Adjust the import path as per your project structure

const PROTO_PATH = "./"; // Adjust the path to your proto file

const TimeSeriesChart = () => {
  const [chartOptions, setChartOptions] = useState({
    title: { text: "Time Series Data" },
    series: [{ name: "EEG_CZ_REF", data: [] }],
    xAxis: { type: "datetime" },
  });

  const clientRef = useRef(null);

  useEffect(() => {
    const client = new TimeSeriesService(
      "localhost:50051",
      grpc.credentials.createInsecure()
    );
    clientRef.current = client;

    const streamRequest = {
      start_timestamp: 0,
      end_timestamp: Date.now(),
      limit: 100,
    }; // Example request params

    const stream = client.StreamTimeSeriesData(streamRequest);
    stream.on("data", (data) => {
      updateChart(data);
    });

    stream.on("error", (err) => {
      console.error("Error in streaming:", err);
    });

    stream.on("end", () => {
      console.log("Streaming ended");
    });

    return () => {
      if (clientRef.current) {
        clientRef.current.close(); // Close client connection on unmount or cleanup
      }
    };
  }, []);

  const updateChart = (data) => {
    setChartOptions((prevOptions) => {
      const newData = [
        ...prevOptions.series[0].data,
        [data.time, data.EEG_CZ_REF],
      ]; // Adjust based on the field you want to plot
      return {
        ...prevOptions,
        series: [{ ...prevOptions.series[0], data: newData }],
      };
    });
  };

  return (
    <div>
      <HighchartsReact highcharts={Highcharts} options={chartOptions} />
    </div>
  );
};

export default TimeSeriesChart;
