import { protobuf } from "protobufjs";
async function compileProto() {
  try {
    const root = await protobuf.load("timeseries.proto");
    const TimeSeriesService = root.lookupType("timeseries.TimeSeriesService");
    const StreamRequest = root.lookupType("timeseries.StreamRequest");
    const TimeSeriesData = root.lookupType("timeseries.TimeSeriesData");

    // Export the types you need
    module.exports = {
      TimeSeriesService,
      StreamRequest,
      TimeSeriesData,
    };
  } catch (err) {
    console.error("Error compiling protobuf:", err);
  }
}

compileProto();
