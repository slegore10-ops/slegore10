from datetime import datetime

# ======================
# LOGIN
# ======================
cashier = input("Enter cashier name: ")
print("Welcome,", cashier)

# ======================
# STORE ITEMS
# ======================
store_items = {
    "bread": {"price": 500, "stock": 15, "category": "groceries"},
    "flour": {"price": 350, "stock": 10, "category": "groceries"},
    "sugar": {"price": 200, "stock": 12, "category": "groceries"},
    "egg": {"price": 25, "stock": 30, "category": "groceries"},

    "water": {"price": 150, "stock": 20, "category": "beverages"},
    "juice": {"price": 180, "stock": 15, "category": "beverages"},
    "soda": {"price": 220, "stock": 18, "category": "beverages"},
    "milk": {"price": 250, "stock": 10, "category": "beverages"},

    "soap": {"price": 150, "stock": 8, "category": "household"},
    "detergent": {"price": 600, "stock": 6, "category": "household"},
    "toilet paper": {"price": 400, "stock": 10, "category": "household"},
    "bleach": {"price": 300, "stock": 7, "category": "household"}
}

shopping_cart = {}

receipt_no = 1
total_money = 0
transactions = 0

LOW_STOCK_THRESHOLD = 5

# ======================
# SHOW ITEMS
# ======================
def display_items():
    print("\nAvailable Items:")
    for item, info in store_items.items():
        print(item, "-", info["category"], "| Price:", info["price"], "| Stock:", info["stock"])

# ======================
# ADD ITEM
# ======================
def add_item():
    name = input("Enter item name: ").lower()

    if name not in store_items:
        print("Item not found.")
        return

    try:
        qty = int(input("Enter quantity: "))
    except:
        print("Invalid number.")
        return

    if qty <= 0:
        print("Invalid quantity.")
        return

    if qty > store_items[name]["stock"]:
        print("Not enough stock.")
        return

    # add to cart
    if name in shopping_cart:
        shopping_cart[name] += qty
    else:
        shopping_cart[name] = qty

    store_items[name]["stock"] -= qty
    print("Item added.")

    # low stock warning immediately
    if store_items[name]["stock"] <= LOW_STOCK_THRESHOLD:
        print("⚠️ Warning:", name, "is running low! Remaining:", store_items[name]["stock"])

# ======================
# REMOVE ITEM
# ======================
def remove_item():
    name = input("Enter item to remove: ").lower()

    if name not in shopping_cart:
        print("Item not in cart.")
        return

    try:
        qty = int(input("Enter quantity to remove: "))
    except:
        print("Invalid input.")
        return

    if qty >= shopping_cart[name]:
        store_items[name]["stock"] += shopping_cart[name]
        del shopping_cart[name]
    else:
        shopping_cart[name] -= qty
        store_items[name]["stock"] += qty

    print("Item removed.")

# ======================
# VIEW CART
# ======================
def view_cart():
    if len(shopping_cart) == 0:
        print("Cart is empty.")
        return

    total = 0
    print("\nCart Items:")

    for item, qty in shopping_cart.items():
        price = store_items[item]["price"]
        cost = price * qty
        total += cost
        print(f"{item} x {qty} = ${cost:,.2f}")

    print(f"Subtotal: ${total:,.2f}")

# ======================
# CALCULATE BILL
# ======================
def compute_bill():
    subtotal = 0

    for item, qty in shopping_cart.items():
        subtotal += store_items[item]["price"] * qty

    tax = subtotal * 0.10

    discount = 0
    if subtotal > 5000:
        discount = subtotal * 0.05

    total = subtotal + tax - discount

    return subtotal, tax, discount, total

# ======================
# CHECKOUT
# ======================
def checkout():
    global receipt_no, total_money, transactions

    if len(shopping_cart) == 0:
        print("Cart is empty.")
        return

    subtotal, tax, discount, total = compute_bill()

    print(f"Total to pay: ${total:,.2f}")

    try:
        paid = float(input("Enter payment: "))
    except:
        print("Invalid payment.")
        return

    if paid < total:
        print("Not enough money.")
        return

    change = paid - total

    # receipt
    now = datetime.now().strftime("%d/%m/%Y %I:%M %p")

    print("\n===== BEST BUY RETAIL STORE =====")
    print("Receipt:", receipt_no)
    print("Date:", now)
    print("Cashier:", cashier)
    print("--------------------------------")
    print("Items:")

    item_no = 1
    for item, qty in shopping_cart.items():
        price = store_items[item]["price"]
        total_item = price * qty
        print(f"{item_no}. {item:<15} x{qty:<3} @ ${price:,.2f} = ${total_item:,.2f}")
        item_no += 1

    print("--------------------------------")
    print(f"Subtotal: ${subtotal:,.2f}")
    print(f"Tax:      ${tax:,.2f}")
    print(f"Discount: ${discount:,.2f}")
    print(f"Total:    ${total:,.2f}")
    print(f"Paid:     ${paid:,.2f}")
    print(f"Change:   ${change:,.2f}")
    print("--------------------------------")
    print("Thank you for shopping!")

    receipt_no += 1
    total_money += total
    transactions += 1

    # low stock alert after checkout
    print("\n--- Stock Alerts ---")
    low_found = False

    for item, info in store_items.items():
        if info["stock"] <= LOW_STOCK_THRESHOLD:
            print(item, "is low on stock! Remaining:", info["stock"])
            low_found = True

    if not low_found:
        print("All stock levels are okay.")

    shopping_cart.clear()

# ======================
# SALES SUMMARY
# ======================
def summary():
    print("\nSales Summary")
    print("Transactions:", transactions)
    print(f"Total Sales: ${total_money:,.2f}")

# ======================
# MENU
# ======================
def menu():
    while True:
        print("\n1. Show Items")
        print("2. Add Item")
        print("3. Remove Item")
        print("4. View Cart")
        print("5. Checkout")
        print("6. Summary")
        print("7. Exit")

        choice = input("Choose: ")

        if choice == "1":
            display_items()
        elif choice == "2":
            add_item()
        elif choice == "3":
            remove_item()
        elif choice == "4":
            view_cart()
        elif choice == "5":
            checkout()
        elif choice == "6":
            summary()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

# ======================
# RUN PROGRAM
# ======================
menu()
