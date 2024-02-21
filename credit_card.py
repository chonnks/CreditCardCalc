"""Perform credit card calculations."""
from argparse import ArgumentParser
import sys

#interest function
def get_min_payment(balance, fees = 0):
    #define the vars
    b = balance 
    m = .02 #percent of the balance that needs to be paid
    f = fees

    #formula
    min_payment = ((b * m) + f)

    #min payment setup
    if min_payment < 25:
        min_payment = 25
        return min_payment

    return min_payment

#interest function
def interest_charged(balance, apr):
    #define vars
    a = apr / 100  
    y = 365
    b = balance
    d = 30
    #formula
    i = (a / y) * b * d

    return i 

#remaining payments function
def remaining_payments(balance, apr, targetamount, credit_line, fees):
    #def vars
    payments_counter = 0
    ThresholdCounter25 = 0
    ThresholdCounter50 = 0
    ThresholdCounter75 = 0

    #loop to get if payment is either minimum or target
    while balance > 0:
        if targetamount is None:
            payment = get_min_payment(balance, fees)
        else:
            payment = targetamount

        #interest definition and balance finding
        interest = interest_charged(balance, apr)
        balance -= (payment + interest + fees)

        if balance > 0 and payment - interest <= 0:
            print("This card cannot be paid off.")
            return None
        
        #math for payments counter
        if balance > 0:
            payments_counter += 1

            if balance > 0.75 * credit_line :
                ThresholdCounter75 += 1
            elif balance > 0.50 * credit_line :
                ThresholdCounter50 += 1
            elif balance > 0.25 * credit_line :
                ThresholdCounter25 += 1
    #return as tuple
    return payments_counter, ThresholdCounter25, ThresholdCounter50, ThresholdCounter75

#main function where we return everything
def main(balance, apr, targetamount, credit_line = 0, fees = 0):
    #recommended minimum payment depending input
    RecMinPayment = get_min_payment(balance, fees)
    
    #pays minimum
    pays_minimum = False
    RemPay = remaining_payments(balance, apr, targetamount, credit_line, fees)

    #target amount makes minimum payment true
    if targetamount is None:
        pays_minimum = True
    else: # prints out how much you will pay off balance in
        if pays_minimum == True:
            print("If you pay the minimum payments each month, you will pay off the balance in ", 
                   RemPay[0], " payments.")
        else: # prints out if targetamount is reached
            print("If you make payments of $", targetamount, 
                     "you will pay off the balance in", RemPay, "payments.")

    #prints final result as a string
    print ("Your recommended starting minimum payment is $" + str(RecMinPayment))
    FinalResult = ("You will spend a total of " + str(RemPay[1]) + " months over 25% of the credit line\nYou will spend a total of " + str(RemPay[2]) + " months over 50% of the credit line\nYou will spend a total of " + str(RemPay[3]) + " months over 75% of the credit line")       
    print (FinalResult)           
    return FinalResult


def parse_args(args_list):
    """Takes a list fo strings from the command prompt and passes them through 
    as arguments 
    
    Args:
        args_list(list): the lits of strings from the command prompt
    Returns:
        args(ArgumentParser)
    """
    parser = ArgumentParser()

    parser.add_argument('balance_amount', type = float, help = 
                         'The total amount of balance left on the credit account')
    parser.add_argument('apr', type = int, help = 
                         'The annual APR, should be an int between 1 and 100')
    parser.add_argument('credit_line',type = int, help = 
                         'The maximum amount of balance allowed on the credit line.')
    parser.add_argument('--payment', type = int, default = None, help = 
                         'The amount the user wants to pay per payment, should be a positive number')
    parser.add_argument('--fees', type = float, default = 0, help = 
                         'The fees that are applied monthly.')

    # parse and validate arguments
    args = parser.parse_args(args_list)
    
    if args.balance_amount < 0:
        raise ValueError("balance amount must be positive")
    if not 0 <= args.apr <= 100:
        raise ValueError("APR must be between 0 and 100")
    if args.credit_line < 1:
        raise ValueError("credit line must be positive")
    if args.payment is not None and args.payment < 0:
        raise ValueError("number of payments per year must be positive")
    if args.fees < 0:
        raise ValueError("fees must be positive")

    return args

if __name__ == "__main__":
    
    try:
        arguments = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))

    print(main(arguments.balance_amount, arguments.apr, 
credit_line = arguments.credit_line, targetamount = arguments.payment, fees = arguments.fees))


