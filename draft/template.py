from tkinter import *  # 导入tkinter包用于GUI设计
from tkinter import ttk # 导入ttk包使用其中的树形展示图
import tkinter.messagebox  # 导入tkinter中的消息框库
import pymysql  # 导入pymysql库用于连接MySQL数据库
import time
import ttkbootstrap
import sys
path = "/Users/liushiwen/Desktop/大四上/"
sys.path.append(f'{path}')
from casper_config import get_db_config

# 登录验证函数
def login_test():
    # 根据输入确定用于查询的SQL语句
    identity_recognize_sql = " SELECT * FROM identity WHERE sno='%s' AND pass_word='%s'" % (User_Name_Entry.get(), Password_Entry.get())
    DataBase_Cursor.execute(identity_recognize_sql)  # 通过游标执行SQL语句
    # 如果有返回结果，说明身份信息库中存在这样的一条记录与用户输入匹配
    if DataBase_Cursor.fetchone() is not None:
        tkinter.messagebox.showinfo("提示信息", "登陆成功！")  # 向用户输出提示信息，表示登录成功
        browsing_window()  # 进入会议室预定系统主界面
        Login_Window.withdraw()
    else:
        tkinter.messagebox.showinfo("提示信息", "登录失败！请检查工号和密码")  # 登录失败，通过消息盒向用户输出提示信息
    # 清空工号和密码的输入
    User_Name_Entry.delete(0, END)
    Password_Entry.delete(0, END)


