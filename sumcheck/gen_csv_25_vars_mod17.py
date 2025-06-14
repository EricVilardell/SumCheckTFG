import csv, random

n = 2**25          # 33 554 432
vals = [random.randint(0, 16) for _ in range(n)]   # mod 17 -> 0..16
with open("func25vars_mod17.csv", "w", newline='') as f:
    csv.writer(f).writerow(vals)
print("CSV listo con", n, "valores en una sola línea.")