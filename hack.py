import json
import os

# File paths
INVENTORY_FILE = "inventory.json"
USERS_FILE = "users.json"
GST_RATE = 0.18

# Load JSON data
def load_json(file, default_data={}):
    if os.path.exists(file) and os.path.getsize(file) > 0:
        with open(file, "r") as f:
            return json.load(f)
    return default_data

# Save JSON data
def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# Load inventory and users
def load_data():
    inventory = load_json(INVENTORY_FILE, default_data={
        "Laptop": {"price": 50000, "quantity": 10, "discount": 10},
        "Keyboard": {"price": 1000, "quantity": 50, "discount": 5},
        "Mouse": {"price": 500, "quantity": 100, "discount": 2},
        "Monitor": {"price": 15000, "quantity": 20, "discount": 8}
    })
    
    users = load_json(USERS_FILE, default_data={})
    
    save_data(inventory, users)  # Save default data if files were empty
    return inventory, users

# Save inventory and users
def save_data(inventory, users):
    save_json(INVENTORY_FILE, inventory)
    save_json(USERS_FILE, users)

# Initialize user
def initialize_user(username, users):
    if username not in users:
        users[username] = {"balance": 100000, "cart": {}, "transactions": []}
        print(f"New user '{username}' created with balance ₹100,000.")
    return users[username]

# View products
def view_products(inventory):
    print("\nAvailable Products:")
    for product, details in inventory.items():
        print(f"{product}: Price - ₹{details['price']}, Stock - {details['quantity']}, Discount - {details['discount']}%")

# Add to cart
def add_to_cart(user, inventory):
    product = input("Enter product name: ").strip()
    
    if product not in inventory:
        print(" Product not found.")
        return
    
    try:
        quantity = int(input("Enter quantity: "))
        if quantity <= 0:
            print(" Quantity must be greater than zero.")
            return
    except ValueError:
        print(" Invalid quantity. Please enter a number.")
        return

    if quantity > inventory[product]["quantity"]:
        print(" Not enough stock available.")
        return

    user["cart"].setdefault(product, {"quantity": 0, "price": inventory[product]["price"]})
    user["cart"][product]["quantity"] += quantity
    inventory[product]["quantity"] -= quantity
    print(f" {quantity} {product}(s) added to cart.")

# View cart
def view_cart(user):
    if not user["cart"]:
        print("\n Your cart is empty.")
        return
    
    print("\nYour Cart:")
    for product, details in user["cart"].items():
        print(f"{product}: Quantity - {details['quantity']}, Price - ₹{details['price']} each")

# Clear cart
def clear_cart(user, inventory):
    if not user["cart"]:
        print("🛒 Cart is already empty.")
        return
    
    for product, details in user["cart"].items():
        inventory[product]["quantity"] += details["quantity"]
    
    user["cart"] = {}
    print("🛒 Cart cleared successfully.")

# Checkout
def checkout(user, inventory):
    if not user["cart"]:
        print(" Your cart is empty. Add items before checkout.")
        return

    total_cost = sum(details["quantity"] * details["price"] for details in user["cart"].values())
    gst = total_cost * GST_RATE
    final_amount = total_cost + gst

    print(f"\n🛍️ Checkout Summary:")
    print(f"Total Cost: ₹{total_cost}")
    print(f"GST (18%): ₹{gst:.2f}")
    print(f"Final Amount: ₹{final_amount:.2f}")

    if user["balance"] < final_amount:
        print(" Insufficient balance. Please remove items or add funds.")
        return

    user["balance"] -= final_amount
    user["transactions"].append({"cart": user["cart"], "total": final_amount})
    user["cart"] = {}
    
    print(" Checkout successful! Thank you for your purchase.")

# Main menu
def main():
    inventory, users = load_data()
    
    username = input("Enter username: ").strip()
    user = initialize_user(username, users)

    while True:
        print("\noptions")
        print("1.view products")
        print("2.add to cart")
        print("3.view cart")
        print("4.clear cart")
        print("5.check out")
        print("6.exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            view_products(inventory)
        elif choice == "2":
            add_to_cart(user, inventory)
        elif choice == "3":
            view_cart(user)
        elif choice == "4":
            clear_cart(user, inventory)
        elif choice == "5":
            checkout(user, inventory)
        elif choice == "6":
            save_data(inventory, users)
            print(" Exiting... Have a great day!")
            break
        else:
            print(" Invalid choice. Please try again.")

        save_data(inventory, users)

if __name__ == "__main__":
    main()