# 系统主窗口函数
def browsing_window():
    main_browsing_view = tkinter.Toplevel(Login_Window)  # 将主窗口设置为登录窗口的子窗口
    main_browsing_view.title("会议室预定系统")  # 给主窗口命名
    main_browsing_view.geometry("800x600")  # 设置主窗口的大小

    main_browsing_introduction_label = Label(main_browsing_view, bg="light blue",text="欢迎进行会议室预定", font=("华文行楷", 30), relief=RAISED,
                                             fg="red")
    main_browsing_introduction_label.place(relx=0.28, rely=0.01)

    search_by_roomnumber_label = Label(main_browsing_view, bg="light blue", font=("楷书", 18), relief=RAISED,text="请输入需要查找的会议室编号", fg="red")
    search_by_roomnumber_label.place(relx=0.1, rely=0.12)

    search_by_roomnumber_entry = Entry(main_browsing_view, bg="white", font=("宋体", 18), relief=RAISED)
    search_by_roomnumber_entry.place(relx=0.55, rely=0.12)

    search_by_roomnumber_button = Button(main_browsing_view,command=lambda: Search_By_roomNumber(search_by_roomnumber_entry.get(),search_by_date_entry1.get(),search_by_time_lowerentry1.get(),search_by_time_upperentry1.get(),main_browsing_view), bg="light blue",fg="red", font=("华文行楷", 16),text="点击查询")
    search_by_roomnumber_button.place(relx=0.45, rely=0.3)

    search_by_date_label1 = Label(main_browsing_view, bg="light blue", font=("楷书", 18), relief=RAISED,
                                  text="会议日期(格式为xxxx-xx-xx)", fg="red")
    search_by_date_label1.place(relx=0.1, rely=0.17)

    search_by_date_entry1 = Entry(main_browsing_view, bg="white", font=("楷书", 18), relief=RAISED, width=20)
    search_by_date_entry1.place(relx=0.55, rely=0.17)
    date = search_by_date_entry1.get()

    search_by_time_label1 = Label(main_browsing_view, bg="light blue", font=("楷书", 18), relief=RAISED, text="时间段（整点计）",
                                  fg="red",width=26)
    search_by_time_label1.place(relx=0.1, rely=0.23)

    search_by_time_lowerentry1 = Entry(main_browsing_view, bg="white", font=("宋体", 18), relief=RAISED, width=9)
    search_by_time_lowerentry1.place(relx=0.55, rely=0.23)
    lowertime = search_by_time_lowerentry1.get()

    search_by_time_upperentry1 = Entry(main_browsing_view, bg="white", font=("宋体", 18), relief=RAISED, width=9)
    search_by_time_upperentry1.place(relx=0.72, rely=0.23)
    uppertime = search_by_time_upperentry1.get()

    search_by_cost_label = Label(main_browsing_view, bg="light blue", font=("楷书", 18), relief=RAISED, text="价格区间", fg="red")
    search_by_cost_label.place(relx=0.1, rely=0.4)

    search_by_cost_lowerentry = Entry(main_browsing_view, bg="white", font=("宋体", 18), relief=RAISED, width=8)
    search_by_cost_lowerentry.place(relx=0.24, rely=0.4)

    search_by_cost_upperentry = Entry(main_browsing_view, bg="white", font=("宋体", 18), relief=RAISED, width=8)
    search_by_cost_upperentry.place(relx=0.37, rely=0.4)

    search_by_capacity_label = Label(main_browsing_view, bg="light blue", font=("楷书", 18), relief=RAISED, text="会议人数",
                                     fg="red")
    search_by_capacity_label.place(relx=0.1, rely=0.47)

    search_by_capacity_entry = Entry(main_browsing_view, bg="white", font=("楷书", 18), relief=RAISED, width=17)
    search_by_capacity_entry.place(relx=0.24, rely=0.47)
    capacity = search_by_capacity_entry.get()

    search_by_date_label2 = Label(main_browsing_view, bg="light blue", font=("楷书", 18), relief=RAISED,
                                  text="会议日期(格式为xxxx-xx-xx)", fg="red")
    search_by_date_label2.place(relx=0.1, rely=0.53)

    search_by_date_entry2 = Entry(main_browsing_view, bg="white", font=("楷书", 18), relief=RAISED, width=20)
    search_by_date_entry2.place(relx=0.55, rely=0.53)
    date = search_by_date_entry2.get()

    search_by_time_label2 = Label(main_browsing_view, bg="light blue", font=("楷书", 18), relief=RAISED, text="时间段（整点计）",
                                  fg="red", width=26)
    search_by_time_label2.place(relx=0.1, rely=0.59)

    search_by_time_lowerentry2 = Entry(main_browsing_view, bg="white", font=("宋体", 18), relief=RAISED, width=9)
    search_by_time_lowerentry2.place(relx=0.55, rely=0.59)
    lowertime = search_by_time_lowerentry2.get()

    search_by_time_upperentry2 = Entry(main_browsing_view, bg="white", font=("宋体", 18), relief=RAISED, width=9)
    search_by_time_upperentry2.place(relx=0.72, rely=0.59)
    uppertime = search_by_time_upperentry2.get()


    search_by_position_label = Label(main_browsing_view, bg="light blue", font=("楷书", 18), relief=RAISED, text="会议室位置",
                                     fg="red")
    search_by_position_label.place(relx=0.52, rely=0.4)

    position_var = IntVar(value=-1)
    position1 = Radiobutton(main_browsing_view, text="东面", variable=position_var, value=1)
    position2 = Radiobutton(main_browsing_view, text="西面", variable=position_var, value=2)
    position3 = Radiobutton(main_browsing_view, text="南面", variable=position_var, value=3)
    position4 = Radiobutton(main_browsing_view, text="北面", variable=position_var, value=4)
    position1.place(relx=0.7, rely=0.4)
    position2.place(relx=0.8, rely=0.4)
    position3.place(relx=0.7, rely=0.45)
    position4.place(relx=0.8, rely=0.45)


    Admin_Entry_Button = Button(main_browsing_view, command=lambda: Admin_Judge(main_browsing_view), bg="yellow",
                                font=("华文行楷", 20), fg="red", text="上传损坏设备")
    Admin_Entry_Button.place(relx=0.1, rely=0.8)

    Search_By_Equipment_Label=Label(main_browsing_view,bg="light blue",fg="red",text="会议室设备:",relief=RAISED,font=("楷书",18))
    Search_By_Equipment_Label.place(relx=0.1,rely=0.66)

    Equip=StringVar(value="无")
    Equip1=Radiobutton(main_browsing_view,text="电脑",variable=Equip,value="电脑")
    Equip2 = Radiobutton(main_browsing_view, text="音响", variable=Equip, value="音响")
    Equip3 = Radiobutton(main_browsing_view, text="投影仪", variable=Equip, value="投影仪")
    Equip4 = Radiobutton(main_browsing_view, text="话筒", variable=Equip, value="话筒")
    Equip5 = Radiobutton(main_browsing_view, text="摄像机", variable=Equip, value="摄像机")
    Equip6 = Radiobutton(main_browsing_view, text="讲台", variable=Equip, value="讲台")
    Equip1.place(relx=0.33,rely=0.67)
    Equip2.place(relx=0.43, rely=0.67)
    Equip3.place(relx=0.53, rely=0.67)
    Equip4.place(relx=0.63, rely=0.67)
    Equip5.place(relx=0.73, rely=0.67)
    Equip6.place(relx=0.83, rely=0.67)


    Search_By_Multiple_Button = Button(main_browsing_view,
                                       command=lambda: Search_By_Multiple(main_browsing_view,
                                                                          search_by_cost_lowerentry.get(),
                                                                          search_by_cost_upperentry.get(),
                                                                          position_var.get(),
                                                                          search_by_capacity_entry.get(),
                                                                          search_by_date_entry2.get(),
                                                                          search_by_time_lowerentry2.get(),
                                                                          search_by_time_upperentry2.get(),
                                                                          Equip.get()),
                                       bg="light blue",
                                       fg="red", font=("华文行楷", 16), text="点击查询")
    Search_By_Multiple_Button.place(relx=0.45, rely=0.77)

    My_Information_Button = Button(main_browsing_view, command=lambda: Enter_My_Panel(main_browsing_view), bg="yellow",
                                   font=("华文行楷", 20), fg="red", text="我的主页")
    My_Information_Button.place(relx=0.74, rely=0.8)


    main_browsing_view.mainloop()


