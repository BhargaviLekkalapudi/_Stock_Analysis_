# Import CSV file

import csv

# Read data from CSV file
def read_csv_data(filename):
    stocks = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    name = row['Stock'].strip()
                    sector = row['Sector'].strip()
                    start_price = float(row['PriceStart'])
                    end_price = float(row['PriceEnd'])

                    if start_price > 0 and end_price > 0:
                        stocks.append({
                            'Stock': name,
                            'Sector': sector,
                            'PriceStart': start_price,
                            'PriceEnd': end_price
                        })
                except:
                    # Skip invalid data
                    continue
    except FileNotFoundError:
        print("File not found:", filename)
    return stocks


# Calculate return for each stock
def calculate_return(stock):
    start = stock['PriceStart']
    end = stock['PriceEnd']
    change = ((end - start) / start) * 100
    stock['Return'] = round(change, 2)
    return stock


# Sort stocks by return
def sort_stocks(data):
    return sorted(data, key=lambda x: x['Return'], reverse=True)


# Find average return by sector
def get_sector_summary(data):
    summary = {}
    for s in data:
        sector = s['Sector']
        if sector not in summary:
            summary[sector] = {'total': 0, 'count': 0}
        summary[sector]['total'] += s['Return']
        summary[sector]['count'] += 1

    for sec in summary:
        avg = summary[sec]['total'] / summary[sec]['count']
        summary[sec]['avg_return'] = round(avg, 2)
    return summary


# Print report on screen
def print_report(data, summary):
    print("\nAll Stock Details")
    print("-" * 60)
    print(f"{'Stock':<15}{'Sector':<20}{'Start':<10}{'End':<10}{'Return(%)':<10}")
    for s in data:
        print(f"{s['Stock']:<15}{s['Sector']:<20}{s['PriceStart']:<10}{s['PriceEnd']:<10}{s['Return']:<10}")

    print("\nTop 5 Stocks by Return")
    print("-" * 60)
    for s in data[:5]:
        print(f"{s['Stock']:<15}{s['Return']}%")

    print("\nSector Summary")
    print("-" * 60)
    best = max(summary.items(), key=lambda x: x[1]['avg_return'])
    for sec, val in summary.items():
        print(f"{sec:<20} Avg Return: {val['avg_return']}%   Count: {val['count']}")
    print(f"\nBest Sector: {best[0]} ({best[1]['avg_return']}%)")


# Save results to CSV file
def save_to_csv(data, filename="stock_returns.csv"):
    fields = ['Stock', 'Sector', 'PriceStart', 'PriceEnd', 'Return']
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
    print("\nData saved to", filename)


# Main program
if __name__ == "__main__":
    filename = "stock_sample_data.csv"
    data = read_csv_data(filename)

    if not data:
        print("No valid data found. Exiting program.")
        exit()

    data = [calculate_return(s) for s in data]
    data = sort_stocks(data)
    summary = get_sector_summary(data)

    print_report(data, summary)
    save_to_csv(data)