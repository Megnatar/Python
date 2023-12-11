key=['23000', '24000', '25000']

List1=['23458', '23459', '23460', '23461']     # value1={'23458': '23458', '23459': 'Gaaaaaa', '23460': '23460', '23461': '23461'}
List2=['1212', '2378', '467']                  # value2={'1212': '1212', '2378': '2378', '467':'467'}
List3=['8785', '4455', '9979', '1212']         # value3={'8785': '8785', '4455': '4455', '9979': '9979', '1212': '1212'}
Lists = [List1, List2, List3]

i = 0; dictonary = {}

while not len(key) == i:
    dictonary.update({key[i]: Lists[i]}); i += 1
i = 0

for k in dictonary.keys():
    print("key: \t\t\t", k, "\nlist: \t\t\t", dictonary[k], "\nfirst value in list:\t", dictonary[k][0], "\n")

