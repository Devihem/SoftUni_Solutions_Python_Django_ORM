
from main import Session
from models import User, Order

# Task1
with Session() as session:

    new_user = User(username='john_doe',email='john@example.com')
    session.add(new_user)
    session.commit()

# Task2
with Session() as session:
    users = session.query(User).all()
    for user in users:
        print(user.username, user.email)


# Task3
with Session() as session:
    user_to_update = session.query(User).filter_by(username='john_doe').first()

    if user_to_update:
        user_to_update.email = 'new_email@example.com'
        session.commit()
        print("User updated successfully")
    else:
        print("User not found")

# Task 4
with Session() as session:
    user_to_delete = session.query(User).filter_by(username='john_doe').first()

    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()
        print("User deleted successfully")
    else:
        print("User not found")

# Task 5 - Personal Code
with Session() as session:
    users_and_emails = [("john_doe", "john.doe@example.com"),
                        ("sarah_smith", "sarah.smith@gmail.com"),
                        ("mike_jones", "mike.jones@company.com"),
                        ("emma_wilson", "emma.wilson@domain.net"),
                        ("david_brown", "david.brown@email.org")]

    for data in users_and_emails:
        new_user = User(username=data[0], email=data[1])
        session.add(new_user)
        session.commit()

# Task 6
session = Session()

try:
    session.begin()
    session.query(User).delete()
    session.commit()
    print("All Users deleted successfully")

except Exception as e:
    session.rollback()
    print("An error occurred:", str(e))

finally:
    session.close()

# Task 7
with Session() as session:
    session.add_all((Order(user_id=23), Order(user_id=25)))
    session.commit()

# Task 8
with Session() as session:
    orders = session.query(Order).order_by(Order.user_id.desc()).all()

    if not orders:
        print("No orders yet.")
    else:
        for order in orders:
            user = order.user
            print(f"Order number {order.id}, Is completed: {order.is_completed}, Username: {user.username}")
