// ChartComponent.jsx

import React, { useEffect, useRef } from "react";
import Highcharts from "highcharts";

const ChartComponent = ({ data }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (chartRef.current && data.length > 0) {
      const seriesData = Object.keys(data[0]) // Assume time is a key, check for the correct key
        .filter((key) => key !== "time") // Exclude 'time' key from series creation
        .map((key) => ({
          name: key,
          data: data.map((item) => [item.time, item[key]]),
        }));

      const options = {
        title: {
          text: "EEG Data Over Time",
        },
        xAxis: {
          title: {
            text: "Time",
          },
        },
        yAxis: {
          title: {
            text: "Value",
          },
        },
        series: seriesData,
      };

      new Highcharts.Chart(chartRef.current, options);
    }
  }, [data]);

  return <div ref={chartRef} />;
};

export default ChartComponent;
