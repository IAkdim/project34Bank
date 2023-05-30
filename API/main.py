from flask import Flask, request, jsonify
from database import Account, User, session

app = Flask(__name__)
@app.route('/api/balance', methods=['POST'])
def balance():
    data = request.get_json()
    iban: str = data.get('acctNo')
    pin: str = data.get('pin')

    account = session.query(Account).filter_by(iban=iban).first()
    if not account:
        return jsonify({'status': 400, 'message': 'Invalid account number.', 'success' : False, 'acctNo' : None})

    if account.status == 1:
        return jsonify({'status': 403, 'message': 'This account is blocked.', 'success' : False, 'acctNo' : None})

    user = session.query(User).filter_by(user_id=account.user_id).first()
    if not user or not user.verify_pin(pin):
        account.increment_attempts()
        return jsonify({'status': 401, 'message': 'Invalid user status or PIN.', 'success' : False, 'acctNo' : None})

    account.reset_attempts()
    balance = account.balance
    return jsonify({'status': 200, 'balance': balance, 'success' : True, 'acctNo' : iban})

@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json()
    iban: str = data.get('acctNo')
    pin: str = data.get('pin')
    amount: int = data.get('amount')

    account = session.query(Account).filter_by(iban=iban).first()
    if not account:
        return jsonify({'status': 400, 'message': 'Invalid account number.', 'success' : False, 'acctNo' : None})

    if account.status == 1:
        return jsonify({'status': 403, 'message': 'This account is blocked.', 'success' : False, 'acctNo' : None})

    user = session.query(User).filter_by(user_id=account.user_id).first()
    if not user or not user.verify_pin(pin):
        account.increment_attempts()
        return jsonify({'status': 401, 'message': 'Invalid user status or PIN.', 'success' : False, 'acctNo' : None})

    if account.balance < amount:
        account.reset_attempts()
        return jsonify({'status': 402, 'message': 'Insufficient balance.', 'success' : False, 'acctNo' : None})

    account.balance -= amount
    session.commit()
    account.reset_attempts()
    return jsonify({'status': 200, 'message': 'Withdrawal successful.', 'success' : True, 'acctNo' : iban})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)