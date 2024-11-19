import csv

def calc_e(q1, q2, p1, p2):
    if p1 == 0 or q1 == 0:
        raise ValueError("Initial price and quantity must be greater than zero.")
    return ((q2 - q1) / q1) / ((p2 - p1) / p1)

def calc_k(bp, e, t, f):
    if t <= 0 or f < 0:
        raise ValueError("Time sensitivity must be positive and external factors cannot be negative.")
    return (e * bp) / (t + f)

def calc_p(d, s, k):
    if s == 0:
        raise ValueError("Supply cannot be zero.")
    return k * (d / s - 1)

def calc_pc(q1, q2, p1, p2, bp, s, t, f):
    e = calc_e(q1, q2, p1, p2)
    k = calc_k(bp, e, t, f)
    return calc_p(q2, s, k)

def process_csv(input_file, output_file):
    with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['price_change']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in reader:
            try:
                q1 = float(row['initial_quantity'])
                q2 = float(row['new_quantity'])
                p1 = float(row['initial_price'])
                p2 = float(row['new_price'])
                bp = float(row['base_price'])
                s = float(row['supply'])
                t = float(row['time_sensitivity'])
                f = float(row['external_factors'])

                row['price_change'] = round(calc_pc(q1, q2, p1, p2, bp, s, t, f), 2)
            except ValueError as e:
                row['price_change'] = f"Error: {e}"
            writer.writerow(row)

if __name__ == "__main__":
    input_csv = 'Python\market\goods_data.csv'
    output_csv = 'goods_data_with_price_change.csv'
    process_csv(input_csv, output_csv)
    print(f"Processed data saved to {output_csv}.")
