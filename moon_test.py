import moon
def test_Waitingtime():
    if moon.Waitingtime(1738000,0,1738000,0,0,1000,45) == 0:
        print('test_Waitingtime is OK')
    else:
        print('test_Waitingtime is Fail')

def test_output():
    if moon.output(0,0,0,0,0,0,0,45) == [0,0,0,0,0,0]:
        print('test_output is OK')
    else:
        print('test_output is Fail')

def test_coordinates():
    if moon.coordinates(0,0,0,0,0,0,0,45,90) == [0,0,385000000,0,0,0]:
        print('test_coordinates is OK')
    else:
        print('test_coordinates is Fail')

test_Waitingtime()
test_output()
test_coordinates()