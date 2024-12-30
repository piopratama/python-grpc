import grpc
import streaming_pb2
import streaming_pb2_grpc

def stream_data(user_id):
    with grpc.insecure_channel("localhost:50051") as channel:  # Connect to server
        stub = streaming_pb2_grpc.StreamingServiceStub(channel)  # Create a client stub
        request = streaming_pb2.StreamRequest(user_id=user_id)  # Build the request

        print(f"Streaming data for {user_id}:")
        for response in stub.StreamData(request):  # Iterate over the stream
            print(response.message)

if __name__ == "__main__":
    # Simulate multiple users connecting to the server
    user_ids = ["Alice", "Bob", "Charlie"]
    for user_id in user_ids:
        stream_data(user_id)
        print("-" * 40)  # Separator for different user outputs