def Search_By_roomNumber(Room_Number, DateString,Start,End,Window):
    Start_DateTime=time.strftime(DateString+" "+str(Start)+":00:00")
    End_DateTime=time.strftime(DateString+" "+str(End)+"00:00")
    Search_By_roomNumber_SQL = "SELECT * FROM ROOM WHERE rno=%s AND RNO NOT IN (SELECT RNO FROM BOOK WHERE STARTIME<str_to_date('%s','%%Y-%%m-%%d %%h:%%i:%%S') AND ENDTIME>str_to_date('%s','%%Y-%%m-%%d %%h:%%i:%%S'))"%(Room_Number,End_DateTime,Start_DateTime)
    DataBase_Cursor.execute(Search_By_roomNumber_SQL)
    Search_Results = DataBase_Cursor.fetchall()
    if DataBase_Cursor.rowcount != 0:
        Show_Meetingroom_Results(Search_Results, Window)
    else:
        tkinter.messagebox.showinfo("提示信息", "没有找到该编号的会议室哦~")


def Search_By_Multiple(Window, LowerCost, UpperCost, Position, Capacity,DateString,Start,End,Equipment):
    Start_DateTime = time.strftime(DateString + " " + str(Start) + ":00:00")
    End_DateTime = time.strftime(DateString + " " + str(End) + "00:00")
    if len(LowerCost) == 0:
        LowerCost = '0'
    if len(UpperCost) == 0:
        UpperCost = '1000'
    if len(Capacity) == 0:
        Capacity = '1'
    if Position == -1:
        Search_By_Multiple_SQL = " SELECT * From ROOM WHERE (COST BETWEEN '%s' AND '%s') AND Capa>='%s' AND RNO IN (SELECT DISTINCT RNO FROM RE,EQUIP WHERE RE.ENO=EQUIP.ENO AND EQUIP.ETYPE='%s' AND EQUIP.ESTATE=1) AND RNO NOT IN (SELECT RNO FROM BOOK WHERE STARTIME<str_to_date('%s','%%Y-%%m-%%d %%h:%%i:%%S') AND ENDTIME>str_to_date('%s','%%Y-%%m-%%d %%h:%%i:%%S'))"% (LowerCost, UpperCost, Capacity,Equipment,End_DateTime,Start_DateTime)
    else:
        if Position==1:
            Search_By_Multiple_SQL = " SELECT * From ROOM WHERE LOCATION='东' AND (COST BETWEEN '%s' AND '%s') AND Capa>='%s' AND RNO NOT IN (SELECT RNO FROM BOOK WHERE STARTIME<str_to_date('%s','%%Y-%%m-%%d %%h:%%i:%%S') AND ENDTIME>str_to_date('%s','%%Y-%%m-%%d %%h:%%i:%%S')) AND RNO IN (SELECT DISTINCT RNO FROM RE,EQUIP WHERE RE.ENO=EQUIP.ENO AND EQUIP.ETYPE='%s' AND EQUIP.ESTATE=1)" \
                                     % (LowerCost, UpperCost, Capacity,End_DateTime,Start_DateTime,Equipment)
        elif Position==2:
            Search_By_Multiple_SQL = " SELECT * From ROOM WHERE LOCATION='西' AND (COST BETWEEN '%s' AND '%s') AND Capa>='%s' AND RNO NOT IN (SELECT RNO FROM BOOK WHERE STARTIME<str_to_date('%s','%%Y-%%m-%%d %%h:%%i:%%S') AND ENDTIME>str_to_date('%s','%%Y-%%m-%%d %%h:%%i:%%S')) AND RNO IN (SELECT DISTINCT RNO FROM RE,EQUIP WHERE RE.ENO=EQUIP.ENO AND EQUIP.ETYPE='%s' AND EQUIP.ESTATE=1)" \
                                     % (LowerCost, UpperCost, Capacity, End_DateTime, Start_DateTime,Equipment)
        elif Position==3:
            Search_By_Multiple_SQL = " SELECT * From ROOM WHERE LOCATION='南' AND (COST BETWEEN '%s' AND '%s') AND Capa>='%s' AND RNO NOT IN (SELECT RNO FROM BOOK WHERE STARTIME<str_to_date('%s','%%Y-%%m-%%d %%h:%%i:%%S') AND ENDTIME>str_to_date('%s','%%Y-%%m-%%d %%h:%%i:%%S')) AND RNO IN (SELECT DISTINCT RNO FROM RE,EQUIP WHERE RE.ENO=EQUIP.ENO AND EQUIP.ETYPE='%s' AND EQUIP.ESTATE=1)" \
                                     % (LowerCost, UpperCost, Capacity, End_DateTime, Start_DateTime,Equipment)
        else:
            Search_By_Multiple_SQL = " SELECT * From ROOM WHERE LOCATION='北' AND (COST BETWEEN '%s' AND '%s') AND Capa>='%s' AND RNO NOT IN (SELECT RNO FROM BOOK WHERE STARTIME<str_to_date('%s','%%Y-%%m-%%d %%h:%%i:%%S') AND ENDTIME>str_to_date('%s','%%Y-%%m-%%d %%h:%%i:%%S')) AND RNO IN (SELECT DISTINCT RNO FROM RE,EQUIP WHERE RE.ENO=EQUIP.ENO AND EQUIP.ETYPE='%s' AND EQUIP.ESTATE=1)" \
                                     % (LowerCost, UpperCost, Capacity, End_DateTime, Start_DateTime,Equipment)

    DataBase_Cursor.execute(Search_By_Multiple_SQL)
    Search_Results = DataBase_Cursor.fetchall()
    if DataBase_Cursor.rowcount!=0:
        Show_Meetingroom_Results(Search_Results, Window)
    else:
        tkinter.messagebox.showinfo("提示信息", "没有找到满足条件的会议室哦~")


