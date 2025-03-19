import json
import logging
import sys
from collections import defaultdict, Counter

YELLOW = "\033[33m"
RESET = "\033[0m"

class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_msg = super().format(record)
        if record.levelno == logging.INFO:
            return f"{YELLOW}{log_msg}{RESET}"
        return log_msg

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(CustomFormatter("%(levelname)s: %(message)s"))

logging.basicConfig(level=logging.INFO, handlers=[handler])

json_file_path = "shopping_data.json"
relations_file_path = "relations.json"

shopping_data = {
    "users": [
        {"id": 1, "purchases": ["laptop", "headphones", "smartphone"]},
        {"id": 2, "purchases": ["sneakers", "t-shirt", "jacket"]},
        {"id": 3, "purchases": ["detective book", "science book", "fantasy book"]},
        {"id": 4, "purchases": ["dumbbells", "treadmill", "bicycle"]},
        {"id": 5, "purchases": ["car oil", "car tires", "car accessories"]}
    ]
}

try:
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError:
    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(shopping_data, file, indent=4, ensure_ascii=False)
    data = shopping_data

def load_shopping_data():
    with open(json_file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def build_product_relations(data):
    relations = defaultdict(list)
    for user in data["users"]:
        for item in user["purchases"]:
            relations[item].extend(user["purchases"])

    for item in relations:
        relations[item] = list(set(relations[item]) - {item})

    with open(relations_file_path, "w", encoding="utf-8") as file:
        json.dump(relations, file, indent=4, ensure_ascii=False)

    return relations

try:
    with open(relations_file_path, "r", encoding="utf-8") as file:
        product_relations = json.load(file)
except FileNotFoundError:
    product_relations = build_product_relations(data)

def recommend_purchases(purchase_history, product_relations):
    logging.info(f"Generating recommendations for: {purchase_history}")
    recommended = Counter()

    for item in purchase_history:
        if item in product_relations:
            recommended.update(product_relations[item])

    for item in purchase_history:
        recommended.pop(item, None)

    return [item for item, _ in recommended.most_common(3)]

def update_shopping_data(user_id, new_purchases):
    data = load_shopping_data()

    for user in data["users"]:
        if user["id"] == user_id:
            user["purchases"].extend(new_purchases)
            user["purchases"] = list(set(user["purchases"]))
            break
    else:
        data["users"].append({"id": user_id, "purchases": new_purchases})

    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    logging.info(f"✅ Updated shopping data for user {user_id}!")

    return build_product_relations(data)

user_history = ["laptop", "smartphone"]
suggested_purchases = recommend_purchases(user_history, product_relations)
print(f"🛒 Based on {user_history}, recommended purchases: {suggested_purchases}")

product_relations = update_shopping_data(6, ["tablet", "smartwatch"])
product_relations = update_shopping_data(7, ["gaming mouse", "gaming keyboard"])

new_user_history = ["gaming mouse"]
suggested_purchases_new = recommend_purchases(new_user_history, product_relations)
print(f"🛒 Based on {new_user_history}, recommended purchases: {suggested_purchases_new}")

while True:
    user_input = input("\n🔹 Enter your purchases (comma-separated) or 'exit' to quit: \n")
    if user_input.lower() == "exit":
        break
    user_history = [item.strip() for item in user_input.split(",")]
    recommendations = recommend_purchases(user_history, product_relations)
    print(f"🛒 Recommended based on {user_history}: {recommendations}")
