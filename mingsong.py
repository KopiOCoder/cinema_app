import time

def calculate_fare(num_adults, num_children):
    ADULT_PRICE = 15.00
    CHILD_PRICE = 10.00
    
    total_fare = (num_adults * ADULT_PRICE) + (num_children * CHILD_PRICE)
    return total_fare

def display_summary(num_adults, num_children, total_fare):
    print("\n" + "="*30)
    print("      🎬 Order Summary")
    print("="*30)
    print(f"Adult Tickets: {num_adults} x $15.00")
    print(f"Child Tickets: {num_children} x $10.00")
    print("-"*30)
    print(f"Total: ${total_fare:.2f}")
    print("="*30)

def payment():
    print("\n" + "="*30)
    print("      💳 Payment")
    print("="*30)
    input("Please press Enter to pay...")
    print("\nProcessing payment...")
    time.sleep(2) 
    print("Payment successful! 🎉")
    time.sleep(1)

def print_receipt(num_adults, num_children, total_fare):
    print("\n" + "="*30)
    print("      🎥 Cinema Ticket Receipt")
    print("="*30)
    print(f"Adult Tickets: {num_adults} x $15.00")
    print(f"Child Tickets: {num_children} x $10.00")
    print("-"*30)
    print(f"Total Paid: ${total_fare:.2f}")
    print("="*30)
    print("    Thank you for your visit! 🎟️")
    print("="*30)

def main():
    try:
        num_adults = int(input("Enter the number of adult tickets: "))
        num_children = int(input("Enter the number of child tickets: "))
        
        if num_adults < 0 or num_children < 0:
            print("Number of tickets cannot be negative.")
            return
            
        total_price = calculate_fare(num_adults, num_children)

        display_summary(num_adults, num_children, total_price)

        confirm = input("Would you like to proceed to payment? (yes/no): ").lower()
        if confirm == 'yes':
            payment()
            
            print_receipt(num_adults, num_children, total_price)
        else:
            print("Order cancelled. Thank you for visiting.")
        
    except ValueError:
        print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()