def Admin_Judge(Window):
    User_Name_Input = User_Name_Entry.get()
    Admin_Judge_SQL = "SELECT * FROM STAFF WHERE SNO=%s AND slimit=1"%(User_Name_Input)
    DataBase_Cursor.execute(Admin_Judge_SQL)
    if DataBase_Cursor.rowcount!=0:
        Equipment_Control(Window)
    else:
        tkinter.messagebox.showinfo("提示信息", "您不是管理员哦！")


def Equipment_Control(Window):
    Equipment_Control_Window = Toplevel(Window)
    Equipment_Control_Window.geometry("400x300")
    Equipment_Control_Window.title("损坏设备登记")

    Equipment_Control_Label = Label(Equipment_Control_Window, text="请输入损坏设备编号", font=("华文行楷", 25), relief=RAISED,bg="light blue",fg="red")
    Equipment_Control_Label.place(relx=0.15, rely=0.24)

    Equipment_Control_Entry = Entry(Equipment_Control_Window, font=("宋体", 22))
    Equipment_Control_Entry.place(relx=0.12, rely=0.4)

    Equipment_Control_Button = Button(Equipment_Control_Window, text="确认上传", font=("华文行楷",22),bg="light blue",fg="red",
                                      command=lambda: Upload_Equipment(Equipment_Control_Entry.get()))
    Equipment_Control_Button.place(relx=0.33, rely=0.6)
    Equipment_Control_Window.mainloop()


def Upload_Equipment(Number):
    Upload_Equipment_SQL = "UPDATE EQUIP SET ESTATE=0 WHERE ENO=%s"%(Number)
    DataBase_Cursor.execute(Upload_Equipment_SQL)
    DataBase.commit()
    tkinter.messagebox.showinfo("提示信息", "上传成功！")


