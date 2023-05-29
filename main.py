from flask import Flask, request, jsonify, make_response
from database import Account, User, session

app = Flask(__name__)

@app.route('/api/balance', methods=['POST'])
def balance():
    data = request.get_json()
    iban = data.get('acctNo')
    pin = data.get('pin')
    try:
        account = session.query(Account).filter_by(iban=iban).first()
        if account:
            user = session.query(User).filter_by(user_id=account.user_id).first()
            if user and user.verify_pin(pin):
                balance = account.balance
                response = {'status': 200, 'balance': balance}
            else:
                response = {'status': 400, 'message': 'Invalid user ID or PIN.'}
        else:
            response = {'status': 400, 'message': 'Invalid account number.'}
    except Exception as e:
        print(f"Database Error: {str(e)}")
        response = {'status': 400, 'message': 'An error occurred while accessing the database.'}
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)