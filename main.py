import pandas as pd
import matplotlib.pyplot as plot


def get_stocks_from_file():
    screws = []
    with open('stocks.txt', 'r') as file:
        for line in file:
            # we don't care about reading lines  with comments
            if line[0] != '#':
                l = line.strip().split(',')
                total_stock = int(l[3]) + int(l[4]) + int(l[5])
                screw = {
                    "Material": l[0],
                    "Head Type": l[1],
                    "Length": int(l[2]),
                    "Stock 50": int(l[3]),
                    "Stock 100": int(l[4]),
                    "Stock 200": int(l[5]),
                    "Total Stock": total_stock,
                    "Cost": float(l[6]),
                    "Total Value": float(l[6]) * total_stock,
                    "Discount": l[7],
                }
                screws.append(screw)
    return screws


# get_stocks_from_file()


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


def total_in_stock_per_length_category_6(stocks):
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
        elif choice == 6:
            total_in_stock_per_length_category_6(stocks)


main()
# def total_in_stock_per_length_category(stock):
# def screws_based_on_length(stock, length):
# def main():
# stock = get_stocks_from_file()

# if __name__ == "__main__":
# main()
