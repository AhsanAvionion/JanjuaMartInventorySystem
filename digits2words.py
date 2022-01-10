#!/usr/bin/env python

# Python program to print a given number in
# words. The program handles numbers
# from 0 to 9999

# A function that prints
# given number in words

def _convert_to_words(num):
    
    try:
        while num[0] == "0":
            if len(num)>1:
                num = num[1:]
            else:
                num = ""
    except:
        num = ""

    # Get number of digits
    # in given number
    l = len(num)

    # Base cases
    if (l == 0):
        #print("empty string")
        return ""

    if (l > 4):
        #print("Length more than 4 is not supported")
        return ""

    # The first string is not used,
    # it is to make array indexing simple
    single_digits = ["Zero", "One", "Two", "Three",
					"Four", "Five", "Six", "Seven",
					"Eight", "Nine"]

    # The first string is not used,
    # it is to make array indexing simple
    two_digits = ["", "Ten", "Eleven", "Twelve",
				"Thirteen", "Fourteen", "Fifteen",
				"Sixteen", "Seventeen", "Eighteen",
				"Nineteen"]

    # The first two string are not used,
    # they are to make array indexing simple
    tens_multiple = ["", "", "Twenty", "Thirty", "Forty",
					"Fifty", "Sixty", "Seventy", "Eighty",
					"Ninety"]

    tens_power = ["Hundred", "Thousand"]

    # Used for debugging purpose only
    #print(num, ":", end=" ")
    #print num ,
    #print " " ,
    digitsInWords = ""
    # For single digit number
    if (l == 1):
        #print(single_digits[ord(num[0]) - 48])
        digitsInWords = single_digits[ord(num[0]) - 48]
        return digitsInWords

    # Iterate while num is not '\0'
    x = 0
    while (x < len(num)):

        # Code path for first 2 digits
        if (l >= 3):
            if (ord(num[x]) - 48 != 0):
                #print single_digits[ord(num[x]) - 48] ,
                digitsInWords +=  single_digits[ord(num[x]) - 48]
                #print tens_power[l - 3] ,
                digitsInWords +=  tens_power[l - 3] + " "
                #print "" , # here len can be 3 or 4
                l -= 1
            else:
                l -= 1

        # Code path for last 2 digits
        else:

            # Need to explicitly handle
            # 10-19. Sum of the two digits
            # is used as index of "two_digits"
            # array of strings
            if (ord(num[x]) - 48 == 1):
                sum = (ord(num[x]) - 48 +
					ord(num[x+1]) - 48)
                #print two_digits[sum],
                digitsInWords +=  two_digits[sum]
                return digitsInWords

            # Need to explicitely handle 20
            elif (ord(num[x]) - 48 == 2 and
                ord(num[x + 1]) - 48 == 0):
                #print tens_multiple[2],
                digitsInWords += tens_multiple[2] + " "
                return digitsInWords

            # Rest of the two digit
            # numbers i.e., 21 to 99
            else:
                i = ord(num[x]) - 48
                if(i > 0):
                    #print tens_multiple[i],
                    digitsInWords += tens_multiple[i]
                else:
                    #print "",
                    digitsInWords += " "
                x += 1
                #print(num,"index#",x)
                if(ord(num[x]) - 48 != 0):
                    #print single_digits[ord(num[x]) - 48]
                    digitsInWords += single_digits[ord(num[x]) - 48]
        x += 1
    return digitsInWords
def convert_to_words(num1):
    
    num = num1.split('.')[0]
    fractionPart = ""
    tenThousandPart = ""
    if num1.find('.')>-1:
        fractionPart = num1.split('.')[1]
        len_fractionPart = len(fractionPart)
        if len_fractionPart > 0:
            if len_fractionPart == 1:
                if fractionPart == "0":
                    fractionPart = ""
                else:
                    fractionPart = fractionPart + "0"
            elif len_fractionPart > 2:
                fractionPart = fractionPart[0:2]
            #elif len_fractionPart == 2:
            #    fractionPart = fractionPart
    
    # Get number of digits
    # in given number
    l = len(num)
    

    # Base cases
    if (l == 0):
        print("empty string")
        return "ERROR: Empty String"
    

    if (l > 5):
        print("Length more than 5 is not supported")
        return "ERROR: Length more than 5 is not supported"
    
    if (l == 5):
        tenThousandPart = num[0:2]
        num = num[2:5]
    
    digitsInWords = ""
    if len(tenThousandPart) > 0:
        digitsInWords = _convert_to_words(tenThousandPart) + "Thousands " + _convert_to_words(num) + " Rupees"
    else:
        digitsInWords = _convert_to_words(num) + " Rupees"
    if len(fractionPart)>0:
        digitsInWords += " and " + _convert_to_words(fractionPart) + " Paisa"
    return digitsInWords

if __name__ == "__main__":
    # Driver Code
    print(convert_to_words("30000")) # Four Digits
    print(convert_to_words("9523.98")) # Three Digits
    print(convert_to_words("892")) # Two Digits
    print(convert_to_words("8")) # One Digits
    print(convert_to_words("21")) # One Digits
    print(convert_to_words("39720")) # One Digits
    print(convert_to_words("1010")) # One Digits

# This code is contributed
# by Mithun Kumar
