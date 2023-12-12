from flask import Flask, request, jsonify
from database_connection import verify_user

app = Flask(__name__)

@app.route('/verify', methods=['GET'])
def verify():
    token = request.args.get('token')
    if token:
        if verify_user(token):
            # Update your response as needed
            return jsonify({"status": "success", "message": "Account verified successfully."}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid or expired token."}), 400
    return jsonify({"status": "error", "message": "No token provided."}), 400

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production
