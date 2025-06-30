from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/mutate', methods=['POST'])
def mutate():
    request_json = request.get_json()

    # Check if the incoming request is for a Pod creation
    if request_json['request']['kind']['kind'] == 'Pod':
        labels = request_json['request']['object']['metadata'].get('labels', {})

        # Check if the Pod is a KubeDB provisioner pod
        if labels.get('app.kubernetes.io/name') == 'kubedb-provisioner':
            # Add the required label
            patch = [{
                "op": "add",
                "path": "/metadata/labels/azure.workload.identity~1use",
                "value": "true"
            }]
            response_json = {
                "response": {
                    "uid": request_json['request']['uid'],
                    "allowed": True,
                    "patchType": "JSONPatch",
                    "patch": patch
                }
            }
            return jsonify(response_json)
    
    # If the pod does not match, allow it without modification
    response_json = {
        "response": {
            "uid": request_json['request']['uid'],
            "allowed": True
        }
    }
    return jsonify(response_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('/certs/webhook-server.crt', '/certs/webhook-server.key'))
