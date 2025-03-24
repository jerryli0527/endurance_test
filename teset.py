#import numpy as np
import time
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.ttk import Notebook
from tkinter import messagebox
import datetime
import threading
import paramiko
import re

root = tk.Tk()
root.title('Endurance Test -  V0.1')
window_width = root.winfo_screenwidth()    # 取得螢幕寬度
window_height = root.winfo_screenheight()  # 取得螢幕高度
left = int((window_width - 1200)/2)       # 計算左上 x 座標
top = int((window_height - 680)/2)      # 計算左上 y 座標
root.geometry(f'1200x680+{left}+{top}')  # 定義視窗的尺寸和位置
root.resizable(False, False)   # 設定 x 方向和 y 方向都不能縮放
tab_main = ttk.Notebook()
tab_main.place(x=3, y=1,width=1197, height=679)

# 全局變數來控制Run/Stop
runStatus_stop = False
runStatus_run = False
# 全局變數儲存各功能設定
PC_config = {"PC_enable": [tk.BooleanVar() for _ in range(8)],  # 新增enable 列
             "Console": [tk.BooleanVar() for _ in range(8)],
             "Apps": [[tk.BooleanVar() for _ in range(8)] for _ in range(15)],
             "Ctrl_ip": [tk.StringVar() for _ in range(8)],
             "PC_ip": [tk.StringVar() for _ in range(8)],
             "Con_DUT": [tk.StringVar() for _ in range(8)],
             "Con_Interface": [tk.StringVar() for _ in range(8)]}

