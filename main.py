from flask import Flask, request, jsonify, make_response
from database import Account, User, session

app = Flask(__name__)
@app.route('/api/balance', methods=['POST'])
def balance():
    data = request.get_json()
    iban = data.get('acctNo')
    pin = data.get('pin')

    account = session.query(Account).filter_by(iban=iban).first()
    if not account:
        return jsonify({'status': 400, 'message': 'Invalid account number.'}), 400

    if account.status == 1:
        return jsonify({'status': 403, 'message': 'This account is blocked.'}), 403

    user = session.query(User).filter_by(user_id=account.user_id).first()
    if not user or not user.verify_pin(pin):
        account.increment_attempts()
        return jsonify({'status': 400, 'message': 'Invalid user ID or PIN.'}), 400

    account.reset_attempts()
    balance = account.balance
    return jsonify({'status': 200, 'balance': balance}), 200

@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json()
    iban = data.get('acctNo')
    pin = data.get('pin')
    amount = data.get('amount')

    account = session.query(Account).filter_by(iban=iban).first()
    if not account:
        return jsonify({'status': 400, 'message': 'Invalid account number.'}), 400

    if account.status == 1:
        return jsonify({'status': 403, 'message': 'This account is blocked.'}), 403

    user = session.query(User).filter_by(user_id=account.user_id).first()
    if not user or not user.verify_pin(pin):
        account.increment_attempts()
        return jsonify({'status': 400, 'message': 'Invalid user ID or PIN.'}), 400

    if account.balance < amount:
        account.reset_attempts()
        return jsonify({'status': 400, 'message': 'Insufficient balance.'}), 400

    account.balance -= amount
    session.commit()
    account.reset_attempts()
    return jsonify({'status': 200, 'message': 'Withdrawal successful.'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)