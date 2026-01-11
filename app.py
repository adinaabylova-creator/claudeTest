from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'API is running'
    }), 200

@app.route('/echo', methods=['POST'])
def echo():
    """Echo endpoint that returns the received data"""
    data = request.get_json()
    return jsonify({
        'echoed': data
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
