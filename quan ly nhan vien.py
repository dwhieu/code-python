import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import os
from datetime import datetime
import pandas as pd

# Hàm lưu dữ liệu vào CSV
def save_to_csv(data, filename="employee_data.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Mã", "Tên", "Ngày sinh", "Giới tính", "Đơn vị", "Chức danh", "Số CMND", "Ngày cấp", "Nơi cấp"])
        writer.writerow(data)
# Hàm lưu dữ liệu vào CSV
def save_to_csv(data, filename="employee_data.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Mã", "Tên", "Ngày sinh", "Giới tính", "Đơn vị", "Chức danh", "Số CMND", "Ngày cấp", "Nơi cấp", "Loại đối tượng"])
        writer.writerow(data)

# Hàm xuất toàn bộ danh sách ra file Excel

def export_to_excel():
    try:
        df = pd.read_csv("employee_data.csv")

        # Chuyển đổi cột "Ngày sinh" sang datetime để sắp xếp
        df["Ngày sinh"] = pd.to_datetime(df["Ngày sinh"], format="%d/%m/%Y", errors="coerce")

        # Loại bỏ các hàng không hợp lệ và sắp xếp theo tuổi giảm dần
        df = df.dropna(subset=["Ngày sinh"])
        df = df.sort_values(by="Ngày sinh", ascending=True)  # Ngày sinh sớm -> tuổi cao hơn

        export_file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if export_file:
            df.to_excel(export_file, index=False)
            messagebox.showinfo("Thành công", "Xuất file Excel thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xuất file Excel: {str(e)}")


# Hàm hiển thị nhân viên có sinh nhật hôm nay
def show_today_birthdays():
    try:
        if not os.path.isfile("employee_data.csv"):
            messagebox.showinfo("Thông báo", "Không có dữ liệu nhân viên.")
            return

        today = datetime.now().strftime("%d/%m")
        with open("employee_data.csv", mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            birthdays = [row for row in reader if row["Ngày sinh"].startswith(today)]

        if birthdays:
            messagebox.showinfo("Sinh nhật hôm nay", "\n".join([f"{b['Tên']} - {b['Ngày sinh']}" for b in birthdays]))
        else:
            messagebox.showinfo("Thông báo", "Hôm nay không có ai sinh nhật.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể hiển thị sinh nhật hôm nay: {str(e)}")

# Hàm thêm nhân viên
def add_employee():
    data = [
        id_entry.get(),
        name_entry.get(),
        dob_entry.get(),
        gender_var.get(),
        unit_entry.get(),
        title_entry.get(),
        id_card_entry.get(),
        issue_date_entry.get(),
        issue_place_entry.get()
    ]

    if "" in data:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin.")
        return

    save_to_csv(data)
    messagebox.showinfo("Thành công", "Đã thêm nhân viên thành công!")
    for entry in [id_entry, name_entry, dob_entry, unit_entry, title_entry, id_card_entry, issue_date_entry, issue_place_entry]:
        entry.delete(0, tk.END)
    object_type_var.set("")


# Tạo các ô nhập liệu

def create_id_entry(root):
    tk.Label(root, text="Mã").place(x=50, y=55)
    entry = tk.Entry(root)
    entry.place(x=50, y=75, width=150)
    return entry

def create_name_entry(root):
    tk.Label(root, text="Tên").place(x=210, y=55)
    entry = tk.Entry(root)
    entry.place(x=210, y=75, width=180)
    return entry

def create_dob_entry(root):
    tk.Label(root, text="Ngày sinh (dd/mm/yyyy)").place(x=430, y=55)
    entry = tk.Entry(root)
    entry.place(x=430, y=75, width=200)
    return entry

def create_gender_entry(root):
    tk.Label(root, text="Giới tính").place(x=650, y=55)
    gender_var = tk.StringVar(value="Nam")
    tk.Radiobutton(root, text="Nam", variable=gender_var, value="Nam").place(x=650, y=75)
    tk.Radiobutton(root, text="Nữ", variable=gender_var, value="Nữ").place(x=750, y=75)
    return gender_var

def create_unit_entry(root):
    tk.Label(root, text="Đơn vị").place(x=50, y=105)
    entry = tk.Entry(root)
    entry.place(x=50, y=125, width=340)
    return entry

def create_title_entry(root):
    tk.Label(root, text="Chức danh").place(x=50, y=155)
    entry = tk.Entry(root)
    entry.place(x=50, y=175, width=340)
    return entry

def create_id_card_entry(root):
    tk.Label(root, text="Số CMND").place(x=430, y=105)
    entry = tk.Entry(root)
    entry.place(x=430, y=125, width=280)
    return entry

def create_issue_date_entry(root):
    tk.Label(root, text="Ngày cấp (dd/mm/yyyy)").place(x=715, y=105)
    entry = tk.Entry(root)
    entry.place(x=715, y=125, width=200)
    return entry

def create_issue_place_entry(root):
    tk.Label(root, text="Nơi cấp").place(x=430,y=155)
    entry = tk.Entry(root)
    entry.place(x=430, y=175, width=485)
    return entry

def create_object_type_selection(root):
    object_type_var = tk.StringVar()
    tk.Checkbutton(root, text="Là nhân viên",font=("Arial",13), variable=object_type_var, onvalue="Nhân viên", offvalue="").place(x=300, y=25)
    tk.Checkbutton(root, text="Là nhà cung cấp",font=("Arial",13,), variable=object_type_var, onvalue="Nhà cung cấp", offvalue="").place(x=450, y=25)
    return object_type_var

# Giao diện chính
root = tk.Tk()
root.title("Quản lý nhân viên")
root.geometry("950x300")  # Tăng chiều dài và chiều rộng cửa sổ

# Thêm dòng chữ "Thông tin nhân viên"
tk.Label(root, text="Thông tin nhân viên", font=("Arial", 16, "bold")).place(x=20, y=20)

# Khởi tạo các ô nhập liệu
id_entry = create_id_entry(root)
name_entry = create_name_entry(root)
dob_entry = create_dob_entry(root)
gender_var = create_gender_entry(root)
unit_entry = create_unit_entry(root)
title_entry = create_title_entry(root)
id_card_entry = create_id_card_entry(root)
issue_date_entry = create_issue_date_entry(root)
issue_place_entry = create_issue_place_entry(root)
object_type_var = create_object_type_selection(root)

# Các nút chức năng
tk.Button(root, text="Thêm nhân viên", command=add_employee).place(x=50, y=235)
tk.Button(root, text="Sinh nhật hôm nay", command=show_today_birthdays).place(x=200, y=235)
tk.Button(root, text="Xuất danh sách", command=export_to_excel).place(x=350, y=235)

root.mainloop()
