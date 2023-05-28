from flask import Flask, request, jsonify
from database import Account, User, session

app = Flask(__name__)

# Balance route
@app.route('/api/balance', methods=['POST'])
def balance():
    # Retrieve account number and PIN from the request body
    data = request.get_json()
    account_id = data.get('acctNo')
    pin = data.get('pin')

    try:
        # Fetch the account from the accounts table based on the account number
        account = session.query(Account).filter_by(account_id=account_id).first()

        if account:
            # Fetch the user from the users table based on the user ID associated with the account
            user = session.query(User).filter_by(user_id=account.user_id).first()

            if user and user.verify_pin(pin):
                balance = account.balance
                response = {'status': 'success', 'balance': balance}
            else:
                response = {'status': 'error', 'message': 'Invalid user ID or PIN.'}
        else:
            response = {'status': 'error', 'message': 'Invalid account number.'}

        return jsonify(response)

    except Exception as e:
        print(f"Database Error: {str(e)}")
        response = {'status': 'error', 'message': 'An error occurred while accessing the database.'}
        return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
