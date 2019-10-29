x = "ab"
y = "bc"
i = 0
cipher = ""
while i <= len(x):
    z = int(ord(x[i]) + ord((y[i]-96)))
    a = chr(z)
    cipher += a
    i += 1 
print("cipher")

    