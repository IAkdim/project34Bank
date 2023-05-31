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
    iban: str = process_RFID("COM9") #insert correct port here
    if iban == "No match found":
        return redirect("/error")
    return redirect("/pincode?iban=" + iban)

# 'status' not available to external costumers, /error is used as a catch-all redirection message for them 
@app.route("/pincode", methods=["GET", "POST"])
def pincode():
    iban = request.args.get("iban")
    session['data']['acctNo'] = iban    
    response = post_balance(session['data'])
    json_data = response.json()
    if request.method == "POST":
        pin = request.form.get("pinInput")
        session['data']['pin'] = pin
        if response.status_code == 200:
            if json_data.get('status') == 200 or json_data.get('acctNo') != None :
                session['validated'] = True
                session['balance'] = json_data.get('balance')
                return redirect("/choiceMenu")
            elif json_data.get('status') == 403:
                return redirect("/blocked")
            elif json_data.get('status') == 401:
                return redirect("/wrongPin")           
        return redirect("/error")
    return render_template("pincode.html", iban=iban)

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/blocked")
def blocked():
    return render_template("blocked.html")

@app.route("/wrongPin")
def wrong_pin():
    return render_template("wrongPin.html")

@app.route("/choiceMenu")
def choice_menu():
    if session['validated'] == False:
        return redirect("/")
    return render_template("choiceMenu.html")

@app.route("/balance")
def balance():
    if session['validated'] == False:
        return redirect("/")
    balance = session['balance']
    return render_template("balance.html", balance=str(balance))

@app.route("/moneyChoice")
def money_choice():
    if session['validated'] == False:
        return redirect("/")
    return render_template("moneyChoice.html")

@app.route("/customChoice", methods=["GET", "POST"])
def custom_choice():
    if session['validated'] == False:
        return redirect("/")
    if request.method == "POST":
        amount = int(request.form.get("money-input"))
        return redirect(f"/wait?amount={amount}")
    return render_template("customChoice.html")

@app.route("/wait")
def wait():
    if session['validated'] == False:
        return redirect("/")
    session.modified = True
    session['data']['amount'] = int(request.args.get("amount"))
    return render_template("wait.html")

@app.route("/dispense")
def dispense():
    if session['validated'] == False:
        return redirect("/")
    amount: int = session['data']['amount']
    billsToDispense: dict = dispenser.get_denominations(amount)
    if billsToDispense != None:
        sleep(1)
        response = post_withdraw(session['data'])
        json_data = response.json()
        if response.status_code == 200 or json_data.get('acctNo') != "" :
            print("here")
            if json_data.get('status') == 200 or json_data.get('success') == True:
                return redirect('/bon')
            elif json_data.get('status') == 401:
                return redirect("/wrongPin")
            elif json_data.get('status') == 402:
                return redirect("/exceededBalance")
            elif json_data.get('status') == 403:
                return redirect("/blocked")
        return redirect("/error")
    else:
        return redirect('/inventoryError')
    
@app.route("/inventoryError")
def inventory_error():
    return render_template("inventoryError.html")
    
@app.route("/exceededBalance")
def exceeded_balance():
    return render_template("exceededBalance.html")

@app.route("/bon", methods=["GET", "POST"])
def bon():
    if session['validated'] == False:
        return redirect("/")
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
    app.run(host="127.0.0.1", port=5000)