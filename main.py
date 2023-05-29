import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from database import Account, User, session

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/balance':
            self.handle_balance_request()
        elif self.path == '/api/transaction':
            self.handle_transaction_request()
        # Add more elif conditions for additional endpoints

    def handle_balance_request(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        iban = data.get('acctNo')
        pin = data.get('pin')

        try:
            account = session.query(Account).filter_by(iban=iban).first()

            if account:
                user = session.query(User).filter_by(user_id=account.user_id).first()

                if user:
                    if user.verify_pin(pin):
                        balance = account.balance
                        response = {'status': 'success', 'balance': balance}
                        self.send_response(200)
                    else:
                        response = {'status': 'error', 'message': 'Invalid PIN for the account.'}
                        self.send_response(400)
                else:
                    response = {'status': 'error', 'message': 'Invalid user associated with the account.'}
                    self.send_response(400)
            else:
                response = {'status': 'error', 'message': 'Invalid account number.'}
                self.send_response(400)

        except Exception as e:
            print(f"Database Error: {str(e)}")
            response = {'status': 'error', 'message': 'An error occurred while accessing the database.'}
            self.send_response(500)

        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def handle_transaction_request(self):
        # Implement logic for the '/api/transaction' endpoint
        pass

    # Add more handler methods for additional endpoints

    def log_message(self, format, *args):
        # Get the source IP address from the client_address tuple
        client_ip = self.client_address[0]
        message = format % args
        print(f"Incoming request from {client_ip}: {message}")

def run(server_class=HTTPServer, handler_class=MyHandler, host='0.0.0.0', port=8080):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on {host}:{port}...')
    httpd.serve_forever()

run()
