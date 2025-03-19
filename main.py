import json
from collections import defaultdict, Counter

shopping_data = {
    "users": [
        {"id": 1, "purchases": ["laptop", "headphones", "smartphone"]},
        {"id": 2, "purchases": ["sneakers", "t-shirt", "jacket"]},
        {"id": 3, "purchases": ["detective book", "science book", "fantasy book"]},
        {"id": 4, "purchases": ["dumbbells", "treadmill", "bicycle"]},
        {"id": 5, "purchases": ["car oil", "car tires", "car accessories"]}
    ]
}

json_file_path = "shopping_data.json"

with open(json_file_path, "w", encoding="utf-8") as file:
    json.dump(shopping_data, file, indent=4, ensure_ascii=False)


# Функция загрузки данных из JSON
def load_shopping_data():
    with open(json_file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# Функция построения связей между товарами
def build_product_relations(data):
    relations = defaultdict(list)
    for user in data["users"]:
        for item in user["purchases"]:
            relations[item].extend(user["purchases"])

    # Удаляем дубликаты и сам товар из списка рекомендаций
    for item in relations:
        relations[item] = list(set(relations[item]) - {item})

    return relations


# Функция рекомендации товаров
def recommend_purchases(purchase_history, product_relations):
    recommended = Counter()
    for item in purchase_history:
        if item in product_relations:
            recommended.update(product_relations[item])

    # Убираем уже купленные товары
    for item in purchase_history:
        recommended.pop(item, None)

    return [item for item, _ in recommended.most_common(3)]  # Топ-3 рекомендации


# Функция обновления покупок (обучение)
def update_shopping_data(user_id, new_purchases):
    data = load_shopping_data()

    for user in data["users"]:
        if user["id"] == user_id:
            user["purchases"].extend(new_purchases)
            user["purchases"] = list(set(user["purchases"]))  # Убираем дубликаты
            break
    else:
        data["users"].append({"id": user_id, "purchases": new_purchases})

    # Обновляем JSON-файл
    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"✅ Updated shopping data for user {user_id}!")

    # Обновляем связи после добавления новых покупок
    return build_product_relations(data)


# 🔹 2. Загружаем данные и строим связи
data = load_shopping_data()
product_relations = build_product_relations(data)

# 🔹 3. Проверяем рекомендации перед обучением
user_history = ["laptop", "smartphone"]
suggested_purchases = recommend_purchases(user_history, product_relations)
print(f"🛒 Based on {user_history}, recommended purchases: {suggested_purchases}")

# 🔹 4. Обучение системы (добавляем новые покупки)
product_relations = update_shopping_data(6, ["tablet", "smartwatch"])
product_relations = update_shopping_data(7, ["gaming mouse", "gaming keyboard"])

# 🔹 5. Теперь проверяем рекомендации для нового товара
new_user_history = ["gaming mouse"]
suggested_purchases_new = recommend_purchases(new_user_history, product_relations)
print(f"🛒 Based on {new_user_history}, recommended purchases: {suggested_purchases_new}")