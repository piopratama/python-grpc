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
    stream_data("User1")
