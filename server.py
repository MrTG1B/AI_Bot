from flask import Flask, request, jsonify
import brain as br

app = Flask(__name__)

@app.route('/alldata', methods=['POST'])
def alldata():
    try:
        data = request.get_json()
        
        # Ensure data is a string
        if isinstance(data, dict) and "message" in data:
            data = data["message"]
        elif not isinstance(data, str):
            return jsonify({"error": "Invalid input, expected a string."}), 400
        
        response = br.get_response(data)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)