import time
from flask import Flask, request, jsonify
import grpc
import grpc_server_pb2_grpc
import grpc_server_pb2

app = Flask(__name__)
# pip3 install grpcio
# pip3 install grpcio-tools
# python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. grpc_server.proto

def main(label,surface, taux):
    channel = grpc.insecure_channel('localhost:5050')
    stub = grpc_server_pb2_grpc.ServertestStub(channel)

    request = grpc_server_pb2.TerrainRequest(
        label=label,
        surface=float(surface),
        taux=float(taux)
    )
    start_time = time.time()
    response = stub.TerrainCalcul(request)
    response_time = time.time() - start_time
    print(f"Response time: {response_time} s")

    return response

@app.route('/grpc', methods=['GET'])
def show_result():
    label=request.args.get('label')
    surface = request.args.get('surface')
    taux = request.args.get('taux')
    if surface and taux:
        response = main(label,surface, taux)
        return jsonify({'prix': response.prix})
    return jsonify({'message': 'surface or taux null'}), 400

if __name__ == '__main__':
    app.run(port=5000)
