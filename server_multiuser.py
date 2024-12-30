import time
from concurrent import futures
import grpc
import streaming_pb2
import streaming_pb2_grpc

class StreamingService(streaming_pb2_grpc.StreamingServiceServicer):
    def StreamData(self, request, context):
        user_id = request.user_id  # Extract user_id from the client
        for i in range(5):
            yield streaming_pb2.StreamResponse(message=f"Hello {user_id}, this is message {i + 1}")
            time.sleep(1)  # Simulate delay between messages

def serve():
    # Create a gRPC server with a thread pool to handle multiple clients
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streaming_pb2_grpc.add_StreamingServiceServicer_to_server(StreamingService(), server)
    server.add_insecure_port("[::]:50051")  # Listen on port 50051
    print("Server is running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
