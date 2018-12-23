# !/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import tkinter.ttk
from threading import Thread
import time
from tkinter import *
from tkinter.font import Font
from tkinter.messagebox import *
from imp import reload

import run
from functions import load_config

config_path = "config.json"

reload(sys)


# sys.setdefaultencoding('utf-8')


class GUI(object):
    """GUI对象"""

    def __init__(self):
        self.mainwindow = Tk()
        # self.after = Tk()
        self.mainwindow.title('武汉大学图书馆预约抢座平台(Version 4.0)')
        self.mainwindow.resizable(True, True)
        # self.mainwindow.wm_attributes("-topmost", 1) # 置于顶层
        self.mainwindow.geometry('+450+250')
        self.sysfont = Font(self.mainwindow, size=11)

        RELIEF = ["flat", "raised", "sunken", "solid", "ridge", "groove"]

        # 学号，密码label
        self.label_username = Label(self.mainwindow, text='学号:', padx=8, pady=10)
        self.label_password = Label(self.mainwindow, text='密码:', padx=8)
        self.label_username.grid(row=0, column=0)
        self.label_password.grid(row=1, column=0)

        # 学号，密码entry
        self.entry_username = tkinter.ttk.Entry(self.mainwindow, font=self.sysfont, width=24)
        self.entry_password = tkinter.ttk.Entry(self.mainwindow, font=self.sysfont, width=24)
        self.entry_username.grid(row=0, column=1, columnspan=2, padx=2)
        self.entry_password.grid(row=1, column=1, columnspan=2, padx=2)

        # 从config.json中读取用户名和密码
        self.entry_username.insert(0, self.load_config_before()["username"])
        self.entry_password.insert(0, self.load_config_before()["password"])  # 隐藏密码
        self.entry_password.config(show='*')

        self.entry_username.config(validate='focusin',
                                   validatecommand=lambda: self.validate_func('self.entry_username'),
                                   invalidcommand=lambda: self.invalid_func('self.entry_username'))
        self.entry_password.config(validate='focusin',
                                   validatecommand=lambda: self.validate_func('self.entry_password'),
                                   invalidcommand=lambda: self.invalid_func('self.entry_password'))
        # 记住密码checkbutton
        self.checkbutton_remember_var = IntVar()
        self.checkbutton_remember = Checkbutton(self.mainwindow, text='记住密码', underline=0,
                                                variable=self.checkbutton_remember_var)
        self.checkbutton_remember.select()
        self.checkbutton_remember.grid(row=5, column=0)
        '''
        # 启用邮件通知checkbutton
        self.checkbutton_email_var = IntVar()
        self.checkbutton_email = Checkbutton(self.mainwindow, text='启用邮件通知', underline=0,
                                             variable=self.checkbutton_email_var)
        self.checkbutton_email.select()
        self.checkbutton_email.grid(row=5, column=1)
        '''
        # 登录按钮
        self.button_print = tkinter.ttk.Button(self.mainwindow, text='登录',
                                               command=lambda: self.thread_it(self.login))
        self.button_print.grid(row=5, column=1, pady=3)
        # self.button_print.config(command=self.process_func)

        # 确定按钮
        self.button_print = tkinter.ttk.Button(self.mainwindow, text='确定')
        self.button_print.grid(row=5, column=2, pady=3)
        self.button_print.config(command=self.process_func)

        # 日期下拉列表
        self.date = StringVar()
        self.combobox_date = tkinter.ttk.Combobox(self.mainwindow, width=40, textvariable=self.date, state='readonly')
        self.combobox_date['values'] = ("today", "tomorrow")  # 设置下拉列表的值
        self.combobox_date.grid(column=0, row=4, columnspan=3, pady=8, padx=3)  # 设置其在界面中出现的位置, column代表列, row 代表行
        self.combobox_date.current(0)  # 设置下拉列表默认显示的值, 0为numberChosen['values']的下标值

        # 起始时间下拉列表
        self.startTime = StringVar()
        self.combobox_startTime = tkinter.ttk.Combobox(self.mainwindow, width=10, textvariable=self.startTime,
                                                       state='readonly')
        self.combobox_startTime['values'] = (
            "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30",
            "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30",
            "20:00", "20:30", "21:00", "21:30", "22:00")  # 设置下拉列表的值
        self.combobox_startTime.grid(column=1, row=3, padx=10)  # 设置其在界面中出现的位置, column代表列, row 代表行
        self.combobox_startTime.current(0)  # 设置下拉列表默认显示的值, 0为numberChosen['values']的下标值

        # 终止时间下拉列表
        self.endTime = StringVar()
        self.combobox_endTime = tkinter.ttk.Combobox(self.mainwindow, width=10, textvariable=self.endTime,
                                                     state='readonly')
        self.combobox_endTime['values'] = (
            "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30",
            "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30",
            "20:00", "20:30", "21:00", "21:30", "22:00")  # 设置下拉列表的值
        self.combobox_endTime.grid(column=2, row=3)  # 设置其在界面中出现的位置, column代表列, row 代表行
        self.combobox_endTime.current(0)  # 设置下拉列表默认显示的值, 0为numberChosen['values']的下标值

        # 信息栏Text
        # self.info = ScrolledText(self.mainwindow, height=8, width=30, state="normal")
        # self.info.grid(column=4, row=0, rowspan=4, padx=3)
        # self.info.insert(END, "Runtime Info:\n\n")
        # self.info.focus()

        # 分馆下拉列表
        self.lib = StringVar()
        self.combobox_lib = tkinter.ttk.Combobox(self.mainwindow, width=10, textvariable=self.lib, state='readonly')
        self.combobox_lib['values'] = ("信息分馆", "工学分馆", "医学分馆", "总馆")  # 设置下拉列表的值
        self.combobox_lib.bind('<<ComboboxSelected>>', self.combobox_lib_selected)  # 绑定虚拟事件：cbb选值
        self.combobox_lib.grid(column=0, row=2, pady=8, padx=3)  # 设置其在界面中出现的位置, column代表列, row 代表行
        self.combobox_lib.current(0)  # 设置下拉列表默认显示的值, 0为numberChosen['values']的下标值

        # 楼层下拉列表
        self.floor = StringVar()
        self.combobox_floor = tkinter.ttk.Combobox(self.mainwindow, width=10, textvariable=self.floor, state='readonly')
        self.combobox_floor['values'] = ("一楼", "二楼", "三楼", "四楼")  # 设置下拉列表的值
        self.combobox_floor.bind('<<ComboboxSelected>>', self.combobox_floor_selected)  # 绑定虚拟事件：cbb选值
        self.combobox_floor.grid(column=1, row=2, pady=8, padx=3)  # 设置其在界面中出现的位置, column代表列, row 代表行
        self.combobox_floor.current(0)  # 设置下拉列表默认显示的值, 0为numberChosen['values']的下标值

        # 房间下拉列表
        self.room = StringVar()
        self.combobox_room = tkinter.ttk.Combobox(self.mainwindow, width=10, textvariable=self.room, state='readonly')
        # TODO: 用户可能使用缺省的分馆和楼层（没有combobox_floor_selected虚拟事件），缺省的房间必须对应缺省分馆和缺省楼层
        self.combobox_room['values'] = ("双屏电脑", "电子资源阅览区", "3C创客空间", "创新学习讨论区", "MAC电脑", "云桌面")  # 设置下拉列表的值
        self.combobox_room.bind('<<ComboboxSelected>>', self.combobox_room_selected)  # 绑定虚拟事件：cbb选值
        self.combobox_room.grid(column=2, row=2, pady=8, padx=3)  # 设置其在界面中出现的位置, column代表列, row 代表行
        self.combobox_room.current(5)  # 设置下拉列表默认显示的值, 0为numberChosen['values']的下标值

        # 座位下拉列表
        self.seat = StringVar()
        self.combobox_seat = tkinter.ttk.Combobox(self.mainwindow, width=10, textvariable=self.seat, state='readonly')
        # TODO: 用户可能使用缺省的分馆和楼层和房间（没有combobox_floor_selected虚拟事件），缺省的房间必须对应缺省分馆，缺省楼层和缺省房间
        self.combobox_seat['values'] = ["%03d" % i for i in range(1, 21)]  # 设置下拉列表的值
        self.combobox_seat.grid(column=0, row=3, pady=8, padx=3)  # 设置其在界面中出现的位置, column代表列, row 代表行

        # 显示控制台输出
        self.infoFrame = Frame(self.mainwindow, borderwidth=3)
        self.infoFrame.grid(row=6, column=0, rowspan=6, columnspan=5, padx=1)
        self.console = Text(self.infoFrame, width=50, height=13, )
        self.console.configure(highlightbackground="white",
                               highlightcolor="white")
        self.console.grid()
        self.console.insert(END, "欢迎！\n本工具用于武汉大学图书馆。\n")
        self.console.insert(END, "请勿恶意刷、抢、占座!\n\n")
        self.console.insert(END, "请先点击登录按钮后再选择座位!\n\n\n")
        self.console.insert(END, "Copyright © Reserve\nContact: billgoo0813@gmail.com\n")

        self.token
        self.session

        self.mainwindow.mainloop()

    @staticmethod
    def thread_it(func, *args):
        t = Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    def login(self):
        """
        登录并获取token
        :return:
        """
        self.console.delete("1.0", END)
        status = self.session.login(self.username.get(), self.password.get())
        if status == 0:
            self.console.insert(END, "登入成功！\n")
        elif status == 1:
            self.console.insert(END, "登入失败！\n用户不存在，检查学号。\n")
        elif status == 2:
            self.console.insert(END, "登入失败！\n密码错误，请重新输入。\n")
        else:
            self.console.insert(END, "登入失败！\n请检查网络环境！\n")

    def combobox_lib_selected(self, event):
        """选定combobox_lib时触发函数"""
        # TODO: 除信息分馆外，其他馆还没适配
        if self.lib.get() == "信息分馆":
            self.combobox_floor['values'] = ["一楼", "二楼", "三楼", "四楼"]
        elif self.lib.get() == "总馆":
            self.combobox_floor['values'] = ["一楼", "二楼", "三楼", "四楼", "五楼"]
        elif self.lib.get() == "工学分馆":
            self.combobox_floor['values'] = ["一楼", "二楼", "三楼", "四楼", "五楼"]
        elif self.lib.get() == "医学分馆":
            self.combobox_floor['values'] = ["一楼", "二楼", "三楼", "四楼", "五楼"]

    def combobox_floor_selected(self, event):
        """选定combobox_floor时触发函数"""
        if self.floor.get() == "一楼":
            self.combobox_room['values'] = ["3C创客空间", "创新学习讨论区", "双屏电脑", "MAC电脑", "云桌面"]
            self.combobox_room.current(0)
        if self.floor.get() == "二楼":
            self.combobox_room['values'] = ["二楼东", "二楼西"]
            self.combobox_room.current(0)
        if self.floor.get() == "三楼":
            self.combobox_room['values'] = ["三楼东", "三楼自主学习区", "三楼西"]
            self.combobox_room.current(0)
        if self.floor.get() == "四楼":
            self.combobox_room['values'] = ["四楼东", "四楼西"]
            self.combobox_room.current(0)

    def combobox_room_selected(self, event):
        """选定combobox_floor时触发函数"""
        if self.room.get() == "3C创客空间":
            self.combobox_seat['values'] = ["%03d" % i for i in range(1, 21)]
        if self.room.get() == "创新学习讨论区":
            self.combobox_seat['values'] = ["%03d" % i for i in range(1, 21)]
        if self.room.get() == "双屏电脑":
            self.combobox_seat['values'] = ["%03d" % i for i in range(1, 111)]
        if self.room.get() == "MAC电脑":
            self.combobox_seat['values'] = ["%03d" % i for i in range(1, 65)]
        if self.room.get() == "云桌面":
            self.combobox_seat['values'] = ["%03d" % i for i in range(1, 13)]
        if self.room.get() == "二楼东":
            self.combobox_seat['values'] = ["%03d" % i for i in range(1, 93)]
        if self.room.get() == "二楼西":
            self.combobox_seat['values'] = ["%03d" % i for i in range(1, 93)]
        if self.room.get() == "三楼东":
            self.combobox_seat['values'] = ["%03d" % i for i in range(1, 85)]
        if self.room.get() == "三楼自主学习区":
            self.combobox_seat['values'] = ["%03d" % i for i in range(1, 189)]
        if self.room.get() == "三楼西":
            self.combobox_seat['values'] = ["%03d" % i for i in range(1, 89)]
        if self.room.get() == "四楼东":
            self.combobox_seat['values'] = ["%03d" % i for i in range(1, 81)]
        if self.room.get() == "四楼西":
            self.combobox_seat['values'] = ["%03d" % i for i in range(1, 89)]

    def load_config_before(self):
        """从config.json中读取原来的配置"""
        return load_config(config_path)

    def validate_func(self, en):
        """验证输入"""
        return False if eval(en).get().strip() != '' else True

    def invalid_func(self, en):
        """没什么用"""
        value = eval(en).get().strip()
        if value == '输入学号' or value == '输入密码':
            eval(en).delete(0, END)
        if en == 'self.entry_password':
            eval(en).config(show='*')

    def process_func(self):
        """GUI部分的主函数，允许用户在窗口修改 config.json 的参数，并调用 run.py 执行选座"""
        # TODO: 改混乱的变量名
        value_username = self.entry_username.get().strip()
        value_password = self.entry_password.get().strip()
        value_date = self.combobox_date.get()  # get()方法是必需的
        value_startTime = int(self.startTime.get().split(":")[0]) * 60 + int(self.startTime.get().split(":")[1])
        value_endTime = int(self.endTime.get().split(":")[0]) * 60 + int(self.endTime.get().split(":")[1])
        value_allow_email = str(self.checkbutton_email_var.get())
        value_remember_pwd = str(self.checkbutton_remember_var.get())
        room_value = "14"
        if self.room.get() == "3C创客空间":
            room_value = "4"
        elif self.room.get() == "创新学习讨论区":
            room_value = "5"
        elif self.room.get() == "双屏电脑":
            room_value = "14"
        elif self.room.get() == "MAC电脑":
            room_value = "15"
        elif self.room.get() == "云桌面":
            room_value = "16"
        elif self.room.get() == "二楼西":
            room_value = "6"
        elif self.room.get() == "二楼东":
            room_value = "7"
        elif self.room.get() == "三楼西":
            room_value = "8"
        elif self.room.get() == "三楼东":
            room_value = "10"
        elif self.room.get() == "三楼自主学习区":
            room_value = "12"
        elif self.room.get() == "四楼西":
            room_value = "9"
        elif self.room.get() == "四楼东":
            room_value = "11"

        txt = '''
        学号:  %s 
        密码:  %s 
        ''' % (self.entry_username.get(), self.entry_password.get())
        if value_username == '' or value_username == '输入学号':
            showwarning('无学号', '请输入学号')
        elif value_password == '' or value_password == '输入密码':
            showwarning('无密码', '请输入密码')
        else:
            # 接收到学号和密码的情况
            # showinfo('学号密码', txt)
            # 打开文件取出数据并修改，然后存入变量
            with open(config_path, 'r') as f:
                config_before = json.load(f)
                config_before["username"] = value_username

                # 复选框选中则保存密码，否则清空
                if value_remember_pwd == "1":
                    config_before["password"] = value_password
                else:
                    config_before["password"] = ''

                # 日期选择为today时禁用预约模式，为tomorrow时启用预约模式，而是否进入suspending则由 functions.py 中的schedule_run判断
                if value_date == "today":
                    config_before["schedule_flag"] = "0"
                elif value_date == "tomorrow":
                    config_before["schedule_flag"] = "1"

                # 保存在GUI中设置的日期，起止时间，是否启用邮件提醒
                config_before["date_flag"] = value_date
                config_before["startTime"] = str(value_startTime)
                config_before["endTime"] = str(value_endTime)
                config_before["send_mail_flag"] = value_allow_email
                config_before["room"] = room_value
                config_after = config_before

            # 打开文件并覆盖写入修改后内容
            with open(config_path, 'w') as f:
                json.dump(config_after, f)

            # TODO: 写入info框
            # self.info.focus()
            # self.info.insert(END, "------用户设置已保存------\n")
            # self.info.insert(END, "------开始运行主程序------\n\n")
            self.mainwindow.iconify()  # 把主窗口藏起来，先不destroy()，因为后面还要showinfo()
            # self.mainwindow.withdraw()
            # 调用 run.py 执行选座流程！
            # time.sleep(10)
            userinfo, status, response = run.run(config_after)
            # self.info.insert(END, json.dumps(info).decode('unicode-escape'))
            # self.info.insert(END, "\n")
            # self.info.insert(END, "\n")
            # self.info.see(END)
            # self.info.insert(END, json.dumps(response).decode('unicode-escape'))
            # self.info.insert(END, "\n")
            # self.info.see(END)
            info = str(userinfo) + '\n\n' + str(status) + '\n\n' + str(response)
            showinfo('座位预约结果', info)
            # TODO: 以合适的方式结束对话框
            # TODO: showinfo
            self.mainwindow.destroy()


if __name__ == "__main__":
    GUI()