def Enter_My_Panel(Window):
    My_Information_Panel = Toplevel(Window)
    My_Information_Panel.geometry("800x600")
    My_Information_Panel.title("我的主页")

    Deposit_Button = Button(My_Information_Panel, bg="light blue", fg="red", font=("华文行楷", 22), text="充值",
                            command=lambda: Make_Deposit(Window))
    Deposit_Button.place(relx=0.4, rely=0.33)

    My_Sno_Label=Label(My_Information_Panel,bg="light blue",fg="red",text="我的工号："+User_Name_Entry.get(),font=("楷书",22))
    My_Sno_Label.place(relx=0.1,rely=0.15)

    Deposit_Search_SQL="SELECT SDE FROM STAFF WHERE SNO=%s"%(User_Name_Entry.get())
    DataBase_Cursor.execute(Deposit_Search_SQL)
    Deposit=DataBase_Cursor.fetchone()
    My_Deposit_Label=Label(My_Information_Panel,bg="light blue",fg="red",text="我的余额："+str(Deposit)[1:-2],font=("楷书",22))
    My_Deposit_Label.place(relx=0.1,rely=0.35)

    Search_Ontime_SQL="SELECT * FROM BOOK WHERE SNO=%s"%(User_Name_Entry.get())
    DataBase_Cursor.execute(Search_Ontime_SQL)
    if DataBase_Cursor.rowcount==0:
        Information="暂无预定"
        Ontime_Record="暂无预定"
    else:
        Ontime_Record=DataBase_Cursor.fetchone()
        Room_Number=str(Ontime_Record[1])
        Start_time=str(Ontime_Record[3])
        End_time=str(Ontime_Record[4])
        print(Room_Number,Start_time,End_time)
        Information="您预定了"+Room_Number+"号会议室，会议时间为："+Start_time+"至"+End_time

    My_Reserve_Ontime = Label(My_Information_Panel, bg="light blue", fg="red", text="当前预定", bd=4, font=("楷书", 22))
    My_Reserve_Ontime.place(relx=0.44, rely=0.55)

    My_Reserve_Ontime=Label(My_Information_Panel,bg="light blue",fg="red",text=Information,bd=4,font=("楷书",16))
    My_Reserve_Ontime.place(relx=0.02,rely=0.65)

    Cancel_Reserve=Button(My_Information_Panel,bg="light blue",fg="red",text="取消预约",bd=4,font=("楷书",22),relief=RAISED,command=lambda:Cancel_Reserve_Func(Ontime_Record))
    Cancel_Reserve.place(relx=0.1,rely=0.75)

    My_Reserve_OutOfTime = Button(My_Information_Panel, bg="light blue", fg="red", text="查看历史预约", bd=4, font=("楷书", 22),command=lambda:Search_Previous_Records(My_Information_Panel))
    My_Reserve_OutOfTime.place(relx=0.37, rely=0.75)

    UpDate_Reserve_Button=Button(My_Information_Panel,bg="light blue",fg="red",bd=4,text="更新历史预约",font=("楷书",22),command=Update_History)
    UpDate_Reserve_Button.place(relx=0.68,rely=0.75)

    My_Information_Panel.mainloop()

def Update_History():
    SELECT_SQL="SELECT * FROM BOOK WHERE SNO='%s' AND NOW()>=ENDTIME"%(User_Name_Entry.get())
    DataBase_Cursor.execute(SELECT_SQL)
    print(User_Name_Entry.get())
    if DataBase_Cursor.rowcount==0:
        tkinter.messagebox.showinfo("提示信息","您当前没有已经结束的预约哦~")
    else:
        INSERT_SQL="INSERT INTO USED SELECT * FROM BOOK WHERE SNO='%s'"%(User_Name_Entry.get())
        DataBase_Cursor.execute(INSERT_SQL)
        DataBase.commit()

        UPDATE_SQL = "UPDATE STAFF SET SDE=SDE-(SELECT COST FROM BOOK WHERE SNO=%s) WHERE SNO=%s"%(User_Name_Entry.get(),
                                                                                                 User_Name_Entry.get())
        DataBase_Cursor.execute(UPDATE_SQL)
        DataBase.commit()

        DELETE_SQL="DELETE FROM BOOK WHERE SNO=%s"%(User_Name_Entry.get())
        DataBase_Cursor.execute(DELETE_SQL)
        DataBase.commit()

        tkinter.messagebox.showinfo("提示信息","已经帮助您完成结算")


