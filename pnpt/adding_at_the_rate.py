combined = open('combined.txt', 'r')

all_names = combined.readlines()

for a in all_names:
    print(a.strip() + '@thepastamentors.com')