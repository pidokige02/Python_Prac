import sys

print(sys.argv)  # list type

if len(sys.argv) == 1:
    print("first_argu : " + sys.argv[0])
elif len(sys.argv) == 2:
    print("first_argu : " + sys.argv[0])
    print("second_argu : " + sys.argv[1])
else:
    print("first_argu : " + sys.argv[0])
    print("second_argu : " + sys.argv[1])
    print("Third_argu : " + sys.argv[2])

# if len(sys.argv) != 2:
#     print("Insufficient arguments")
#     sys.exit()