def Cancel_Reserve_Func(Ontime_Record):
    if Ontime_Record=="暂无预定":
        tkinter.messagebox.showinfo("提示信息","您当前没有预约哦~")
    else:
        SELECT_SQL="SELECT * FROM BOOK WHERE SNO=%s"%(User_Name_Entry.get())
        DataBase_Cursor.execute(SELECT_SQL)
        SELECT_Result=DataBase_Cursor.fetchone()
        Start_Time=SELECT_Result[3].strftime("%Y-%m-%d %H:%I:%S")
        Book_Time=SELECT_Result[2].strftime("%Y-%m-%d %H:%I:%S")
        End_Time=SELECT_Result[4].strftime("%Y-%m-%d %H:%I:%S")
        if Start_Time[8]=='0':
            Day=int(Start_Time[9])
        else:
            Day=int(Start_Time[8:10])
        Day_Dif_SQL="SELECT %s-Day(Now())"%(Day)
        DataBase_Cursor.execute(Day_Dif_SQL)
        Day_difference=int(str(DataBase_Cursor.fetchone())[1:-2])
        DELETE_SQL="DELETE FROM BOOK WHERE SNO=%s"%(User_Name_Entry.get())
        DataBase_Cursor.execute(DELETE_SQL)
        DataBase.commit()
        print(type(SELECT_Result[5]))
        if Day_difference>=3:
            Default_Charge=0
        elif 1<=Day_difference<3:
            Default_Charge=0.1*SELECT_Result[5]
        else:
            Default_Charge=0.3*SELECT_Result[5]
        print(Default_Charge)
        INSERT_SQL="INSERT INTO CANCEL (SNO,RNO,BookTime,STARTIME,CANCELTIME,COST) VALUES('%s','%s',str_to_date('%s','%%Y-%%m-%%d %%H:%%i:%%S'),str_to_date('%s','%%Y-%%m-%%d %%H:%%i:%%S'),str_to_date('%s','%%Y-%%m-%%d %%H:%%i:%%S'),%s)"%(SELECT_Result[0],SELECT_Result[1],Book_Time,Start_Time,End_Time,Default_Charge)
        DataBase_Cursor.execute(INSERT_SQL)
        DataBase.commit()
        UPDATE_SQL="UPDATE STAFF SET SDE=SDE-%s WHERE SNO=%s"%(Default_Charge,User_Name_Entry.get())
        DataBase_Cursor.execute(UPDATE_SQL)
        DataBase.commit()
        tkinter.messagebox.showinfo("提示信息","您已成功取消预约，手续费为"+str(Default_Charge)+"元")


def Search_Previous_Records(Window):
    Search_Previous_Records_SQL="SELECT * FROM USED WHERE SNO=%s"%(User_Name_Entry.get())
    DataBase_Cursor.execute(Search_Previous_Records_SQL)
    if DataBase_Cursor.rowcount==0:
        tkinter.messagebox.showinfo("提示信息","您还没有进行过会议室预约哦~")
    else:
        Search_Previous_Records_Window = Toplevel(Window)
        Search_Previous_Records_Window.geometry("600x400")
        Search_Previous_Records_Window.title("我的历史预约记录")
        Column_Names=("工号","会议室号","预约时间","开始时间","结束时间","总费用")
        xbar=Scrollbar(Search_Previous_Records_Window,orient=HORIZONTAL)
        xbar.pack(side=BOTTOM,fill=X)
        Records_TreeView = ttk.Treeview(Search_Previous_Records_Window, height=12, show="headings", columns=Column_Names,xscrollcommand=xbar.set)
        Records_TreeView.column("工号", width=50, anchor="center")
        Records_TreeView.column("会议室号", width=50, anchor="center")
        Records_TreeView.column("预约时间", width=200, anchor="center")
        Records_TreeView.column("开始时间", width=200, anchor="center")
        Records_TreeView.column("结束时间", width=200, anchor="center")
        Records_TreeView.column("总费用", width=50, anchor="center")
        Records_TreeView.heading("工号", text="工号")
        Records_TreeView.heading("会议室号", text="会议室号")
        Records_TreeView.heading("预约时间", text="开始时间")
        Records_TreeView.heading("开始时间", text="开始时间")
        Records_TreeView.heading("结束时间", text="结束时间")
        Records_TreeView.heading("总费用",text="总费用")
        Snos=[]
        Rnos = []
        Book_Times=[]
        Start_Times = []
        End_Times = []
        Costs = []
        Search_Results=DataBase_Cursor.fetchall()
        for r in Search_Results:
            Snos.append(r[0])
            Rnos.append(r[1])
            Book_Times.append(r[2])
            Start_Times.append(r[3])
            End_Times.append(r[4])
            Costs.append(r[5])
        for i in range(len(Rnos)):
            Records_TreeView.insert("", i, values=(Snos[i],Rnos[i], Book_Times[i],Start_Times[i], End_Times[i], Costs[i]))
        Records_TreeView.place(relx=0.1, rely=0.2)

def Make_Deposit(Window):
    Deposit_Window = Toplevel(Window)
    Deposit_Window.geometry("400x300")
    Deposit_Window.title("充值中心")

    Deposit_Label = Label(Deposit_Window, text="请输入充值金额：", font=("楷书", 22), relief=RAISED)
    Deposit_Label.place(relx=0.25, rely=0.24)

    Deposit_Entry = Entry(Deposit_Window, font=("宋体", 22), bg="white")
    Deposit_Entry.place(relx=0.16, rely=0.4)

    Deposit_Button = Button(Deposit_Window, text="确认充值", font=("华文行楷",22), command=lambda:upload_deposit(Deposit_Entry.get()))
    Deposit_Button.place(relx=0.35, rely=0.6)
    Deposit_Window.mainloop()

