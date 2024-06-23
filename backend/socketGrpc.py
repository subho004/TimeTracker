import asyncio
import json
import websockets
from grpc import insecure_channel
from timeseries_pb2 import StreamRequest
from timeseries_pb2_grpc import TimeSeriesServiceStub
import time

class GrpcStreamManager:
    def __init__(self):
        self.channel = insecure_channel('localhost:50051')
        self.stub = TimeSeriesServiceStub(self.channel)
        self.websocket = None
        self.streaming_task = None
        self.start_timestamp = 0.0  # Set your desired start timestamp
        self.end_timestamp = int(time.time())# Set your desired end timestamp (current time in seconds since epoch)
        self.limit = 677500  # Set your desired limit

    async def start_stream(self, websocket):
        self.websocket = websocket
        try:
            request = StreamRequest(
                start_timestamp=self.start_timestamp,
                end_timestamp=self.end_timestamp,
                limit=self.limit
            )
            async for response in self.stub.StreamTimeSeriesData(request):
                data = {
                    'id': response.id,
                    'time': response.time,
                    'EEG_CZ_REF': response.EEG_CZ_REF,
                    # Include other fields as needed
                }
                await self.websocket.send(json.dumps(data))
        except websockets.exceptions.ConnectionClosedError:
            print("WebSocket connection closed unexpectedly.")
        except Exception as e:
            print(f"Exception in gRPC streaming: {e}")
        finally:
            await self.websocket.close()
            print("WebSocket connection closed.")

    async def stop_stream(self):
        if self.streaming_task:
            self.streaming_task.cancel()
            try:
                await self.streaming_task
            except asyncio.CancelledError:
                pass
            self.streaming_task = None
            print("Stopped gRPC streaming.")

async def websocket_server(websocket, path):
    global grpc_manager
    if path == "/stream":
        await grpc_manager.start_stream(websocket)
    else:
        await websocket.close()

async def start_websocket_server():
    global grpc_manager
    async with websockets.serve(websocket_server, 'localhost', 8766):
        print("WebSocket server started on ws://localhost:8766")
        await asyncio.Future()  # Run forever

if __name__ == '__main__':
    grpc_manager = GrpcStreamManager()
    asyncio.run(start_websocket_server())
