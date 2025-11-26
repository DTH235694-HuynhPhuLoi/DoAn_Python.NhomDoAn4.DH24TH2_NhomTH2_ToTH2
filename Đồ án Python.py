import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import mysql.connector
from PIL import Image, ImageTk
import os, platform, subprocess

# ====== KẾT NỐI CSDL ======
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="qlSach"
    )

# ====== HỖ TRỢ UI ======
def center_window(win, width, height):
    win.update_idletasks()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    x, y = int((sw - width) / 2), int((sh - height) / 2)
    win.geometry(f"{width}x{height}+{x}+{y}")
    win.resizable(False, False)

# ====== MÀN HÌNH ĐĂNG NHẬP ======
class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng nhập Hệ thống Nhà sách")
        center_window(root, 420, 400)

        # Gradient Canvas
        self.canvas = tk.Canvas(root, width=420, height=400, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.draw_gradient(self.canvas, "#96f1b9", "#c4baf0")

        # Card đăng nhập
        card = tk.Frame(self.canvas, bg="white", bd=5, relief="raised")
        card.place(relx=0.5, rely=0.5, anchor="c", width=340, height=340)

        tk.Label(card, text="👋 Chào mừng trở lại", font=("Segoe UI",18,"bold"), fg="#1e88e5", bg="white").pack(pady=(20,5))
        tk.Label(card, text="Vui lòng đăng nhập để tiếp tục", font=("Segoe UI",10), fg="#757575", bg="white").pack(pady=(0,15))

        frame=tk.Frame(card,bg="white"); frame.pack(padx=20, fill="x")
        tk.Label(frame,text="Tên đăng nhập",font=("Segoe UI",10,"bold"),bg="white").pack(anchor="w")
        self.username=tk.Entry(frame,font=("Segoe UI",12)); self.username.pack(pady=2,fill="x",ipady=6)
        tk.Label(frame,text="Mật khẩu",font=("Segoe UI",10,"bold"),bg="white").pack(anchor="w",pady=(5,0))
        self.password=tk.Entry(frame,font=("Segoe UI",12),show="*"); self.password.pack(pady=2,fill="x",ipady=6)
        tk.Button(card,text="Đăng nhập",bg="#1e88e5",fg="white",font=("Segoe UI",12,"bold"),command=self.login).pack(pady=15,ipadx=30)

    def draw_gradient(self, canvas, color1, color2):
        w, h = int(canvas['width']), int(canvas['height'])
        r1,g1,b1 = canvas.winfo_rgb(color1)
        r2,g2,b2 = canvas.winfo_rgb(color2)
        for i in range(h):
            nr = int(r1 + (r2-r1)*i/h)//256
            ng = int(g1 + (g2-g1)*i/h)//256
            nb = int(b1 + (b2-b1)*i/h)//256
            canvas.create_line(0,i,w,i,fill=f'#{nr:02x}{ng:02x}{nb:02x}')

    def login(self):
        user,pw=self.username.get().strip(),self.password.get().strip()
        if not user or not pw: return messagebox.showwarning("⚠️","Nhập tên đăng nhập và mật khẩu!")
        try:
            conn=connect_db(); cur=conn.cursor()
            cur.execute("SELECT quyen FROM taikhoan WHERE username=%s AND password=%s",(user,pw))
            res=cur.fetchone()
            cur.close(); conn.close()
        except Exception as e: messagebox.showerror("❌ Lỗi DB",str(e)); return

        if res:
            quyen=res[0].strip().lower()
            self.root.destroy()
            main_app(quyen,user)
        else:
            messagebox.showerror("❌","Sai tên đăng nhập hoặc mật khẩu!")

# ====== MÀN HÌNH CHÍNH ======
class MainApp:
    def __init__(self, root, quyen, username):
        self.root = root
        self.quyen = quyen
        self.username = username

        role = " Chủ" if quyen == "chu" else " Nhân viên"
        self.root.title(f"📚 Quản lý Nhà sách - ({role})")

        center_window(root, 1200, 760)
        self.root.configure(bg="#f7f9fc")

        # ============================
        #  HEADER + GRADIENT
        # ============================
        self.header = tk.Canvas(root, height=60, highlightthickness=0, bd=0)
        self.header.pack(fill="x")

        # --- Hàm tạo gradient ---
        def draw_gradient(canvas, color1, color2):
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            canvas.delete("gradient")

            white_len = int(width * 0.5)  

      
            r1, g1, b1 = root.winfo_rgb(color1)
            r2, g2, b2 = root.winfo_rgb(color2)

            grad_width = max(1, width - white_len)
            r_ratio = (r2 - r1) / grad_width
            g_ratio = (g2 - g1) / grad_width
            b_ratio = (b2 - b1) / grad_width

            for i in range(white_len):
                canvas.create_line(i, 0, i, height, fill=color1, tags="gradient")

            for i in range(grad_width):
                nr = int(r1 + r_ratio * i)
                ng = int(g1 + g_ratio * i)
                nb = int(b1 + b_ratio * i)
                color = f"#{nr//256:02x}{ng//256:02x}{nb//256:02x}"
                canvas.create_line(white_len + i, 0, white_len + i, height, fill=color, tags="gradient")

        self.header.bind("<Configure>", lambda e: draw_gradient(self.header, "#ffffff", "#eab0f3"))

        # Logo
        try:
            img = Image.open(r"C:\Users\MyPC\OneDrive\Pictures\sach.png").resize((40, 40))
            self.logo = ImageTk.PhotoImage(img)
            logo_lbl = tk.Label(root, image=self.logo, bg="#000000")
        except:
            logo_lbl = tk.Label(root, text="📘", font=("Segoe UI", 22), bg="#ffffff")

        # Tiêu đề
        title_lbl = tk.Label(
             root,
            text=f"Hệ thống Quản lý Nhà Sách | Xin chào, {username} ({role})",
            font=("Segoe UI", 12, "bold"),
            bg="#ffffff"
            )
                

        # Nút logout
        logout_btn = tk.Button(
            root,
            text="🚪 Đăng xuất",
            bg="#F44336",
            fg="white",
            command=self.logout
        )

        # Đặt widget lên canvas
        self.header.create_window(15, 30, window=logo_lbl, anchor="w")
        self.header.create_window(70, 30, window=title_lbl, anchor="w")
        self.header.create_window(1150, 30, window=logout_btn, anchor="e")

        # ============================
        #  TABS
        # ============================
        tabs = ttk.Notebook(root)

        self.book_tab = ttk.Frame(tabs)
        self.sale_tab = ttk.Frame(tabs)
        self.invoice_tab = ttk.Frame(tabs)

        tabs.add(self.book_tab, text="📚 Quản lý Sách")
        tabs.add(self.sale_tab, text="🛒 Bán Sách")
        tabs.add(self.invoice_tab, text="🧾 Quản lý Hoá Đơn")

        if quyen == "chu":
            self.emp_tab = ttk.Frame(tabs)
            tabs.add(self.emp_tab, text="👥 Quản lý Nhân viên")

        tabs.pack(expand=1, fill="both", padx=10, pady=10)

        # ============================
        #  KHỞI TẠO CLASS TAB
        # ============================
        BookManager(self.book_tab)
        SaleManager(self.sale_tab, username)
        InvoiceManager(self.invoice_tab)

        if quyen == "chu":
            EmployeeManager(self.emp_tab)

    # ============================
    #  HÀM ĐĂNG XUẤT
    # ============================
    def logout(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            self.root.destroy()
            main_app("login")

# ====== QUẢN LÝ SÁCH ======
class BookManager:
    def __init__(self,root):
        frame=tk.LabelFrame(root,text="📘 Thông tin sách",font=("Segoe UI",11)); frame.pack(fill="x",padx=10,pady=5)
        labels=["Mã sách","Tên sách","Tác giả","Thể loại","Giá bán","Số lượng"]
        self.entries={}; 
        for i,l in enumerate(labels):
            tk.Label(frame,text=l,font=("Segoe UI",10)).grid(row=i//3,column=(i%3)*2,padx=5,pady=5,sticky="w")
            e=tk.Entry(frame,width=30); e.grid(row=i//3,column=(i%3)*2+1,padx=5,pady=5); self.entries[l]=e
        btn_frame=tk.Frame(root); btn_frame.pack(fill="x",padx=10,pady=5)
        tk.Button(btn_frame,text="➕ Thêm",bg="#2196F3",fg="white",command=self.add_book).pack(side="left",padx=5)
        tk.Button(btn_frame,text="✏️ Sửa",bg="#FFC107",command=self.update_book).pack(side="left",padx=5)
        tk.Button(btn_frame,text="🗑️ Xóa",bg="#F44336",fg="white",command=self.delete_book).pack(side="left",padx=5)
        tk.Button(btn_frame,text="🔄 Tải lại",bg="#9C27B0",fg="white",command=self.load_data).pack(side="left",padx=5)

        table=tk.Frame(root); table.pack(fill="both",expand=True,padx=10,pady=10)
        self.tree=ttk.Treeview(table,columns=("ma","ten","tg","tl","gia","sl"),show="headings")
        for col,text in zip(("ma","ten","tg","tl","gia","sl"),("📕 Mã sách","📗 Tên sách","✍️ Tác giả","🏷️ Thể loại","💰 Giá","📦 SL")):
            self.tree.heading(col,text=text); self.tree.column(col,anchor="center",width=150)
        vsb=ttk.Scrollbar(table,orient="vertical",command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left",fill="both",expand=True); vsb.pack(side="right",fill="y")
        self.tree.bind("<ButtonRelease-1>",self.select_row)
        self.load_data()

    def load_data(self):
        try: conn=connect_db(); cur=conn.cursor(); cur.execute("SELECT * FROM qlsach"); rows=cur.fetchall(); cur.close(); conn.close()
        except: rows=[]
        self.tree.delete(*self.tree.get_children()); [self.tree.insert("", "end", values=r) for r in rows]

    def add_book(self):
        values=tuple(self.entries[l].get().strip() for l in self.entries)
        if any(v=="" for v in values): return messagebox.showwarning("⚠️","Điền đủ thông tin!")
        try: conn=connect_db(); cur=conn.cursor(); cur.execute("INSERT INTO qlsach VALUES (%s,%s,%s,%s,%s,%s)",values); conn.commit(); cur.close(); conn.close(); self.load_data(); messagebox.showinfo("✅","Đã thêm sách!")
        except Exception as e: messagebox.showerror("❌",str(e))

    def update_book(self):
        ma=self.entries["Mã sách"].get().strip(); 
        if not ma: return messagebox.showwarning("⚠️","Nhập Mã sách!")
        try:
            ten=self.entries["Tên sách"].get().strip()
            tg=self.entries["Tác giả"].get().strip()
            tl=self.entries["Thể loại"].get().strip()
            gia=float(self.entries["Giá bán"].get())
            sl=int(self.entries["Số lượng"].get())
            conn=connect_db(); cur=conn.cursor()
            cur.execute("UPDATE qlsach SET ten_sach=%s, tac_gia=%s, the_loai=%s, gia_ban=%s, so_luong=%s WHERE ma_sach=%s",(ten,tg,tl,gia,sl,ma))
            conn.commit(); cur.close(); conn.close(); self.load_data(); messagebox.showinfo("✅","Đã cập nhật!")
        except Exception as e: messagebox.showerror("❌",str(e))

    def delete_book(self):
        ma=self.entries["Mã sách"].get().strip()
        if not ma: return messagebox.showwarning("⚠️","Chưa chọn sách!")
        if not messagebox.askyesno("Xác nhận",f"Xóa sách '{ma}'?"): return
        try: conn=connect_db(); cur=conn.cursor(); cur.execute("DELETE FROM qlsach WHERE ma_sach=%s",(ma,)); conn.commit(); cur.close(); conn.close(); self.load_data(); messagebox.showinfo("🗑️","Đã xóa!")
        except Exception as e: messagebox.showerror("❌",str(e))

    def select_row(self,e):
        sel=self.tree.focus(); d=self.tree.item(sel,"values")
        if d:
            for i,k in enumerate(self.entries):
                self.entries[k].delete(0,tk.END)
                self.entries[k].insert(0,d[i])

# ====== QUẢN LÝ BÁN HÀNG ======
class SaleManager:
    def __init__(self, root, username):
        self.root=root; self.username=username; self.cart=[]
        self.checkout_data = {} 
        
        top=tk.Frame(root); top.pack(fill="x",padx=10,pady=5)
        sf=tk.LabelFrame(top,text="Tìm sách",font=("Segoe UI",10)); sf.pack(side="left",fill="y",padx=5)
        tk.Label(sf,text="Từ khóa (mã sách):").pack(anchor="w",padx=5)
        self.search_var=tk.StringVar(); self.search_var.trace_add("write", lambda *a:self.load_books())
        tk.Entry(sf,textvariable=self.search_var,width=30).pack(padx=5,pady=3)
        tk.Button(sf,text="✖ Xóa",command=lambda:self.search_var.set("")).pack(padx=5,pady=3)
        
        lf=tk.LabelFrame(top,text="📚 Danh sách Sách",font=("Segoe UI",11)); lf.pack(side="left",fill="both",expand=True,padx=5)
        self.tree_books=ttk.Treeview(lf,columns=("ma","ten","tg","tl","gia","sl"),show="headings",height=8)
        for col,text in zip(("ma","ten","tg","tl","gia","sl"),("📕 Mã","📗 Tên","✍️ TG","🏷️ TL","💰 Giá","📦 Tồn")):
            self.tree_books.heading(col,text=text); self.tree_books.column(col,anchor="center",width=130)
        vsb=ttk.Scrollbar(lf,orient="vertical",command=self.tree_books.yview); self.tree_books.configure(yscrollcommand=vsb.set)
        self.tree_books.pack(side="left",fill="both",expand=True); vsb.pack(side="right",fill="y")
        self.tree_books.bind("<ButtonRelease-1>",self.select_book)
        self.load_books()

        f=tk.Frame(root); f.pack(fill="x",padx=10,pady=5)
        tk.Label(f,text="📕 Mã sách").grid(row=0,column=0,padx=5,pady=5)
        tk.Label(f,text="📦 SL").grid(row=0,column=2,padx=5,pady=5)
        self.ma_sach=tk.Entry(f); self.so_luong=tk.Entry(f,width=10)
        self.ma_sach.grid(row=0,column=1,padx=5); self.so_luong.grid(row=0,column=3,padx=5)
        tk.Button(f,text="🧾 Thêm",bg="#4CAF50",fg="white",command=self.add_to_cart).grid(row=0,column=4,padx=5)
        tk.Button(f,text="🔄 Làm mới",bg="#9C27B0",fg="white",command=self.load_books).grid(row=0,column=5,padx=5)

        cf=tk.LabelFrame(root,text="🛒 Giỏ hàng",font=("Segoe UI",11)); cf.pack(fill="both",expand=True,padx=10,pady=5)
        self.tree_cart=ttk.Treeview(cf,columns=("ma","ten","sl","gia","tong"),show="headings")
        for c,t in zip(("ma","ten","sl","gia","tong"),("📕 Mã","📗 Tên","📦 SL","💰 Giá","💵 Thành tiền")):
            self.tree_cart.heading(c,text=t); self.tree_cart.column(c,anchor="center",width=160)
        vsb2=ttk.Scrollbar(cf,orient="vertical",command=self.tree_cart.yview); self.tree_cart.configure(yscrollcommand=vsb2.set)
        self.tree_cart.pack(side="left",fill="both",expand=True); vsb2.pack(side="right",fill="y")

        bf=tk.Frame(root); bf.pack(fill="x",padx=10,pady=8)
        tk.Button(bf,text="🗑️ Xóa khỏi giỏ",bg="#F44336",fg="white",command=self.remove_from_cart).pack(side="left",padx=5)
        tk.Button(bf,text="💳 Thanh toán",bg="#2196F3",fg="white",font=("Segoe UI",11,"bold"),command=self.checkout).pack(side="right",padx=5)

    def load_books(self):
        key=self.search_var.get().strip()
        try:
            conn=connect_db(); cur=conn.cursor()
            if not key: cur.execute("SELECT * FROM qlsach")
            else:
                like=f"%{key}%"
                cur.execute("SELECT * FROM qlsach WHERE ma_sach LIKE %s ",(like,))
            rows=cur.fetchall(); cur.close(); conn.close()
        except: rows=[]
        self.tree_books.delete(*self.tree_books.get_children()); [self.tree_books.insert("", "end", values=r) for r in rows]

    def select_book(self,e):
        sel=self.tree_books.focus(); d=self.tree_books.item(sel,"values")
        if d: self.ma_sach.delete(0,tk.END); self.ma_sach.insert(0,d[0])

    def add_to_cart(self):
        ma=self.ma_sach.get().strip(); sl=self.so_luong.get().strip()
        if not ma or not sl: return messagebox.showwarning("⚠️","Nhập mã và SL!")
        try:
            sl=int(sl)
            if sl <= 0: return messagebox.showwarning("⚠️","SL phải lớn hơn 0!")
            
            conn=connect_db(); cur=conn.cursor()
            cur.execute("SELECT ten_sach,gia_ban,so_luong FROM qlsach WHERE ma_sach=%s",(ma,))
            res=cur.fetchone(); cur.close(); conn.close()
            if not res: return messagebox.showerror("❌","Không tìm thấy sách!")
            ten,gia,ton=res
            if sl>ton: return messagebox.showwarning("⚠️",f"Không đủ hàng! (Chỉ còn {ton})")
            
            for i,item in enumerate(self.cart):
                if item[0]==ma:
                    if item[2]+sl>ton: return messagebox.showwarning("⚠️",f"Không đủ hàng để cộng dồn! (Chỉ còn {ton})")
                    self.cart[i]=(ma,ten,item[2]+sl,gia,(item[2]+sl)*gia); self.refresh_cart(); return
            self.cart.append((ma,ten,sl,gia,sl*gia)); self.refresh_cart()
        except ValueError: messagebox.showwarning("⚠️","SL phải là số nguyên!")
        except Exception as e: messagebox.showerror("❌",str(e))

    def refresh_cart(self):
        self.tree_cart.delete(*self.tree_cart.get_children()); [self.tree_cart.insert("", "end", values=c) for c in self.cart]

    def remove_from_cart(self):
        sel=self.tree_cart.focus(); 
        if not sel: return messagebox.showwarning("⚠️","Chưa chọn mục!")
        ma=self.tree_cart.item(sel,"values")[0]
        if messagebox.askyesno("Xác nhận",f"Xóa mã {ma} khỏi giỏ?"):
            self.cart=[c for c in self.cart if c[0]!=ma]; self.refresh_cart()

    def _calculate_discount(self, points):
        if points >= 50:
            return 0.50, 50 
        elif points >= 40:
            return 0.40, 40
        elif points >= 30:
            return 0.30, 30
        elif points >= 20:
            return 0.20, 20
        elif points >= 10:
            return 0.10, 10
        else:
            return 0.0, 0 

    def _check_customer_points(self):
        sdt = self.sdt_kh_entry.get().strip()
        if not sdt:
            messagebox.showwarning("⚠️", "Vui lòng nhập SĐT!", parent=self.checkout_win)
            return

        tam_tinh = sum(item[4] for item in self.cart)
        current_points = 0
        
        try:
            conn = connect_db(); cur = conn.cursor()
            cur.execute("SELECT ten_kh, diem_tich_luy FROM khachhang WHERE sdt = %s", (sdt,))
            res = cur.fetchone()
            cur.close(); conn.close()
            
            if res: 
                ten_kh, current_points = res
                self.ten_kh_entry.delete(0, tk.END)
                self.ten_kh_entry.insert(0, ten_kh)
                self.lbl_info_diem.config(text=f"Điểm hiện tại: {current_points} điểm")
            else: 
                self.lbl_info_diem.config(text="Khách hàng mới (0 điểm)")
                current_points = 0
        
        except Exception as e:
            messagebox.showerror("❌ Lỗi DB", str(e), parent=self.checkout_win)
            return
        
        discount_percent, points_used = self._calculate_discount(current_points)
        giam_gia = tam_tinh * discount_percent
        final_total = tam_tinh - giam_gia
        
        self.lbl_giam_gia.config(text=f"Giảm giá ({points_used} điểm): -{giam_gia:,.0f}đ")
        self.lbl_thanh_tien.config(text=f"{final_total:,.0f}đ", font=("Segoe UI", 12, "bold"), fg="#dc3545")
        
        points_earned = sum(item[2] for item in self.cart) * 2
        
        self.checkout_data = {
            "sdt": sdt,
            "ten_kh": self.ten_kh_entry.get().strip(),
            "tam_tinh": tam_tinh,
            "giam_gia": giam_gia,
            "final_total": final_total,
            "current_points": current_points,
            "points_used": points_used,
            "points_earned": points_earned
        }

    def checkout(self):
        if not self.cart: 
            return messagebox.showwarning("⚠️","Giỏ hàng trống!")
        
        self.checkout_data = {}
        tam_tinh = sum(item[4] for item in self.cart)

        self.checkout_win = tk.Toplevel(self.root)
        self.checkout_win.title("Xác nhận Thanh toán")
        center_window(self.checkout_win, 450, 450) 
        self.checkout_win.transient(self.root)
        self.checkout_win.grab_set()

        f = tk.Frame(self.checkout_win, padx=15, pady=15)
        f.pack(expand=True, fill="both")

        info_frame = tk.Frame(f)
        info_frame.pack(fill="x", pady=5)
        
        tk.Label(info_frame, text="📞 Số điện thoại:", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.sdt_kh_entry = tk.Entry(info_frame, font=("Segoe UI", 10), width=18)
        self.sdt_kh_entry.grid(row=0, column=1, pady=5, padx=5)
        
        btn_check = tk.Button(info_frame, text="Kiểm tra SĐT", bg="#007bff", fg="white", command=self._check_customer_points)
        btn_check.grid(row=0, column=2, pady=5, padx=5)

        tk.Label(info_frame, text="👤 Tên khách hàng:", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.ten_kh_entry = tk.Entry(info_frame, font=("Segoe UI", 10), width=30)
        self.ten_kh_entry.grid(row=1, column=1, columnspan=2, pady=5, padx=5, sticky="w")

        ttk.Separator(f, orient="horizontal").pack(fill="x", pady=10)

        bill_frame = tk.Frame(f)
        bill_frame.pack(fill="x", pady=5)
        
        self.lbl_info_diem = tk.Label(bill_frame, text="Vui lòng 'Kiểm tra SĐT' để xem điểm", font=("Segoe UI", 10, "italic"), fg="blue")
        self.lbl_info_diem.pack(fill="x", pady=2)

        tk.Label(bill_frame, text=f"Tạm tính: {tam_tinh:,.0f}đ", font=("Segoe UI", 10)).pack(anchor="e", fill="x", pady=2)

        self.lbl_giam_gia = tk.Label(bill_frame, text="Giảm giá (Điểm): -0đ", font=("Segoe UI", 10, "bold"), fg="#007bff")
        self.lbl_giam_gia.pack(anchor="e", fill="x", pady=2)
        
        self.lbl_thanh_tien = tk.Label(bill_frame, text=f"{tam_tinh:,.0f}đ", font=("Segoe UI", 12, "bold"), fg="#dc3545")
        self.lbl_thanh_tien.pack(anchor="e", fill="x", pady=5)

        btn_frame = tk.Frame(f)
        btn_frame.pack(pady=(20, 0))
        
        tk.Button(btn_frame, text="✅ Xác nhận Thanh toán", bg="#28a745", fg="white", font=("Segoe UI", 11, "bold"), 
                  command=self._confirm_checkout).pack(side="left", padx=10, ipady=5)
        
        tk.Button(btn_frame, text="Hủy bỏ", bg="#6c757d", fg="white", font=("Segoe UI", 11),
                  command=self.checkout_win.destroy).pack(side="left", padx=10, ipady=5)
        
        self.root.wait_window(self.checkout_win)

    # ====== HÀM XÁC NHẬN THANH TOÁN ======
    def _confirm_checkout(self):
        if not self.checkout_data:
            messagebox.showwarning("⚠️", "Vui lòng bấm 'Kiểm tra SĐT' trước khi thanh toán!", parent=self.checkout_win)
            return
            
        ten_kh = self.ten_kh_entry.get().strip()
        if not ten_kh:
            messagebox.showwarning("⚠️", "Vui lòng nhập tên khách hàng!", parent=self.checkout_win)
            return

        data = self.checkout_data
        data["ten_kh"] = ten_kh 

        try:
            conn=connect_db(); cur=conn.cursor()
            ngay=datetime.now()
            
            new_total_points = data['current_points'] - data['points_used'] + data['points_earned']
            
            cur.execute(
                "INSERT INTO khachhang (sdt, ten_kh, diem_tich_luy) VALUES (%s, %s, %s) "
                "ON DUPLICATE KEY UPDATE ten_kh=%s, diem_tich_luy=%s",
                (data['sdt'], data['ten_kh'], new_total_points, data['ten_kh'], new_total_points)
            )
            
            cur.execute(
                "INSERT INTO hoadon (ngay_ban, tong_tien, sdt_kh, giam_gia_diem, diem_su_dung) "
                "VALUES (%s, %s, %s, %s, %s)",
                (ngay, data['final_total'], data['sdt'], data['giam_gia'], data['points_used'])
            )
            ma_hd=cur.lastrowid
        
            for ma,ten,sl,gia,tong in self.cart:
                cur.execute("UPDATE qlsach SET so_luong=so_luong-%s WHERE ma_sach=%s",(sl,ma))
                # Thêm 'ma_hd' vào câu lệnh INSERT
                cur.execute(
                    "INSERT INTO banhang(ma_sach,ten_sach,so_luong,tong_tien,ngay,ma_hd) "
                    "VALUES (%s,%s,%s,%s,%s,%s)",
                    (ma,ten,sl,tong,ngay,ma_hd)
                )
            
            conn.commit(); cur.close(); conn.close()

            invoice_id=f"HD{ma_hd:05d}"
            lines=[
                f"HÓA ĐƠN BÁN HÀNG - {invoice_id}",
                f"Ngày: {ngay.strftime('%Y-%m-%d %H:%M:%S')}",
                f"Nhân viên: {self.username}",
                f"Khách hàng: {data['ten_kh']} - SĐT: {data['sdt']}",
                "",
                "Mã    Tên sách                           SL         Giá      Thành tiền",
                "-"*90
            ]
            
            for ma,ten,sl,gia,tong in self.cart: 
                lines.append(f"{ma:<5} {ten[:35]:<35} {sl:>5} {gia:>12,.0f} {tong:>15,.0f}")
            
            lines.append("-"*90)
            lines.append(f"Tạm tính: {data['tam_tinh']:,.0f}đ")
            lines.append(f"Điểm hiện tại: {data['current_points']} điểm")
            lines.append(f"Điểm sử dụng: -{data['points_used']} điểm")
            lines.append(f"Giảm giá (Điểm): -{data['giam_gia']:,.0f}đ")
            lines.append(f"Điểm tích lũy (HĐ này): +{data['points_earned']} điểm")
            lines.append(f"TỔNG CỘNG: {data['final_total']:,.0f}đ")
            lines.append(f"Điểm cuối kỳ: {new_total_points} điểm")

            save=filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text file","*.txt")],title=f"Lưu hóa đơn {invoice_id}", parent=self.checkout_win)
            if save:
                with open(save,"w",encoding="utf-8") as f: f.write("\n".join(lines))
                try:
                    if platform.system()=="Windows": os.startfile(save)
                    elif platform.system()=="Darwin": subprocess.call(["open",save])
                    else: subprocess.call(["xdg-open",save])
                except: pass

            messagebox.showinfo("✅",f"Thanh toán thành công!\nMã hóa đơn: {invoice_id}")
            self.cart.clear(); self.refresh_cart(); self.load_books()
            self.checkout_win.destroy() 
        
        except Exception as e: 
            messagebox.showerror("❌",str(e), parent=self.checkout_win)
            
# ====== QUẢN LÝ NHÂN VIÊN ======
class EmployeeManager:
    def __init__(self,tab):
        f=tk.LabelFrame(tab,text="👥 Thông tin nhân viên",font=("Segoe UI",11,"bold")); f.pack(fill="x",padx=10,pady=5)
        tk.Label(f,text="👤 Username").grid(row=0,column=0,padx=5,pady=5,sticky="e")
        tk.Label(f,text="🔑 Password").grid(row=1,column=0,padx=5,pady=5,sticky="e")
        tk.Label(f,text="⚙️ Quyền").grid(row=2,column=0,padx=5,pady=5,sticky="e")
        self.username=tk.Entry(f,width=30); self.password=tk.Entry(f,width=30,show="*")
        self.role=ttk.Combobox(f,values=["nhanvien","chu"],state="readonly",width=28); self.role.current(0)
        self.username.grid(row=0,column=1); self.password.grid(row=1,column=1); self.role.grid(row=2,column=1)
        btn=tk.Frame(tab); btn.pack(fill="x",padx=10,pady=5)
        tk.Button(btn,text="➕ Thêm",bg="#2196F3",fg="white",command=self.add_user).pack(side="left",padx=5)
        tk.Button(btn,text="🗑️ Xóa",bg="#F44336",fg="white",command=self.delete_user).pack(side="left",padx=5)
        tk.Button(btn,text="🔄 Tải lại",bg="#9C27B0",fg="white",command=self.load_users).pack(side="left",padx=5)
        self.tree=ttk.Treeview(tab,columns=("username","role"),show="headings"); self.tree.heading("username",text="👤 Username"); self.tree.heading("role",text="⚙️ Quyền"); self.tree.pack(fill="both",expand=True,padx=10,pady=5)
        self.tree.bind("<ButtonRelease-1>",self.select_row)
        self.load_users()

    def load_users(self):
        try: conn=connect_db(); cur=conn.cursor(); cur.execute("SELECT username,quyen FROM taikhoan"); rows=cur.fetchall(); cur.close(); conn.close()
        except: rows=[]
        self.tree.delete(*self.tree.get_children()); [self.tree.insert("", "end", values=r) for r in rows]

    def add_user(self):
        u,p,r=self.username.get().strip(),self.password.get().strip(),self.role.get().strip()
        if not u or not p: return messagebox.showwarning("⚠️","Điền đầy đủ thông tin!")
        try: 
            conn=connect_db(); cur=conn.cursor()
            cur.execute("INSERT INTO taikhoan(username,password,quyen) VALUES(%s,%s,%s)",(u,p,r))
            conn.commit(); cur.close(); conn.close(); self.load_users()
        except Exception as e: messagebox.showerror("❌",str(e))

    def delete_user(self):
        u=self.username.get().strip()
        if not u: return messagebox.showwarning("⚠️","Chưa chọn nhân viên!")
        if not messagebox.askyesno("Xác nhận",f"Xóa nhân viên '{u}'?"): return
        try: conn=connect_db(); cur=conn.cursor(); cur.execute("DELETE FROM taikhoan WHERE username=%s",(u,)); conn.commit(); cur.close(); conn.close(); self.load_users()
        except Exception as e: messagebox.showerror("❌",str(e))

    def select_row(self,e):
        sel=self.tree.focus(); d=self.tree.item(sel,"values")
        if d: self.username.delete(0,tk.END); self.username.insert(0,d[0]); self.role.set(d[1])

# ====== QUẢN LÝ HOÁ ĐƠN ======
class InvoiceManager:
    def __init__(self, tab):
        self.tab = tab
        
        # --- Main Frames ---
        # Chia 2 khung: Trên (danh sách HĐ), Dưới (chi tiết HĐ)
        top_frame = tk.Frame(tab, height=300); top_frame.pack(fill="x", padx=10, pady=(10, 5))
        bottom_frame = tk.Frame(tab); bottom_frame.pack(fill="both", expand=True, padx=10, pady=5)

        lf_invoices = tk.LabelFrame(top_frame, text="🧾 Danh sách Hoá đơn", font=("Segoe UI", 11, "bold"))
        lf_invoices.pack(fill="both", expand=True)

        tk.Button(lf_invoices, text="🔄 Tải lại", bg="#007bff", fg="white", command=self.load_invoices).pack(side="top", anchor="e", padx=5, pady=5)

        cols_invoice = ("ma_hd", "ngay_ban", "sdt_kh", "giam_gia", "diem_sd", "tong_tien")
        headings_invoice = ("Mã HĐ", "Ngày bán", "SĐT Khách", "Giảm giá (Điểm)", "Điểm SD", "Tổng tiền")
        
        self.tree_invoices = ttk.Treeview(lf_invoices, columns=cols_invoice, show="headings", height=10)
        for col, heading in zip(cols_invoice, headings_invoice):
            self.tree_invoices.heading(col, text=heading)
            self.tree_invoices.column(col, anchor="w", width=150)
        
        # Tùy chỉnh cột
        self.tree_invoices.column("ma_hd", width=80, anchor="center")
        self.tree_invoices.column("tong_tien", width=120, anchor="e")
        self.tree_invoices.column("giam_gia", width=120, anchor="e")
        self.tree_invoices.column("diem_sd", width=80, anchor="center")

        # Scrollbars cho tree_invoices
        vsb_invoice = ttk.Scrollbar(lf_invoices, orient="vertical", command=self.tree_invoices.yview)
        hsb_invoice = ttk.Scrollbar(lf_invoices, orient="horizontal", command=self.tree_invoices.xview)
        self.tree_invoices.configure(yscrollcommand=vsb_invoice.set, xscrollcommand=hsb_invoice.set)

        vsb_invoice.pack(side="right", fill="y")
        hsb_invoice.pack(side="bottom", fill="x")
        self.tree_invoices.pack(side="left", fill="both", expand=True)
        
        # Bind sự kiện click
        self.tree_invoices.bind("<ButtonRelease-1>", self.on_invoice_select)

        lf_details = tk.LabelFrame(bottom_frame, text="📦 Chi tiết Hoá đơn", font=("Segoe UI", 11, "bold"))
        lf_details.pack(fill="both", expand=True)

        cols_detail = ("ma_sach", "ten_sach", "so_luong", "thanh_tien")
        headings_detail = ("Mã Sách", "Tên Sách", "Số lượng", "Thành tiền")

        self.tree_details = ttk.Treeview(lf_details, columns=cols_detail, show="headings")
        for col, heading in zip(cols_detail, headings_detail):
            self.tree_details.heading(col, text=heading)
            self.tree_details.column(col, anchor="w", width=200)

        self.tree_details.column("so_luong", width=100, anchor="center")
        self.tree_details.column("thanh_tien", width=150, anchor="e")
        
        vsb_detail = ttk.Scrollbar(lf_details, orient="vertical", command=self.tree_details.yview)
        self.tree_details.configure(yscrollcommand=vsb_detail.set)
        
        vsb_detail.pack(side="right", fill="y")
        self.tree_details.pack(side="left", fill="both", expand=True)
        
        # Tải DS Hóa đơn khi mở tab
        self.load_invoices()

    def load_invoices(self):
        # Xóa dữ liệu cũ
        self.tree_invoices.delete(*self.tree_invoices.get_children())
        self.tree_details.delete(*self.tree_details.get_children())
        
        try:
            conn = connect_db(); cur = conn.cursor()
            # Lấy các cột cần thiết, sắp xếp HĐ mới nhất lên đầu
            cur.execute("SELECT ma_hd, ngay_ban, sdt_kh, giam_gia_diem, diem_su_dung, tong_tien FROM hoadon ORDER BY ma_hd DESC")
            rows = cur.fetchall()
            cur.close(); conn.close()
            
            for row in rows:
                self.tree_invoices.insert("", "end", values=row)
                
        except Exception as e:
            messagebox.showerror("❌ Lỗi DB", f"Không thể tải danh sách hoá đơn: {str(e)}")

    def on_invoice_select(self, event):
        selected_item = self.tree_invoices.focus()
        if not selected_item:
            return
            
        try:
            invoice_data = self.tree_invoices.item(selected_item, "values")
            ma_hd = invoice_data[0] # Mã HĐ là cột đầu tiên
            self.load_invoice_details(ma_hd)
        except Exception:
             # Người dùng click vào khoảng trống
             pass

    def load_invoice_details(self, ma_hd):
        self.tree_details.delete(*self.tree_details.get_children())
        
        try:
            conn = connect_db(); cur = conn.cursor()
            # Lấy chi tiết từ bảng banhang
            cur.execute("SELECT ma_sach, ten_sach, so_luong, tong_tien FROM banhang WHERE ma_hd = %s", (ma_hd,))
            rows = cur.fetchall()
            cur.close(); conn.close()
            
            for row in rows:
                self.tree_details.insert("", "end", values=row)
                
        except Exception as e:
            messagebox.showerror("❌ Lỗi DB", f"Không thể tải chi tiết hoá đơn {ma_hd}: {str(e)}")


# ====== CHẠY APP ======
def main_app(mode,user=""):
    root=tk.Tk()
    if mode=="login": LoginScreen(root)
    else: MainApp(root,mode,user)
    root.mainloop()

if __name__=="__main__":
    main_app("login")