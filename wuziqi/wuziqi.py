#导入所需的模块
import random
import threading
import time
import sys
import pygame
from  button import Button
from  word import Word
from socket import  *
import inspect
import ctypes
tcp_socket = socket(AF_INET, SOCK_STREAM)
# 2.准备连接服务器，建立连接
serve_ip = "192.168.43.171"
tuichu = 1
serve_port = 8000
tcp_socket = socket(AF_INET, SOCK_STREAM)
# 2.准备连接服务器，建立连接
serve_ip = "192.168.43.171"
tuichu = 1
serve_port = 8000
qianzui="010414"

def _async_raise( tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)

    if not inspect.isclass(exctype):
        exctype = type(exctype)
    # print("womeiyong")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    print("womeiyong")

    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread (thread):
   _async_raise(thread.ident, SystemExit)

class chessboard:
    def __init__(self):
        self.win=False
        self.czf=0
        self.zhishi=0
        self.suo=0
        self.cike='black'
        pygame.init()
        self.stats=False
        self.diyici=1
        self.screen = pygame.display.set_mode((900,800))
        self.play_button=Button(self,'重开',450,20)
        self.start_button=Button(self,'开始',350,20)
        self.tc_button=Button(self,'退出',550,20)
        self.ok_button=Button(self,'同意',370,350)
        self.no_button=Button(self,'拒绝',470,350)
        self.kaishi_text=Word(self,70,30)

        pygame.display.set_caption('五子棋')
        self.screen.fill('white')

        self.grid_count=20
        pygame.draw.rect(self.screen, (185, 122, 87),[125,75,650,650])
        for i in range(21):
         pygame.draw.line(self.screen,(0.0,0,0),(150+(i)*30,100),(150+(i)*30,700))
         pygame.draw.line(self.screen,(0.0,0,0),(150,100+(i)*30),(750,100+(i)*30))
        self.grid = []
        for i in range(self.grid_count+1):
            self.grid.append(list("." * (self.grid_count+1)))

        self.play_button.draw_button()

        self.start_button.draw_button()

        self.tc_button.draw_button()
        self.kaishi_text.draw_text("点击开始连接服务端")
        self.number = random.randint(1,2)
        tcp_socket.connect((serve_ip, serve_port))
        tcp_socket.send("okok".encode())
        self.t = threading.Thread(target=self.run, args=())
        self.t.daemon = True
        self.t.start()


    def faxiaoxi(self,senddata):

            tcp_socket.send(senddata.encode())

    def shouxiaoxi(self):
        while (True):
            recv_data = tcp_socket.recv(4096)
            msg=recv_data.decode()
            print(msg)
            if msg=="return"  :
                if self.zhishi==0:
                    self.stats=False
                    self.kaishi_text.draw_text("                  ")
                    self.kaishi_text.draw_text("对方申请重开")
                    self.start_button.updatetext("同意")
                    self.play_button.updatetext("拒绝")
                    self.czf=1
                elif self.zhishi==1:
                    self.stats=False
                    self.kaishi_text.draw_text("                  ")
                    self.kaishi_text.draw_text("等待对方同意重开")

            if msg=="dfexit" and self.stats:
                self.kaishi_text.draw_text("                  ")
                self.kaishi_text.draw_text("对方已退出")
                time.sleep(2)
                self.congzhi()
                self.stats=False
                self.kaishi_text.draw_text("点击开始连接服务端")
            if msg=="jjl" :
                if self.czf==1:
                 self.kaishi_text.draw_text("                  ")
                 self.kaishi_text.draw_text("你拒绝了重开申请")
                if self.czf == 0:
                    self.kaishi_text.draw_text("                  ")
                    self.kaishi_text.draw_text("对方拒绝了重开申请")

                self.zhishi=0
                self.czf=0
                self.play_button.updatetext("重开")
                print("whywhy=================")
                if not self.win:
                 self.start_button.updatetext("开始")
                self.tc_button.updatetext("退出")
                if not self.win:
                 self.stats=True
                if self.win:
                  self.start_button.draw_kong()
                time.sleep(1)
                if self.suo == 1 and not self.win:


                    self.kaishi_text.draw_text("                  ")
                    self.kaishi_text.draw_text("我方回合")
                elif self.suo == 0 and not self.win:

                    self.kaishi_text.draw_text("                  ")
                    self.kaishi_text.draw_text("对方回合")
            if msg=="tyl" :
                self.zhishi=0
                self.czf=0
                print("whywhy=================")
                self.play_button.updatetext("重开")
                self.start_button.updatetext("开始")
                self.tc_button.updatetext("退出")
                self.congzhi()
                tcp_socket.send("wait".encode())
            if msg=="wait" and self.stats:
             self.kaishi_text.draw_text("                  ")
             self.kaishi_text.draw_text("等待对方连接")
            elif msg=="wait" and not self.stats:
             self.kaishi_text.draw_text("                  ")
             self.kaishi_text.draw_text("对方已准备好")
            elif msg=="1":
                self.kaishi_text.draw_text("                  ")
                self.kaishi_text.draw_text("我是先手黑子")
                self.suo=1
            elif msg=="0":
                self.kaishi_text.draw_text("                  ")
                self.kaishi_text.draw_text("我是后手白子")
                self.suo=0
            elif msg[0:6]=="010414":
                uy=[]
                x=msg[6:12].strip()
                y=msg[12:18].strip()
                print(x)
                print(y)
                uy.append(int(x))
                uy.append(int(y))
                if self.suo==0:
                    self.kaishi_text.draw_text("                  ")
                    self.kaishi_text.draw_text("我方回合")
                    self.suo=1
                    print("jiechu")
                elif self.suo==1:
                    self.kaishi_text.draw_text("                  ")
                    self.kaishi_text.draw_text("对方回合")
                    self.suo=0
                self.placechess(uy)


    def run(self):

              self.shouxiaoxi()


    def check_button(self,mouse_pos):
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        button_clicked1=self.start_button.rect.collidepoint(mouse_pos)
        button_clicked2=self.tc_button.rect.collidepoint(mouse_pos)
        if button_clicked and (self.stats or self.win) and self.zhishi==0 and self.czf==0: #重开按钮
            # tcp_socket.send("return".encode())
            self.stats=False
            self.zhishi=1
            self.start_button.draw_kong()
            self.tc_button.draw_kong()
            self.play_button.draw_kong()
            tcp_socket.send("return".encode())
            # self.congzhi()
        if button_clicked2  and self.zhishi==0 and self.czf==0: #退出按钮
            tcp_socket.send("exit".encode())
            pygame.quit()

            sys.exit()

        if button_clicked1 and not self.stats and self.zhishi==0 and self.czf==0 and not self.win: #开始按钮

            self.kaishi_text.draw_text("                      ")
            self.start()
            tcp_socket.send("wait".encode())
        if button_clicked1  and self.czf==1: #开始按钮
            tcp_socket.send("tyl".encode())
            print("=====okok======")
        if button_clicked and self.czf==1: #开始按钮
            tcp_socket.send("jjl".encode())
            print("=====okok======")

    def start(self):

        self.stats=True

    def congzhi(self):
        self.suo=0
        self.stats=True
        for i in range(self.grid_count):
            for ix in range(self.grid_count):
                self.grid[i][ix]='.'
        pygame.draw.rect(self.screen,(185, 122, 87),[125,75,650,650])
        for i in range(21):
            pygame.draw.line(self.screen,(0.0,0,0),(150+(i)*30,100),(150+(i)*30,700))
            pygame.draw.line(self.screen,(0.0,0,0),(150,100+(i)*30),(750,100+(i)*30))


    def xrun(self):

        while True:

            for event in pygame.event.get():
                button_clicked = self.play_button.rect.collidepoint(pygame.mouse.get_pos())
                button_clicked1 = self.start_button.rect.collidepoint(pygame.mouse.get_pos())
                button_clicked2 = self.tc_button.rect.collidepoint(pygame.mouse.get_pos())
                if event.type == pygame.QUIT:
                    # stop_thread(self.t)
                    tcp_socket.send("exit".encode())
                    pygame.quit()
                    print("kasi")
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    e = pygame.mouse.get_pos()
                    self.check_button(e)
                    if e[0]<135 or e[0]>765 or e[1]>715 or e[1]<90:
                        continue
                    else:
                     x=round((e[0]-150)/30)
                     y=round((e[1]-100)/30)
                     if x<0:
                       x=0
                     if y<0:
                       y=0
                     if self.suo == 1 and self.stats and not button_clicked1 and not button_clicked and not button_clicked2 and self.grid[x][y]==".":
                      a=str(e[0])
                      b=str(e[1])
                      hg=a.ljust(6)
                      gh=b.ljust(6)
                      daan=qianzui+hg+gh
                      print(daan)
                      tcp_socket.send(daan.encode())

                     print("jhd")
            pygame.display.flip()





    def placechess(self,e):
        if e[0]<135 or e[0]>765 or e[1]>715 or e[1]<90:

            return  0
        else:
            x=round((e[0]-150)/30)
            y=round((e[1]-100)/30)
            if x<0:
                x=0
            if y<0:
                y=0


            print(self.grid[x][y])

            if self.grid[x][y]=="." and self.cike =='white' and self.stats:
             pygame.draw.circle(self.screen,(255,255,255),(150+x*30,100+y*30),15)
             self.grid[x][y]='white'
             if(self.check_win(x,y,self.cike)):
                 self.kaishi_text.draw_text("白子获胜")
                 self.stats=False
                 self.win=True
                 self.start_button.draw_kong()

             self.cike='black'

            if self.grid[x][y]=="." and self.cike =='black' and self.stats:
                pygame.draw.circle(self.screen,(0,0,0),(150+x*30,100+y*30),15)
                self.grid[x][y]='black'
                if(self.check_win(x,y,self.cike)):
                    self.kaishi_text.draw_text("黑子获胜")
                    self.stats=False
                    self.win=True
                    self.start_button.draw_kong()
                    print('congzhi')


                self.cike='white'
                print("fangshengle")

    def countchess(self,x,y,rightpian,uppian,color):
        sum=0
        nowx=x+rightpian
        nowy=y+uppian
        while True:
            if(nowx<0 or nowy<0 or nowx>=self.grid_count+1 or nowy>=self.grid_count+1):
                return sum
            if(self.grid[nowx][nowy]!=color):
                break
            nowx=nowx+rightpian
            nowy=nowy+uppian
            sum=sum+1
        return sum

    def check_win(self,x,y,color):
        nowr=self.countchess(x,y,1,0,color)  #右边棋子数目
        nowl=self.countchess(x,y,-1,0,color)  #左边棋子数目
        nowu=self.countchess(x,y,0,1,color)  #上边棋子数目
        nowd=self.countchess(x,y,0,-1,color)  #下边棋子数目
        nowru=self.countchess(x,y,1,1,color)  #右上边棋子数目
        nowlu=self.countchess(x,y,-1,1,color)  #左上棋子数目
        nowld=self.countchess(x,y,-1,-1,color)  #左下棋子数目
        nowrd=self.countchess(x,y,1,-1,color)  #右下棋子数目
        print('('+str(x)+','+str(y)+')'+ color+'横有'+str(nowr+nowl+1))
        print('('+str(x)+','+str(y)+')'+ color+'竖有'+str(nowu+nowd+1))
        print('('+str(x)+','+str(y)+')'+ color+'右斜有'+str(nowru+nowld+1))
        print('('+str(x)+','+str(y)+')'+ color+'左斜有'+str(nowrd+nowlu+1))
        if nowr+nowl+1>=5 or nowu+nowd+1>=5 or nowru+nowld+1>=5 or nowrd+nowlu+1>=5:
            return True
        else:
            return False



if __name__=="__main__":
    game=chessboard()
    game.xrun()