def upload_deposit(money):
    User_Name_Input=User_Name_Entry.get()
    if len(money) !=0:
        upload_deposit_sql = "UPDATE STAFF SET SDE=SDE+'%s' WHERE SNO=%s" % (money, User_Name_Input)
        DataBase_Cursor.execute(upload_deposit_sql)
        DataBase.commit()
        tkinter.messagebox.showinfo("提示信息", "充值成功！")

def Show_Meetingroom_Results(Search_Results, Window):
    Show_meetingRooms_window = Toplevel(Window)
    Show_meetingRooms_window.title("查询结果界面")
    Show_meetingRooms_window.geometry("800x600")
    Column_Names = ("编号", "位置", "最大容量", "价格")
    Results_TreeView = ttk.Treeview(Show_meetingRooms_window, height=18, show="headings", columns=Column_Names)
    Results_TreeView.column("编号", width=100, anchor="center")
    Results_TreeView.column("位置", width=100, anchor="center")
    Results_TreeView.column("最大容量", width=100, anchor="center")
    Results_TreeView.column("价格", width=100, anchor="center")
    Results_TreeView.heading("编号", text="会议室编号")
    Results_TreeView.heading("位置", text="会议室位置")
    Results_TreeView.heading("最大容量", text="最多承担人数")
    Results_TreeView.heading("价格", text="价格（元/小时）")
    Rnos = []
    Locations = []
    Capacities = []
    Costs = []
    for r in Search_Results:
        Rnos.append(r[0])
        Locations.append(r[1])
        Capacities.append(r[2])
        Costs.append(r[3])
    for i in range(len(Rnos)):
        Results_TreeView.insert("", i, values=(Rnos[i], Locations[i], Capacities[i], Costs[i]))
    Results_TreeView.place(relx=0.25, rely=0.1)

    Result_Label=Label(Show_meetingRooms_window,text="为您找到以下结果",font=("楷书",20),fg="red",bg="light blue")
    Result_Label.place(relx=0.37,rely=0.02)

    Reserve_Number_Label=Label(Show_meetingRooms_window,text="预定会议室编号：",font=("楷书",20),bg="light blue",fg="red")
    Reserve_Number_Label.place(relx=0.15,rely=0.75)

    Reserve_Number_Entry=Entry(Show_meetingRooms_window,font=("宋体",20))
    Reserve_Number_Entry.place(relx=0.45,rely=0.75)

    Reserve_Time_Label = Label(Show_meetingRooms_window, text="预定时间：",font=("楷书",20),bg="light blue",fg="red")
    Reserve_Time_Label.place(relx=0.15, rely=0.83)

    Reserve_Time_Entry = Entry(Show_meetingRooms_window,font=("宋体",20),width=28)
    Reserve_Time_Entry.place(relx=0.35, rely=0.83)
    Reserve_Time_Entry.insert(0,"格式为xxxx-xx-xx xx-xx")

    Reserve_Button=Button(Show_meetingRooms_window,text="点击预定",bg="light blue",fg="red",font=("华文行楷",20),relief=RAISED,command=lambda:Reserving(Reserve_Number_Entry.get(),Reserve_Time_Entry.get()))
    Reserve_Button.place(relx=0.43,rely=0.9)

    Show_meetingRooms_window.mainloop()

