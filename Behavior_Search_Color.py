from Behavior import Behavior
from Cam import Cam
from PIL import Image


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


class Search_Color(Behavior):
    def __init__(self, bbcon, sensobs):
        super().__init__(bbcon, sensobs)
        self.time = 0

    def consider_activation(self):
        if self.time == 0:
            self.time += 1
            return False
        elif self.time == 1:
            self.time = 0
            return True

    def consider_deactivation(self):
        return True

    def sense_and_act(self):
        image = self.sensobs.get_value()
        loaded = image.load()
        motor_recommendation = 'N'
        match_degree = 0.1
        halt_request = False
        sigma_x = 0
        n_points = 0
        width = self.sensobs.img_width
        height = self.sensobs.img_height
        for x in range(width):
            for y in range(height):
                r, g, b = loaded[x, y]
                # remove red from the pic
                if r < 100 and g > 120 and b < 100:
                    sigma_x += x
                    n_points += 1

        print(n_points)
        if n_points != 0:
            x = int(sigma_x/n_points)
            x = translate(x, 0, width, -100, 100)
            if x < -60:
                motor_recommendation = 'W'
            elif x < -30:
                motor_recommendation = 'NW'
            elif x > 60:
                motor_recommendation = 'NE'
            elif x > 30:
                motor_recommendation = 'E'
            match_degree = 1


        return motor_recommendation, match_degree, halt_request


if __name__ == "__main__":
    cam = Cam()
    # Temp:
    cam.update()
    behav = Search_Color("bbcon", cam)
    behav.sense_and_act()