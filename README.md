# gRPC Secure Multi-User Streaming Project

This project demonstrates how to implement a secure multi-user gRPC streaming service in Python. It showcases basic gRPC concepts and step-by-step instructions to create a secure server and client using JWT for authentication.

---

## **Basic Concepts of gRPC**

### What is gRPC?
- gRPC (Google Remote Procedure Call) is a high-performance, open-source RPC framework.
- It uses HTTP/2 for transport, Protocol Buffers (Protobuf) as the interface definition language, and provides features such as bi-directional streaming, multiplexing, and flow control.

### Key Features
1. **Efficient Serialization**:
   - Protocol Buffers ensure compact and fast data serialization.
2. **Streaming Support**:
   - gRPC supports unary, server-streaming, client-streaming, and bi-directional streaming RPCs.
3. **Language-Neutral**:
   - The `.proto` file can be used to generate client and server code in multiple languages.
4. **Authentication**:
   - Secure communication with tokens (e.g., JWT) and SSL/TLS.

### RPC Types Used in This Project
- **Server Streaming RPC**: The client sends a request, and the server streams multiple responses over time.

---

## **Project Overview**

This project includes the following components:
1. A **`.proto` file** that defines the service and message structures.
2. A **secure gRPC server** that validates JWT tokens and streams personalized responses.
3. A **secure gRPC client** that sends authenticated requests to the server.

### Project Structure
```plaintext
grpc-secure-streaming/
├── streaming.proto             # Protobuf definition file
├── streaming_pb2.py            # Generated Python file for message types
├── streaming_pb2_grpc.py       # Generated Python file for service stubs
├── server_multiuser_secure.py  # Secure gRPC server implementation
├── client_multiuser_secure.py  # Secure gRPC client implementation
├── requirements.txt            # Dependency file
├── README.md                   # Documentation (this file)
```

---

## **Step-by-Step Instructions**

### Step 1: Define the `.proto` File
Create a file named `streaming.proto` with the following content:
```proto
syntax = "proto3";

package streaming;

service StreamingService {
  rpc StreamData (StreamRequest) returns (stream StreamResponse);
}

message StreamRequest {
  string user_id = 1;
}

message StreamResponse {
  string message = 1;
}
```

- **Service**: `StreamingService` defines the `StreamData` RPC.
- **Messages**:
  - `StreamRequest`: Contains the `user_id` sent by the client.
  - `StreamResponse`: Contains the personalized message sent by the server.

### Step 2: Generate Python Code
Run the following command to generate Python files from the `.proto` file:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. streaming.proto
```
This will generate:
1. `streaming_pb2.py`: Definitions for Protobuf message types.
2. `streaming_pb2_grpc.py`: Stubs for the gRPC service.

### Step 3: Implement the Server
Create a file named `server_multiuser_secure.py`:
```python
import time
import grpc
from concurrent import futures
import jwt
import streaming_pb2
import streaming_pb2_grpc

SECRET_KEY = "my_secret_key"

class StreamingService(streaming_pb2_grpc.StreamingServiceServicer):
    def StreamData(self, request, context):
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

        user_id = payload.get("user_id")
        if not user_id:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token payload")

        for i in range(5):
            yield streaming_pb2.StreamResponse(message=f"Hello {user_id}, this is message {i + 1}")
            time.sleep(1)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streaming_pb2_grpc.add_StreamingServiceServicer_to_server(StreamingService(), server)
    server.add_insecure_port("[::]:50051")
    print("Secure server is running...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
```

### Step 4: Implement the Client
Create a file named `client_multiuser_secure.py`:
```python
import time
import grpc
import jwt
import streaming_pb2
import streaming_pb2_grpc

SECRET_KEY = "my_secret_key"

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": time.time() + 60
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def stream_data(user_id):
    token = generate_token(user_id)

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = streaming_pb2_grpc.StreamingServiceStub(channel)
        metadata = [("authorization", token)]

        try:
            print(f"Streaming data for {user_id}:")
            for response in stub.StreamData(streaming_pb2.StreamRequest(user_id=user_id), metadata=metadata):
                print(response.message)
        except grpc.RpcError as e:
            print(f"Error: {e.details()} (Code: {e.code()})")

if __name__ == "__main__":
    user_ids = ["Alice", "Bob"]
    for user_id in user_ids:
        stream_data(user_id)
        print("-" * 40)
```

### Step 5: Install Dependencies
Create a file named `requirements.txt`:
```plaintext
grpcio==1.57.0
grpcio-tools==1.57.0
PyJWT==2.7.0
```
Install the dependencies:
```bash
pip install -r requirements.txt
```

### Step 6: Run the Project
1. **Start the Server**:
   ```bash
   python server_multiuser_secure.py
   ```

2. **Run the Client**:
   ```bash
   python client_multiuser_secure.py
   ```

---

## **Expected Output**

### Server Output
```plaintext
Secure server is running...
```

### Client Output
```plaintext
Streaming data for Alice:
Hello Alice, this is message 1
Hello Alice, this is message 2
Hello Alice, this is message 3
Hello Alice, this is message 4
Hello Alice, this is message 5
----------------------------------------
Streaming data for Bob:
Hello Bob, this is message 1
Hello Bob, this is message 2
Hello Bob, this is message 3
Hello Bob, this is message 4
Hello Bob, this is message 5
```

---
