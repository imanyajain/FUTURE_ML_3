import pandas as pd
import csv

# Customer support training data
data = [
    {"intent": "greeting", "user_message": "Hi", "bot_response": "Hello! How can I assist you today?", "category": "greeting"},
    {"intent": "greeting", "user_message": "Hello", "bot_response": "Hi there! I'm here to help. What can I do for you?", "category": "greeting"},
    {"intent": "greeting", "user_message": "Good morning", "bot_response": "Good morning! How may I help you today?", "category": "greeting"},
    {"intent": "order_status", "user_message": "Where is my order?", "bot_response": "I can help you track your order. Please provide your order number.", "category": "orders"},
    {"intent": "order_status", "user_message": "Track my package", "bot_response": "I'd be happy to help you track your package. What's your order number?", "category": "orders"},
    {"intent": "return_request", "user_message": "I want to return my order", "bot_response": "I can help you with your return request. Our return policy allows returns within 30 days. Do you have your order number?", "category": "returns"},
    {"intent": "refund_request", "user_message": "I need a refund", "bot_response": "I can help you with your refund request. Refunds are typically processed within 5-7 business days. What's your order number?", "category": "returns"},
    {"intent": "shipping_info", "user_message": "How long does shipping take?", "bot_response": "Shipping typically takes 3-5 business days for standard delivery and 1-2 business days for express shipping.", "category": "shipping"},
    {"intent": "account_help", "user_message": "I forgot my password", "bot_response": "No problem! You can reset your password by clicking the 'Forgot Password' link on the login page.", "category": "account"},
    {"intent": "payment_help", "user_message": "My payment was declined", "bot_response": "I'm sorry your payment was declined. Please check with your bank or try a different payment method.", "category": "payment"},
    {"intent": "fallback", "user_message": "I don't understand", "bot_response": "I apologize for any confusion. Let me connect you with a human agent.", "category": "fallback"},
    {"intent": "goodbye", "user_message": "Thank you", "bot_response": "You're welcome! Is there anything else I can help you with today?", "category": "goodbye"}
]

# Save as DataFrame and CSV
df = pd.DataFrame(data)
df.to_csv('customer_support_dataset.csv', index=False)
print("Dataset created successfully!")
print(f"Total samples: {len(df)}")
