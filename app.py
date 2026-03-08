from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Load ornament data (sample)
with open("data/ornaments.json") as f:
    ornaments = json.load(f)

chat_context = {
    "stage": 0,
    "type": None,
    "design": None,
    "weight": None
}

@app.route("/")
def home():
    chat_context.update({"stage": 0, "type": None, "design": None, "weight": None})
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip().lower()

    # Stage 0 – welcome
    if chat_context["stage"] == 0:
        chat_context["stage"] = 1
        return jsonify({"reply": "Welcome! 💍 Do you prefer Gold or Silver ornaments?"})

    # Stage 1 – type
    elif chat_context["stage"] == 1:
        if user_input not in ["gold", "silver"]:
            return jsonify({"reply": "Please choose either Gold or Silver."})
        chat_context["type"] = user_input
        chat_context["stage"] = 2
        designs = ", ".join(ornaments[user_input].keys())
        return jsonify({"reply": f"Great! Which design do you like: {designs}?"})

    # Stage 2 – design
    elif chat_context["stage"] == 2:
        type_ = chat_context["type"]
        if user_input not in ornaments[type_]:
            return jsonify({"reply": f"That design isn't available. Try one of: {', '.join(ornaments[type_].keys())}."})
        chat_context["design"] = user_input
        chat_context["stage"] = 3
        return jsonify({"reply": "Perfect! Please tell me the weight (in grams) you want."})

    # Stage 3 – weight
    elif chat_context["stage"] == 3:
        try:
            weight = float(user_input)
        except ValueError:
            return jsonify({"reply": "Please enter a valid number for weight (e.g., 10)."})
        chat_context["weight"] = weight
        chat_context["stage"] = 4

        type_ = chat_context["type"]
        design = chat_context["design"]
        price_per_gram = ornaments[type_][design]["price"]
        total_price = price_per_gram * weight
        image_url = ornaments[type_][design]["image"]

        quotation = {
            "type": type_.capitalize(),
            "design": design.capitalize(),
            "weight": f"{weight} g",
            "price_per_gram": f"₹{price_per_gram}",
            "total_price": f"₹{total_price:.2f}",
            "image": image_url
        }

        os.makedirs("output", exist_ok=True)
        with open("output/last_quotation.json", "w") as f:
            json.dump(quotation, f, indent=4)

        return jsonify({
            "reply": f"💎 Here’s your quotation! [Click here to view it →](/quotation)"
        })

    return jsonify({"reply": "I'm not sure I understood that. Try again?"})


@app.route("/quotation")
def quotation():
    with open("output/last_quotation.json") as f:
        quotation_data = json.load(f)
    return render_template("quotation.html", q=quotation_data)


if __name__ == "__main__":
    app.run(debug=True)