# PCnum = tk.IntVar(value=0) # 計算Enable PC數量
pc_num = 8
def Dashboard_tab():
    tab1 = tk.Frame(tab_main)
    tab_main.add(tab1, text='  Dashboard  ',)
    def DUT_select():
        DUT_frame = tk.LabelFrame(tab1, width=280, height=230,relief='flat')
        DUT_frame.place(x=1, y=1)
        DUT_frame.pack_propagate(False)
        titlelabel = tk.Label(DUT_frame,text='Endurance Test', font=('Arial',20,'bold'),fg='#404040')
        titlelabel.place(x=10, y=10)
        modellabel = tk.Label(DUT_frame,text='Model: ',font=('Arial',12,'bold'),fg='#404040')
        modellabel.place(x=30, y =65)
        numberlabel = tk.Label(DUT_frame,text='DUT number:',font=('Arial',12,'bold'),fg='#404040')
        numberlabel.place(x=30, y=100)
        baselabel = tk.Label(DUT_frame,text='Base',font=('Arial',12,'bold'),fg='#404040')
        baselabel.place(x=30, y=130)
        sate1label = tk.Label(DUT_frame,text='Satellite1',font=('Arial',12,'bold'),fg='#404040')
        sate1label.place(x=30, y=160)
        sate2label = tk.Label(DUT_frame,text='Satellite2',font=('Arial',12,'bold'),fg='#404040')
        sate2label.place(x=30, y=190)

        modelbox = ttk.Combobox(DUT_frame, width=15, values=['RS600','RS300','RS100','RBE873','RS200v2','RBE273'])
        modelbox.place(x=120, y=65)
        basebox = ttk.Combobox(DUT_frame, width=8, values=['#1','#2','#3','#4','#5','#6'])
        basebox.place(x=120, y=130)
        sate1box = ttk.Combobox(DUT_frame, width=8, values=['#1','#2','#3','#4','#5','#6'])
        sate1box.place(x=120, y=160)
        sate2box = ttk.Combobox(DUT_frame, width=8, values=['#1','#2','#3','#4','#5','#6'])
        sate2box.place(x=120, y=190)
    def testinfo():
        testinfo = tk.LabelFrame(tab1,width=270, height=140)
        testinfo.place(x=280, y=60)
        testinfo.pack_propagate(False)
        infolabel = tk.Label(testinfo,text='Testing Information',font=('Arial',12,'bold','underline'),fg='#404040')
        infolabel.pack()
        modellabel = tk.Label(testinfo,text='Model:',font=('Arial',10,'bold'),fg='#404040')
        modellabel.place(x=5, y=30)
        startlabel = tk.Label(testinfo,text='Start:',font=('Arial',10,'bold'),fg='#404040')
        startlabel.place(x=5, y=50)
        currentlabel = tk.Label(testinfo,text='Current:',font=('Arial',10,'bold'),fg='#404040')
        currentlabel.place(x=5, y=70)
        durationlabel = tk.Label(testinfo,text='Duration:',font=('Arial',10,'bold'),fg='#404040')
        durationlabel.place(x=5, y=90)

        now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
        today = now.strftime('%Y/%m/%d %H:%M:%S')
        currectVaulelabel = tk.Label(testinfo, text=today, font=('Arial', 10, 'bold'), fg='#404040')
        currectVaulelabel.place(x=70, y=70)
    def dutStatus():
        dutStatus = tk.LabelFrame(tab1,width=270, height=410)
        dutStatus.place(x=280, y=210)
        dutStatus.pack_propagate(False)
        dutStatuslabel = tk.Label(dutStatus,text='DUT Status',font=('Arial',12,'bold','underline'),fg='#404040')
        dutStatuslabel.pack()

        dutStatus_sub = tk.LabelFrame(dutStatus, width=260, height=150)
        dutStatus_sub.place(x=4, y=27)

        item1 = tk.Label(dutStatus_sub, text='DUT   Up time        Reboot   Panic   ', font=('Arial',11,'bold'),fg='#404040')
        item1.grid(row=0, column=0, padx=1, pady=1)
        base_up = tk.Label(dutStatus_sub, text='Base    99d/23h/99m 1  1   ', font=('Arial', 11,),fg='#404040')
        base_up.grid(row=1, column=0, padx=0, pady=0)
        sate1_up = tk.Label(dutStatus_sub, text='Sate1    99d/23h/99m 1  1   ', font=('Arial', 11,),fg='#404040')
        sate1_up.grid(row=2, column=0, padx=0, pady=0)
        sate2_up = tk.Label(dutStatus_sub, text='Sate2    99d/23h/99m 1  1   ', font=('Arial', 11,),fg='#404040')
        sate2_up.grid(row=3, column=0, padx=0, pady=0)
        item2 = tk.Label(dutStatus_sub, text='DUT    CPU   Memory   Session     ', font=('Arial',11,'bold'),fg='#404040')
        item2.grid(row=4, column=0, padx=1, pady=1)
        base_dn = tk.Label(dutStatus_sub, text='Base    99d/23h/99m 1  1', font=('Arial', 11,),fg='#404040')
        base_dn.grid(row=5, column=0, padx=0, pady=0)
        sate1_dn = tk.Label(dutStatus_sub, text='Sate1    99d/23h/99m 1  1', font=('Arial', 11,),fg='#404040')
        sate1_dn.grid(row=6, column=0, padx=0, pady=0)
        sate2_dn = tk.Label(dutStatus_sub, text='Sate2    99d/23h/99m 1  1', font=('Arial', 11,),fg='#404040')
        sate2_dn.grid(row=7, column=0, padx=0, pady=0)
        # upTimelabel = tk.Label(dutStatus,text='Up time:',font=('Arial',10,'bold'),fg='#404040')
        # upTimelabel.place(x=5, y=30)
        # cpuUsagelabel = tk.Label(dutStatus,text='CPU usage:',font=('Arial',10,'bold'),fg='#404040')
        # cpuUsagelabel.place(x=5, y=50)
        # memUsagelabel = tk.Label(dutStatus,text='Memory usage:',font=('Arial',10,'bold'),fg='#404040')
        # memUsagelabel.place(x=5, y=70)
        # sessionlabel = tk.Label(dutStatus,text='Session number:',font=('Arial',10,'bold'),fg='#404040')
        # sessionlabel.place(x=5, y=90)
        # rebootlabel = tk.Label(dutStatus,text='Reboot:',font=('Arial',10,'bold'),fg='#404040')
        # rebootlabel.place(x=5, y=110)
        # kernellabel = tk.Label(dutStatus,text='Kernel panic:',font=('Arial',10,'bold'),fg='#404040')
        # kernellabel.place(x=5, y=130)
    def pcStatus():
        pcStatus_ = tk.LabelFrame(tab1,width=320, height=300)
        pcStatus_.place(x=560, y=60)
        pcStatus_.pack_propagate(False)
        pcStatuslabel = tk.Label(pcStatus_,text='PC Status',font=('Arial',12,'bold','underline'),fg='#404040')
        pcStatuslabel.pack()
        pcStatus = tk.LabelFrame(pcStatus_,width=313, height=170, relief='flat')
        pcStatus.place(x=2, y=30)
        pcStatus.pack_propagate(False)
        scrollbar = tk.Scrollbar(pcStatus)
        scrollbar.pack(side='right', fill='y')
        interfaces = ['Ethernet', '6G', '5G', '2.4G', '5G-Guest', '6G-Guest', '-', '-']
        connectDUT = ['Base', 'Base', 'Satellite1', 'Satellite1', 'Satellite2', 'Satellite2', '-', '-']
        connectStatus = ['Connect', 'Disconnect', 'Connect', 'Connect', 'Connect', 'Disconnect', '-', '-',]
        pc_y = 5

        for i in range(0, 8):
            num = str(i+1)
            intfc = interfaces[i]
            cntDUT = connectDUT[i]
            cntSts = connectStatus[i]
            pclabel = tk.Label(pcStatus, text='PC' + num, font=('Arial', 10, 'bold'), fg='#404040')
            pclabel.place(x=5, y=pc_y)
            intfclabel = tk.Label(pcStatus, text=intfc, font=('Arial', 10, 'bold'), fg='#404040')
            intfclabel.place(x=50, y=pc_y)
            cntDUTlabel = tk.Label(pcStatus, text=cntDUT, font=('Arial', 10, 'bold'), fg='#404040')
            cntDUTlabel.place(x=130, y=pc_y)
            if cntSts == 'Connect':
                cntDUTlabel = tk.Label(pcStatus, text=cntSts, font=('Arial', 10, 'bold'), fg='#0065A5')
                cntDUTlabel.place(x=210, y=pc_y)
            else:
                cntDUTlabel = tk.Label(pcStatus, text=cntSts, font=('Arial', 10, 'bold'), fg='#FF0000')
                cntDUTlabel.place(x=210, y=pc_y)
            pc_y = pc_y+20

        reboot_btn = tk.Button(pcStatus_, text='  Reboot All PC  ')
        reboot_btn.place(x=30, y=220)
        recntintfc_btn = tk.Button(pcStatus_, text=' Reconnect Interface ')
        recntintfc_btn.place(x=160, y=220)
        refresh_btn = tk.Button(pcStatus_, text=' Refresh ')
        refresh_btn.place(x=230, y=260)
        refreshlabel = tk.Label(pcStatus_, text='Refresh every 15 minutes', font=('Arial',8, 'bold'), fg='#404040')
        refreshlabel.place(x=10, y=270)


    def pingLoss():
        pingLoss_ = tk.LabelFrame(tab1,width=320, height=250)
        pingLoss_.place(x=560, y=370)
        pingLoss_.pack_propagate(False)
        pingLosslabel = tk.Label(pingLoss_,text='PC ping loss rate',font=('Arial',12,'bold','underline'),fg='#404040')
        pingLosslabel.pack()

        pingLoss = tk.LabelFrame(pingLoss_, width=313, height=170, relief='flat')
        pingLoss.place(x=2, y=30)
        pingLoss.pack_propagate(False)
        scrollbar = tk.Scrollbar(pingLoss)
        scrollbar.pack(side='right', fill='y')

        dutRate = ['0%', '99%', '0%', '2%', '1%', '99%', '-', '-']
        ipv4Rate = ['0%', '99%', '0%', '4%', '1%', '99%', '-', '-']
        ipv6Rate = ['0%', '99%', '0%', '3%', '3%', '99%', '-', '-']
        ping_y = 5
        for i in range(0, 8):
            num = str(i + 1)
            rate1 = dutRate[i]
            rate2 = ipv4Rate[i]
            rate3 = ipv6Rate[i]
            pcPinglabel = tk.Label(pingLoss, text='PC' + num, font=('Arial', 10, 'bold'), fg='#404040')
            pcPinglabel.place(x=5, y=ping_y)
            dutPinglabel = tk.Label(pingLoss, text='DUT: ' + rate1, font=('Arial', 10, 'bold'), fg='#404040')
            dutPinglabel.place(x=50, y=ping_y)
            ipv4Pinglabel = tk.Label(pingLoss, text='IPv4: ' + rate2, font=('Arial', 10, 'bold'), fg='#404040')
            ipv4Pinglabel.place(x=130, y=ping_y)
            ipv6Pinglabel = tk.Label(pingLoss, text='IPv6: ' + rate3, font=('Arial', 10, 'bold'), fg='#404040')
            ipv6Pinglabel.place(x=210, y=ping_y)
            ping_y = ping_y + 20
        refresh_btn = tk.Button(pingLoss_, text=' Refresh ', command=run_ping_loss, font=("Arial", 14))
        refresh_btn.place(x=230, y=210)
        refreshlabel = tk.Label(pingLoss_, text='Refresh every 15 minutes', font=('Arial',8, 'bold'), fg='#404040')
        refreshlabel.place(x=10, y=220)
    def run_ping_loss():
        remote_ip = '192.168.13.194'
        remote_DUT_username = 'dnisqa2'
        remote_DUT_password = 'Sqa2sqa2'
        batch_file_path = 'C:\\Users\\dnisqa2\\Desktop\\ping_ipv4.bat'
        results = []









    def speedtest_UI():
        speedtest = tk.LabelFrame(tab1, width=280, height=560)
        speedtest.place(x=890, y=60)
        speedtest.pack_propagate(False)
        speedtestlabel = tk.Label(speedtest, text='Speedtest', font=('Arial', 12, 'bold', 'underline'), fg='#404040')
        speedtestlabel.pack()
        reslabel = tk.Label(speedtest, text='\nThe best result UL/DL: ', font=('Arial', 10, 'bold'), fg='#404040')
        reslabel.pack()
        resBest = '11 Mbps / 22 Mbps'
        resTime = '[2025/02/13 10:58]'
        resBestlabel = tk.Label(speedtest, text= resBest, font=('Arial', 16, 'bold'), fg='#404040')
        resBestlabel.pack()
        resTimelabel = tk.Label(speedtest, text= 'Time: '+ resTime, font=('Arial', 10, 'bold'), fg='#404040')
        resTimelabel.pack()
        periodlabel = tk.Label(speedtest, text='Time period (HR)', font=('Arial', 10, 'bold'), fg='#404040')
        periodlabel.place(x=5, y= 130)
        text = tk.Text(speedtest, width=5, height=1)
        text.place(x=120, y=133)
    def run_UI():
        run_frame = tk.LabelFrame(tab1, width=270, height=411, relief='flat')
        run_frame.place(x=0, y=220)
        run_frame.pack_propagate(False)
        autoTitlelabel = tk.Label(run_frame,text='\nAutomation Status:',font=('Arial',16,'bold'),fg='#404040')
        autoTitlelabel.pack()
        autoStatuslabel = tk.Label(run_frame,text='\nStandby',font=('Arial',20,'bold'),fg='#7F7F7F')
        autoStatuslabel.pack()
        run_chk_frame = tk.LabelFrame(run_frame, width=250, height=190)
        run_chk_frame.place(x=15, y=207)
        run_chk_frame.pack_propagate(False)

        def rebootPC():
            autoStatuslabel.config(text='\nRebooting All PC', fg='#0065A5')
            messagebox.showinfo("Rebooting All PC", "Rebooting All PC")
        def DUT_setting():
            autoStatuslabel.config(text='\nDUT is setting', fg='#0065A5')
            messagebox.showinfo("DUT is setting", "DUT is setting", )
        def speedtest():
            autoStatuslabel.config(text='\nRunning', fg='#0065A5')
            messagebox.showinfo("Speedtest is testing", "Speedtest is testing")
            # 執行多線程 speedtest
        def running():
            autoStatuslabel.config(text='\nRunning', fg='#0065A5')
            global runStatus_stop
            runStatus_stop = False # 確保開始不會立即停止
            messagebox.showinfo("Running", "Running")
            # 執行多線程 DUT status
            # 執行多線程 PC status
            # 執行多線程 Ping loss

        def stop():
            autoStatuslabel.config(text='\nStandby', fg='#7F7F7F')
            messagebox.showinfo("APPs are stopped", "APPs are stopped")

            # 恢復按鈕狀態，允許重新Run
            run_btn.config(text='RUN')
            global runStatus_run
            runStatus_run = False # 重置狀態
        def run_tasks():
            global runStatus_run, runStatus_stop

            if not runStatus_run:
                # 執行 running 及 checkbox 項目
                run_btn.config(text='STOP')
                runStatus_run = True

                if var1.get():
                    rebootPC()
                if var2.get():
                    DUT_setting()
                if var3.get():
                    speedtest()

                threading.Thread(target=running, daemon=True).start()
            else:
                # 停止 running，執行 stop
                run_btn.config(text='RUN')
                runStatus_stop = True
                threading.Thread(target=stop, daemon=True).start()
        var1 = tk.BooleanVar()
        var2 = tk.BooleanVar()
        var3 = tk.BooleanVar()
        run1chk = tk.Checkbutton(run_chk_frame, text='Reboot All PC',font=('Arial',10,'bold'),fg='#404040', variable=var1)
        run1chk.place(x=110, y=30)
        run2chk = tk.Checkbutton(run_chk_frame,text='DUT Setting',font=('Arial',10,'bold'),fg='#404040',variable=var2)
        run2chk.place(x=110, y=60)
        run3chk = tk.Checkbutton(run_chk_frame,text='Speedtest',font=('Arial',10,'bold'),fg='#404040', variable=var3)
        run3chk.place(x=110, y=90)

        run_btn = tk.Button(run_chk_frame, text=' RUN ', font=('Arial',12,'bold'),bg='#BFBFBF', fg='black', width=8, height=6, command=run_tasks)
        run_btn.place(x=10, y=30)

    DUT_select()
    testinfo()
    dutStatus()
    pcStatus()
    pingLoss()
    speedtest_UI()
    run_UI()
