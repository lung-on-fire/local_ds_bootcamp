def data_types():
    var0 = 123
    var1 = "string"
    var2 = 123.123
    var3 = True
    var4 = ["table", "face", "octopus"]
    var5 = {
        "city":"Moscow",
        "street":"Semashko",
        "house": "156"
    }
    var6 = ("table", "face", "octopus" , "face")
    var7 = {"table", "face", "octopus"}
    variables = [var0, var1, var2 , var3, var4, var5, var6, var7]


    print([type(var).__name__  for var in variables])

if __name__ == '__main__':
    data_types()
