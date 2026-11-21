str = input("Enter string :")
freq_count={}
def char_frequency(str):
    for i in str :
        if i in freq_count:
            freq_count[i]+=1
        else:
            freq_count[i]=1
    return freq_count
char_frequency(str)
print(freq_count)

