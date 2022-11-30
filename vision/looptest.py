while True:
    arr = [1,2]
    try:
        arr[100]
    except Exception as e:
        print('try again')