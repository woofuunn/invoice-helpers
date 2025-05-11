soure1 = 61 #int
soure2 = 59.5   #float
good = 'pass'   #str
bad = 'fail'    #str

def is_pass(soure):
    result = good if soure >= 60 else bad
    result_bool = soure >= 60
    print(result, result_bool)


is_pass(soure1)
is_pass(soure2)


