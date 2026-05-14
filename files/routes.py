from flask import Blueprint, jsonify, request

main = Blueprint("main", __name__)

# In-memory store (acts as a simple DB)
items = {}
next_id = 1


@main.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Flask API is running"}), 200


@main.route("/items", methods=["GET"])
def get_items():
    return jsonify({"items": list(items.values())}), 200


@main.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = items.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@main.route("/items", methods=["POST"])
def create_item():
    global next_id
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Field 'name' is required"}), 400

    item = {
        "id": next_id,
        "name": data["name"],
        "description": data.get("description", ""),
    }
    items[next_id] = item
    next_id += 1
    return jsonify(item), 201


@main.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = items.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    item["name"] = data.get("name", item["name"])
    item["description"] = data.get("description", item["description"])
    items[item_id] = item
    return jsonify(item), 200


@main.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    if item_id not in items:
        return jsonify({"error": "Item not found"}), 404
    deleted = items.pop(item_id)
    return jsonify({"message": "Item deleted", "item": deleted}), 200
