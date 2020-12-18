import machine
import time
import esp32
# ssd1306 library from
# https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py
# file dated 2020-03-29
import ssd1306
import uos
import utime

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
oled = ssd1306.SSD1306_I2C(128,64, i2c)
oled.fill(0)
oled.show()

class Life:
    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols
        self.iterations=0
        #init blank array
        start=utime.ticks_ms()
        self.arr1=[[0 for i in range(cols)] for j in range(rows)]
        self.arr2=[[0 for i in range(cols)] for j in range(rows)]
        end=utime.ticks_ms()
        print("time to init blank array:\t" + str(end-start) + " ms")
        #init random
        start=utime.ticks_ms()
        for i in range(self.rows):
            for j in range(self.cols):
                tmp=int.from_bytes(uos.urandom(1),'little')
                #192/256 chance of being 0
                if tmp < 192:
                    self.arr1[i][j]=0
                else:
                    self.arr1[i][j]=1
        end=utime.ticks_ms()
        print("time to init random array:\t" + str(end-start) + " ms")

    def printarr2(self):
        #print arr2 to console
        start=utime.ticks_ms()
        print("arr2")
        for i in range(self.rows):
            for j in range(self.cols):
                if self.arr2[i][j]==0:
                    print('.',end='')
                else:
                    print('#',end='')
            print()
        end=utime.ticks_ms()
        print("time to print to console:\t" + str(end-start) + " ms")

    def process_next(self):
        #9 sections, 3x3 split from 2d array, n=neighbors, avoids cpu time on bounds check this way
        self.iterations+=1
        print("iteration:\t" + str(self.iterations))
        start=utime.ticks_ms()
        n=0
        n=(self.arr1[0][1]+self.arr1[1][0]+self.arr1[1][1])
        if (self.arr1[0][0])==1 and (n < 2) or (n > 3):
            self.arr2[0][0]=0
        if (self.arr1[0][0]==0) and (n==3):
            self.arr2[0][0]=1

        for j in range(1, self.cols-1):
            n=(self.arr1[0][j-1]+self.arr1[0][j+1]+self.arr1[1][j-1]+self.arr1[1][j]+self.arr1[1][j+1])
            if (self.arr1[0][j])==1 and (n < 2) or (n > 3):
                self.arr2[0][j]=0
            if (self.arr1[0][j]==0) and (n==3):
                self.arr2[0][j]=1    

        n=(self.arr1[0][self.cols-2]+self.arr1[1][self.cols-2]+self.arr1[1][self.cols-1])
        if (self.arr1[0][self.cols-1])==1 and (n < 2) or (n > 3):
            self.arr2[0][self.cols-1]=0
        if (self.arr1[0][self.cols-1]==0) and (n==3):
            self.arr2[0][self.cols-1]=1

        for i in range(1, self.rows-1):
            n=(self.arr1[i-1][0]+self.arr1[i-1][1]+self.arr1[i][1]+self.arr1[i+1][1]+self.arr1[i+1][0])
            if (self.arr1[i][0])==1 and (n < 2) or (n > 3):
                self.arr2[i][0]=0
            if (self.arr1[i][0]==0) and (n==3):
                self.arr2[i][0]=1

        for i in range(1, self.rows-1):
            for j in range(1, self.cols-1):
                n=(self.arr1[i-1][j-1]+self.arr1[i-1][j]+self.arr1[i-1][j+1]+self.arr1[i][j-1]+self.arr1[i][j+1]+self.arr1[i+1][j-1]+self.arr1[i+1][j]+self.arr1[i+1][j+1])
                if (self.arr1[i][j])==1 and (n < 2) or (n > 3):
                    self.arr2[i][j]=0
                if (self.arr1[i][j]==0) and (n==3):
                    self.arr2[i][j]=1

        for i in range(1, self.rows-1):
            n=(self.arr1[i-1][self.cols-2]+self.arr1[i-1][self.cols-1]+self.arr1[i][self.cols-2]+self.arr1[i+1][self.cols-2]+self.arr1[i+1][self.cols-1])
            if (self.arr1[i][self.cols-1])==1 and (n < 2) or (n > 3):
                self.arr2[i][self.cols-1]=0
            if (self.arr1[i][self.cols-1]==0) and (n==3):
                self.arr2[i][self.cols-1]=0

        n=(self.arr1[self.rows-2][0]+self.arr1[self.rows-2][1]+self.arr1[self.rows-1][1])
        if (self.arr1[self.rows-1][0])==1 and (n < 2) or (n > 3):
            self.arr2[self.rows-1][0]=0
        if (self.arr1[self.rows-1][0]==0) and (n==3):
            self.arr2[self.rows-1][0]=1

        for j in range(1, self.cols-1):
            n=0
            n=(self.arr1[self.rows-2][j-1]+self.arr1[self.rows-2][j]+self.arr1[1][j-2]+self.arr1[self.rows-1][j-1]+self.arr1[self.rows-1][j+1])
            if (self.arr1[self.rows-1][j])==1 and (n < 2) or (n > 3):
                self.arr2[self.rows-1][j]=0
            if (self.arr1[self.rows-1][j]==0) and (n==3):
                self.arr2[self.rows-1][j]=1

        n=(self.arr1[self.rows-2][self.cols-2]+self.arr1[self.rows-1][self.cols-1]+self.arr1[self.rows-1][self.cols-2])
        if (self.arr1[self.rows-1][self.cols-1])==1 and (n < 2) or (n > 3):
            self.arr2[self.rows-1][self.cols-1]=0
        if (self.arr1[self.rows-1][self.cols-1]==0) and (n==3):
            self.arr2[self.rows-1][self.cols-1]=1
        end=utime.ticks_ms()
        print("time to process next iteration:\t" + str(end-start) + " ms")    
        #end of neighbor processing step

    def copy(self):
        #copy back to arr1 and to oled buffer
        start=utime.ticks_ms()
        for i in range(self.rows):
            for j in range(self.cols):
                self.arr1[i][j]=self.arr2[i][j]
                oled.pixel(j,i,self.arr1[i][j])

        end=utime.ticks_ms()
        print("time to copy back and to oled buffer:\t" + str(end-start) + " ms")

#"main" function
life=Life(64,128)
while True:    
    life.process_next()
    #life.printarr2()
    life.copy()
    oled.show()

