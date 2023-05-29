from flask import Flask, request, jsonify, make_response
from database import Account, User, session

app = Flask(__name__)

@app.route('/api/balance', methods=['POST'])
def balance():
    data = request.get_json()
    account_id = data.get('acctNo')
    pin = data.get('pin')

    try:
        account = session.query(Account).filter_by(account_id=account_id).first()

        if account:
            user = session.query(User).filter_by(user_id=account.user_id).first()

            if user and user.verify_pin(pin):
                balance = account.balance
                response = {'status': 'success', 'balance': balance}
                # Change the response code to 201 (Created)
                return make_response(jsonify(response), 201)
            else:
                response = {'status': 'error', 'message': 'Invalid user ID or PIN.'}
                # Change the response code to 400 (Bad Request)
                return make_response(jsonify(response), 400)
        else:
            response = {'status': 'error', 'message': 'Invalid account number.'}
            # Change the response code to 400 (Bad Request)
            return make_response(jsonify(response), 400)

    except Exception as e:
        print(f"Database Error: {str(e)}")
        response = {'status': 'error', 'message': 'An error occurred while accessing the database.'}
        # Change the response code to 500 (Internal Server Error)
        return make_response(jsonify(response), 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
