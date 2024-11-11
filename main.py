import json
import threading
from nicegui import ui

data = {}
items_to_redeem = {}

def save_data():
    global data
    with open("./data/save.json", "w") as save_file:
        save_file.write(json.dumps(data))

def read_data():
    with open("./data/save.json", "r") as save_file:
        return json.loads(save_file.read())

def read_items():
    with open("./data/items.json", "r") as save_file:
        return json.loads(save_file.read())

def complete_task(task, label):
    global data
    data["challenges"][task]["times"] += 1  # Use the task name directly here
    label.set_text("Times completed: " + str(data["challenges"][task]["times"]))
    data["coins"] += data["challenges"][task]["reward"]
    save_data()

def purchase_product(price):
    global data
    data["coins"] -= price
    save_data()

def new_task(new_task_name, new_task_reward):
    global data
    data["challenges"][new_task_name] = {"times": 0, "reward": int(new_task_reward)}
    ui.notify("New task created, restart service to refresh the UI.")
    save_data()

def update():
    global data, coin_label
    while True:
        coin_label.set_text("Coins: " + str(data["coins"]))

data = read_data()
items_to_redeem = read_items()

coin_label = ui.label("Coins: " + str(data["coins"]))

ui.label("Tasks").classes('text-h4')

with ui.row():
    for challenge_name in data["challenges"]:
        with ui.card():
            ui.label("Name: " + str(challenge_name))
            ui.label("Reward: " + str(data["challenges"][challenge_name]["reward"]))
            times_completed = ui.label("Times completed: " + str(data["challenges"][challenge_name]["times"]))
            # Fix the lambda here by passing `challenge_name` as an argument
            ui.button("Completed!", on_click=lambda challenge_name=challenge_name, label=times_completed: complete_task(challenge_name, label))

ui.label("Redeem").classes('text-h4')

with ui.row():
    for item in items_to_redeem:
        with ui.card():
            ui.label("Name: " + str(item))
            ui.label("Price: " + str(items_to_redeem[item]))
            ui.button("Purchase", on_click=lambda price=items_to_redeem[item]: purchase_product(price))

ui.label("New Task").classes('text-h4')

with ui.row():
    new_task_name = ui.input(label="Task name.")
    new_task_reward = ui.number(label="Task reward.")
    ui.button("Create task.", on_click=lambda: new_task(new_task_name.value, new_task_reward.value))

# Start the update thread to update the coin count periodically
threading.Thread(target=update, daemon=True).start()

ui.run(reload=False)
