import pandas as pd
import matplotlib.pyplot as plot


def calculate_total_units(box_size, box_quantity):
    unit_of_stock = 50

    num_units = (box_size / unit_of_stock) * box_quantity
    return num_units


def calculate_cost_unit50(costper_unit):
    bulk50cost = 50 * costper_unit
    return bulk50cost


def calculate_cost_unit100(costper_unit):
    bulk100cost = 100 * (costper_unit * 0.9)
    return bulk100cost


def calculate_cost_unit200(costper_unit):
    bulk200cost = 200 * (costper_unit * 0.85)
    return bulk200cost


def get_stocks_from_file():
    screws = []
    with open('stocks.txt', 'r') as file:
        for line in file:
            # we don't care about reading lines  with comments
            if line[0] != '#':
                l = line.strip().split(',')

                num_fifty_boxes = l[3]
                num_hundred_boxes = l[4]
                num_two_hundred_boxes = l[5]
                costperunit = l[6]

                total_units_fifty_box = calculate_total_units(50, int(num_fifty_boxes))
                total_units_hundred_box = calculate_total_units(100, int(num_hundred_boxes))
                total_units_two_hundred_box = calculate_total_units(200, int(num_two_hundred_boxes))

                costunit50 = calculate_cost_unit50(float(costperunit))
                costunit100 = calculate_cost_unit100(float(costperunit))
                costunit200 = calculate_cost_unit200(float(costperunit))

                total_stock = total_units_fifty_box + total_units_hundred_box + total_units_two_hundred_box
                total_cost = costunit50 + costunit100 + costunit200

                screw = {
                    "Material": l[0],
                    "Head Type": l[1],
                    "Length": int(l[2]),
                    "Stock 50": int(l[3]),
                    "Stock 100": int(l[4]),
                    "Stock 200": int(l[5]),
                    "Total Stock": total_stock,
                    "Cost": float(l[6]),
                    "Total Value": total_cost,
                    "Discount": l[7].strip(),
                }
                screws.append(screw)

    return screws


# get_stocks_from_file()
# TASK 1!

def summary_report(stocks):
    total_units = 0
    total_value = 0
    for screw in stocks:
        total_units += screw["Total Stock"]
        total_value += screw["Total Value"]
    pretty = pd.DataFrame.from_records(stocks,
                                       columns=["Material", "Head Type", "Length", "Stock 50", "Stock 100", "Stock 200",
                                                "Cost", "Discount"])
    print("""
    Here are all the screws we have in stock:
    {}
    
    Total number of units:
    {}
    
    Total value: 
    {}
    
    """.format(pretty, total_units, total_value))


# TASK 2!!

def total_in_stock_per_length_category(stocks):
    length_per_category = {}
    for screw in stocks:
        length = screw["Length"]
        total_stock = screw["Total Stock"]
        if length in length_per_category:
            v = length_per_category[length]
            v += total_stock
            length_per_category[length] = v
        else:
            length_per_category[length] = total_stock

    prettier = pd.DataFrame.from_records([length_per_category],
                                         columns=[20, 40, 60])
    print("Total in stock per length category: ")
    print(prettier)


# TASK 3!

def screws_based_on_length(stocks, length):
    results = []
    for screw in stocks:
        if length == screw["Length"]:
            results.append(screw)
    pretty_print = pd.DataFrame.from_records(results,
                                             columns=["Material", "Head Type", "Length", "Stock 50", "Stock 100",
                                                      "Stock 200",
                                                      "Cost", "Discount"])
    if len(results) == 0:
        print("no screws available for length.{}".format(length))

    else:
        print(pretty_print)


# TASK 4!

def queries(stocks):
    query = input(
        "What screw type's availability would you like to check? (please format like this: eg. 'brass,slot,20'): ")
    stock_level = input(
        "Would you like to increase or decrease stock level or make a sale? (please answer either 'increase' or 'decrease' or 'sale': ")
    how_much = int(input("How many units would you like to increase/decrease by: "))
    for screw in stocks:
        category = "{},{},{}".format(screw["Material"], screw["Head Type"], screw["Length"])
        if query == category:
            if stock_level == 'increase':
                stock = screw["Total Stock"]
                new_stock = stock + how_much
                screw["Total Stock"] = new_stock

            elif stock_level == 'decrease':
                stock = screw["Total Stock"]
                new_stock = stock - how_much
                screw["Total Stock"] = new_stock

            elif stock_level == 'sale':
                stock = screw["Total Stock"]
                new_stock = stock + how_much
                if new_stock <= screw["Total Stock"]:
                    print("Total cost of order is: ", screw["Total Value"])
                else:
                    want_to_continue = input(
                        "Your order can only be partially fufilled, do you wish to continue(yes/no)? ")
                    if want_to_continue == 'yes':
                        print("Total cost of order is: ", screw["Total Value"])
                    else:
                        print("Order cancelled.")
                        return

            else:
                print("invalid option")
                return


# TASK 5!


def discount_feature(stocks):
    largest_screw_category = " "
    largest_stock = 0
    for screw in stocks:
        category = "{},{},{}".format(screw["Material"], screw["Head Type"], screw["Length"])
        screw_type_stock = screw["Total Stock"]
        if screw_type_stock > largest_stock:
            largest_screw_category = category
            largest_stock = screw_type_stock
    print("The largest screw category is: {}".format(largest_screw_category))

    decision = input("Would you like to place a 10% discount on that category (yes/no): ")
    yes_choices = ['yes', 'Yes']
    no_choices = ['no', 'No']

    if decision in yes_choices:
        for screw in stocks:
            category = "{},{},{}".format(screw["Material"], screw["Head Type"], screw["Length"])
            discount = screw["Total Value"] * 0.1
            discounted_total_value = screw["Total Value"] - discount
            if category == largest_screw_category:
                screw["Discount"] = 'yes'
                print("Discount applied new total value is: ", discounted_total_value)
            else:
                screw["Discount"] = 'no'

    if decision in no_choices:
        print("No discount added.")


# TASK 6!

def total_in_stock_per_length_category_chart(stocks):
    length_per_category = {}
    for screw in stocks:
        length = screw["Length"]
        total_stock = screw["Total Stock"]
        if length in length_per_category:
            v = length_per_category[length]
            v += total_stock
            length_per_category[length] = v
        else:
            length_per_category[length] = total_stock
            print(length_per_category)
    barchart = {"Lengths": [],
                "Total Stock": []}
    for length, total_stock in length_per_category.items():
        barchart["Lengths"].append(length)
        barchart["Total Stock"].append(total_stock)
    dataFrame = pd.DataFrame(data=barchart)
    dataFrame.plot.bar(x="Lengths", y="Total Stock", title="Units per Length Category")

    plot.show(block=True)


def main():
    stocks = get_stocks_from_file()
    choice = 0
    while choice != 7:
        choice = int(input("""
                    Welcome to Simply Screws

                    ***MAIN MENU***
                    1: List of screw types available and their details
                    2: Report showing total number of units in stock in each length
                    3: List of screws and their details based on desired length
                    4: Queries
                    5: Discount feature
                    6: Barchart
                    7: Quit

                    """))
        if choice == 1:
            summary_report(stocks)
        elif choice == 2:
            total_in_stock_per_length_category(stocks)
        elif choice == 3:
            length_category = int(input('Enter desired length: '))
            screws_based_on_length(stocks, length_category)
        elif choice == 4:
            queries(stocks)
        elif choice == 5:
            discount_feature(stocks)
        elif choice == 6:
            total_in_stock_per_length_category_chart(stocks)


main()
