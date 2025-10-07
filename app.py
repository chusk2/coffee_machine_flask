from flask import Flask, render_template, request, redirect, url_for
from coffee_machine_logic import CoffeeMachine, Espresso, Latte, Cappuccino

app = Flask(__name__)

# --- Create a single, persistent CoffeeMachine instance ---
# This object will live as long as the Flask app is running.
# We instantiate it using the dictionary format from coffee_machine2.py
machine = CoffeeMachine(
    menu={
        'Espresso': Espresso(),
        'Latte': Latte(),
        'Cappuccino': Cappuccino()
    },
    max_resources={
        "water": 1000,
        "beans": 500,
        "milk": 750
    }
)

# --- Message store ---
# A simple list to hold messages to display to the user.
messages = []

@app.route('/')
def index():
    """
    Main page. Displays the menu, machine status, and any messages.
    """
    # We need to pass a list of drink objects to the template, not a dict.
    menu_list = list(machine.menu.values())
    
    # Pop all messages to display them, then clear the list.
    current_messages = messages.copy()
    messages.clear()

    # The template expects `machine.money_credit`, so we pass `machine.user_credit`.
    return render_template('index.html',
                           machine=machine,
                           menu_list=menu_list,
                           user_credit=machine.user_credit,
                           messages=current_messages
                           )

@app.route('/insert-money', methods=['POST'])
def insert_money():
    """Handles the form submission for inserting money."""
    try:
        amount = float(request.form['amount'])
        if amount > 0:
            machine.insert_money(amount)
            messages.append(f"Successfully inserted €{amount:.2f}.")
        else:
            messages.append("Please insert a valid amount.")
    except (ValueError, TypeError):
        messages.append("Invalid amount. Please enter a number.")
    
    return redirect(url_for('index'))

## ADD COINS TO CURRENT TRANSACTION
@app.route('/add-coin', methods=['POST'])
def add_coin():
    """Handles a single coin click from the UI."""
    try:
        coin_value = float(request.form.get('coin_value', 0))
        if coin_value > 0:
            machine.insert_money(coin_value)
            # Optional: add a message for each coin insertion
    except (ValueError, TypeError):
        messages.append("Invalid coin value.")
    return redirect(url_for('index'))

@app.route('/select-drink', methods=['POST'])
def select_drink():
    """Handles the form submission for selecting a drink."""
    selected_coffee = request.form['drink']
    # The new `make_drink` method returns a user-friendly message!
    result_message = machine.order_coffee(selected_coffee)
    messages.append(result_message)
    
    return redirect(url_for('index'))

@app.route('/cancel-entry', methods=['POST'])
def cancel_entry():
    """Returns any credit the user has in the machine."""
    entered_money = machine.user_credit
    if entered_money > 0:
        messages.append(f"Returned ${entered_money:.2f}.")
        machine.user_credit = 0.0
    else:
        messages.append("No money in credit to return.")
        
    return redirect(url_for('index'))

@app.route('/refill', methods=['POST'])
def refill():
    """A maintenance action to refill the machine's resources."""
    machine.refill_resources()
    messages.append("Machine resources have been refilled.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)