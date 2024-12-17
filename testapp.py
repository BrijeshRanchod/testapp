import streamlit as st

# Simulated "Database" of restaurants, menus, and orders
restaurants = {
    "Pasta Palace": {
        "Spaghetti Bolognese": 12.99,
        "Fettuccine Alfredo": 14.49,
        "Penne Arrabbiata": 11.99,
    },
    "Burger Barn": {
        "Classic Cheeseburger": 10.49,
        "Bacon Burger": 11.99,
        "Vegan Burger": 9.99,
    },
    "Sushi Stop": {
        "California Roll": 8.49,
        "Spicy Tuna Roll": 9.99,
        "Salmon Sashimi": 12.49,
    },
}

# Initialize session state for cart
if 'cart' not in st.session_state:
    st.session_state.cart = {}

if 'total_price' not in st.session_state:
    st.session_state.total_price = 0.0


# --- Functions ---
def add_to_cart(restaurant_name, item_name, item_price):
    """Add a selected item to the cart."""
    if restaurant_name not in st.session_state.cart:
        st.session_state.cart[restaurant_name] = {}
    if item_name not in st.session_state.cart[restaurant_name]:
        st.session_state.cart[restaurant_name][item_name] = {'quantity': 0, 'price': item_price}
    
    st.session_state.cart[restaurant_name][item_name]['quantity'] += 1
    st.session_state.total_price += item_price
    st.success(f"Added {item_name} from {restaurant_name} to your cart!")


def display_cart():
    """Display the current cart and allow users to place an order."""
    st.header("🛒 Your Cart")
    if not st.session_state.cart:
        st.write("Your cart is empty.")
        return

    total_price = 0
    for restaurant, items in st.session_state.cart.items():
        st.subheader(restaurant)
        for item_name, details in items.items():
            quantity = details['quantity']
            item_price = details['price']
            total_item_price = quantity * item_price
            st.write(f"{item_name} x {quantity} = ${total_item_price:.2f}")
            total_price += total_item_price

    st.write(f"**Total Price: ${total_price:.2f}**")

    if st.button("Place Order"):
        st.success("🎉 Your order has been placed successfully!")
        st.session_state.cart = {}  # Clear the cart
        st.session_state.total_price = 0.0


# --- Streamlit App Layout ---
st.title("🍔 Uber Eats Clone")

# Tabs for Restaurants and Cart
tabs = st.tabs(["Restaurants", "Cart"])

# --- Tab 1: Restaurant List ---
with tabs[0]:
    st.header("🍽️ Restaurants")
    for restaurant_name, menu in restaurants.items():
        st.subheader(restaurant_name)
        for item_name, item_price in menu.items():
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"**{item_name}**")
            col2.write(f"${item_price:.2f}")
            if col3.button(f"Add {item_name}", key=f"{restaurant_name}-{item_name}"):
                add_to_cart(restaurant_name, item_name, item_price)

# --- Tab 2: Cart ---
with tabs[1]:
    display_cart()
