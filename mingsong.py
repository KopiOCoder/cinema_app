import time
import datetime

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
    print("      💳 Card Payment")
    print("="*30)
    
    #testing first
    card_number = input("Enter card number (16 digits): ")
    if not card_number.isdigit() or len(card_number) != 1:
        print("❌ Invalid card number. Please enter a 16-digit number.")
        return False

    cvv = input("Enter CVV (3 digits): ")
    if not cvv.isdigit() or len(cvv) != 3:
        print("❌ Invalid CVV. Please enter a 3-digit number.")
        return False

    expiry_date = input("Enter expiry date (MM/YY): ")
    if len(expiry_date) != 5 or expiry_date[2] != '/':
        print("❌ Invalid expiry date format. Please use MM/YY.")
        return False
        
    print("\nProcessing payment...")
    time.sleep(2) 
    print("Payment successful! 🎉")
    time.sleep(1)
    return True

def print_receipt(num_adults, num_children, total_fare):
    current = datetime.datetime.now()
    receipt_time = current.strftime("%I:%M %p") # Format as HH:MM AM/PM
    receipt_date = current.strftime("%d %B %Y") # Format as Day Month Year
    
    print("\n" + "="*30)
    print("      🎥 Cinema Ticket Receipt")
    print("="*30)
    print(f"Date: {receipt_date}")
    print(f"Time: {receipt_time}")
    print("-"*30)
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

        while True:

            confirm = input("Would you like to proceed to payment? (yes/no): ").lower()
            if confirm == 'yes':
            
                if payment():
                    print_receipt(num_adults, num_children, total_price)
                else:
                    
                    print("Payment failed. Order cancelled.")
                break   

            elif confirm == 'no':
                print("Order cancelled. Thank you for visiting.")
                break

            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
            
    except ValueError:
        print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()