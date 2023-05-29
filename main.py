# from flask import Flask, request, jsonify
# from database import Account, User, session

# app = Flask(__name__)

# # Balance route
# @app.route('/api/balance', methods=['POST'])
# def balance():
#     # Retrieve account number and PIN from the request body
#     data = request.get_json()
#     account_id = data.get('acctNo')
#     pin = data.get('pin')

#     try:
#         # Fetch the account from the accounts table based on the account number
#         account = session.query(Account).filter_by(account_id=account_id).first()

#         if account:
#             # Fetch the user from the users table based on the user ID associated with the account
#             user = session.query(User).filter_by(user_id=account.user_id).first()

#             if user and user.verify_pin(pin):
#                 balance = account.balance
#                 response = {'status': 'success', 'balance': balance}
#             else:
#                 response = {'status': 'error', 'message': 'Invalid user ID or PIN.'}
#         else:
#             response = {'status': 'error', 'message': 'Invalid account number.'}

#         return jsonify(response)

#     except Exception as e:
#         print(f"Database Error: {str(e)}")
#         response = {'status': 'error', 'message': 'An error occurred while accessing the database.'}
#         return jsonify(response)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from database import Account, User, session

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/balance':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data: dict = json.loads(body)

            iban: str = data.get('acctNo')
            pin: str = data.get('pin')

            try:
                account = session.query(Account).filter_by(iban=iban).first()

                if account:
                    user = session.query(User).filter_by(user_id=account.user_id).first()

                    if user and user.verify_pin(pin):
                        balance = account.balance
                        response = {'status': 'success', 'balance': balance}
                    else:
                        response = {'status': 'error', 'message': 'Invalid user ID or PIN.'}
                else:
                    response = {'status': 'error', 'message': 'Invalid account number.'}

            except Exception as e:
                print(f"Database Error: {str(e)}")
                response = {'status': 'error', 'message': 'An error occurred while accessing the database.'}

            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Disable logging of incoming requests
        pass

def run(server_class=HTTPServer, handler_class=MyHandler, host='0.0.0.0', port=8080):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on {host}:{port}...')
    httpd.serve_forever()

run()
