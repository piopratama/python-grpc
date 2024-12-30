import time
import grpc
from concurrent import futures
import jwt  # For token decoding
import streaming_pb2
import streaming_pb2_grpc

SECRET_KEY = "my_secret_key"  # Secret key for JWT validation

class StreamingService(streaming_pb2_grpc.StreamingServiceServicer):
    def StreamData(self, request, context):
        # Extract and validate JWT from metadata
        metadata = dict(context.invocation_metadata())
        token = metadata.get("authorization")
        if not token:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Authorization token is missing")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Authorization token has expired")
        except jwt.InvalidTokenError:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid authorization token")

        # Retrieve user_id from the payload
        user_id = payload.get("user_id")
        if not user_id:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token payload")

        # Stream personalized messages
        for i in range(5):
            yield streaming_pb2.StreamResponse(message=f"Hello {user_id}, this is message {i + 1}")
            time.sleep(1)  # Simulate a delay between messages

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # Handle multiple clients
    streaming_pb2_grpc.add_StreamingServiceServicer_to_server(StreamingService(), server)
    server.add_insecure_port("[::]:50051")  # Listen on port 50051
    print("Secure server is running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