def PC_config_tab(): # 創建 GUI
    tab2 = tk.Frame(tab_main)
    tab_main.add(tab2, text='  PC Config.  ')

    # 創建標籤 X軸 PC1 ~ PC8
    for col in range(8):
        X_label = tk.Label(tab2, text=f"PC{col+1}", font=('Arial',14,'bold'),fg='#404040')
        X_label.grid(row=1, column=col+1, padx=40, pady=5)

    # 創建標籤 Y軸 app
    Y_items = ['  ', 'Enable', 'Console Terminal', 'Control Network', 'Connection - DUT', 'Connection - Interface',
               'PC IP address', 'FTP Server', 'FTP Client', 'VLC Server', 'VLC Client', 'USB samba upload',
               'YouTube', 'Circulate ping IPv4/IPv6', 'uTorren', 'PPTV', 'Open GUI']
    App_items = ['FTP Server', 'FTP Client', 'VLC Server', 'VLC Client', 'USB samba upload',
               'YouTube', 'Circulate ping IPv4/IPv6', 'uTorren', 'PPTV', 'Open GUI']
    for row in range(17):
        y_label = tk.Label(tab2, text=Y_items[row], font=('Arial',10,'bold'),fg='#404040')
        y_label.grid(row=row+1, column=0, padx=10, pady=5)

    # Enable PC 列 checkbox
    for col in range(8):
        enable_chk = tk.Checkbutton(tab2, variable=PC_config["PC_enable"][col])
        enable_chk.grid(row=2, column=col+1)

    # Console Terminal
    for col in range(8):
        console_chk = tk.Checkbutton(tab2, variable=PC_config["Console"][col])
        console_chk.grid(row=3, column=col+1)

    # Control Network IP address
    for col in range(8):
        Ctrl_ip_entry = tk.Entry(tab2, textvariable= PC_config["Ctrl_ip"][col], width=12)
        Ctrl_ip_entry.grid(row=4, column=col+1)

    # Connection - DUT
    for col in range(8):
        con_DUT = ttk.Combobox(tab2, width=9, textvariable=PC_config["Con_DUT"][col])
        con_DUT['values'] = ('Base', 'Satellite1', 'Satellite2')
        con_DUT.grid(row=5, column=col+1)
        con_DUT.current(0) # 預設值

    # Connection - Interface
    for col in range(8):
        Con_Interface = ttk.Combobox(tab2, width=9,textvariable=PC_config["Con_Interface"][col])
        Con_Interface['values'] = ('Ethernet', '2.4G', '5G', '6G', '2.4G-Guest', '5G-Guest', '6G-Guest')
        Con_Interface.grid(row=6, column=col+1)
        Con_Interface.current(0)

    # PC IP address
    for col in range(8):
        PC_ip_entry = tk.Entry(tab2, textvariable= PC_config["PC_ip"][col], width=12)
        PC_ip_entry.grid(row=7, column=col+1)

    # APPs checkbox
    for row in range(0, 10):
        for col in range(8):
            app_chk = tk.Checkbutton(tab2, variable=PC_config["Apps"][row][col])
            app_chk.grid(row=row+8, column=col+1)

    # 儲存到文字檔
    def save_config():
        with open("config\Endurance_config.txt", "w") as f:
            # 儲存 PC 數輛
            f.write(" PC num:    ")
            for num in range(pc_num):
                f.write(f" PC{num+1} ")
            f.write(f"\n")
            # 儲存 enable 設定
            enable_states = [str(int(var.get())) for var in PC_config["PC_enable"]]
            f.write(" Enable:     "+"    ".join(enable_states)+"\n")

            # 儲存 Console IP 設定
            console_states = [str(int(var.get())) for var in PC_config["Console"]]
            f.write(" Consle:     " + "    ".join(console_states) + "\n")

            # 儲存 Control IP 設定
            Ctrl_ip_entries = [PC_config["Ctrl_ip"][col].get() or "0 " for col in range(pc_num)]
            f.write(f" CtrlIP:     " + "   ".join(Ctrl_ip_entries) + "\n")

            # 儲存 Connection - DUT 設定
            ConDUT_entries = [PC_config["Con_DUT"][col].get() or "0" for col in range(pc_num)]
            f.write(f" ConDUT:     " + "   ".join(ConDUT_entries) + "\n")

            # 儲存 Connection - Interface 設定
            ConInterface_entries = [PC_config["Con_Interface"][col].get() or "0" for col in range(pc_num)]
            f.write(f" Intrfc:     " + "   ".join(ConInterface_entries) + "\n")

            # 儲存 PC IP 設定
            PC_ip_entries = [PC_config["PC_ip"][col].get() or "0 " for col in range(pc_num)]
            f.write(f" PC IP :     " + "   ".join(PC_ip_entries) + "\n")

            # 儲存 PC 數輛 for APP
            f.write(f"\n"+" PC num:    ")
            for num in range(pc_num):
                f.write(f" PC{num+1} ")
            f.write(f"\n")

            # 儲存 APP checkbox 設定
            for row in range(0, 10):
                apps_states = [str(int(PC_config["Apps"][row][col].get())) for col in range(pc_num)]
                f.write(f" APP{row+1}:       " + "    ".join(apps_states) +"\n")

            f.write(f"\n"+" ----- Comment -----" + "\n")
            for i in range(0, 10):
                app_txt = App_items[i]
                f.write(f" APP{i+1}: "+app_txt + "\n")

            messagebox.showinfo("Saved", "Config saved")

    # 儲存按鈕
    save_btn = tk.Button(tab2, text="Save Config", font=('Arial',12,), command=save_config)
    # save_btn.grid(row=18, column=0, columnspan=10, pady=10)
    save_btn.place(x=1050, y=580)

    # 啟動時load config
    def load_config():
        # messagebox.showinfo("Load config", "Load config")
        try:
            with open("config\Endurance_config.txt", "r") as f:
                lines = f.readlines()
                # 載入 enable 設定
                enable_values = lines[1].strip().split(": ")[1].split() # txt檔，APP 從第1列開始
                for col in range(pc_num):
                    PC_config["PC_enable"][col].set(int(enable_values[col]))

                # 載入 console 設定
                console_values = lines[2].strip().split(": ")[1].split()
                for col in range(pc_num):
                    PC_config["Console"][col].set(int(console_values[col]))

                # 載入 Ctrl_ip 設定
                Ctrl_ip_values = lines[3].strip().split(": ")[1].split()
                for col in range(pc_num):
                    PC_config["Ctrl_ip"][col].set(Ctrl_ip_values[col] if Ctrl_ip_values[col] != "0" else "")

                # 載入 Connection - DUT 設定
                ConDUT_values = lines[4].strip().split(": ")[1].split()
                for col in range(pc_num):
                    PC_config["Con_DUT"][col].set(ConDUT_values[col] if Ctrl_ip_values[col] != "0" else "")

                # 載入 Connection - Interface 設定
                Intrfc_values = lines[5].strip().split(": ")[1].split()
                for col in range(pc_num):
                    PC_config["Con_Interface"][col].set(Intrfc_values[col] if Ctrl_ip_values[col] != "0" else "")

                # 載入 PC_ip_entries 設定
                PC_ip_values = lines[6].strip().split(": ")[1].split()
                for col in range(pc_num):
                    PC_config["PC_ip"][col].set(PC_ip_values[col] if PC_ip_values[col] != "0" else "")

                # 載入 App 設定
                for row in range(0, 10):
                    app_values = lines[row+9].strip().split(": ")[1].split() # txt檔，APP 從第4列開始
                    # print(app_values)
                    for col in range(pc_num):
                        PC_config["Apps"][row][col].set(int(app_values[col]))

        except FileNotFoundError:
            print("No config file found. Using default settings.")

    load_config()
def DUT_config_tab():
    tab3 = tk.Frame(tab_main)
    tab_main.add(tab3, text='  DUT Config.  ')

Dashboard_tab()
PC_config_tab()
DUT_config_tab()

root.mainloop()
