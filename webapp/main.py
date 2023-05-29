from flask import Flask, render_template, redirect, request, session
from time import sleep
from configparser import ConfigParser
from Transaction import Transaction
from hardware import process_RFID, Money_Dispenser
from api import post_balance, post_withdraw

config = ConfigParser()
config.read('config.ini')

app = Flask(__name__)
app.secret_key = config.get('Session', 'key')
dispenser = Money_Dispenser(5, 5, 5)

@app.route("/")
def index():
    session.modified = True
    session['validated'] = False
    session['data'] = {}
    return render_template("index.html")

@app.route("/rfid")
def rfid():
    # iban: str = process_RFID("COM9")
    iban = "CHBAHE312843209"
    return redirect("/pincode?iban=" + iban)


@app.route("/pincode", methods=["GET", "POST"])
def pincode():
    iban = request.args.get("iban")
    session['data']['acctNo'] = iban    

    if request.method == "POST":
        pin = request.form.get("pinInput")
        session['data']['pin'] = pin

        response = post_balance(session['data'])
        if response.status_code == 200:
            json_data = response.json()
            if json_data.get('status') == 200:
                session['validated'] = True
                session['balance'] = json_data.get('balance')
                return redirect("/choiceMenu")
            elif json_data.get('status') == 403:
                return redirect("/blocked")
            elif json_data.get('status') == 401:
                return redirect("/wrongPin")
            
    return render_template("pincode.html", iban=iban)


@app.route("/blocked")
def blocked():
    return render_template("blocked.html")

@app.route("/wrongPin")
def wrong_pin():
    return render_template("wrongPin.html")

@app.route("/choiceMenu")
def choice_menu():
    if not session['validated']:
        return redirect("/")
    return render_template("choiceMenu.html")

@app.route("/balance")
def balance():
    balance = session['balance']
    return render_template("balance.html", balance=str(balance))

@app.route("/moneyChoice")
def money_choice():
    return render_template("moneyChoice.html")

@app.route("/customChoice", methods=["GET", "POST"])
def custom_choice():
    if request.method == "POST":
        amount = int(request.form.get("money-input"))
        return redirect(f"/wait?amount={amount}")
    return render_template("customChoice.html")

@app.route("/wait")
def wait():
    session.modified = True
    session['data']['amount'] = int(request.args.get("amount"))
    return render_template("wait.html")

@app.route("/dispense")
def dispense():
    amount: int = session['data']['amount']
    print(amount)
    billsToDispense: dict = dispenser.get_denominations(amount)
    if billsToDispense != None:
        sleep(1)
        response = post_withdraw(session['data'])
        if response.status_code == 200:
            json_data = response.json()
            if json_data.get('status') == 200:
                return redirect('/bon')
            elif json_data.get('status') == 401:
                return redirect("/wrongPin")
            elif json_data.get('status') == 402:
                return redirect("/exceededBalance")
            elif json_data.get('status') == 403:
                return redirect("/blocked")
            
        else:
            return redirect("/error")
    else:
        return redirect('/inventoryError')
    
@app.route("/exceededBalance")
def exceeded_balance():
    return render_template("exceededBalance.html")

@app.route("/bon", methods=["GET", "POST"])
def bon():
    language = request.cookies.get('language')
    transaction = Transaction(session['data']['amount'], session['data']['acctNo'], language)
    if request.method == "POST":
        if request.form.get("decision") == 'yes':
            # transaction.print_transaction_details()
            sleep(2)
        return redirect("/end")
    transaction.record_transaction_to_db()
    return render_template("bon.html")

@app.route("/end")
def end():
    session.modified = True
    session['validated'] = False
    session['data'] = {}
    return render_template("end.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)