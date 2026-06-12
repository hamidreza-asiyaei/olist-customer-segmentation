import pandas as pd

# Load datasets
customers = pd.read_csv("DATA/olist_customers_dataset.csv")
orders = pd.read_csv("DATA/olist_orders_dataset.csv")
payments = pd.read_csv("DATA/olist_order_payments_dataset.csv")

# Merge orders + payments
order_payments = orders.merge(
    payments,
    on="order_id",
    how="inner"
)

# Merge with customers
customer_data = order_payments.merge(
    customers,
    on="customer_id",
    how="inner"
)

# Customer Summary Table
customer_summary = customer_data.groupby(
    "customer_unique_id"
).agg(
    total_orders=("order_id", "nunique"),
    total_spent=("payment_value", "sum")
).reset_index()

print(customer_summary.head())
# Top 10 Customers by Spending

top_customers = customer_summary.sort_values(
    by="total_spent",
    ascending=False
).head(10)

print("\nTop 10 Customers:")
print(top_customers)

import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
plt.bar(
    top_customers["customer_unique_id"],
    top_customers["total_spent"]
)

plt.title("Top 10 Customers by Spending")
plt.xlabel("Customer ID")
plt.ylabel("Total Spent")

plt.xticks(rotation=90)

plt.tight_layout()
plt.show()

print("\nTotal Customers:")
print(customer_summary.shape[0])

customer_summary.to_csv(
    "customer_summary.csv",
    index=False
)

print("\nRows:", customer_data.shape[0])
print("Columns:", customer_data.shape[1])
# Revenue by State

top_states = customer_data.groupby(
    "customer_state"
).agg(
    total_revenue=("payment_value", "sum")
).sort_values(
    by="total_revenue",
    ascending=False
).head(10)

print(top_states)
import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))

top_states["total_revenue"].plot(
    kind="bar"
)

plt.title("Top 10 States by Revenue")
plt.xlabel("State")
plt.ylabel("Revenue")

plt.tight_layout()
plt.savefig("top_states_revenue.png")
plt.show()
