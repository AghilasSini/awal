""" This is the main script  """


#
#Pylint Tutorial
#

class Car:
    """ tutorial to learn how to us PyLint   """
    color = ''
    def __init__(self, color):
        self.color = color
    def __string__(self):
        print(self.color)
    def get_color(self):
        """ Getter """
        return self.color
    def set_color(self, color):
        """ Setter  """
        self.color = color




def crach(car1, car2):
    """  Craching function is used to processing Car Object  """
    car1.color = car2.color

def main():
    """ main function  """
    my_car = Car('blue')
    crach(Car('red'), my_car)
    print('my new car color {}'.format(my_car.get_color()))

if __name__ == '__main__':
    main()
