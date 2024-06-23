// App.jsx

import React, { useEffect, useRef, useState } from "react";
import Highcharts from "highcharts";
import streamedData from "./streamed_data.json"; // Import JSON data

const App = () => {
  const chartRef = useRef(null);
  const [chartOptions, setChartOptions] = useState(null);

  useEffect(() => {
    if (chartRef && chartRef.current) {
      const xAxisData = streamedData.map((item) => item.time);

      const series = Object.keys(streamedData[0])
        .filter((key) => key !== "id" && key !== "time")
        .map((key, index) => ({
          name: key,
          data: streamedData.map((item) => item[key]),
          yAxis: index,
        }));

      const yAxisOptions = Object.keys(streamedData[0])
        .filter((key) => key !== "id" && key !== "time")
        .map((key, index) => ({
          title: {
            text: key,
          },
          top: index * 150,
          height: 100,
          offset: 0,
        }));

      const options = {
        chart: {
          type: "line",
          height: 1500,
          renderTo: chartRef.current,
        },
        title: {
          text: "",
        },
        xAxis: {
          categories: xAxisData,
          title: {
            text: "Time",
          },
          offset: 100,
        },
        yAxis: yAxisOptions,
        series: series,
      };

      setChartOptions(options);
    }
  }, []);

  useEffect(() => {
    if (chartOptions && chartRef.current) {
      new Highcharts.Chart(chartOptions);
    }
  }, [chartOptions]);

  return (
    <div className="App">
      <h1>Highcharts Example in React</h1>
      <div ref={chartRef} />
    </div>
  );
};

export default App;