def Reserving(Number,Time):
    Year=Time[0:4]
    Month=Time[5:7]
    if Month[0]=='0':
        Int_Month=int(Month[1])
    else:
        Int_Month=eval(Month)
    Day=Time[8:10]
    if Day[0]=='0':
        Int_Day=int(Day[1])
    else:
        Int_Month=eval(Day)
    Start_Hour=Time[11:13]
    if Start_Hour[0]=='0':
        Int_Start_Hour=int(Start_Hour[1])
    else:
        Int_Start_Hour=eval(Start_Hour)
    End_Hour=Time[14:16]
    if End_Hour[0]=='0':
        Int_End_Hour=int(End_Hour[1])
    else:
        Int_End_Hour=eval(End_Hour)
    print(Int_Month,Int_Day,Int_Start_Hour,Int_End_Hour)
    t=time.localtime()
    if Int_Month <1 or Int_Month>12 or Int_Day<1 or Int_Day>31 or Int_Start_Hour<9 or Int_End_Hour>18 or Int_Start_Hour>=Int_End_Hour:
        tkinter.messagebox.showinfo("提示信息","请输入正确的时间")
    else:
        DateTime_Start_String=time.strftime(Year+"-"+Month+"-"+Day+" "+Start_Hour+":00:00")
        DateTime_End_String=time.strftime(Year+"-"+Month+"-"+Day+" "+End_Hour+":00:00")
        print(DateTime_Start_String,DateTime_End_String,type(DateTime_End_String))
        SELECT_SQL=\
        "SELECT RNO FROM ROOM WHERE RNO=%s AND " \
        "RNO NOT IN (SELECT RNO FROM BOOK WHERE STARTIME<str_to_date('%s','%%Y-%%m-%%d %%h:%%i:%%S') AND ENDTIME>str_to_date('%s','%%Y-%%m-%%d %%h:%%i:%%S'))"%(Number,DateTime_End_String,DateTime_Start_String)
        DataBase_Cursor.execute(SELECT_SQL)
        if DataBase_Cursor.rowcount==0:
            tkinter.messagebox.showinfo("提示信息","此时间段该会议室已经被预约了哦~")
        else:
            SELECT_CHARGE_SQL="SELECT COST FROM ROOM WHERE RNO=%s"%(Number)
            DataBase_Cursor.execute(SELECT_CHARGE_SQL)
            Charge_Per_Hour=(DataBase_Cursor.fetchone())[0]
            Predicted_Charge=Charge_Per_Hour*(Int_End_Hour-Int_Start_Hour)
            tkinter.messagebox.showinfo("提示信息","恭喜你预约成功！请准时参加会议。预期花费为"+str(Predicted_Charge)+"元")
            INSERT_SQL="INSERT INTO BOOK VALUES('%s','%s',now(),str_to_date('%s','%%Y-%%m-%%d %%H:%%i:%%S'),str_to_date('%s','%%Y-%%m-%%d %%H:%%i:%%S'),%s)"%(User_Name_Entry.get(),Number,DateTime_Start_String,DateTime_End_String,Predicted_Charge)
            DataBase_Cursor.execute(INSERT_SQL)
            DataBase.commit()


# 下方为主函数部分

db_settings = get_db_config()
print(db_settings)
# 首先连接数据库，并创建一个游标对象用于访问和操作数据库
DataBase = pymysql.connect(**db_settings)
DataBase_Cursor = DataBase.cursor()
# 
Login_Window = Tk()  # 定义一个根窗体
Login_Window.title("欢迎使用会议室预约系统")  # 定义窗体名字
Login_Window.geometry("800x600")  # 设置根窗体的大小

style=ttkbootstrap.Style(theme="superhero")
TOP6=style.master

# 在根窗体上放置一个标签，记录本数据库系统的名字
Database_Name_Label = Label(Login_Window, bg="light blue", bd=4, fg="red", text="会议室预约系统", relief=RAISED, font=("楷书", 32),height=1, width=30)
Database_Name_Label.place(relx=0.1, rely=0.1)

# 在根窗体上放置一个标签，提示用户输入工号
User_Name_Label = Label(Login_Window, bg="light blue", bd=4,fg="red", text="请输入工号：", font=("楷书", 22), relief=RAISED)
User_Name_Label.place(relx=0.2, rely=0.3)

# 在根窗体上放置一个单行输入框，用于用户输入工号
User_Name_Entry = Entry(Login_Window, bg="white", bd=4, font=("宋体", 22), relief=RAISED)
User_Name_Entry.place(relx=0.45, rely=0.3)

# 在根窗体上放置一个标签，提示用户输入密码
Password_Label = Label(Login_Window, bg="light blue", bd=4, fg="red", text="请输入密码：", font=("楷书", 22), relief=RAISED)
Password_Label.place(relx=0.2, rely=0.5)

# 在根窗体上放置一个单行输入框，用于用户输入密码
Password_Entry = Entry(Login_Window, bg="white", bd=4, font=("宋体", 22), relief=RAISED,show="*")
Password_Entry.place(relx=0.45, rely=0.5)

# 在根窗体上放置一个按钮，用户点击该按钮即会进行身份验证登录
Login_Button = Button(Login_Window, command=login_test, bg="light blue", bd=4, font=("楷书", 22), fg="red",relief=RAISED, text="点击登录")
Login_Button.place(relx=0.42, rely=0.7)

# 在用户关闭根窗口前保持程序运行
Login_Window.mainloop()

# 用户关闭根窗口后同时也需要切断游标以及数据库的连接
DataBase_Cursor.close()
DataBase.close()
