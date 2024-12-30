import time
import grpc
import jwt  # For token generation
import streaming_pb2
import streaming_pb2_grpc

SECRET_KEY = "my_secret_key"  # Secret key for JWT generation

def generate_token(user_id):
    """Generate a JWT token for a given user ID."""
    payload = {
        "user_id": user_id,
        "exp": time.time() + 60  # Token expires in 60 seconds
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def stream_data(user_id):
    token = generate_token(user_id)  # Generate JWT token

    with grpc.insecure_channel("localhost:50051") as channel:  # Connect to secure server
        stub = streaming_pb2_grpc.StreamingServiceStub(channel)
        metadata = [("authorization", token)]  # Include token in metadata

        try:
            print(f"Streaming data for {user_id}:")
            for response in stub.StreamData(streaming_pb2.StreamRequest(user_id=user_id), metadata=metadata):
                print(response.message)
        except grpc.RpcError as e:
            print(f"Error: {e.details()} (Code: {e.code()})")

if __name__ == "__main__":
    # Simulate multiple users
    user_ids = ["Alice", "Bob"]
    for user_id in user_ids:
        stream_data(user_id)
        print("-" * 40)
