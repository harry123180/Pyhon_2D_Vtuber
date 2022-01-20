class object:
    # 建構式
    def __init__(self, image):
        self.image = image  # 顏色屬性
        self.x,self.y,self.a = image.shape
        self.half_x,self.half_y = int(self.x/2),int(self.y/2)
        self.px_array = [[],[]]
        for i in range(self.x):
            for j in range(self.y):
                if (self.image[i][j][0] == 255 and self.image[i][j][1] == 255 and self.image[i][j][2] == 255):
                    # 都是背景 沿用
                    pass
                elif (self.image[i][j][0] == 0 and self.image[i][j][1] == 0 and self.image[i][j][2] == 0):
                    pass
                else:
                    self.px_array[0].append(i)
                    self.px_array[1].append(j)
        self.indx_len = len(self.px_array[0])

class background:
    def __init__(self,back):
        self.back = back
def putOBJ(background,logo_obj,tar_x,tar_y):
    print(background.shape,logo_obj.indx_len)
    for i in range(logo_obj.indx_len):
            #print([i+tar_y-logo_obj.half_y],[j+tar_x-logo_obj.half_x])
            background[logo_obj.px_array[0][i]+tar_y-logo_obj.half_y][logo_obj.px_array[1][i]+tar_x-logo_obj.half_x] =\
                logo_obj.image[logo_obj.px_array[0][i]][logo_obj.px_array[1][i]]
    return background
def d(p1,p2):
    a= pow(p2[0]-p1[0],2)
    b = pow(p2[1]-p1[1],2)
    return pow(a+b,0.5)