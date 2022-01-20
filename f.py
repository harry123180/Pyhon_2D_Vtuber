class object:
    # 建構式
    def __init__(self, image):
        self.image = image  # 顏色屬性
        self.x,self.y,self.a = image.shape
class background:
    def __init__(self,back):
        self.back = back
def putOBJ(image,logo,x,y):
    logo_x,logo_y,logo_a = logo.shape
    for i in range(logo_x):
        for j in range(logo_y):
            if (logo[i][j][0] == 255 and logo[i][j][1] == 255 and logo[i][j][2] == 255):
                # 都是背景 沿用
                pass
            elif (logo[i][j][0] == 0 and logo[i][j][1] == 0 and logo[i][j][2] == 0):
                pass
            else:
                image[i+y-int(logo_y/2)][j+x-int(logo_x/2)] = logo[i][j]
    return image