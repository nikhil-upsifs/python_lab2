class student :
    #def __init__(self):
        #self.branch="Btech" .... No constructor overloading in python
    branch="Btech" # if common for all objects then we can use class variable
    def __init__(self,name,roll):
        self.name =name 
        self.roll=roll
S1=student("John",101)
S2=student("Jane",102)
S3=student("Doe",103)
print(S1.name,S1.roll,S1.branch)
print(S2.name,S2.roll,S2.branch)
print(S3.name,S3.roll,S3.branch)