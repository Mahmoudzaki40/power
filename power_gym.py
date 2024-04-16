import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime, timedelta
import qrcode
import os
import logging
import io
import base64
import shutil
from PIL import Image
from io import BytesIO
from tkinter import PhotoImage

debt_tree = None  # تعريف المتغير كـ None للتأكد من توفره
subscription_duration_var = None  # تعريف المتغير عالميًا
price_options = None  # تعريف المتغير بشكل عام على مستوى الوحدة

# باقي الشيفرة
image_path_var = None
subscription_number_var = None


selected_image_path = None
from tkinter import PhotoImage

# اتصال بقاعدة البيانات SQLite
conn = sqlite3.connect('gym_database.db')
cursor = conn.cursor()

# استعلام SQL لاستعراض رقم الاشتراك من جدول MAIN
cursor.execute("SELECT رقم_الاشتراك FROM MAIN")

# استخراج القيمة المسترجعة (رقم الاشتراك) من الاستعلام
row = cursor.fetchone()
if row:
    subscription_number = row[0]
else:
    print("لم يتم العثور على رقم الاشتراك.")

conn.close()



# تكوين مستوى تسجيل الأخطاء
logging.basicConfig(filename='app.log', level=logging.DEBUG)

def open_subscriptions_page():
    try:
        # الشيفرة الحالية لفتح صفحة الاشتراكات

        # إذا كان هناك خطأ، يمكنك تسجيله باستخدام logging
        logging.error("حدث خطأ في open_subscriptions_page")
    except Exception as e:
        logging.error(f"حدث خطأ: {str(e)}")

    log_activity("الاشتراكات", "الاشتراكات.")

existing_members = []

# قم بتحديد المجلد الذي ترغب في حفظ الصور فيه


# Function to get the next member ID
def get_next_member_id():
    # In this example, we assume the list represents existing members
    # The next member ID is the length of the list + 1
    return len(existing_members) + 1




registration_date_var = None
subscription_number_var = None
name_var = None
age_var = None
phone_var = None
subscription_duration_var = None
subscription_status_var = None
notes_var = None
record_number_var = None
remaining_days_var = None  # إضافة المتغير للأيام المتبقية
image_label = None
edit_window = None
image_path_var = None  # تعريف المتغير في النطاق العلوي للبرنامج

# اتصال بقاعدة البيانات SQLite
conn = sqlite3.connect('gym_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS main (
        تاريخ_التسجيل TEXT,
        رقم_الاشتراك TEXT,
        الاسم TEXT,
        العمر TEXT,
        الهاتف TEXT,
        مدة_الاشتراك TEXT,
        حالة_الاشتراك TEXT,
        ملاحظات TEXT,
        رقم_السجل TEXT,
        تاريخ_الانتهاء TEXT,
        الأيام_المتبقية INTEGER,
        المبلغ_المدفوع REAL,
        تاريخ_الدفع TEXT,
        مسار_الصورة TEXT  -- إضافة حقل مسار_الصورة هنا
    )
''')
conn.commit()

# إغلاق اتصال قاعدة البيانات عند الانتهاء
conn.close()

import shutil


# اتصال بقاعدة البيانات
conn = sqlite3.connect('gym_database.db')
cursor = conn.cursor()

# إنشاء جدول IMAGES إذا لم يكن موجودًا بالفعل
cursor.execute('''
    CREATE TABLE IF NOT EXISTS IMAGES (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        SUBSCRIPTION_NUMBER TEXT,
        IMAGE_DATA TEXT
    )
''')

# قم بتأكيد الأمور وأغلق الاتصال
conn.commit()
conn.close()







def save_image(image_path, subscription_number):
    # تأكد من وجود المجلد المخصص لتخزين الصور
    image_folder = 'C:/Users/POWER KING/Desktop/sest/images'
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # قم بنسخ الصورة إلى المجلد المحدد
    destination_path = os.path.join(image_folder, f"{subscription_number}.jpg")
    shutil.copy(image_path, destination_path)

    # قم بتحديث مسار الصورة في قاعدة البيانات
    save_image_to_db(destination_path, subscription_number)

    # عين مسار الصورة للمتغير المناسب للعرض
    image_path_var.set(destination_path)


# الدالة لتحويل الصورة إلى تمثيل بيانات Base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        return image_data



# الدالة لتحويل البيانات Base64 إلى صورة
def base64_to_image(base64_data):
    image_binary = base64.b64decode(base64_data)
    image = Image.open(BytesIO(image_binary))
    return image


import logging

def save_image_to_db(image_path, subscription_number):
    try:
        conn = sqlite3.connect('gym_database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE main SET مسار_الصورة = ? WHERE رقم_الاشتراك = ?", (image_path, subscription_number))
        conn.commit()
    except sqlite3.Error as e:
        logging.error("حدث خطأ أثناء تحديث مسار الصورة في قاعدة البيانات: " + str(e))
    finally:
        conn.close()


# استرجاع الصورة من الجدول IMAGES
# الدالة لاسترجاع مسار الصورة من قاعدة البيانات
def get_image_path_from_db(subscription_number):
    try:
        conn = sqlite3.connect('gym_database.db')
        cursor = conn.cursor()

        # استعلام للاستعلام عن مسار الصورة المرتبط برقم الاشتراك
        cursor.execute("SELECT مسار_الصورة FROM MAIN WHERE رقم_الاشتراك=?", (subscription_number,))
        row = cursor.fetchone()

        if row:
            image_path = row[0]
            conn.close()
            return image_path
        else:
            conn.close()
            return None
    except sqlite3.Error as e:
        print("حدث خطأ أثناء استعلام قاعدة البيانات:", e)
        return None

import logging

def select_image():
    try:
        file_path = filedialog.askopenfilename()
        if file_path:
            subscription_number = get_subscription_number_for_image(file_path)
            image_data = image_to_base64(file_path)  # تحويل الصورة إلى بيانات بت نقية
            save_image_to_db(image_data, subscription_number)  # تمرير subscription_number هنا
            print("تم حفظ الصورة في قاعدة البيانات.")
            image_path_var.set(file_path)
    except Exception as e:
        logging.error("حدثت مشكلة أثناء حفظ الصورة في قاعدة البيانات. السبب: " + str(e))



import sqlite3

def get_subscription_number_for_image(image_path):
    try:
        conn = sqlite3.connect('gym_database.db')
        cursor = conn.cursor()

        # استعلام للحصول على رقم الاشتراك المرتبط بالصورة
        cursor.execute("SELECT رقم_الاشتراك FROM MAIN WHERE مسار_الصورة=?", (image_to_base64(image_path),))
        row = cursor.fetchone()

        if row:
            subscription_number = row[0]
            conn.close()
            return subscription_number
        else:
            conn.close()
            return None
    except sqlite3.Error as e:
        print("حدث خطأ أثناء استعلام قاعدة البيانات:", e)
        return None





# اتصال بقاعدة البيانات SQLite
conn = sqlite3.connect('gym_database.db')
cursor = conn.cursor()

# إنشاء جدول لأسعار الاشتراك
cursor.execute('''
    CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY,
        name TEXT,
        duration INTEGER,
        amount REAL
    )
''')

# إنشاء جدول جديد للأسعار الحالية
cursor.execute('''
    CREATE TABLE IF NOT EXISTS current_prices (
        id INTEGER PRIMARY KEY,
        name TEXT,
        duration INTEGER,
        amount REAL
    )
''')

conn.commit()




def get_current_prices():
    try:
        conn = sqlite3.connect('gym_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT amount FROM current_prices")
        rows = cursor.fetchall()
        conn.close()
        prices = [row[0] for row in rows]  # قائمة بالأسعار المحددة فقط
        return prices
    except sqlite3.Error as e:
        messagebox.showerror("خطأ", f"حدث خطأ أثناء استرجاع الأسعار: {str(e)}")
        return []



# دالة لنقل السعر المحدد إلى الجدول الجديد
def move_to_current_price(price_id):
    cursor.execute('SELECT * FROM prices WHERE id = ?', (price_id,))
    price_data = cursor.fetchone()

    if price_data:
        cursor.execute('INSERT INTO current_prices (name, duration, amount) VALUES (?, ?, ?)', price_data[1:])
        print("Data moved to current_prices table.")  # طباعة رسالة بنجاح نقل البيانات
    else:
        print("No data found in prices table for price ID:", price_id)

# دالة لإعادة السعر المحدد إلى الجدول القديم
def move_to_old_price(price_id):
    cursor.execute('SELECT * FROM current_prices WHERE id = ?', (price_id,))
    price_data = cursor.fetchone()

    if price_data:
        cursor.execute('INSERT INTO prices (name, duration, amount) VALUES (?, ?, ?)', price_data[1:])
        print("Data moved to prices table.")  # طباعة رسالة بنجاح نقل البيانات
    else:
        print("No data found in current_prices table for price ID:", price_id)

# تعديل الدوال الخاصة بالتحديد والغاء التحديد لتنفيذ دوال النقل
# دالة لتحديد السعر
# تحديد المتغيرات العامة
selected_prices = []

# دالة لتحديد السعر
# دالة لتحديد السعر
# دالة لتحديد السعر
def select_price(price_id):
    selected_prices.append(price_id)
    # نقل السعر المحدد إلى الجدول الجديد
    move_to_current_price(price_id)
    # عرض رسالة النجاح
    messagebox.showinfo("نجاح", "تم تحديد السعر بنجاح.")
    # Update offer based on the selected price
    handle_selected_price_for_offer()

# دالة لإلغاء تحديد السعر
# دالة لإلغاء تحديد السعر
# دالة لإلغاء تحديد السعر
# دالة لإلغاء تحديد السعر
def deselect_price(price_id):
    selected_prices.remove(price_id)
    # إذا كان السعر المحدد موجودًا في الجدول الحالي، قم بحذفه
    if is_price_in_current_prices(price_id):
        delete_price_from_current_prices(price_id)
        # عرض رسالة النجاح
        messagebox.showinfo("نجاح", "تم إلغاء تحديد السعر بنجاح.")
        # Update offer based on the deselected price
        handle_selected_price_for_offer()
        # تحديث عرض الأسعار في الواجهة الرسومية
        update_price_list()
    else:
        # عرض رسالة بأن السعر لم يتم العثور عليه في الجدول الحالي
        messagebox.showwarning("تحذير", "لم يتم العثور على السعر في الجدول الحالي.")

# دالة للتحقق مما إذا كان السعر موجودًا في الجدول الحالي
def is_price_in_current_prices(price_id):
    cursor.execute("SELECT id FROM current_prices WHERE id = ?", (price_id,))
    row = cursor.fetchone()
    return row is not None

# دالة لحذف السعر من الجدول الحالي
def delete_price_from_current_prices(price_id):
    cursor.execute("DELETE FROM current_prices WHERE id = ?", (price_id,))
    conn.commit()






# إعداد قاعدة البيانات
conn = sqlite3.connect('gym_database.db')
cursor = conn.cursor()

# متغير global لنافذة الرئيسية
root = None

# قائمة لتخزين الأسعار المحددة
selected_prices = []

# دالة لفتح نافذة إضافة قائمة سعر جديدة
def open_add_price_window():
    add_price_window = tk.Toplevel(root)
    add_price_window.title("إنشاء قائمة سعر")

    tk.Label(add_price_window, text="المعرف:").grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(add_price_window)
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_price_window, text="الاسم:").grid(row=1, column=0, padx=10, pady=5)
    name_entry = tk.Entry(add_price_window)
    name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_price_window, text="المدة بالأيام:").grid(row=2, column=0, padx=10, pady=5)
    duration_entry = tk.Entry(add_price_window)
    duration_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_price_window, text="السعر:").grid(row=3, column=0, padx=10, pady=5)
    amount_entry = tk.Entry(add_price_window)
    amount_entry.grid(row=3, column=1, padx=10, pady=5)

    def add_price():
        id = id_entry.get()
        name = name_entry.get()
        duration = duration_entry.get()
        amount = amount_entry.get()
        cursor.execute("INSERT INTO prices (id, name, duration, amount) VALUES (?, ?, ?, ?)",
                       (id, name, duration, amount))
        conn.commit()
        add_price_window.destroy()

    tk.Button(add_price_window, text="إضافة سعر", command=add_price).grid(row=4, columnspan=2, pady=10)
    log_activity("قائمة اسعار", "قائمة اسعار.")


def update_price_list():
    update_price_window = tk.Toplevel(root)
    update_price_window.title("عرض قوائم الأسعار")

    cursor.execute("SELECT id, name, duration, amount FROM prices")
    rows = cursor.fetchall()

    current_prices_names = get_current_prices_names()

    if rows:
        # إنشاء جدول لعرض الأسعار
        frame = tk.Frame(update_price_window)
        frame.pack()

        columns = ["المعرف", "الاسم", "المدة بالأيام", "السعر", "الحذف الجزئي", "الحذف النهائي"]
        for col_index, col_name in enumerate(columns):
            tk.Label(frame, text=col_name, relief=tk.RIDGE, width=15).grid(row=0, column=col_index)

        for row_index, row_data in enumerate(rows):
            for col_index, col_value in enumerate(row_data):
                if row_data[1] in current_prices_names:
                    label_color = 'blue'  # لون مختلف للسعر الموجود في جدول الأسعار الحالي
                else:
                    label_color = 'black'
                tk.Label(frame, text=col_value, relief=tk.RIDGE, width=15, fg=label_color).grid(row=row_index + 1,
                                                                                                column=col_index)

            # زري تعديل وحذف لكل صف
            edit_button = tk.Button(frame, text="تعديل", command=lambda row=row_data: edit_price(row))
            partial_delete_button = tk.Button(frame, text="حذف جزئي",
                                              command=lambda id=row_data[0]: delete_partial_price(id))
            final_delete_button = tk.Button(frame, text="حذف نهائي", command=lambda id=row_data[0]: delete_price(id))
            add_to_current_button = tk.Button(frame, text="إضافة للاسعار الحالية",
                                              command=lambda id=row_data[0], name=row_data[1], duration=row_data[2],
                                                             amount=row_data[3]: add_to_current_prices(id, name,
                                                                                                       duration,
                                                                                                       amount))

            edit_button.grid(row=row_index + 1, column=len(columns) + 1, padx=5)
            partial_delete_button.grid(row=row_index + 1, column=len(columns) + 2, padx=5)  # زر الحذف الجزئي
            final_delete_button.grid(row=row_index + 1, column=len(columns) + 3, padx=5)  # زر الحذف النهائي
            add_to_current_button.grid(row=row_index + 1, column=len(columns) + 4, padx=5)  # زر إضافة للاسعار الحالية

    else:
        tk.Label(update_price_window, text="لا توجد قوائم أسعار متاحة.").pack()

    conn.commit()


def add_to_current_prices(id, name, duration, amount):
    try:
        # التحقق من عدم وجود معرف السعر مسبقًا في الجدول الحالي
        cursor.execute("SELECT id FROM current_prices WHERE id=?", (id,))
        existing_id = cursor.fetchone()
        if existing_id:
            tk.messagebox.showwarning("تحذير", "السعر موجود بالفعل في جدول الأسعار الحالي.")
            return  # يتم إيقاف العملية إذا كان السعر موجودًا بالفعل

        # إضافة السعر إلى الجدول الحالي إذا لم يكن موجودًا بالفعل
        cursor.execute("INSERT INTO current_prices (id, name, duration, amount) VALUES (?, ?, ?, ?)",
                       (id, name, duration, amount))
        conn.commit()
        tk.messagebox.showinfo("نجاح", "تمت إضافة السعر بنجاح إلى جدول الأسعار الحالي.")
    except sqlite3.Error as e:
        tk.messagebox.showerror("خطأ", f"حدث خطأ أثناء إضافة السعر إلى جدول الأسعار الحالي: {str(e)}")






def get_current_prices_names():
    cursor.execute("SELECT name FROM current_prices")
    current_prices = cursor.fetchall()
    return [price[0] for price in current_prices]



# دالة للتعامل مع السعر المحدد للعرض
# دالة للتعامل مع السعر المحدد للعرض
def handle_selected_price_for_offer():
    if selected_prices:
        selected_price_id = selected_prices[0]
        print("Selected price ID:", selected_price_id)

        # هنا يمكنك استخدام معرف السعر المحدد لتنفيذ تعاملات العرض
        # مثلا يمكنك استخدامه لاسترجاع معلومات السعر المحدد وعرضها للمستخدم
        cursor.execute('SELECT * FROM prices WHERE id = ?', (selected_price_id,))
        selected_price_data = cursor.fetchone()
        if selected_price_data:
            print("Selected price details:", selected_price_data)
        else:
            print("No data found for selected price ID:", selected_price_id)



# تعديل الدوال الخاصة بالتحديد والغاء التحديد لتنفيذ دوال النقل

# متغير global لتخزين السعر المحدد
selected_prices = []

# إعداد قاعدة البيانات
conn = sqlite3.connect('gym_database.db')
cursor = conn.cursor()

# دالة لفتح نافذة تعديل قائمة سعر
def edit_price(row_data):
    edit_price_window = tk.Toplevel(root)
    edit_price_window.title("تعديل قائمة سعر")

    tk.Label(edit_price_window, text="المعرف:").grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(edit_price_window)
    id_entry.grid(row=0, column=1, padx=10, pady=5)
    id_entry.insert(0, row_data[0])

    tk.Label(edit_price_window, text="الاسم:").grid(row=1, column=0, padx=10, pady=5)
    name_entry = tk.Entry(edit_price_window)
    name_entry.grid(row=1, column=1, padx=10, pady=5)
    name_entry.insert(0, row_data[1])

    tk.Label(edit_price_window, text="المدة بالأيام:").grid(row=2, column=0, padx=10, pady=5)
    duration_entry = tk.Entry(edit_price_window)
    duration_entry.grid(row=2, column=1, padx=10, pady=5)
    duration_entry.insert(0, row_data[2])

    tk.Label(edit_price_window, text="السعر:").grid(row=3, column=0, padx=10, pady=5)
    amount_entry = tk.Entry(edit_price_window)
    amount_entry.grid(row=3, column=1, padx=10, pady=5)
    amount_entry.insert(0, row_data[3])

    def update_price():
        new_id = id_entry.get()
        new_name = name_entry.get()
        new_duration = duration_entry.get()
        new_amount = amount_entry.get()
        cursor.execute("UPDATE prices SET id=?, name=?, duration=?, amount=? WHERE id=?",
                       (new_id, new_name, new_duration, new_amount, row_data[0]))
        conn.commit()
        edit_price_window.destroy()

        # If the updated price was selected, update the offer accordingly
        if row_data[0] in selected_prices:
            handle_selected_price_for_offer()

    tk.Button(edit_price_window, text="تحديث السعر", command=update_price).grid(row=4, columnspan=2, pady=10)

# قائمة لتخزين الأسعار المحذوفة
deleted_prices = []

# دالة لتحديد السعر للحذف
def delete_price(id):
    result = tk.messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد أنك تريد حذف هذا السعر؟")
    if result:
        cursor.execute("DELETE FROM prices WHERE id=?", (id,))
        conn.commit()
        tk.messagebox.showinfo("تم الحذف", "تم حذف السعر بنجاح.")
        # إضافة معرف السعر المحذوف إلى القائمة
        deleted_prices.append(id)
        # تحديث العرض إذا كان السعر المحذوف محددًا
        if id in selected_prices:
            selected_prices.remove(id)
            handle_selected_price_for_offer()

# دالة لحذف السعر من الجدول الحالي دون مسحه من جدول الأسعار
# دالة لحذف السعر من الجدول الحالي دون مسحه من جدول الأسعار
def delete_partial_price(id):
    result = messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد أنك تريد حذف عرض السعر؟")
    if result:
        # احصل على معرف العرض
        cursor.execute("SELECT id FROM prices WHERE id=?", (id,))
        row = cursor.fetchone()
        if row:
            # إذا كان هناك سجل في جدول الأسعار
            cursor.execute("DELETE FROM current_prices WHERE id=?", (id,))
            conn.commit()
            tk.messagebox.showinfo("تم الحذف", "تم حذف عرض السعر بنجاح من جدول الأسعار الحالي.")
            update_price_list()
        else:
            tk.messagebox.showwarning("تحذير", "العرض غير موجود في جدول الأسعار.")




def remove_from_current_price(name):
    cursor.execute("DELETE FROM current_prices WHERE name=?", (name,))
    conn.commit()






# دالة لإعادة السعر المحذوف إلى الجدول القديم
def restore_price(id):
    cursor.execute('SELECT * FROM prices WHERE id = ?', (id,))
    price_data = cursor.fetchone()

    if price_data:
        cursor.execute('INSERT INTO prices (name, duration, amount) VALUES (?, ?, ?)', price_data[1:])
        print("Data restored to prices table.")
        # إزالة معرف السعر المحذوف من القائمة
        deleted_prices.remove(id)
    else:
        print("No data found for price ID:", id)

# دالة لإلغاء تحديد السعر
def deselect_price(price_id):
    selected_prices.remove(price_id)
    # تحديث العرض إذا كان السعر المحذوف محددًا
    if price_id in deleted_prices:
        restore_price(price_id)
    # عرض رسالة النجاح
    messagebox.showinfo("نجاح", "تم إلغاء تحديد السعر بنجاح.")



def get_price_for_duration(duration):
    try:
        conn = sqlite3.connect('gym_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT amount FROM current_prices WHERE duration <= ? ORDER BY duration DESC LIMIT 1", (duration,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
    except sqlite3.Error as e:
        messagebox.showerror("خطأ", f"حدث خطأ أثناء استرجاع السعر: {str(e)}")
    return None

def calculate_subscription_price(days):
    try:
        conn = sqlite3.connect('gym_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT amount FROM current_prices WHERE duration <= ? ORDER BY duration DESC LIMIT 1", (days,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
    except sqlite3.Error as e:
        messagebox.showerror("خطأ", f"حدث خطأ أثناء استرجاع السعر: {str(e)}")
    return None

payment_amount_entry = None

def process_payment():
    remaining_days = int(remaining_days_var.get())
    payment_type = payment_type_var.get()  # احصل على نوع المبلغ

    global payment_amount_entry  # تحديد أن المتغير يشير إلى المتغير العالمي

    if payment_type == "كامل":
        subscription_price = calculate_subscription_price(remaining_days)
        payment_amount_var.set(subscription_price)
        payment_amount_entry.config(state="disabled")  # تعطيل حقل إدخال المبلغ
    elif payment_type == "جزء":
        payment_amount_entry.config(state="normal")  # تمكين حقل إدخال المبلغ

    paid_amount = float(payment_amount_var.get())  # المبلغ المدفوع
    subscription_price = calculate_subscription_price(remaining_days)  # السعر الاشتراك

    if paid_amount < subscription_price:
        remaining_debt = subscription_price - paid_amount
        age_note = f"دين: {remaining_debt}"
    else:
        age_note = ""




# دالة للحصول على الأسعار المتاحة من قاعدة البيانات
def get_available_prices():
    try:
        conn = sqlite3.connect('gym_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT amount FROM prices")
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows] if rows else []
    except sqlite3.Error as e:
        messagebox.showerror("خطأ", f"حدث خطأ أثناء استرجاع الأسعار: {str(e)}")
        return []




def get_debt_subscribers(search_query=None, search_type=None):
    try:
        conn = sqlite3.connect('gym_database.db')
        cursor = conn.cursor()
        query = "SELECT * FROM main WHERE العمر LIKE 'دين%'"
        if search_type and search_query:
            if search_type == "الاسم":
                query += f" AND الاسم LIKE '%{search_query}%'"
            elif search_type == "رقم الاشتراك":
                query += f" AND رقم_الاشتراك = '{search_query}'"
            elif search_type == "رقم السجل":
                query += f" AND رقم_السجل = '{search_query}'"
            elif search_type == "الهاتف":
                query += f" AND الهاتف = '{search_query}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        print("حدث خطأ أثناء استعلام قاعدة البيانات:", e)
        return []

def pay_debt(subscriber_id, paid_amount):
    try:
        conn = sqlite3.connect('gym_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT المبلغ_المدفوع, مدة_الاشتراك FROM main WHERE رقم_الاشتراك = ?", (subscriber_id,))
        result = cursor.fetchone()

        if result:
            paid, subscription_duration = result
            remaining_debt = calculate_subscription_price(subscription_duration) - (paid + paid_amount)

            if remaining_debt <= 0:
                # إذا كان المبلغ المتبقي للدين أقل من أو يساوي صفر، قم بتحديث المبلغ المدفوع واحذف الدين
                cursor.execute("UPDATE main SET المبلغ_المدفوع = ?, العمر = ? WHERE رقم_الاشتراك = ?", (paid + paid_amount, "", subscriber_id))
            else:
                # إذا كان هناك مبلغ دين متبقي، قم بتحديث المبلغ المدفوع والدين المتبقي
                cursor.execute("UPDATE main SET المبلغ_المدفوع = ?, العمر = ? WHERE رقم_الاشتراك = ?", (paid + paid_amount, f"دين: {remaining_debt}", subscriber_id))

            conn.commit()
            conn.close()
            messagebox.showinfo("نجاح", "تم سداد المبلغ بنجاح.")
            # قم بتحديث قائمة الديون لعرض البيانات المحدثة
            refresh_debt_list()
        else:
            conn.close()
            messagebox.showerror("خطأ", "لم يتم العثور على المشترك.")
    except sqlite3.Error as e:
        print("حدث خطأ أثناء تحديث الدين:", e)
        messagebox.showerror("خطأ", "حدث خطأ أثناء تحديث الدين")


def refresh_debt_list():
    # تحديث قائمة الديون
    pass  # يمكنك تحديد تفاصيل التحديث هنا



def display_debt_subscribers():
    debt_window = tk.Toplevel()
    debt_window.title("المشتركين الذين لديهم دين")


    search_label = ttk.Label(debt_window, text="البحث:")
    search_label.pack()

    search_var = tk.StringVar()
    search_entry = ttk.Entry(debt_window, textvariable=search_var)
    search_entry.pack()

    search_type_label = ttk.Label(debt_window, text="نوع البحث:")
    search_type_label.pack()

    search_type_var = tk.StringVar()
    search_type_combobox = ttk.Combobox(debt_window, textvariable=search_type_var, values=["الاسم", "رقم الاشتراك", "رقم السجل", "الهاتف"])
    search_type_combobox.pack()

    search_button = ttk.Button(debt_window, text="ابحث", command=lambda: search_debt_subscribers(debt_tree, search_var.get(), search_type_var.get()))
    search_button.pack()

    debt_tree = ttk.Treeview(debt_window)
    debt_tree["columns"] = ("الاسم", "العمر", "تاريخ التسجيل", "رقم الاشتراك")

    debt_tree.column("#1", anchor=tk.W, width=200)
    debt_tree.column("#2", anchor=tk.W, width=200)
    debt_tree.column("#3", anchor=tk.W, width=200)
    debt_tree.column("#4", anchor=tk.W, width=200)

    debt_tree.heading("#1", text="الاسم")
    debt_tree.heading("#2", text="العمر")
    debt_tree.heading("#3", text="تاريخ التسجيل")
    debt_tree.heading("#4", text="رقم الاشتراك")

    debt_tree.pack()

    subscribers = get_debt_subscribers()  # Fetch all debt subscribers initially

    for subscriber in subscribers:
        debt_tree.insert("", tk.END, values=(subscriber[2], subscriber[3], subscriber[0], subscriber[1]))

    def search_debt_subscribers(tree, search_query, search_type):
        tree.delete(*tree.get_children())
        subscribers = get_debt_subscribers(search_query, search_type)
        for subscriber in subscribers:
            tree.insert("", tk.END, values=(subscriber[2], subscriber[3], subscriber[0], subscriber[1]))

    def pay_debt_selected():
        selected_item = debt_tree.selection()
        if selected_item:
            subscriber_id = debt_tree.item(selected_item[0])["values"][3]
            # Retrieve the existing debt amount from the 'العمر' field
            existing_debt = float(debt_tree.item(selected_item[0])["values"][1].split(' ')[-1])
            if existing_debt > 0:
                # Pay the full debt amount
                pay_debt(subscriber_id, existing_debt)
                messagebox.showinfo("نجاح", f"تم سداد الدين بنجاح: {existing_debt}")
                debt_window.destroy()
                display_debt_subscribers()

    pay_button = ttk.Button(debt_window, text="سداد الدين المحدد", command=pay_debt_selected)
    pay_button.pack()
    log_activity("الديون", "الديون.")
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import filedialog
import qrcode
price_options = None


def add_member():
    global member_window, registration_date_var, name_var, age_var, phone_var, subscription_duration_var, subscription_status_var, notes_var, record_number_var, remaining_days_var, payment_date_var, payment_amount_var, image_path_var, subscription_number_var, payment_type_var

    member_window = tk.Toplevel()
    member_window.title("إدراج مشترك جديد")
    member_window.geometry("1100x400")  # زيادة عرض النافذة

    frame = ttk.Frame(member_window)
    frame.pack(padx=15, pady=15)

    style = ttk.Style()
    style.configure('TEntry', relief="solid", borderwidth=2)
    style.configure('TCombobox', relief="solid", borderwidth=2)
    style.configure('TButton', relief="raised", borderwidth=2)

    # استرجاع الأسعار المحددة من جدول current_prices
    cursor.execute("SELECT name FROM current_prices")
    selected_prices = cursor.fetchall()

    # تحويل الأسعار المسترجعة إلى قائمة من الأسماء
    available_prices = [price[0] for price in selected_prices]

    price_options = ttk.Combobox(frame, textvariable=subscription_number_var, values=available_prices, width=35, style='TCombobox')
    price_options.grid(row=0, column=0, pady=10, padx=10)



    payment_type_var = tk.StringVar()
    payment_type_var.set("كامل")

    payment_type_frame = ttk.Frame(frame)
    payment_type_frame.grid(row=0, column=1, pady=10)

    ttk.Label(payment_type_frame, text="نوع الدفع:").pack(side=tk.LEFT, padx=10)

    ttk.Radiobutton(payment_type_frame, text="كامل", variable=payment_type_var, value="كامل").pack(side=tk.LEFT)
    ttk.Radiobutton(payment_type_frame, text="جزء", variable=payment_type_var, value="جزء").pack(side=tk.LEFT)

    registration_date_var = tk.StringVar()
    subscription_number_var = tk.StringVar()
    name_var = tk.StringVar()
    age_var = tk.StringVar()
    phone_var = tk.StringVar()
    subscription_duration_var = tk.StringVar()
    subscription_status_var = tk.StringVar()
    notes_var = tk.StringVar()
    record_number_var = tk.StringVar()
    remaining_days_var = tk.StringVar()
    payment_date_var = tk.StringVar()
    payment_amount_var = tk.StringVar()
    image_path_var = tk.StringVar()

    current_date = datetime.now().strftime("%Y-%m-%d")
    registration_date_var.set(current_date)

    if payment_date_var.get() == "":
        payment_date_var.set(current_date)

    payment_amount_var.set("")

    entry_width = 30  # تقليل عرض حقول الإدخال

    ttk.Label(frame, text="").grid(row=1, column=6, pady=10, padx=10)
    ttk.Label(frame, text="").grid(row=2, column=6, pady=10, padx=10)
    ttk.Label(frame, text="").grid(row=3, column=6, pady=10, padx=10)
    ttk.Label(frame, text="").grid(row=4, column=6, pady=10, padx=10)
    ttk.Label(frame, text="").grid(row=5, column=6, pady=10, padx=10)  # إضافة صف للملاحظات

    ttk.Label(frame, text="تاريخ التسجيل").grid(row=1, column=5)
    registration_date_entry = ttk.Entry(frame, textvariable=registration_date_var, width=entry_width, style='TEntry')
    registration_date_entry.grid(row=1, column=4)

    ttk.Label(frame, text="الاسم").grid(row=1, column=3)
    name_entry = ttk.Entry(frame, textvariable=name_var, width=entry_width, style='TEntry')
    name_entry.grid(row=1, column=2)

    ttk.Label(frame, text="رقم الاشتراك").grid(row=1, column=1)
    subscription_number_entry = ttk.Entry(frame, textvariable=subscription_number_var, width=entry_width, style='TEntry')
    subscription_number_entry.grid(row=1, column=0)

    ttk.Label(frame, text="مدة الاشتراك (أيام)").grid(row=2, column=5)
    subscription_duration_entry = ttk.Entry(frame, textvariable=subscription_duration_var, width=entry_width, style='TEntry')
    subscription_duration_entry.grid(row=2, column=4)

    ttk.Label(frame, text="الأيام المتبقية").grid(row=2, column=3)
    remaining_days_entry = ttk.Entry(frame, textvariable=remaining_days_var, width=entry_width, style='TEntry')
    remaining_days_entry.grid(row=2, column=2)

    ttk.Label(frame, text="حالة الاشتراك").grid(row=2, column=1)
    subscription_status_combobox = ttk.Combobox(frame, textvariable=subscription_status_var, values=["مستمر", "متوقف"], width=entry_width, style='TCombobox')
    subscription_status_combobox.grid(row=2, column=0)

    ttk.Label(frame, text="رقم السجل").grid(row=3, column=5)
    record_number_entry = ttk.Entry(frame, textvariable=record_number_var, width=entry_width, style='TEntry')
    record_number_entry.grid(row=3, column=4)

    ttk.Label(frame, text="رقم الهاتف").grid(row=3, column=3)
    phone_entry = ttk.Entry(frame, textvariable=phone_var, width=entry_width, style='TEntry')
    phone_entry.grid(row=3, column=2)

    ttk.Label(frame, text="الدين").grid(row=3, column=1)
    age_entry = ttk.Entry(frame, textvariable=age_var, width=entry_width, style='TEntry')
    age_entry.grid(row=3, column=0)

    ttk.Label(frame, text="المبلغ المدفوع").grid(row=4, column=5)
    payment_amount_entry = ttk.Entry(frame, textvariable=payment_amount_var, width=entry_width, style='TEntry')
    payment_amount_entry.grid(row=4, column=4)

    ttk.Label(frame, text="تاريخ الدفع").grid(row=4, column=3)
    payment_date_entry = ttk.Entry(frame, textvariable=payment_date_var, width=entry_width, style='TEntry')
    payment_date_entry.grid(row=4, column=2)

    ttk.Label(frame, text="مسار الصورة").grid(row=4, column=1)
    image_path_entry = ttk.Entry(frame, textvariable=image_path_var, width=entry_width, style='TEntry')
    image_path_entry.grid(row=4, column=0)

    ttk.Label(frame, text="الملاحظات").grid(row=5, column=2, padx=10)  # تحديث الموقع
    notes_label = ttk.Label(frame, text="")
    notes_entry = ttk.Entry(frame, textvariable=notes_var, width=entry_width, style='TEntry')
    notes_entry.grid(row=5, column=2,)  # تحديث الموقع والاستمرار على العرض

    select_image_button = ttk.Button(frame, text="اختيار صورة", command=select_image, style='TButton')
    select_image_button.grid(row=6, column=0, pady=10)

    generate_qr_code_button = ttk.Button(frame, text="QR Code", command=generate_qr_code, style='TButton')
    generate_qr_code_button.grid(row=6, column=1, pady=10)

    save_button = ttk.Button(frame, text="موافق",
                             command=lambda: save_member_data(member_window, subscription_number_var.get(),
                                                              upgrade_function=handle_selected_price_for_offer),
                             style='TButton')
    save_button.grid(row=6, column=2, pady=10)

    cancel_button = ttk.Button(frame, text="إلغاء", command=member_window.destroy, style='TButton')
    cancel_button.grid(row=6, column=3, pady=10)

    log_activity("إدراج مشترك جديد", "قام بإدراج مشترك جديد.")

def update_payment_amount(*args):
    global price_options
    subscription_duration = subscription_duration_var.get()
    if subscription_duration:
        try:
            subscription_duration = int(subscription_duration)
            subscription_price = get_price_for_duration(subscription_duration)
            if subscription_price is not None:
                payment_amount_var.set(subscription_price)

            if price_options:
                price_options.set("")
                available_prices = get_current_prices()  # تحصل على الأسعار المحددة من الجدول current_prices
                if available_prices:
                    price_options["values"] = available_prices

        except ValueError:
            pass


from PIL import Image, ImageDraw

def generate_qr_code():
    subscription_number = subscription_number_var.get()
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(subscription_number)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="white", back_color="black")  # تغيير لون الرمز والخلفية

    # Convert QR code image to mode '1' (1-bit pixels, black and white, stored with one pixel per byte)
    qr_image = qr_image.convert('1')

    # Load the background image
    background_image_path = "C:/Users/POWER KING/Desktop/sest/logoqr.png"  # تحقق من مسار الصورة
    background_image = Image.open(background_image_path)

    # Calculate the position to place QR code in the center
    background_width, background_height = background_image.size
    qr_width, qr_height = qr_image.size
    x_offset = (background_width - qr_width) // 2
    y_offset = (background_height - qr_height) // 2

    # Paste the QR code onto the background image
    background_image.paste(qr_image, (x_offset, y_offset))

    # Save the final image
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if file_path:
        background_image.save(file_path)




def check_existing_subscription(subscription_number):
    try:
        conn = sqlite3.connect('gym_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM main WHERE رقم_الاشتراك = ?", (subscription_number,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    except sqlite3.Error as e:
        print("حدث خطأ أثناء التحقق من وجود رقم الاشتراك:", e)
        return False


def display_member_info(member_data):
    member_info_window = tk.Toplevel()
    member_info_window.title("بيانات المشترك")

    frame = ttk.Frame(member_info_window)
    frame.pack(padx=15, pady=15)

    for i, (key, value) in enumerate(member_data.items()):
        ttk.Label(frame, text=key + ":").grid(row=i, column=0, sticky="e", padx=5, pady=2)
        ttk.Label(frame, text=value).grid(row=i, column=1, sticky="w", padx=5, pady=2)

def save_member_data(member_window):
    # قم بتنفيذ الخطوات اللازمة لحفظ بيانات المشترك هنا
    # بعد الحفظ، يمكنك إغلاق نافذة إضافة المشترك باستدعاء member_window.destroy()


    # Update remaining days
    update_remaining_days()
    member_window.protocol("WM_DELETE_WINDOW", lambda: [update_remaining_days(), member_window.destroy()])

def save_member_data(member_window, subscription_number, upgrade_function=None):
    existing_subscription = check_existing_subscription(subscription_number_var.get())
    if existing_subscription:
        messagebox.showerror("خطأ", "رقم الاشتراك موجود بالفعل. الرجاء تغيير رقم الاشتراك.")
        return

    try:
        subscription_duration = int(subscription_duration_var.get())
    except ValueError:
        messagebox.showerror("خطأ", "قيمة فترة الاشتراك غير صحيحة")
        return

    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = (datetime.strptime(tomorrow_date, "%Y-%m-%d") + timedelta(days=subscription_duration)).strftime("%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    remaining_days = (end_date_obj - datetime.now()).days

    payment_type = payment_type_var.get()

    try:
        payment_amount = float(payment_amount_var.get())
    except ValueError:
        messagebox.showerror("خطأ", "المبلغ المدفوع يجب أن يكون رقمًا صحيحًا.")
        return

    # إذا كان الاشتراك مجمدًا، قم بتجميد حساب الأيام ولا تحسب أيام جديدة
    if subscription_status_var.get() == "مجمد":
        remaining_days = remaining_days_var.get()

    subscription_price = calculate_subscription_price(remaining_days)
    remaining_debt = subscription_price - payment_amount

    age_note = ""
    if remaining_debt > 0:
        age_note = f"دين: {remaining_debt}"

    if upgrade_function:
        upgrade_function()

    cursor.execute('''
        INSERT INTO main (تاريخ_التسجيل, رقم_الاشتراك, الاسم, العمر, الهاتف, مدة_الاشتراك, حالة_الاشتراك, ملاحظات, رقم_السجل, تاريخ_الانتهاء, الأيام_المتبقية, المبلغ_المدفوع, تاريخ_الدفع, مسار_الصورة)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        registration_date_var.get(),
        subscription_number_var.get(),
        name_var.get(),
        age_note,
        phone_var.get(),
        subscription_duration_var.get(),
        subscription_status_var.get(),
        notes_var.get(),
        record_number_var.get(),
        end_date,
        remaining_days,  # استخدم remaining_days المجمدة هنا
        payment_amount,
        payment_date_var.get(),
        image_path_var.get()
    ))

    conn.commit()
    messagebox.showinfo("نجاح", "تمت إضافة المشترك بنجاح!")

    member_data = {
        'تاريخ_التسجيل': registration_date_var.get(),
        'رقم_الاشتراك': subscription_number_var.get(),
        'الاسم': name_var.get(),
        'العمر': age_note,
        'الهاتف': phone_var.get(),
        'مدة_الاشتراك': subscription_duration_var.get(),
        'حالة_الاشتراك': subscription_status_var.get(),
        'ملاحظات': notes_var.get(),
        'رقم السجل': record_number_var.get(),
        'الأيام المتبقية': remaining_days,
        'المبلغ المدفوع': payment_amount,
        'تاريخ الدفع': payment_date_var.get(),
        'مسار_الصورة': image_path_var.get()
    }

    display_member_info(member_data)

    image_path = image_path_var.get()
    subscription_number = subscription_number_var.get()

    try:
        if image_path:
            save_image(image_path, subscription_number)
        else:
            messagebox.showerror("خطأ", "الرجاء تحديد ملف صورة قبل الحفظ.")
    except sqlite3.Error as e:
        print("حدث خطأ أثناء حفظ الصورة:", e)

    if upgrade_function:
        upgrade_function()





def open_upgrade_subscription_window(root):
    global upgrade_window, old_subscription_number_var

    upgrade_window = tk.Toplevel(root)
    upgrade_window.title("ترقية الاشتراك")
    upgrade_window.geometry("400x200")

    ttk.Label(upgrade_window, text="رقم المشترك القديم:").pack(pady=10)
    old_subscription_number_var = tk.StringVar()
    old_subscription_entry = ttk.Entry(upgrade_window, textvariable=old_subscription_number_var)
    old_subscription_entry.pack()

    search_button = ttk.Button(upgrade_window, text="بحث", command=search_and_upgrade_subscription)
    search_button.pack(pady=10)

def search_and_upgrade_subscription():
    old_subscription_number = old_subscription_number_var.get()

    # ابحث في قاعدة البيانات باستخدام رقم الاشتراك القديم
    cursor.execute("SELECT * FROM main WHERE رقم_الاشتراك=?", (old_subscription_number,))
    member_data = cursor.fetchone()

    if member_data:
        show_upgrade_confirmation(member_data)
    else:
        messagebox.showerror("خطأ", "لا يوجد مشترك بهذا الرقم.")


def show_upgrade_confirmation(member_data, remaining_days_old, remaining_days_new, price_difference):
    global upgrade_window, registration_date_var, subscription_duration_var, payment_amount_var, subscription_number_var

    upgrade_confirmation_window = tk.Toplevel(upgrade_window)
    upgrade_confirmation_window.title("تأكيد الترقية")
    upgrade_confirmation_window.geometry("400x300")

    ttk.Label(upgrade_confirmation_window, text=f"بيانات المشترك {member_data[2]}:").pack(pady=10)

    display_member_data(upgrade_confirmation_window, member_data)

    current_date = datetime.now().strftime("%Y-%m-%d")

    registration_date_var = tk.StringVar(value=current_date)
    registration_date_var.set(current_date)

    subscription_number_var = tk.StringVar(value=str(member_data[1]))
    ttk.Label(upgrade_confirmation_window, text="رقم الاشتراك").pack(pady=5)
    subscription_number_entry = ttk.Entry(upgrade_confirmation_window, textvariable=subscription_number_var)
    subscription_number_entry.pack(pady=5)

    subscription_duration_var = tk.StringVar(value=str(subscription_duration_var.get()))

    ttk.Label(upgrade_confirmation_window, text="تاريخ التسجيل").pack(pady=5)
    registration_date_entry = ttk.Entry(upgrade_confirmation_window, textvariable=registration_date_var)
    registration_date_entry.pack(pady=5)

    ttk.Label(upgrade_confirmation_window, text="مدة الاشتراك (أيام)").pack(pady=5)
    subscription_duration_entry = ttk.Entry(upgrade_confirmation_window, textvariable=subscription_duration_var)
    subscription_duration_entry.pack(pady=5)

    ttk.Label(upgrade_confirmation_window, text="المبلغ المدفوع").pack(pady=5)
    payment_amount_var = tk.StringVar(value=str(price_difference))
    payment_amount_var.set(str(price_difference))
    payment_amount_entry = ttk.Entry(upgrade_confirmation_window, textvariable=payment_amount_var)
    payment_amount_entry.pack(pady=5)

    update_button = ttk.Button(upgrade_confirmation_window, text="تحديث البيانات",
                               command=lambda: update_member_data(member_data, registration_date_var.get(),
                                                                  subscription_duration_var.get(), payment_amount_var.get()))
    update_button.pack(pady=10)




def display_member_data(window, member_data):
    fields = ["تاريخ_التسجيل", "رقم_الاشتراك", "الاسم", "العمر", "الهاتف", "مدة_الاشتراك", "حالة_الاشتراك", "ملاحظات",
              "رقم_السجل", "تاريخ_الانتهاء", "الأيام_المتبقية", "المبلغ_المدفوع", "تاريخ_الدفع"]

    for field in fields:
        ttk.Label(window, text=f"{field}: {member_data[fields.index(field)]}").pack(pady=5)

def update_member_data(member_data, registration_date, subscription_duration, payment_amount):
    global upgrade_window

    fields = ["تاريخ_التسجيل", "رقم_الاشتراك", "الاسم", "العمر", "الهاتف", "مدة_الاشتراك", "حالة_الاشتراك", "ملاحظات", "رقم_السجل", "تاريخ_الانتهاء", "الأيام_المتبقية", "المبلغ_المدفوع", "تاريخ_الدفع"]

    registration_date = registration_date_var.get()
    subscription_duration = subscription_duration_var.get()
    subscription_number = subscription_number_var.get()
    payment_amount = payment_amount_var.get()

    # احسب المدة الإضافية
    additional_days = int(subscription_duration) - int(member_data[fields.index("مدة_الاشتراك")])

    # احسب تاريخ الانتهاء والأيام المتبقية الجديدة
    new_end_date = (datetime.strptime(member_data[fields.index("تاريخ_الانتهاء")], "%Y-%m-%d") + timedelta(days=additional_days)).strftime("%Y-%m-%d")
    new_remaining_days = (datetime.strptime(new_end_date, "%Y-%m-%d") - datetime.now()).days

    # تحديث قاعدة البيانات بالبيانات الجديدة
    cursor.execute('''
        UPDATE main
        SET رقم_الاشتراك=?, تاريخ_التسجيل=?, مدة_الاشتراك=?, تاريخ_الانتهاء=?, الأيام_المتبقية=?, المبلغ_المدفوع=?, تاريخ_الدفع=?
        WHERE رقم_الاشتراك=?
    ''', (
        subscription_number,
        registration_date,
        int(member_data[fields.index("مدة_الاشتراك")]) + additional_days,
        new_end_date,
        new_remaining_days,
        payment_amount,
        datetime.now().strftime("%Y-%m-%d"),
        member_data[fields.index("رقم_الاشتراك")]
    ))

    conn.commit()

    messagebox.showinfo("تم التحديث", f"تم تحديث بيانات الاشتراك للمشترك {member_data[fields.index('الاسم')]} بنجاح.")

    # إغلاق نافذة الترقية إذا كنت تستخدمها
    if upgrade_window:
        upgrade_window.destroy()





# حساب فرق المبلغ
# حساب فرق المبلغ
def calculate_price_difference():
    global payment_amount_var, old_subscription_number_var, subscription_duration_var, registration_date_var

    old_subscription_number = old_subscription_number_var.get()

    # ابحث في قاعدة البيانات باستخدام رقم الاشتراك القديم
    cursor.execute("SELECT * FROM main WHERE رقم_الاشتراك=?", (old_subscription_number,))
    old_member_data = cursor.fetchone()

    if not old_member_data:
        messagebox.showerror("خطأ", "لا يوجد مشترك بهذا الرقم.")
        return

    try:
        subscription_duration = int(subscription_duration_var.get())
    except ValueError:
        messagebox.showerror("خطأ", "مدة الاشتراك يجب أن تكون رقم صحيح.")
        return

    # حساب الأيام المتبقية من الاشتراك القديم
    remaining_days_old_subscription = (datetime.strptime(old_member_data[10], "%Y-%m-%d") - datetime.now()).days

    # حساب الفرق في المدة بين الاشتراكين
    additional_days = subscription_duration - old_member_data[5]

    # حساب الأيام المتبقية للفترة الجديدة
    remaining_days_new_subscription = remaining_days_old_subscription + additional_days

    # حساب التاريخ الجديد لنهاية الاشتراك
    new_end_date = (datetime.now() + timedelta(days=remaining_days_new_subscription)).strftime("%Y-%m-%d")

    # حساب الفرق في السعر
    price_difference = calculate_subscription_price(remaining_days_new_subscription) - calculate_subscription_price(remaining_days_old_subscription)

    # تحديث القيم في النوافذ
    registration_date_var.set(datetime.now().strftime("%Y-%m-%d"))
    subscription_duration_var.set(str(subscription_duration))
    payment_amount_var.set(str(price_difference))

    # عرض تأكيد الترقية
    show_upgrade_confirmation(old_member_data, remaining_days_old_subscription, remaining_days_new_subscription, price_difference)




# دالة لحساب تفاصيل الاشتراك
def calculate_subscription_details(registration_date, subscription_duration):
    try:
        # حساب تاريخ الانتهاء الجديد بناءً على تاريخ التسجيل ومدة الاشتراك
        new_end_date = (datetime.strptime(registration_date, "%Y-%m-%d") + timedelta(days=int(subscription_duration))).strftime("%Y-%m-%d")
        new_remaining_days = (datetime.strptime(new_end_date, "%Y-%m-%d") - datetime.now()).days

        # حساب المبلغ المستحق بناءً على المدة المتبقية
        subscription_price = calculate_subscription_price(new_remaining_days)

        return new_end_date, new_remaining_days, subscription_price

    except ValueError:
        return None, None, None





import sqlite3

# الاتصال بقاعدة البيانات
conn = sqlite3.connect("gym_database.db")  # استبدل بالاسم الصحيح
cursor = conn.cursor()

# إنشاء جدول SuspensionActivation إذا لم يكن موجودًا بالفعل
cursor.execute('''
    CREATE TABLE IF NOT EXISTS SuspensionActivation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subscription_number INTEGER,
        suspend_date DATE,
        activate_date DATE,
        remaining_days INTEGER,
        FOREIGN KEY (subscription_number) REFERENCES main (رقم_الاشتراك)
    )
''')

# حفظ التغييرات
conn.commit()

# إغلاق الاتصال
conn.close()





import sqlite3
from datetime import datetime, timedelta

def freeze_subscription(subscription_number):
    connection = sqlite3.connect("gym_database.db")  # استبدل بالاسم الصحيح
    cursor = connection.cursor()

    try:
        cursor.execute('SELECT * FROM main WHERE رقم_الاشتراك=?', (subscription_number,))
        member_data = cursor.fetchone()

        if member_data:
            remaining_days = calculate_remaining_days(member_data[9])
            if remaining_days is not None and remaining_days > 0:
                # تجميد الاشتراك
                frozen_end_date = datetime.now() + timedelta(days=remaining_days)
                cursor.execute('UPDATE main SET حالة_الاشتراك=?, ملاحظات=? WHERE رقم_الاشتراك=?',
                               ('مجمد', f'ايقاف - {datetime.now().strftime("%Y-%m-%d")}', subscription_number))
                cursor.execute('INSERT INTO SuspensionActivation (subscription_number, suspend_date, remaining_days) VALUES (?, ?, ?)',
                               (subscription_number, datetime.now().strftime("%Y-%m-%d"), remaining_days))
                connection.commit()
                messagebox.showinfo("تم التجميد", "تم تجميد الاشتراك بنجاح.")
            else:
                messagebox.showwarning("تحذير", "لا يمكن تجميد الاشتراك لأنه قد انتهى.")
    finally:
        cursor.close()
        connection.close()

def activate_subscription(subscription_number):
    connection = sqlite3.connect("gym_database.db")  # استبدل بالاسم الصحيح
    cursor = connection.cursor()

    try:
        cursor.execute('SELECT * FROM SuspensionActivation WHERE subscription_number=? ORDER BY id DESC LIMIT 1', (subscription_number,))
        suspension_data = cursor.fetchone()

        if suspension_data:
            remaining_days = suspension_data[4]  # استعادة عدد الأيام المتبقية قبل التجميد
            cursor.execute('UPDATE main SET حالة_الاشتراك=?, ملاحظات=? WHERE رقم_الاشتراك=?',
                           ('تفعيل', f'تفعيل - {datetime.now().strftime("%Y-%m-%d")}', subscription_number))
            cursor.execute('UPDATE SuspensionActivation SET activate_date=? WHERE id=?',
                           (datetime.now().strftime("%Y-%m-%d"), suspension_data[0]))  # تحديث تاريخ التفعيل في جدول SuspensionActivation
            connection.commit()
            messagebox.showinfo("تم التفعيل", "تم تفعيل الاشتراك بنجاح.")
        else:
            messagebox.showwarning("تحذير", "لا يمكن تفعيل الاشتراك لأنه لم يتم تجميده.")
    finally:
        cursor.close()
        connection.close()


# الدالة التي تقوم بحساب الأيام المتبقية
def calculate_remaining_days(end_date_str):
    try:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        remaining_days = (end_date - datetime.now()).days
        return remaining_days
    except ValueError:
        return None

def search_member_by_subscription_number(subscription_number):
    cursor.execute('SELECT * FROM main WHERE رقم_الاشتراك=?', (subscription_number,))
    member_data = cursor.fetchone()
    print(member_data)  # قم بإضافة هذا السطر للتحقق من القيمة المسترجعة
    if member_data:
        show_member_data(member_data, subscription_number)
    else:
        messagebox.showinfo("تنبيه", "لم يتم العثور على مشترك بهذا الرقم.")


def show_member_data(data, subscription_number):
    member_data_window = tk.Toplevel()
    member_data_window.title("بيانات العضو")

    frame = ttk.Frame(member_data_window)
    frame.pack(padx=10, pady=10)

    labels = ["تاريخ التسجيل", "رقم الاشتراك", "الاسم", "العمر", "الهاتف", "مدة الاشتراك",
              "حالة الاشتراك", "ملاحظات", "رقم السجل", "تاريخ الانتهاء", "الأيام المتبقية", "المبلغ المدفوع",
              "تاريخ الدفع", "مسار الصورة"]

    for row, label in enumerate(labels):
        ttk.Label(frame, text=label + ":").grid(row=row, column=0, sticky="e")
        if label == "الأيام المتبقية":
            remaining_days = calculate_remaining_days(data[9])  # تحديث الاستدعاء للدالة
            ttk.Label(frame, text=str(remaining_days)).grid(row=row, column=1)
        else:
            ttk.Label(frame, text=data[row]).grid(row=row, column=1)

    cancel_button = ttk.Button(frame, text="إغلاق", command=member_data_window.destroy)
    cancel_button.grid(row=len(labels), column=0, columnspan=2)

    stop_button = ttk.Button(frame, text="إيقاف مؤقت", command=lambda: freeze_subscription(subscription_number))
    stop_button.grid(row=len(labels) + 1, column=0, pady=10)

    activate_button = ttk.Button(frame, text="تفعيل", command=lambda: activate_subscription(subscription_number))
    activate_button.grid(row=len(labels) + 1, column=1, pady=10)




def stop_subscription_window():
    stop_window = tk.Toplevel()
    stop_window.title("إيقاف الاشتراك مؤقتًا")

    frame = ttk.Frame(stop_window)
    frame.pack(padx=10, pady=10)

    ttk.Label(frame, text="رقم الاشتراك:").grid(row=0, column=0)
    subscription_entry = ttk.Entry(frame, width=30)
    subscription_entry.grid(row=0, column=1)

    search_button = ttk.Button(frame, text="بحث", command=lambda: search_member_by_subscription_number(subscription_entry.get()))
    search_button.grid(row=1, column=0, pady=10)

    cancel_button = ttk.Button(frame, text="إلغاء", command=stop_window.destroy)
    cancel_button.grid(row=1, column=1, columnspan=2, pady=10)

    # Add freeze button
    freeze_button = ttk.Button(frame, text="تجميد", command=lambda: freeze_subscription(subscription_entry.get()))
    freeze_button.grid(row=2, column=0, columnspan=2, pady=10)


conn = sqlite3.connect('gym_database.db')
cursor = conn.cursor()


def setup_entry_widgets(frame, label, var, row, column):
    label_frame = ttk.LabelFrame(frame)
    label_frame.grid(row=row * 2, column=column, padx=0.01 * 600, pady=0.005 * 300, sticky="nsew")

    entry = ttk.Entry(label_frame, textvariable=var)
    entry.grid(row=1, column=0, padx=5, pady=1)
    ttk.Label(label_frame, text=label).grid(row=0, column=0, padx=5, pady=1)

    return entry  # إرجاع المرجع إلى الحقل النصي


def calculate_end_date(start_date, subscription_days):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = start_date + timedelta(days=int(subscription_days))
    return end_date.strftime("%Y-%m-%d")


def calculate_subscription_fee(duration, cursor):
    try:
        cursor.execute('''
            SELECT amount FROM current_prices WHERE duration=?
        ''', [duration])

        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            messagebox.showerror("خطأ", "لم يتم العثور على معدل الاشتراك لهذه المدة.")
            return None
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ أثناء استعلام معدل الاشتراك: {str(e)}")
        return None



def renew_subscription(conn, cursor, results_table):
    selected_item = results_table.selection()
    if not selected_item:
        messagebox.showerror("خطأ", "الرجاء تحديد مشترك لتجديد اشتراكه.")
        return

    selected_row_data = results_table.item(selected_item, "values")

    renew_window = tk.Toplevel()
    renew_window.title("تجديد الاشتراك")
    renew_window.geometry("800x600")  # تعيين حجم النافذة

    # تقسيم النافذة إلى عدة أعمدة
    renew_window.columnconfigure(0, weight=1)
    renew_window.columnconfigure(1, weight=1)

    # إعداد متغيرات النص للبيانات
    data_vars = [tk.StringVar(value=value) for value in selected_row_data]

    # الترتيب الصحيح للمربعات
    labels = ["تاريخ التسجيل", "رقم الاشتراك", "الاسم", "العمر", "الهاتف", "مدة الاشتراك", "حالة الاشتراك", "ملاحظات",
              "رقم السجل", "تاريخ الانتهاء", "الأيام المتبقية", "المبلغ المدفوع", "تاريخ الدفع", "مسار الصورة"]

    entry_widgets = []  # قائمة لتخزين مراجع إلى الحقول النصية لتمكين التحديث

    for i, (label, var) in enumerate(zip(labels, data_vars)):
        entry = setup_entry_widgets(renew_window, label, var, i // 2, i % 2)
        entry_widgets.append(entry)  # إضافة المرجع إلى الحقل النصي إلى القائمة

    # حدث التغيير التلقائي لتاريخ التسجيل
    data_vars[0].set(datetime.now().strftime("%Y-%m-%d"))

    # إنشاء كمبوبوكس لاختيار مدة الاشتراك
    duration_var = tk.StringVar()
    # تغيير القيم المعروضة لتعكس الأيام بدلاً من الأشهر
    duration_combobox = ttk.Combobox(renew_window, textvariable=duration_var,
                                     values=["30", "90", "180", "360"])
    duration_combobox.grid(row=len(labels), columnspan=2, padx=5, pady=5)

    def update_payment_amount():
        selected_duration = duration_var.get()
        if selected_duration:
            subscription_fee = calculate_subscription_fee(selected_duration, cursor)
            if subscription_fee is not None:
                data_vars[11].set(subscription_fee)  # تحديث المبلغ المدفوع بالمبلغ المناسب للمدة المختارة
                entry_widgets[11].configure(state="normal")  # تمكين التحرير على المبلغ المدفوع
                payment_amount_str = selected_row_data[11]
                if payment_amount_str:
                    payment_amount = float(payment_amount_str)
                    difference = payment_amount - subscription_fee
                    if difference < 0:
                        new_debt = float(selected_row_data[12]) + abs(difference)
                        data_vars[12].set(new_debt)  # تحديث الدين بفرق السعر
                        new_age = f"دين: {abs(difference)}"
                        data_vars[3].set(new_age)  # تحديث العمر ليعكس المبلغ المدفوع بالفرق الإضافي كدين
            else:
                entry_widgets[11].configure(state="normal")  # تمكين التحرير على المبلغ المدفوع

    def update_subscription_info():
        selected_duration = duration_var.get()
        if selected_duration:
            # تحديث مدة الاشتراك وتاريخ الانتهاء بناءً على المدة المختارة
            if selected_duration == "30":
                data_vars[5].set(30)  # تحديث مدة الاشتراك إلى 30 يوم
            elif selected_duration == "90":
                data_vars[5].set(90)  # تحديث مدة الاشتراك إلى 90 يوم
            elif selected_duration == "180":
                data_vars[5].set(180)  # تحديث مدة الاشتراك إلى 180 يوم
            elif selected_duration == "360":
                data_vars[5].set(365)  # تحديث مدة الاشتراك إلى 365 يوم

            # تحديث تاريخ الدفع إلى تاريخ اليوم
            payment_date = datetime.now().strftime("%Y-%m-%d")
            data_vars[12].set(payment_date)

            # حساب التاريخ الجديد لنهاية الاشتراك
            new_end_date = calculate_end_date(data_vars[0].get(), data_vars[5].get())
            data_vars[9].set(new_end_date)  # تحديث تاريخ الانتهاء

            # حساب الأيام المتبقية
            remaining_days = (datetime.strptime(new_end_date, "%Y-%m-%d") - datetime.now()).days
            data_vars[10].set(remaining_days)  # تحديث الأيام المتبقية

            # تحديث المبلغ المدفوع بناءً على المدة المختارة
            subscription_fee = calculate_subscription_fee(selected_duration, cursor)
            if subscription_fee is not None:
                data_vars[11].set(subscription_fee)  # تحديث المبلغ المدفوع
                payment_amount_str = selected_row_data[11]
                if payment_amount_str:
                    payment_amount = float(payment_amount_str)
                    if payment_amount < subscription_fee:
                        difference = subscription_fee - payment_amount
                        # تحديث خانة العمر بالدين الجديد
                        data_vars[3].set(f"دين: {difference}")

                        # تمكين التحرير على المبلغ المدفوع
                        entry_widgets[11].configure(state="normal")

            else:
                # في حالة عدم العثور على رسم الاشتراك، يتم تعيين المبلغ المدفوع والعمر إلى قيمة افتراضية
                data_vars[11].set(0)
                data_vars[3].set("دين: 0")


    # ربط دالة التحديث مع حدث اختيار مدة جديدة
    duration_combobox.bind("<<ComboboxSelected>>", lambda event: update_subscription_info())

    # استدعاء دالة تحديث المعلومات عند البداية
    update_subscription_info()

    def save_renewed_subscription():
        try:
            new_data = [var.get() for var in data_vars]

            # حساب تاريخ الانتهاء الجديد
            new_data[9] = calculate_end_date(new_data[0], new_data[5])

            # تجميد حساب الأيام إذا كان الاشتراك متجمدًا
            if new_data[6] == "مجمد":
                new_data[10] = remaining_days_var.get()

            # حساب المبلغ المتبقي
            if new_data[11] is not None:
                remaining_amount = float(new_data[11]) - calculate_subscription_fee(new_data[5], cursor)
                if remaining_amount < 0:
                    new_data[3] = abs(remaining_amount)  # تعيين المبلغ المتبقي كدين في الكود المستخدم في إدراج البيانات
                    new_age = f"دين: {abs(remaining_amount)}"
                    new_data[3] = new_age  # تحديث العمر بالدين المتبقي
                else:
                    new_data[11] = new_data[11]  # لا تغيير في حالة وجود دين سابق

            cursor.execute('''
                    DELETE FROM main
                    WHERE رقم_السجل=?
                ''', [selected_row_data[8]])
            cursor.execute('''
                        INSERT INTO main VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', new_data)
            conn.commit()
            messagebox.showinfo("نجاح", "تم تجديد الاشتراك بنجاح!")
            renew_window.destroy()
            update_remaining_days()
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء تجديد الاشتراك: {str(e)}")

    # الدالة لتحديث الأيام المتبقية
    def update_remaining_days():
        for child in results_table.get_children():
            item = results_table.item(child)['values']
            end_date = datetime.strptime(item[9], "%Y-%m-%d")
            remaining_days = (end_date - datetime.now()).days
            results_table.item(child, values=(
                item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9],
                remaining_days, item[11], item[12], item[13]))

        results_table.after(86400000, update_remaining_days)  # يُحدث كل 24 ساعة (86400000 مللي ثانية)

    # إضافة زر "حفظ تجديد الاشتراك"
    save_button = ttk.Button(renew_window, text="حفظ تجديد الاشتراك", command=save_renewed_subscription)
    save_button.grid(row=len(labels) + 1, columnspan=2, pady=10)


# الدالة الرئيسية لفتح نافذة تجديد الاشتراك
def open_renew_subscription_window(root):
    renew_window = tk.Toplevel(root)
    renew_window.title("تجديد الاشتراك")

    search_var = tk.StringVar()
    ttk.Label(renew_window, text="البحث باستخدام (الاسم - رقم الاشتراك - رقم الهاتف - رقم السجل)").pack(pady=10)
    entry_search = ttk.Entry(renew_window, textvariable=search_var)
    entry_search.pack(pady=5)

    results_frame = ttk.Frame(renew_window)
    results_frame.pack(pady=10)

    def search_member():
        # حذف جميع العناصر داخل results_frame
        for widget in results_frame.winfo_children():
            widget.destroy()

        # استرجاع وصف الجدول من قاعدة البيانات
        cursor.execute("PRAGMA table_info(main)")
        column_info = cursor.fetchall()
        column_names = [info[1] for info in column_info]

        query = f"SELECT * FROM main WHERE الاسم LIKE '%{search_var.get()}%' OR رقم_الاشتراك LIKE '%{search_var.get()}%' OR الهاتف LIKE '%{search_var.get()}%' OR رقم_السجل LIKE '%{search_var.get()}%'"

        cursor.execute(query)
        search_results = cursor.fetchall()

        # إعادة إنشاء الجدول
        results_table = ttk.Treeview(results_frame, columns=[str(i) for i in range(len(column_names))], show="headings")
        for col in range(len(column_names)):
            results_table.heading(str(col), text=str(column_names[col]))
        results_table.pack(side="left")

        for row in search_results:
            results_table.insert("", "end", values=row)

        # إضافة زر "تجديد الاشتراك"
        renew_button = ttk.Button(renew_window, text="تجديد الاشتراك",
                                  command=lambda: renew_subscription(conn, cursor, results_table))
        renew_button.pack(pady=10)

    search_button = ttk.Button(renew_window, text="بحث", command=search_member)
    search_button.pack(pady=10)




# اتصل بقاعدة البيانات SQLite
conn = sqlite3.connect(r"C:\Users\POWER KING\Desktop\sest\gym_database.db")
cursor = conn.cursor()



def update_remaining_days():
    current_subscription_status = subscription_status_var.get()

    if current_subscription_status == "مستمر":
        end_date = datetime.strptime(payment_date_var.get(), "%Y-%m-%d") + timedelta(
            days=int(subscription_duration_var.get()))
        remaining_days = (end_date - datetime.now()).days
        if remaining_days > 0:
            remaining_days_var.set(str(remaining_days))
        else:
            remaining_days_var.set("انتهى الاشتراك")  # يمكنك تغيير النص حسب احتياجاتك

        # تحديث حالة الاشتراك في قاعدة البيانات لتكون "مستمر"
        update_subscription_status("مستمر")
    else:
        remaining_days_var.set("")

        # تحديث حالة الاشتراك في قاعدة البيانات لتكون "متوقف"
        update_subscription_status("متوقف")

    member_window.after(1000, update_remaining_days)  # سيتم تحديث البيانات كل 1000 مللي ثانية (1 ثانية)

def update_subscription_status(new_status):
    try:
        # تحديث حالة الاشتراك في قاعدة البيانات باستخدام رقم السجل الحالي
        cursor.execute('''
            UPDATE main
            SET حالة_الاشتراك=?
            WHERE رقم_السجل=?
        ''', (new_status, record_number_var.get()))

        conn.commit()
        print("تم تحديث حالة الاشتراك بنجاح")
    except Exception as e:
        print("حدث خطأ أثناء تحديث حالة الاشتراك:", str(e))
# تصدير النتائج إلى ملف نصي أو قاعدة بيانات
def export_data():
    cursor.execute('SELECT * FROM main')
    data = cursor.fetchall()
    with open('exported_data.txt', 'w') as f:
        f.write("تاريخ التسجيل,رقم الاشتراك,الاسم,العمر,الهاتف,مدة الاشتراك,حالة الاشتراك,ملاحظات,رقم السجل,تاريخ الانتهاء,الأيام المتبقية,المبلغ المدفوع,تاريخ الدفع\n")
        for row in data:
            f.write(",".join(map(str, row)) + "\n")


# دالة لعرض نتائج البحث
import sqlite3

from PIL import UnidentifiedImageError

# دالة لعرض نتائج البحث
# دالة لعرض نتائج البحث
def display_search_results(search_window, search_entry, search_option_var):
    # البقاء على نافذة البحث مفتوحة لاحقًا عند الحاجة
    search_query = search_entry.get()
    selected_option = search_option_var.get()

    if selected_option == "الاسم":
        search_field = "الاسم"
    elif selected_option == "رقم الهاتف":
        search_field = "الهاتف"
    elif selected_option == "رقم السجل":
        search_field = "رقم_السجل"
    elif selected_option == "رقم الاشتراك":
        search_field = "رقم_الاشتراك"

    cursor.execute(f"SELECT * FROM main WHERE {search_field} LIKE ?", (f"%{search_query}%",))
    results = cursor.fetchall()

    if results:
        display_results(results)
    else:
        messagebox.showinfo("بحث", "لم يتم العثور على أي نتائج.")


    log_activity(" البحث", " البحث.")


import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel, messagebox, filedialog
from datetime import datetime
from PIL import Image, ImageTk
import sqlite3
import os
import shutil

# تحديث دالة display_results لعرض الصورة بدلاً من مسار الصورة
def display_results(results):
    results_window = Toplevel()
    results_window.title("نتائج البحث")
    new_width = 60  # استبدل هذا بالعرض الجديد الذي ترغب في تحديده للصورة
    new_height = 60  # استبدل هذا بالارتفاع الجديد الذي ترغب في تحديده للصورة


    # الجدول
    results_table = ttk.Treeview(results_window, columns=(
        "تاريخ التسجيل", "رقم الاشتراك", "الاسم", "العمر", "الهاتف",
        "مدة الاشتراك", "حالة الاشتراك", "ملاحظات", "رقم السجل",
        "تاريخ الانتهاء", "الأيام المتبقية", "المبلغ المدفوع", "تاريخ الدفع", "مسار_الصورة"
    ), show="headings")

    results_table.pack(padx=20, pady=10)

    # تعيين عناوين الأعمدة
    results_table.heading("تاريخ التسجيل", text="تاريخ التسجيل")
    results_table.heading("رقم الاشتراك", text="رقم الاشتراك")
    results_table.heading("الاسم", text="الاسم")
    results_table.heading("العمر", text="العمر")
    results_table.heading("الهاتف", text="الهاتف")
    results_table.heading("مدة الاشتراك", text="مدة الاشتراك")
    results_table.heading("حالة الاشتراك", text="حالة الاشتراك")
    results_table.heading("ملاحظات", text="ملاحظات")
    results_table.heading("رقم السجل", text="رقم السجل")
    results_table.heading("تاريخ الانتهاء", text="تاريخ الانتهاء")
    results_table.heading("الأيام المتبقية", text="الأيام المتبقية")
    results_table.heading("المبلغ المدفوع", text="المبلغ المدفوع")
    results_table.heading("تاريخ الدفع", text="تاريخ الدفع")
    results_table.heading("مسار_الصورة", text="مسار_الصورة")

    # تحديد عرض الأعمدة
    results_table.column("تاريخ التسجيل", width=100)
    results_table.column("رقم الاشتراك", width=70)
    results_table.column("الاسم", width=150)
    results_table.column("العمر", width=50)
    results_table.column("الهاتف", width=100)
    results_table.column("مدة الاشتراك", width=100)
    results_table.column("حالة الاشتراك", width=100)
    results_table.column("ملاحظات", width=100)
    results_table.column("رقم السجل", width=100)
    results_table.column("تاريخ الانتهاء", width=100)
    results_table.column("الأيام المتبقية", width=100)
    results_table.column("المبلغ المدفوع", width=100)
    results_table.column("تاريخ الدفع", width=150)
    results_table.column("مسار_الصورة", width=100)

    for result in results:
        # حساب الأيام المتبقية
        end_date = datetime.strptime(result[9], "%Y-%m-%d")  # تاريخ الانتهاء
        remaining_days = (end_date - datetime.now()).days
        result = list(result)  # تحويل الصف إلى قائمة قابلة للتعديل
        result[10] = remaining_days  # تحديث الأيام المتبقية في البيانات

        for result in results:
            # استرجاع مسار الصورة من قاعدة البيانات
            # استرجاع مسار الصورة من قاعدة البيانات
            image_path = get_image_path_from_db(result[1])

            # إذا كان هناك مسار صورة متاح
            if image_path:
                try:
                    img = Image.open(image_path)
                    img.thumbnail((150, 150))  # تحديد الحجم المناسب للصورة
                    photo = ImageTk.PhotoImage(img)
                    label = ttk.Label(results_window, image=photo)
                    label.image = photo
                    label.pack()
                except Exception as e:
                    print("حدث خطأ أثناء عرض الصورة:", e)
            else:
                print("الصورة غير موجودة في قاعدة البيانات.")

                # إضافة صورة افتراضية
                default_image_path = "C:/Users/POWER KING/Desktop/sest/images/default_image.jpg"  # اضف مسار الصورة الافتراضية هنا
                try:
                    img = Image.open(default_image_path)
                    img.thumbnail((150, 150))  # تحديد الحجم المناسب للصورة
                    photo = ImageTk.PhotoImage(img)
                    label = ttk.Label(results_window, image=photo)
                    label.image = photo
                    label.pack()
                except Exception as e:
                    print("حدث خطأ أثناء عرض الصورة الافتراضية:", e)

                # زر لاختيار الصورة وحفظها
                def select_and_save_image(subscription_number):
                    file_path = filedialog.askopenfilename()
                    if file_path:
                        # حفظ الصورة وتحديث مسار الصورة في قاعدة البيانات
                        save_image(file_path, subscription_number)

                        # عرض الصورة بعد الحفظ
                        try:
                            img = Image.open(file_path)
                            img.thumbnail((150, 150))  # تحديد الحجم المناسب للصورة
                            photo = ImageTk.PhotoImage(img)
                            label = ttk.Label(results_window, image=photo)
                            label.image = photo
                            label.pack()
                        except Exception as e:
                            print("حدث خطأ أثناء عرض الصورة:", e)

                # زر لاختيار الصورة وحفظها
                select_image_button = ttk.Button(results_window, text="اختيار الصورة",
                                                 command=lambda sub=result[1]: select_and_save_image(sub))
                select_image_button.pack()

            # تحديث الأيام المتبقية تلقائيًا كل يوم
            def update_remaining_days():
                for child in results_table.get_children():
                    item = results_table.item(child)['values']
                    end_date = datetime.strptime(item[9], "%Y-%m-%d")
                    if item[6] != "متجمد":  # التحقق مما إذا كانت الاشتراك متجمدًا
                        remaining_days = (end_date - datetime.now()).days
                        results_table.item(child, values=(
                            item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9],
                            remaining_days, item[11], item[12], item[13]))

                # تحديث الأيام المتبقية مرة أخرى بعد مرور يوم كامل (24 ساعة)
                results_window.after(86400000, update_remaining_days)

            # بدء تحديث الأيام المتبقية
            results_window.after(0, update_remaining_days)

            # إضافة البيانات إلى الجدول
            results_table.insert("", "end", values=result)

    # إضافة زر "تعديل"
    edit_button = ttk.Button(results_window, text="تعديل", command=lambda: edit_selected_row(results_table))
    edit_button.pack(pady=10)

    # إضافة زر "حذف" مع تعيين الدالة المناسبة
    delete_button = ttk.Button(results_window, text="حذف", command=lambda: delete_selected_row(results_table))
    delete_button.pack(pady=10)




    log_activity("البحث", "البحث.")



# دالة للتحقق من وجود جدول المحذوفين وإنشائه إذا لم يكن موجودًا
def create_deleted_subscribers_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deleted_subscribers_table (
            تاريخ_التسجيل TEXT,
            رقم_الاشتراك INTEGER,
            الاسم TEXT,
            العمر INTEGER,
            الهاتف TEXT,
            مدة_الاشتراك INTEGER,
            حالة_الاشتراك TEXT,
            ملاحظات TEXT,
            رقم_السجل INTEGER,
            تاريخ_الانتهاء TEXT,
            الأيام_المتبقية INTEGER,
            المبلغ_المدفوع REAL,
            تاريخ_الدفع TEXT,
            مسار_الصورة TEXT
        )
    ''')
    conn.commit()

# تحقق من وجود جدول المحذوفين وإنشائه إذا لم يكن موجودًا
create_deleted_subscribers_table()


# دالة لتحديث جدول سلة المحذوفات
# دالة لتحديث جدول سلة المحذوفات
def update_deleted_subscribers_table(subscriber_data):
    try:
        cursor.execute('''
            INSERT INTO deleted_subscribers_table (
                تاريخ_التسجيل, رقم_الاشتراك, الاسم, العمر, الهاتف, مدة_الاشتراك,
                حالة_الاشتراك, ملاحظات, رقم_السجل, تاريخ_الانتهاء, الأيام_المتبقية,
                المبلغ_المدفوع, تاريخ_الدفع, مسار_الصورة
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', subscriber_data)
        conn.commit()
        messagebox.showinfo("تم الحفظ", "تم حفظ البيانات في جدول المحذوفين بنجاح.")
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ أثناء حفظ البيانات: {str(e)}")

def delete_selected_row(results_table):
    # الحصول على العنصر المحدد في الجدول
    selected_item = results_table.selection()
    if not selected_item:
        messagebox.showerror("خطأ", "الرجاء تحديد مشترك لحذفه.")
        return

    # تأكيد الحذف
    confirm = messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد من رغبتك في حذف هذا المشترك؟")
    if confirm:
        try:
            # الحصول على رقم الاشتراك من العنصر المحدد
            subscription_number = results_table.item(selected_item)["values"][1]

            # نقل المشترك المحذوف إلى جدول المحذوفين
            cursor.execute('''
                INSERT INTO deleted_subscribers_table SELECT * FROM main WHERE رقم_الاشتراك=?
            ''', (subscription_number,))

            # حذف المشترك من الجدول الرئيسي
            cursor.execute('''
                DELETE FROM main WHERE رقم_الاشتراك=?
            ''', (subscription_number,))

            conn.commit()

            # بعد الحذف من قاعدة البيانات، قم بحذفه أيضًا من الجدول
            results_table.delete(selected_item)

            messagebox.showinfo("تم الحذف", "تم حذف المشترك بنجاح.")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء الحذف: {str(e)}")

        log_activity("حذف مشترك", "حذف مشترك.")

    log_activity("حذف مشترك", "حذف مشترك .")


# دالة لفتح واجهة سلة المحذوفات
def open_deleted_subscribers_window():
    deleted_subscribers_window = Toplevel()
    deleted_subscribers_window.title("سلة المحذوفات")

    deleted_subscribers_table = ttk.Treeview(deleted_subscribers_window, columns=(
        "تاريخ التسجيل", "رقم الاشتراك", "الاسم", "العمر", "الهاتف",
        "مدة الاشتراك", "حالة الاشتراك", "ملاحظات", "رقم السجل",
        "تاريخ الانتهاء", "الأيام المتبقية", "المبلغ المدفوع", "تاريخ الدفع", "مسار_الصورة"
    ), show="headings")

    deleted_subscribers_table.pack(padx=20, pady=10)

    # تعيين عناوين الأعمدة
    deleted_subscribers_table.heading("تاريخ التسجيل", text="تاريخ التسجيل")
    deleted_subscribers_table.heading("رقم الاشتراك", text="رقم الاشتراك")
    deleted_subscribers_table.heading("الاسم", text="الاسم")
    deleted_subscribers_table.heading("العمر", text="العمر")
    deleted_subscribers_table.heading("الهاتف", text="الهاتف")
    deleted_subscribers_table.heading("مدة الاشتراك", text="مدة الاشتراك")
    deleted_subscribers_table.heading("حالة الاشتراك", text="حالة الاشتراك")
    deleted_subscribers_table.heading("ملاحظات", text="ملاحظات")
    deleted_subscribers_table.heading("رقم السجل", text="رقم السجل")
    deleted_subscribers_table.heading("تاريخ الانتهاء", text="تاريخ الانتهاء")
    deleted_subscribers_table.heading("الأيام المتبقية", text="الأيام المتبقية")
    deleted_subscribers_table.heading("المبلغ المدفوع", text="المبلغ المدفوع")
    deleted_subscribers_table.heading("تاريخ الدفع", text="تاريخ الدفع")
    deleted_subscribers_table.heading("مسار_الصورة", text="مسار_الصورة")

    # تحديد عرض الأعمدة
    deleted_subscribers_table.column("تاريخ التسجيل", width=100)
    deleted_subscribers_table.column("رقم الاشتراك", width=70)
    deleted_subscribers_table.column("الاسم", width=150)
    deleted_subscribers_table.column("العمر", width=50)
    deleted_subscribers_table.column("الهاتف", width=100)
    deleted_subscribers_table.column("مدة الاشتراك", width=100)
    deleted_subscribers_table.column("حالة الاشتراك", width=100)
    deleted_subscribers_table.column("ملاحظات", width=100)
    deleted_subscribers_table.column("رقم السجل", width=100)
    deleted_subscribers_table.column("تاريخ الانتهاء", width=100)
    deleted_subscribers_table.column("الأيام المتبقية", width=100)
    deleted_subscribers_table.column("المبلغ المدفوع", width=100)
    deleted_subscribers_table.column("تاريخ الدفع", width=150)
    deleted_subscribers_table.column("مسار_الصورة", width=100)

    # إضافة زر "استعادة"
    restore_button = ttk.Button(deleted_subscribers_window, text="استعادة", command=lambda: restore_selected_row(deleted_subscribers_table))
    restore_button.pack(pady=10)

    # إضافة زر "حذف نهائيًا"
    delete_forever_button = ttk.Button(deleted_subscribers_window, text="حذف نهائيًا", command=lambda: delete_forever_selected_row(deleted_subscribers_table))
    delete_forever_button.pack(pady=10)

    # ملء الجدول بالبيانات من جدول المحذوفين
    fill_deleted_subscribers_table(deleted_subscribers_table)

# دالة لملء جدول المحذوفين بالبيانات
def fill_deleted_subscribers_table(deleted_subscribers_table):
    cursor.execute('''
        SELECT * FROM deleted_subscribers_table
    ''')
    deleted_subscribers = cursor.fetchall()

    for subscriber in deleted_subscribers:
        # حساب الأيام المتبقية
        end_date = datetime.strptime(subscriber[9], "%Y-%m-%d")  # تاريخ الانتهاء
        remaining_days = (end_date - datetime.now()).days
        subscriber = list(subscriber)  # تحويل الصف إلى قائمة قابلة للتعديل
        subscriber[10] = remaining_days  # تحديث الأيام المتبقية في البيانات

        # إضافة البيانات إلى جدول المحذوفين
        deleted_subscribers_table.insert("", "end", values=subscriber)

# دالة لاستعادة المشترك من جدول المحذوفين
def restore_selected_row(deleted_subscribers_table):
    selected_item = deleted_subscribers_table.selection()
    if not selected_item:
        messagebox.showerror("خطأ", "الرجاء تحديد مشترك لاستعادته.")
        return

    confirm = messagebox.askyesno("تأكيد الاستعادة", "هل أنت متأكد من رغبتك في استعادة هذا المشترك؟")
    if confirm:
        try:
            # الحصول على جميع الأعمدة من جدول المحذوفين
            cursor.execute('''
                SELECT * FROM deleted_subscribers_table WHERE رقم_الاشتراك=?
            ''', (deleted_subscribers_table.item(selected_item)["values"][1],))
            subscriber_data = cursor.fetchone()

            # إدراج البيانات في الجدول الرئيسي
            cursor.execute('''
                INSERT INTO main (تاريخ_التسجيل, رقم_الاشتراك, الاسم, العمر, الهاتف, مدة_الاشتراك, حالة_الاشتراك, ملاحظات, رقم_السجل, تاريخ_الانتهاء, الأيام_المتبقية, المبلغ_المدفوع, تاريخ_الدفع, مسار_الصورة)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', subscriber_data)
            conn.commit()

            # بعد الاستعادة من قاعدة البيانات، قم بحذف المشترك من جدول المحذوفين
            deleted_subscribers_table.delete(selected_item)

            messagebox.showinfo("تم الاستعادة", "تم استعادة المشترك بنجاح.")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء استعادة المشترك: {str(e)}")


# دالة لحذف المشترك نهائيًا
def delete_forever_selected_row(deleted_subscribers_table):
    selected_item = deleted_subscribers_table.selection()
    if not selected_item:
        messagebox.showerror("خطأ", "الرجاء تحديد مشترك لحذفه نهائيًا.")
        return

    confirm = messagebox.askyesno("تأكيد الحذف النهائي", "هل أنت متأكد من رغبتك في حذف هذا المشترك نهائيًا؟")
    if confirm:
        try:
            subscriber_data = deleted_subscribers_table.item(selected_item)["values"]
            cursor.execute('''
                DELETE FROM deleted_subscribers_table WHERE رقم_الاشتراك=?
            ''', (subscriber_data[1],))
            conn.commit()

            # بعد الحذف النهائي من قاعدة البيانات، قم بحذف المشترك من جدول المحذوفين
            deleted_subscribers_table.delete(selected_item)

            messagebox.showinfo("تم الحذف النهائي", "تم حذف المشترك نهائيًا بنجاح.")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء حذف المشترك نهائيًا: {str(e)}")







def edit_selected_row(results_table):
    selected_item = results_table.selection()
    if not selected_item:
        messagebox.showerror("خطأ", "الرجاء تحديد صف للتعديل.")
        return

    selected_row_data = results_table.item(selected_item, "values")
    edit_window = tk.Toplevel()
    edit_window.title("تعديل العضو")

    # الحصول على مفتاح السجل الفريد (رقم السجل) للمشترك المحدد
    selected_record_key = selected_row_data[8]

    # إعداد متغيرات النص للبيانات
    data_vars = [tk.StringVar(value=value) for value in selected_row_data]

    # الترتيب الصحيح للمربعات بناءً على التعديل السابق
    labels = ["تاريخ التسجيل", "رقم الاشتراك", "الاسم", "العمر", "الهاتف", "مدة الاشتراك", "حالة الاشتراك", "ملاحظات",
              "رقم السجل", "تاريخ الانتهاء", "الأيام المتبقية", "المبلغ المدفوع", "تاريخ الدفع", "مسار الصورة"]

    # في الدالة edit_selected_row، قم بتعديل هذا الجزء:
    for label, var in zip(labels, data_vars):
        ttk.Label(edit_window, text=label).pack()
        # قم بتعيين حالة الـ "readonly" بناءً على اختيارك
        entry_state = "normal" if label not in ["رقم الاشتراك", "المبلغ المدفوع", "تاريخ الدفع"] else "normal"
        entry = ttk.Entry(edit_window, textvariable=var, state=entry_state)
        entry.pack()

    # إعداد متغير نصي لحالة الاشتراك
    subscription_status_var = tk.StringVar(value=selected_row_data[6])

    # إعداد متغير نصي لفترة التوقف
    if selected_row_data[6] == "مجمد":
        stop_duration_var = tk.StringVar(value=selected_row_data[10])  # استخدم نفس القيمة المستخدمة لتجميد الاشتراك
    else:
        stop_duration_var = tk.StringVar()  # تأكد من تعريف المتغير هنا

    # إضافة مربعات اختيار لحالة الاشتراك
    ttk.Label(edit_window, text="حالة الاشتراك").pack()
    continuous_checkbox = ttk.Checkbutton(edit_window, text="مستمر", variable=subscription_status_var, onvalue="مستمر")
    continuous_checkbox.pack()
    stopped_checkbox = ttk.Checkbutton(edit_window, text="متوقف", variable=subscription_status_var, onvalue="متوقف")
    stopped_checkbox.pack()

    # إذا تم اختيار "متوقف"، أو "مجمد" قم بإعداد متغير نصي للأيام المتبقية
    if selected_row_data[6] in ["متوقف", "مجمد"]:
        remaining_days_var = tk.StringVar(value=selected_row_data[10])  # استخدم نفس القيمة المستخدمة للأيام المتبقية في حالة التوقف أو التجميد
    else:
        remaining_days_var = tk.StringVar()  # تأكد من تعريف المتغير هنا

    # إضافة مربع لعرض متغير الأيام المتبقية
    ttk.Label(edit_window, text="الأيام المتبقية").pack()
    remaining_days_entry = ttk.Entry(edit_window, textvariable=remaining_days_var, state="readonly")
    remaining_days_entry.pack()

    # إذا تم اختيار "متوقف"، أو "مجمد" قم بإضافة قائمة منسدلة لاختيار مدة التوقف
    if selected_row_data[6] in ["متوقف", "مجمد"]:
        stop_duration_label = ttk.Label(edit_window, text="مدة التوقف")
        stop_duration_label.pack()
        stop_duration_combobox = ttk.Combobox(edit_window, textvariable=stop_duration_var, values=["30 يومًا", "60 يومًا", "90 يومًا"])
        stop_duration_combobox.pack()

    # إعداد متغير نصي لصورة المشترك
    image_path_var = tk.StringVar(value=selected_row_data[13])

    # إضافة حقل لعرض مسار الصورة
    ttk.Label(edit_window, text="مسار الصورة").pack()
    image_path_entry = ttk.Entry(edit_window, textvariable=image_path_var, state="readonly")
    image_path_entry.pack()

    # دالة لفحص وجود ملف الصورة
    def check_image_path():
        if os.path.exists(image_path_var.get()):
            # إذا كان الملف موجودًا، يمكنك تنفيذ الإجراءات المناسبة هنا
            pass
        else:
            messagebox.showwarning("تحذير", "ملف الصورة غير موجود.")

    # إضافة زر "فحص ملف الصورة"
    check_image_button = ttk.Button(edit_window, text="فحص ملف الصورة", command=check_image_path)
    check_image_button.pack()

    # دالة لحفظ التحديث
    def save_updated_data():
        new_data = [var.get() for var in data_vars]
        new_data[6] = subscription_status_var.get()  # تحديث حالة الاشتراك

        # إذا كانت الحالة "متوقف" أو "مجمد"، قم بتحديث متغير الأيام المتبقية
        if subscription_status_var.get() in ["متوقف", "مجمد"]:
            new_data[10] = remaining_days_var.get()

        # إذا تم اختيار "متوقف"، أو "مجمد"، قم بتحديث متغير مدة التوقف
        if subscription_status_var.get() == "متوقف":
            new_data[10] = stop_duration_var.get().split()[0]

        # تحديث الصف المحدد في قاعدة البيانات باستخدام مفتاح السجل الفريد (رقم السجل)
        cursor.execute('''
            UPDATE main
            SET تاريخ_التسجيل=?, رقم_الاشتراك=?, الاسم=?, العمر=?, الهاتف=?, مدة_الاشتراك=?, حالة_الاشتراك=?, ملاحظات=?, رقم_السجل=?, تاريخ_الانتهاء=?, الأيام_المتبقية=?, المبلغ_المدفوع=?, تاريخ_الدفع=?, مسار_الصورة=?
            WHERE رقم_السجل=?
        ''', new_data + [selected_record_key])

        conn.commit()
        messagebox.showinfo("نجاح", "تم حفظ التحديث بنجاح!")
        edit_window.destroy()

    # إضافة زر "حفظ التحديث"
    save_button = ttk.Button(edit_window, text="حفظ التحديث", command=save_updated_data)
    save_button.pack()

    log_activity("تعديل", "تعديل.")





def open_search_window():
    search_window = tk.Toplevel()
    search_window.title("البحث والتعديل")

    # إعداد متغيرات واجهة المستخدم
    search_option_var = tk.StringVar(value="الاسم")

    # إعداد إطار البحث
    search_frame = ttk.Frame(search_window)
    search_frame.pack(padx=40, pady=20)

    search_label = ttk.Label(search_frame, text="بحث حسب:")
    search_label.grid(row=0, column=0, padx=5, pady=5)

    # إضافة خيار "رقم الاشتراك" إلى قائمة البحث
    search_option_menu = ttk.OptionMenu(search_frame, search_option_var, "الاسم", "رقم الهاتف", "رقم السجل", "رقم الاشتراك")
    search_option_menu.grid(row=0, column=1, padx=5, pady=5)

    search_entry = ttk.Entry(search_frame, width=30)
    search_entry.grid(row=0, column=2, padx=5, pady=5)

    # هنا يجب إعداد زر البحث وربطه بالدالة المناسبة
    search_button = ttk.Button(search_frame, text="بحث", command=lambda: display_search_results(search_window, search_entry, search_option_var))
    search_button.grid(row=0, column=3, padx=5, pady=5)


    log_activity("البحث والتعديل", "قام بفتح صفحة البحث والتعديل.")




import sqlite3
import datetime as dt

# إعداد قاعدة البيانات
conn = sqlite3.connect('gym_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY,
        date TEXT,
        description TEXT,
        amount REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        date TEXT,
        description TEXT,
        amount REAL
    )
''')

conn.commit()

# دالة لفتح نافذة الإيرادات
def open_income_window():
    income_window = tk.Toplevel()
    income_window.title("صفحة الإيرادات")

    # إعداد واجهة المستخدم لصفحة الإيرادات
    date_label = ttk.Label(income_window, text="التاريخ:")
    date_label.grid(row=0, column=0, padx=5, pady=5)
    income_date = ttk.Entry(income_window)
    income_date.grid(row=0, column=1, padx=5, pady=5)
    income_date.insert(0, dt.date.today())


    description_label = ttk.Label(income_window, text="وصف الإيراد:")
    description_label.grid(row=1, column=0, padx=5, pady=5)
    income_description = ttk.Entry(income_window)
    income_description.grid(row=1, column=1, padx=5, pady=5)

    amount_label = ttk.Label(income_window, text="المبلغ:")
    amount_label.grid(row=2, column=0, padx=5, pady=5)
    income_amount = ttk.Entry(income_window)
    income_amount.grid(row=2, column=1, padx=5, pady=5)

    def save_income():
        date = income_date.get()
        description = income_description.get()
        amount = income_amount.get()

        if date and description and amount:
            try:
                amount = float(amount)
                cursor.execute("INSERT INTO income (date, description, amount) VALUES (?, ?, ?)",
                               (date, description, amount))
                conn.commit()
                messagebox.showinfo("تم الحفظ", "تم حفظ الإيراد بنجاح.")
                income_window.destroy()
            except ValueError:
                messagebox.showerror("خطأ", "المبلغ يجب أن يكون رقمًا.")
        else:
            messagebox.showerror("خطأ", "الرجاء ملء جميع الحقول.")

    save_button = ttk.Button(income_window, text="حفظ", command=save_income)
    save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    # إضافة قائمة فرعية للإيرادات لاختيار الإيراد للتعديل
    income_list_label = ttk.Label(income_window, text="اختر الإيراد للتعديل:")
    income_list_label.grid(row=4, column=0, padx=5, pady=5)

    # استعلام لاسترداد جميع الإيرادات من قاعدة البيانات
    cursor.execute("SELECT id, date FROM income")
    income_records = cursor.fetchall()
    income_options = [f"{record[0]} - {record[1]}" for record in income_records]

    # قائمة فرعية تحتوي على الإيرادات
    income_combobox = ttk.Combobox(income_window, values=income_options)
    income_combobox.grid(row=4, column=1, padx=5, pady=5)

    def edit_income():
        selected_income = income_combobox.get()

        # استخراج رقم الإيراد من الاختيار المحدد
        selected_income_id = selected_income.split('-')[0].strip()

        # انفتح نافذة تعديل الإيراد باستخدام الرقم المحدد
        if selected_income_id:
            edit_income_window = tk.Toplevel()
            edit_income_window.title("تعديل الإيراد")

            # استعلام لاسترداد بيانات الإيراد المحدد من قاعدة البيانات
            cursor.execute("SELECT * FROM income WHERE id=?", (selected_income_id,))
            income_data = cursor.fetchone()

            if income_data:
                # إعداد واجهة المستخدم لنافذة تعديل الإيراد
                date_label = ttk.Label(edit_income_window, text="التاريخ:")
                date_label.grid(row=0, column=0, padx=5, pady=5)
                edit_date = ttk.Entry(edit_income_window)
                edit_date.grid(row=0, column=1, padx=5, pady=5)
                edit_date.insert(0, income_data[1])  # تعبئة التاريخ الحالي

                description_label = ttk.Label(edit_income_window, text="وصف الإيراد:")
                description_label.grid(row=1, column=0, padx=5, pady=5)
                edit_description = ttk.Entry(edit_income_window)
                edit_description.grid(row=1, column=1, padx=5, pady=5)
                edit_description.insert(0, income_data[2])  # تعبئة وصف الإيراد الحالي

                amount_label = ttk.Label(edit_income_window, text="المبلغ:")
                amount_label.grid(row=2, column=0, padx=5, pady=5)
                edit_amount = ttk.Entry(edit_income_window)
                edit_amount.grid(row=2, column=1, padx=5, pady=5)
                edit_amount.insert(0, income_data[3])  # تعبئة المبلغ الحالي

                def save_edited_income():
                    new_date = edit_date.get()
                    new_description = edit_description.get()
                    new_amount = edit_amount.get()

                    if new_date and new_description and new_amount:
                        try:
                            new_amount = float(new_amount)
                            cursor.execute("UPDATE income SET date=?, description=?, amount=? WHERE id=?",
                                           (new_date, new_description, new_amount, selected_income_id))
                            conn.commit()
                            messagebox.showinfo("تم التعديل", "تم تعديل الإيراد بنجاح.")
                            edit_income_window.destroy()
                        except ValueError:
                            messagebox.showerror("خطأ", "المبلغ يجب أن يكون رقمًا.")
                    else:
                        messagebox.showerror("خطأ", "الرجاء ملء جميع الحقول.")

                save_button = ttk.Button(edit_income_window, text="حفظ التعديل", command=save_edited_income)
                save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
            else:
                messagebox.showerror("خطأ", "لم يتم العثور على الإيراد.")
        else:
            messagebox.showerror("خطأ", "الرجاء اختيار إيراد للتعديل.")

    # زر لتعديل الإيراد
    edit_button = ttk.Button(income_window, text="تعديل الإيراد", command=edit_income)
    edit_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)
    log_activity("الايرادات ", "الايرادات.")

# دالة لفتح نافذة المصروفات
def open_expense_window():
    expense_window = tk.Toplevel()
    expense_window.title("صفحة المصروفات")

    # إعداد واجهة المستخدم لصفحة المصروفات
    date_label = ttk.Label(expense_window, text="التاريخ:")
    date_label.grid(row=0, column=0, padx=5, pady=5)
    expense_date = ttk.Entry(expense_window)
    expense_date.grid(row=0, column=1, padx=5, pady=5)
    expense_date.insert(0, dt.date.today())


    description_label = ttk.Label(expense_window, text="وصف المصروف:")
    description_label.grid(row=1, column=0, padx=5, pady=5)
    expense_description = ttk.Entry(expense_window)
    expense_description.grid(row=1, column=1, padx=5, pady=5)

    amount_label = ttk.Label(expense_window, text="المبلغ:")
    amount_label.grid(row=2, column=0, padx=5, pady=5)
    expense_amount = ttk.Entry(expense_window)
    expense_amount.grid(row=2, column=1, padx=5, pady=5)

    def save_expense():
        date = expense_date.get()
        description = expense_description.get()
        amount = expense_amount.get()

        if date and description and amount:
            try:
                amount = float(amount)
                cursor.execute("INSERT INTO expenses (date, description, amount) VALUES (?, ?, ?)",
                               (date, description, amount))
                conn.commit()
                messagebox.showinfo("تم الحفظ", "تم حفظ المصروف بنجاح.")
                expense_window.destroy()
            except ValueError:
                messagebox.showerror("خطأ", "المبلغ يجب أن يكون رقمًا.")
        else:
            messagebox.showerror("خطأ", "الرجاء ملء جميع الحقول.")

    save_button = ttk.Button(expense_window, text="حفظ", command=save_expense)
    save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    # إضافة قائمة فرعية للمصروفات لاختيار المصروف للتعديل
    expense_list_label = ttk.Label(expense_window, text="اختر المصروف للتعديل:")
    expense_list_label.grid(row=4, column=0, padx=5, pady=5)

    # استعلام لاسترداد جميع المصروفات من قاعدة البيانات
    cursor.execute("SELECT id, date FROM expenses")
    expense_records = cursor.fetchall()
    expense_options = [f"{record[0]} - {record[1]}" for record in expense_records]

    # قائمة فرعية تحتوي على المصروفات
    expense_combobox = ttk.Combobox(expense_window, values=expense_options)
    expense_combobox.grid(row=4, column=1, padx=5, pady=5)

    def edit_expense():
        selected_expense = expense_combobox.get()

        # استخراج رقم المصروف من الاختيار المحدد
        selected_expense_id = selected_expense.split('-')[0].strip()

        # انفتح نافذة تعديل المصروف باستخدام الرقم المحدد
        if selected_expense_id:
            edit_expense_window = tk.Toplevel()
            edit_expense_window.title("تعديل المصروف")

            # استعلام لاسترداد بيانات المصروف المحدد من قاعدة البيانات
            cursor.execute("SELECT * FROM expenses WHERE id=?", (selected_expense_id,))
            expense_data = cursor.fetchone()

            if expense_data:
                # إعداد واجهة المستخدم لنافذة تعديل المصروف
                date_label = ttk.Label(edit_expense_window, text="التاريخ:")
                date_label.grid(row=0, column=0, padx=5, pady=5)
                edit_date = ttk.Entry(edit_expense_window)
                edit_date.grid(row=0, column=1, padx=5, pady=5)
                edit_date.insert(0, expense_data[1])  # تعبئة التاريخ الحالي

                description_label = ttk.Label(edit_expense_window, text="وصف المصروف:")
                description_label.grid(row=1, column=0, padx=5, pady=5)
                edit_description = ttk.Entry(edit_expense_window)
                edit_description.grid(row=1, column=1, padx=5, pady=5)
                edit_description.insert(0, expense_data[2])  # تعبئة وصف المصروف الحالي

                amount_label = ttk.Label(edit_expense_window, text="المبلغ:")
                amount_label.grid(row=2, column=0, padx=5, pady=5)
                edit_amount = ttk.Entry(edit_expense_window)
                edit_amount.grid(row=2, column=1, padx=5, pady=5)
                edit_amount.insert(0, expense_data[3])  # تعبئة المبلغ الحالي

                def save_edited_expense():
                    new_date = edit_date.get()
                    new_description = edit_description.get()
                    new_amount = edit_amount.get()

                    if new_date and new_description and new_amount:
                        try:
                            new_amount = float(new_amount)
                            cursor.execute("UPDATE expenses SET date=?, description=?, amount=? WHERE id=?",
                                           (new_date, new_description, new_amount, selected_expense_id))
                            conn.commit()
                            messagebox.showinfo("تم التعديل", "تم تعديل المصروف بنجاح.")
                            edit_expense_window.destroy()
                        except ValueError:
                            messagebox.showerror("خطأ", "المبلغ يجب أن يكون رقمًا.")
                    else:
                        messagebox.showerror("خطأ", "الرجاء ملء جميع الحقول.")

                save_button = ttk.Button(edit_expense_window, text="حفظ التعديل", command=save_edited_expense)
                save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
            else:
                messagebox.showerror("خطأ", "لم يتم العثور على المصروف.")
        else:
            messagebox.showerror("خطأ", "الرجاء اختيار مصروف للتعديل.")

    # زر لتعديل المصروف
    edit_button = ttk.Button(expense_window, text="تعديل المصروف", command=edit_expense)
    edit_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)
    log_activity("المصروفات", "المصروفات.")


import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime as dt

# إعداد قاعدة البيانات
conn = sqlite3.connect('gym_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY,
        date TEXT,
        description TEXT,
        amount REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        date TEXT,
        description TEXT,
        amount REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS main (
        id INTEGER PRIMARY KEY,
        name TEXT,
        join_date TEXT,
        subscription_fee REAL,
        registration_date TEXT  -- إضافة خانة تاريخ التسجيل
    )
''')


conn.commit()

# دالة لفتح صفحة التقارير
def open_report_window():
    report_window = tk.Toplevel()
    report_window.title("صفحة التقارير")

    # إعداد واجهة المستخدم لصفحة التقارير
    start_date_label = ttk.Label(report_window, text="تاريخ البداية:")
    start_date_label.grid(row=0, column=0, padx=5, pady=5)
    start_date_entry = ttk.Entry(report_window)
    start_date_entry.grid(row=0, column=1, padx=5, pady=5)
    start_date_entry.insert(0, dt.date.today())

    end_date_label = ttk.Label(report_window, text="تاريخ النهاية:")
    end_date_label.grid(row=1, column=0, padx=5, pady=5)
    end_date_entry = ttk.Entry(report_window)
    end_date_entry.grid(row=1, column=1, padx=5, pady=5)
    end_date_entry.insert(0, dt.date.today())

    report_type_label = ttk.Label(report_window, text="نوع التقرير:")
    report_type_label.grid(row=2, column=0, padx=5, pady=5)

    # إضافة قائمة منسدلة لاختيار نوع التقرير
    report_type_combobox = ttk.Combobox(report_window, values=["إيرادات", "مصروفات", "مشتركين"])
    report_type_combobox.grid(row=2, column=1, padx=5, pady=5)

    report_table = None  # تعريف المتغير كمتغير عالمي

    def generate_report():
        global report_table  # قم بتعريف المتغير كمتغير عالمي
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        report_type = report_type_combobox.get()

        if start_date and end_date and report_type:
            # قم بفتح نافذة جديدة لعرض التقرير
            report_result_window = tk.Toplevel()
            report_result_window.title("نتائج التقرير")

            # إعداد الجدول لعرض البيانات
            report_table = ttk.Treeview(report_result_window)

            # تحديد عناوين الأعمدة بناءً على نوع التقرير
            if report_type == "إيرادات":
                report_table["columns"] = ("Date", "Description", "Amount")
                report_table.heading("#1", text="التاريخ")
                report_table.heading("#2", text="الوصف")
                report_table.heading("#3", text="المبلغ")
            elif report_type == "مصروفات":
                report_table["columns"] = ("Date", "Description", "Amount")
                report_table.heading("#1", text="التاريخ")
                report_table.heading("#2", text="الوصف")
                report_table.heading("#3", text="المبلغ")
            elif report_type == "مشتركين":
                report_table = ttk.Treeview(report_result_window, columns=("Name", "Subscription Number", "Join Date", "Subscription Fee"))
                report_table.heading("#1", text="تاريخ الانضمام")
                report_table.heading("#2", text="رقم الاشتراك")
                report_table.heading("#3", text="الاسم")
                report_table.heading("#4", text="المبلغ")

            report_table.pack()

            def close_report_result_window():
                report_result_window.destroy()

            # زر "إلغاء" لإغلاق نافذة عرض التقرير
            cancel_button = ttk.Button(report_result_window, text="إلغاء", command=close_report_result_window)
            cancel_button.pack()

            # إضافة شريط التمرير إذا كان هناك العديد من السجلات
            report_scrollbar = ttk.Scrollbar(report_result_window, orient="vertical", command=report_table.yview)
            report_scrollbar.pack(side="right", fill="y")
            report_table.configure(yscrollcommand=report_scrollbar.set)

            # استخدم استعلام SQL لاسترداد البيانات المطلوبة من قاعدة البيانات
            if report_type == "إيرادات":
                cursor.execute("SELECT date, description, amount FROM income WHERE date BETWEEN ? AND ?",
                               (start_date, end_date))
            elif report_type == "مصروفات":
                cursor.execute("SELECT date, description, amount FROM expenses WHERE date BETWEEN ? AND ?",
                               (start_date, end_date))
            elif report_type == "مشتركين":
                cursor.execute(
                    "SELECT تاريخ_التسجيل, رقم_الاشتراك, الاسم, المبلغ_المدفوع FROM main WHERE تاريخ_التسجيل BETWEEN ? AND ?",
                    (start_date, end_date))


            report_data = cursor.fetchall()

            # إضافة البيانات إلى الجدول
            for row in report_data:
                report_table.insert("", "end", values=row)

            # حساب الإجمالي إذا كان نوع التقرير هو إيرادات أو مصروفات أو مشتركين
            if report_type in ["إيرادات", "مصروفات"]:
                total_amount = sum(float(row[2]) for row in report_data)
                total_label = ttk.Label(report_result_window, text=f"الإجمالي: {total_amount}")
                total_label.pack()
            elif report_type == "مشتركين":
                total_amount = sum(float(row[3]) for row in report_data)  # العمود الرابع هو المبلغ في تقرير المشتركين
                total_label = ttk.Label(report_result_window, text=f"الإجمالي: {total_amount}")
                total_label.pack()

        else:
            messagebox.showerror("خطأ", "الرجاء ملء جميع الحقول.")

    # زر "موافق" لإنشاء التقرير
    generate_button = ttk.Button(report_window, text="موافق", command=generate_report)
    generate_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
    log_activity("التقارير", "التقارير.")

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pyzbar.pyzbar import decode
import sqlite3
from fpdf import FPDF
import cv2
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from playsound import playsound
from reportlab.lib.pagesizes import letter, landscape, portrait
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import arabic_reshaper
from bidi.algorithm import get_display
import pandas as pd
import time  # قم بإضافة استيراد مكتبة الوقت في أعلى الكود
from PIL import Image, ImageTk
import ast
from datetime import datetime
import seaborn as sns

# تثبيت مظهر Seaborn
sns.set_theme()
image = None
image_label = None
results_window = None  # Initialize results_window as a global variable

# تعريف متغير عام لحالة البحث وقائمة للنتائج وقائمة لتاريخ البحث وقائمة لسجل البحث
searching = False
search_results = []
search_dates = []
search_history = []

# تعريف متغير عام لعرض الإحصائيات
stats_label = None
# تعريف متغير لسجل الحضور اليومي
daily_attendance_count = 0  # عدد مسجلي الحضور اليومي
total_attendance_count = 0  # إجمالي عدد مسجلي الحضور
daily_attendance_list = []  # قائمة مسجلي الحضور اليومي

# تعريف متغير عام لحالة الكاميرا وضبطه بالقيمة الافتراضية True للكاميرا مفتوحة
camera_open = True


import sqlite3
import sqlite3

import sqlite3

# تحديث جدول البحث
def create_search_history_table():
    connection = sqlite3.connect("gym_database.db")
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS search_history (
        تاريخ_التسجيل TEXT,
        رقم_الاشتراك TEXT,
        الاسم TEXT,
        العمر TEXT,
        الهاتف TEXT,
        مدة_الاشتراك TEXT,
        حالة_الاشتراك TEXT,
        ملاحظات TEXT,
        رقم_السجل TEXT,
        تاريخ_الانتهاء TEXT,
        الأيام_المتبقية INTEGER,
        المبلغ_المدفوع REAL,
        تاريخ_الدفع TEXT,
        مسار_الصورة TEXT,
        تاريخ_البحث TEXT  -- إضافة حقل تاريخ_البحث هنا
    );
    """)
    connection.commit()
    connection.close()

# تشغيل دالة إنشاء جدول البحث
create_search_history_table()



search_columns = ["تاريخ_التسجيل", "رقم_الاشتراك", "الاسم", "العمر", "الهاتف", "مدة", "حالة_الاشتراك", "ملاحظات", "السجل", "الانتهاء", "الأيام", "المبلغ", "الدفع", "مسار_الصورة"]


# تعريف قائمة لسجل البحث
search_history = []
history_tree = None


# دالة لفتح صفحة البحث بواسطة الكيور ار كود
def open_qr_search():
    global searching
    searching = False

    qr_search_window = tk.Tk()
    qr_search_window.title("بحث بواسطة الكيور ار كود")

    # تكوين خاصية الخط العريض للنص في ttk.Style
    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 14, "bold"))
    style.configure("TButton", font=("Helvetica", 14, "bold"))
    style.configure('Custom.TButton', relief="raised", borderwidth=2, background='#4CAF50', foreground='white')

    # دالة لتحديث العلم searching وإغلاق النافذة بشكل صحيح
    def update_searching():
        global searching
        searching = False
        qr_search_window.destroy()

    # إنشاء إطار لعرض نتائج البحث
    result_frame = ttk.Frame(qr_search_window)
    result_frame.pack(fill="both", expand=True)

    # إنشاء جدول لعرض النتائج في النافذة الرئيسية
    results_table = ttk.Treeview(qr_search_window, columns=(
        "تاريخ التسجيل", "رقم الاشتراك", "الاسم", "العمر", "الهاتف",
        "مدة الاشتراك", "حالة الاشتراك", "ملاحظات", "رقم السجل",
        "تاريخ الانتهاء", "الأيام المتبقية", "المبلغ المدفوع", "تاريخ الدفع", "صورة"
    ), show="headings")

    # تعيين عناوين الأعمدة
    results_table.heading("تاريخ التسجيل", text="تاريخ التسجيل")
    results_table.heading("رقم الاشتراك", text="رقم الاشتراك")
    results_table.heading("الاسم", text="الاسم")
    results_table.heading("العمر", text="العمر")
    results_table.heading("الهاتف", text="الهاتف")
    results_table.heading("مدة الاشتراك", text="مدة الاشتراك")
    results_table.heading("حالة الاشتراك", text="حالة الاشتراك")
    results_table.heading("ملاحظات", text="ملاحظات")
    results_table.heading("رقم السجل", text="رقم السجل")
    results_table.heading("تاريخ الانتهاء", text="تاريخ الانتهاء")
    results_table.heading("الأيام المتبقية", text="الأيام المتبقية")
    results_table.heading("المبلغ المدفوع", text="المبلغ المدفوع")
    results_table.heading("تاريخ الدفع", text="تاريخ الدفع")
    results_table.heading("صورة", text="صورة")

    # تحديد عرض الأعمدة
    results_table.column("تاريخ التسجيل", width=100)
    results_table.column("رقم الاشتراك", width=70)
    results_table.column("الاسم", width=150)
    results_table.column("العمر", width=50)
    results_table.column("الهاتف", width=100)
    results_table.column("مدة الاشتراك", width=100)
    results_table.column("حالة الاشتراك", width=100)
    results_table.column("ملاحظات", width=100)
    results_table.column("رقم السجل", width=100)
    results_table.column("تاريخ الانتهاء", width=100)
    results_table.column("الأيام المتبقية", width=100)
    results_table.column("المبلغ المدفوع", width=100)
    results_table.column("تاريخ الدفع", width=150)
    results_table.column("صورة", width=100)

    results_table.pack(padx=20, pady=10)

    def get_subscription_info(subscription_number):
        try:
            connection = sqlite3.connect("gym_database.db")
            cursor = connection.cursor()

            # استعلام لاسترجاع مدة الاشتراك والأيام المتبقية
            query = f"""
                SELECT مدة_الاشتراك, الايام_المتبقية FROM subscriptions
                WHERE رقم_الاشتراك = '{subscription_number}'
            """
            cursor.execute(query)
            subscription_info = cursor.fetchone()

            connection.close()

            return subscription_info

        except Exception as e:
            print("Error fetching subscription info:", str(e))
            return None

    def get_search_dates(subscription_number):
        try:
            connection = sqlite3.connect("gym_database.db")
            cursor = connection.cursor()

            # استعلام لاسترجاع تواريخ البحث
            query = f"""
                SELECT تاريخ_البحث FROM search_history
                WHERE رقم_الاشتراك = '{subscription_number}'
            """
            cursor.execute(query)
            search_dates = cursor.fetchall()

            connection.close()

            return [date[0] for date in search_dates]

        except Exception as e:
            print("Error fetching search dates:", str(e))
            return []

    def get_attended_days(subscription_number):
        search_dates = get_search_dates(subscription_number)
        return len(search_dates)



    def display_search_results(results):
        global results_window  # Declare results_window as a global variable

        # استخدم الجدول في نافذة النتائج
        results_window = tk.Toplevel()
        results_window.title("نتائج البحث")

        # تحديث العرض ليشمل عدد الأيام التي حضرها المشترك
        for result in results:
            # حساب الأيام المتبقية
            end_date = datetime.strptime(result[9], "%Y-%m-%d")  # تاريخ الانتهاء
            remaining_days = (end_date - datetime.now()).days
            result = list(result)  # تحويل الصف إلى قائمة قابلة للتعديل
            result[10] = remaining_days  # تحديث الأيام المتبقية في البيانات
            # إضافة عدد الأيام التي حضرها المشترك
            attended_days = get_attended_days(result[1])  # استخراج عدد الأيام التي حضرها المشترك
            result.append(attended_days)  # إضافة عدد الأيام التي حضرها المشترك إلى البيانات
            # إخفاء رقم الهاتف بواسطة استبداله بنجمات
            result[4] = '*' * len(result[4])
            # استرجاع مسار الصورة من قاعدة البيانات
            image_path = get_image_path_from_db(result[1])

            # عرض الصورة
            if image_path:
                display_image(image_path, remaining_days, attended_days)
            else:
                # في حالة عدم وجود صورة، قم بعرض صورة افتراضية
                default_image_path = "C:/Users/POWER KING/Desktop/sest/images/افتراضية 2.jpg"
                display_image(default_image_path, remaining_days, attended_days)

            # إضافة البيانات إلى الجدول
            results_table.insert("", "end", values=result)

            # إنشاء زر لاختيار وحفظ الصورة
            select_image_button = ttk.Button(results_window, text="اختيار وحفظ الصورة",
                                             command=lambda sub=result[1]: select_and_save_image(sub))
            select_image_button.pack()

            save_search_to_database(results, search_value)

    def display_image(image_path, remaining_days, attended_days):
        try:
            img = Image.open(image_path)
            img.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(img)
            label = ttk.Label(results_window, image=photo)
            label.image = photo
            label.pack()

            # حساب عدد الأيام التي لم يحضرها المشترك (أيام الغياب)
            total_days = attended_days + remaining_days
            absent_days = total_days - attended_days

            # عرض عدد الأيام التي حضرها المشترك داخل إطار
            attended_frame = ttk.Frame(results_window)
            attended_frame.pack(pady=5)
            attended_label = ttk.Label(attended_frame, text=f"عدد الأيام التي حضرها: {attended_days}",
                                       foreground='green', font=("Helvetica", 12, "bold"))
            attended_label.pack()

            # عرض عدد الأيام المتبقية داخل إطار
            remaining_frame = ttk.Frame(results_window)
            remaining_frame.pack(pady=5)
            remaining_label = ttk.Label(remaining_frame, text=f"الأيام المتبقية: {remaining_days}", foreground='blue',
                                        font=("Helvetica", 12, "bold"))
            remaining_label.pack()



        except Exception as e:
            print("حدث خطأ أثناء عرض الصورة:", e)

    # دالة لاختيار وحفظ الصورة
    def select_and_save_image(subscription_number):
        file_path = filedialog.askopenfilename()
        if file_path:
            # حفظ الصورة في قاعدة البيانات
            save_image(file_path, subscription_number)
            # عرض الصورة
            display_image(file_path)

    # دالة لمسح النتائج الحالية
    def clear_current_results():
        global search_results
        # تفريغ نافذة البحث من النتائج الحالية
        results_table.delete(*results_table.get_children())
        # تفريغ القائمة التي تحتوي على النتائج الحالية
        search_results = []

    # داخل الدالة search_by_qr_code
    # داخل الدالة search_by_qr_code
    def search_by_qr_code():
        global searching, search_results, search_dates, search_value, daily_attendance_count, total_attendance_count, daily_attendance_list
        searching = True
        search_value = None  # Initialize search_value

        cap = cv2.VideoCapture(0)

        while searching:
            ret, frame = cap.read()

            if not ret:
                continue

            decoded_objects = decode(frame)
            for obj in decoded_objects:
                if obj.type == 'QRCODE':
                    search_value = obj.data.decode('utf-8').strip()  # إزالة أي مسافات زائدة

                    # تحقق من أن القيمة المستخرجة هي رقم صحيح
                    try:
                        search_value = int(search_value)
                    except ValueError:
                        messagebox.showerror("خطأ", "قيمة غير صحيحة في الكيور ار كود.")
                        searching = False
                        return

                    connection = sqlite3.connect("gym_database.db")
                    cursor = connection.cursor()
                    query = f"SELECT * FROM main WHERE رقم_الاشتراك = ?"
                    cursor.execute(query, (search_value,))
                    rows = cursor.fetchall()

                    if rows:
                        # تحويل النتائج إلى قواميس وتحديث الأيام المتبقية
                        updated_results = []
                        for row in rows:
                            row_dict = list(row)
                            end_date = datetime.strptime(row[9], "%Y-%m-%d")
                            current_date = datetime.now()
                            remaining_days = (end_date - current_date).days
                            if row[6] == "متجمد":  # التحقق من حالة الاشتراك
                                remaining_days = row[10]  # الاحتفاظ بعدد الأيام المتبقية كما هو
                            row_dict[10] = remaining_days  # تحديث القيمة
                            updated_results.append(row_dict)

                        search_results = updated_results

                        # تحديث الوقت بالتوقيت الحالي داخل الحلقة
                        current_search_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        search_dates.append(current_search_time)
                        print("Search Results:", search_results)  # Add this print statement

                        # تسجيل تاريخ البحث
                        for result in updated_results:
                            result.append(current_search_time)

                        # تشغيل ملف الصوت للنجاح
                        playsound("C:\\Users\\POWER KING\\Desktop\\sest\\ElevenLabs_2023-11-06T16_49_33_Callum.wav")

                        display_search_results(search_results)  # عرض النتائج في الجدول

                        # حفظ سجل البحث
                        # حفظ سجل البحث
                        search_history.append(updated_results)

                        # إضافة السجل إلى قائمة مسجلي الحضور اليومي
                        daily_attendance_list.extend(updated_results)

                        # إحصائيات عدد مسجلي الحضور اليومي
                        daily_attendance_count += len(updated_results)
                        total_attendance_count += len(updated_results)

                        stats_label.config(
                            text=f"عدد مسجلي الحضور اليومي: {len(updated_results)} - إجمالي الحضور: {total_attendance_count}")

                        searching = False
                    else:
                        messagebox.showerror("خطأ", "لم يتم العثور على المشترك.")
                        searching = False

                        # تشغيل ملف الصوت للفشل
                        playsound("C:\\Users\\POWER KING\\Desktop\\sest\\failure_sound.wav")

                    connection.close()

            cv2.imshow("Camera", frame)
            if cv2.waitKey(1) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    # Rest of your code...

    # إضافة وسم لعرض الإحصائيات
    stats_label = ttk.Label(qr_search_window, text="", font=("Helvetica", 12))
    stats_label.pack(pady=10)

    # إضافة زر بحث بواسطة الكيور ار كود
    search_button = ttk.Button(qr_search_window, text="بحث بواسطة الكيور ار كود", command=search_by_qr_code)
    search_button.pack(pady=10)

    # إضافة زر مسح النتائج الحالية
    clear_button = ttk.Button(qr_search_window, text="مسح النتائج الحالية", command=clear_current_results)
    clear_button.pack(pady=10)

    # إضافة زر البحث السابق
    search_history_button = ttk.Button(qr_search_window, text="البحث السابق", command=show_search_history)
    search_history_button.pack(pady=10)

    # إغلاق نافذة البحث بواسطة الكيور ار كود
    qr_search_window.protocol("WM_DELETE_WINDOW", update_searching)

    qr_search_window.mainloop()
    log_activity("بحث qrcode", "بحث qrcode.")


# تعريف الدالة لحفظ نتائج البحث في جدول البحث
def save_search_to_database(search_results, search_value):
    try:
        connection = sqlite3.connect("gym_database.db")
        cursor = connection.cursor()

        columns_order = [
            "تاريخ_التسجيل", "رقم_الاشتراك", "الاسم", "العمر", "الهاتف", "مدة_الاشتراك",
            "حالة_الاشتراك", "ملاحظات", "رقم_السجل", "تاريخ_الانتهاء", "الأيام_المتبقية",
            "المبلغ_المدفوع", "تاريخ_الدفع", "مسار_الصورة", "تاريخ_البحث"
        ]

        search_results_ordered = []
        for result in search_results:
            current_search_time = get_current_date()
            result.append(current_search_time)  # إضافة تاريخ البحث
            ordered_result = [result[columns_order.index(col)] for col in columns_order]
            search_results_ordered.append(ordered_result)

        cursor.executemany("""
            INSERT INTO search_history 
            (تاريخ_التسجيل, رقم_الاشتراك, الاسم, العمر, الهاتف, مدة_الاشتراك,
            حالة_الاشتراك, ملاحظات, رقم_السجل, تاريخ_الانتهاء, الأيام_المتبقية,
            المبلغ_المدفوع, تاريخ_الدفع, مسار_الصورة, تاريخ_البحث) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, search_results_ordered)

        connection.commit()
        connection.close()

        print("تم حفظ البيانات في جدول البحث بنجاح.")
    except Exception as e:
        print("خطأ في حفظ البيانات:", str(e))


# تعريف الدالة للحصول على التاريخ والوقت الحالي
def get_current_date():
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date







def show_search_history():
    global search_history, search_dates

    if search_history:
        history_window = tk.Toplevel()
        history_window.title("سجل البحث السابق")

        history_frame = ttk.Frame(history_window)
        history_frame.pack(fill="both", expand=True)

        history_columns = [
            "تاريخ_التسجيل", "رقم_الاشتراك", "الاسم", "العمر",
            "الهاتف", "مدة_الاشتراك", "حالة_الاشتراك", "ملاحظات", "رقم_السجل",
            "تاريخ_الانتهاء", "الأيام_المتبقية", "المبلغ_المدفوع", "تاريخ_الدفع", "مسار_الصورة", "تاريخ_البحث"
        ]

        history_tree = ttk.Treeview(history_frame, columns=history_columns, show="headings")

        for col in history_columns:
            history_tree.heading(col, text=col)
            history_tree.column(col, width=100)  # تعيين عرض الأعمدة

        history_tree.pack(fill="both", expand=True, padx=10, pady=10, ipadx=10, ipady=10, side="left")

        # إضافة Scrollbar للتمرير الرأسي
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=history_tree.yview)
        # ربط Scrollbar بـ Treeview
        history_tree.configure(yscrollcommand=scrollbar.set)
        # تعيين Scrollbar في النافذة
        scrollbar.pack(side="right", fill="y")

        # تحميل بيانات التسجيل من قاعدة البيانات
        connection = sqlite3.connect("gym_database.db")
        cursor = connection.cursor()
        query = "SELECT * FROM search_history ORDER BY تاريخ_البحث DESC"  # ترتيب النتائج بناءً على تاريخ البحث بترتيب تنازلي
        cursor.execute(query)

        # استخدام cursor.description للحصول على أسماء الأعمدة
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        connection.close()

        print("Columns in Database:", columns)

        # إضافة بيانات التسجيل إلى شجرة التاريخ
        for row in rows:
            modified_row = list(row)  # إنشاء نسخة قابلة للتعديل من الصف
            for i, col in enumerate(columns):
                if col == "الهاتف":
                    # إذا كان العمود هو "الهاتف"، قم بتحويل القيمة إلى سلسلة نجوم
                    modified_row[i] = "*" * len(str(row[i]))

            history_tree.insert("", "end", values=modified_row)

        # تحديد الصف الأول (الأحدث) بعد تحميل البيانات
        history_tree.selection_set(history_tree.get_children()[0])

        # إضافة زر حفظ كـ Excel داخل الصفحة
        save_excel_button = ttk.Button(history_window, text="حفظ كـ Excel", command=save_search_history_as_excel)
        save_excel_button.pack(pady=10)

        # إضافة وسم لعرض إحصائيات مسجلي الحضور اليومي
        attendance_stats_label = ttk.Label(history_window, text="", font=("Helvetica", 12))
        attendance_stats_label.pack(pady=10)

        # حساب وعرض إحصائيات مسجلي الحضور اليومي
        attendance_count = len(daily_attendance_list)
        attendance_stats_label.config(text=f"عدد مسجلي الحضور اليومي: {attendance_count}")

    log_activity("البحث السابق", "البحث السابق.")





import sys

# حفظ القيمة الأصلية لـ sys.stdout
original_stdout = sys.stdout

# تعيين sys.stdout إلى None لمنع الطباعة في الترمينال
sys.stdout = None

# دالة لتحميل البيانات من قاعدة البيانات
def load_data():
    global search_history, search_dates

    # Load data from the database
    connection = sqlite3.connect("gym_database.db")
    cursor = connection.cursor()
    query = "SELECT * FROM search_history"
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.close()

    # Extract data and dates
    for row in rows:
        try:
            evaluated_data = ast.literal_eval(row[3])
            search_history.append(evaluated_data)
        except Exception as e:
            pass  # تجاهل الأخطاء

    search_dates = [row[2] for row in rows]

# استعادة قيمة sys.stdout الأصلية
sys.stdout = original_stdout

# استدعاء load_data() عند بدء تشغيل البرنامج
load_data()



# يتم استدعاء الدالة عند الضغط على الزر "حفظ كـ Excel" في صفحة سجل البحث السابق
def save_search_history_as_excel():
    # اختر ملف الإكسل للحفظ
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])

    if not file_path:
        return  # في حالة الإلغاء

    # إنشاء DataFrame باستخدام جميع السجلات في search_history
    all_history = [item for sublist in search_history for item in sublist]
    df = pd.DataFrame(all_history, columns=search_columns)

    # حفظ DataFrame في ملف إكسل
    df.to_excel(file_path, index=False)

    log_activity("حفظ البحث", "حفظ البحث.")

# دالة لفتح صفحة البحث اليدوي
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from datetime import datetime
import sqlite3

def open_manual_search():
    manual_search_window = tk.Toplevel()
    manual_search_window.title("البحث اليدوي")

    def search_manual():
        search_value = manual_search_var.get()
        search_type = search_type_var.get()

        column_names = [
            "تاريخ_التسجيل", "رقم_الاشتراك", "الاسم", "العمر",
            "الهاتف", "مدة_الاشتراك", "حالة_الاشتراك", "ملاحظات", "رقم_السجل",
            "تاريخ_الانتهاء", "الأيام_المتبقية", "المبلغ_المدفوع", "تاريخ_الدفع"
        ]

        connection = sqlite3.connect("gym_database.db")
        cursor = connection.cursor()
        query = f"SELECT * FROM main WHERE {search_type} LIKE ?"
        cursor.execute(query, (f"%{search_value}%",))
        search_results = cursor.fetchall()

        # حذف النتائج السابقة من جدول النتائج
        for row in result_tree.get_children():
            result_tree.delete(row)

        for result in search_results:
            # حساب الأيام المتبقية
            end_date_str = result[9]  # تاريخ الانتهاء كنص
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")  # تحويله إلى كائن تاريخ
            today = datetime.now()  # تاريخ اليوم
            remaining_days = (end_date - today).days  # حساب الأيام المتبقية

            # التحقق من حالة الاشتراك
            if result[6] == "متجمد":
                remaining_days = result[10]  # الاحتفاظ بعدد الأيام المتبقية كما هو

            # تحديث القيمة في البيانات
            result = list(result)  # تحويل الصف إلى قائمة قابلة للتعديل
            result[4] = '*' * len(result[4])  # تحديث الهاتف ليظهر بدلًا من الرقم
            result[10] = remaining_days  # تحديث الأيام المتبقية في البيانات
            result_tree.insert("", "end", values=result)  # إضافة البيانات إلى الجدول

        connection.close()

    manual_search_var = tk.StringVar()
    manual_search_entry = ttk.Entry(manual_search_window, textvariable=manual_search_var)
    manual_search_entry.pack(pady=10)

    search_type_var = tk.StringVar()
    search_type_var.set("الاسم")
    search_type_combobox = ttk.Combobox(manual_search_window, textvariable=search_type_var,
                                        values=["الاسم", "رقم_الاشتراك", "الهاتف", "رقم_السجل"])
    search_type_combobox.pack(pady=10)

    search_button = ttk.Button(manual_search_window, text="بحث", command=search_manual)
    search_button.pack(pady=10)

    column_names = [
        "تاريخ_التسجيل", "رقم_الاشتراك", "الاسم", "العمر",
        "الهاتف", "مدة_الاشتراك", "حالة_الاشتراك", "ملاحظات", "رقم_السجل",
        "تاريخ_الانتهاء", "الأيام_المتبقية", "المبلغ_المدفوع", "تاريخ_الدفع"
    ]

    result_tree = ttk.Treeview(manual_search_window, columns=column_names, show="headings")

    for column in column_names:
        result_tree.heading(column, text=column)
        result_tree.column(column, width=100)  # قم بتعديل العرض حسب احتياجاتك

    result_tree.pack(pady=20, fill="both", expand=True)

    log_activity("بحث يدوي", "بحث يدوي .")


import webbrowser

# تعريف متغير لتخزين رقم الهاتف المحدد
selected_phone = ""

import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, timedelta


def update_remaining_days():
    try:
        with sqlite3.connect("gym_database.db") as connection:
            connection.execute("BEGIN")
            cursor = connection.cursor()

            current_date = datetime.now().date()
            query = f"SELECT * FROM main WHERE تاريخ_الانتهاء >= '{current_date}'"

            cursor.execute(query)
            subscriptions = cursor.fetchall()

            for subscription in subscriptions:
                end_date = datetime.strptime(subscription[9], "%Y-%m-%d").date()
                remaining_days = (end_date - current_date).days
                if remaining_days < 10:
                    # تحديث الأيام المتبقية في قاعدة البيانات
                    update_query = f"UPDATE main SET الأيام_المتبقية = {remaining_days} WHERE رقم_الاشتراك = {subscription[1]}"
                    cursor.execute(update_query)

            connection.commit()
    except sqlite3.Error as e:
        print("Error updating remaining days:", e)






def show_members_with_remaining_days():
    update_remaining_days()  # تحديث الأيام المتبقية قبل عرض البيانات

    connection = sqlite3.connect("gym_database.db")
    cursor = connection.cursor()

    # استعلام لاستخراج الاشتراكات التي لديها أقل من 10 يومًا متبقية
    query = "SELECT * FROM main WHERE الأيام_المتبقية < 10"

    cursor.execute(query)
    search_results = cursor.fetchall()

    if search_results:
        result_window = tk.Toplevel()
        result_window.title("المشتركين بأقل من 10 يومًا متبقية")

        column_names = [
            "تاريخ_التسجيل", "رقم_الاشتراك", "الاسم", "العمر",
            "الهاتف", "مدة_الاشتراك", "حالة_الاشتراك", "ملاحظات", "رقم_السجل",
            "تاريخ_الانتهاء", "الأيام_المتبقية", "المبلغ_المدفوع", "تاريخ_الدفع"
        ]

        result_tree = ttk.Treeview(result_window, columns=column_names, show="headings", height=10)  # ارتفاع قائمة العناصر

        # تحديد النمط لتغيير حجم النص
        result_tree.tag_configure("myfont", font=("Helvetica", 12))

        for column in column_names:
            result_tree.heading(column, text=column)

        for result in search_results:
            # تطبيق النمط على النص الذي تريد تغيير حجمه
            result_tree.insert("", "end", values=result, tags=("myfont",))

        result_tree.pack(pady=20, fill="both", expand=True)

        # إضافة تمرير رأسي
        yscroll = ttk.Scrollbar(result_window, orient="vertical", command=result_tree.yview)
        yscroll.pack(side="right", fill="y")
        result_tree.configure(yscrollcommand=yscroll.set)

        # إضافة تمرير أفقي
        xscroll = ttk.Scrollbar(result_window, orient="horizontal", command=result_tree.xview)
        xscroll.pack(side="bottom", fill="x")
        result_tree.configure(xscrollcommand=xscroll.set)

        def open_whatsapp():
            global selected_phone
            selected_phone = str(result_tree.item(result_tree.selection())['values'][4]).lstrip('0')
            whatsapp_url = f"https://wa.me/966{selected_phone}"
            webbrowser.open(whatsapp_url)

        # تصغير حجم الزر
        whatsapp_button = ttk.Button(result_window, text="فتح واتساب ومراسلة",
                                     command=open_whatsapp, width=20)
        whatsapp_button.pack(pady=10)
    else:
        messagebox.showinfo("عرض المشتركين", "لا يوجد مشتركين بأقل من 10 أيام متبقية.")

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from datetime import datetime, timedelta

def show_news_ticker(root, time_frame):
    def calculate_remaining_days(subscription_date, duration):
        subscription_date = datetime.strptime(subscription_date, "%Y-%m-%d").date()
        expiration_date = subscription_date + timedelta(days=duration)
        remaining_days = (expiration_date - datetime.now().date()).days
        return remaining_days

    def fetch_expiring_subscribers():
        connection = sqlite3.connect("gym_database.db")
        cursor = connection.cursor()
        query = "SELECT الاسم, تاريخ_التسجيل, رقم_الاشتراك, الأيام_المتبقية, المبلغ_المدفوع FROM main WHERE الأيام_المتبقية <= 5"
        cursor.execute(query)
        expiring_subscribers = cursor.fetchall()

        expiring_subscribers = [(name, subscription_date, subscription_number, calculate_remaining_days(subscription_date, duration), amount_paid)
                                for name, subscription_date, subscription_number, duration, amount_paid in expiring_subscribers]

        return expiring_subscribers

    def update_news():
        nonlocal current_index
        if expiring_subscribers:
            subscriber = expiring_subscribers[current_index]
            name = subscriber[0]
            subscription_date = subscriber[1]
            subscription_number = subscriber[2]
            remaining_days = subscriber[3]
            amount_paid = subscriber[4]
            ticker_text = f"الاسم: {name} | تاريخ الاشتراك: {subscription_date} | رقم الاشتراك: {subscription_number} | الأيام المتبقية: {remaining_days} أيام | المبلغ المدفوع: {amount_paid}"
            ticker_label.config(text=ticker_text)
            current_index = (current_index + 1) % len(expiring_subscribers)
        else:
            ticker_label.config(text="لا يوجد مشتركين بأقل من 5 أيام متبقية.")

        root.after(5000, update_news)

    current_index = 0
    expiring_subscribers = fetch_expiring_subscribers()

    if expiring_subscribers:
        ticker_window = time_frame
        ticker_label = ttk.Label(ticker_window, text="", font=("Helvetica", 12, "bold"), background="#336699", foreground="white")
        ticker_label.pack(fill="x")

        update_news()

    else:
        messagebox.showinfo("عرض الأخبار", "لا يوجد مشتركين بأقل من 5 أيام متبقية.")


    current_index = 0  # تهيئة متغير لتتبع الصف الحالي
    expiring_subscribers = fetch_expiring_subscribers()

    if expiring_subscribers:
        ticker_window = time_frame
        canvas = tk.Canvas(ticker_window, bg="#336699", width=400, height=40)
        canvas.pack()

        news_ticker = canvas.create_text(0, 20, anchor='w', text="", font=("Helvetica", 12, "bold"), fill="white")

        # بدء حركة شريط الأخبار
        root.after(0, update_news)  # بدء تحديث البيانات بمجرد عرض الشريط

        def move_ticker():
            canvas.move(news_ticker, -1, 0)
            root.after(50, move_ticker)

        move_ticker()  # بدء حركة شريط الأخبار

    else:
        messagebox.showinfo("عرض الأخبار", "لا يوجد مشتركين بأقل من 5 أيام متبقية.")


import shutil
import os
import time
from tkinter import messagebox

def backup_data():
    # اسم المجلد الذي ستتم فيه النسخ الاحتياطية
    backup_folder = "backup_" + time.strftime("%Y-%m-%d")

    # إنشاء مجلد النسخ الاحتياطية إذا لم يكن موجودًا
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    try:
        # نسخ ملف البرنامج
        shutil.copy("C:/Users/POWER KING/Desktop/sest/power_gym.py", backup_folder)

        # البحث عن قاعدة البيانات في نفس المجلد ونسخها
        db_path = "C:/Users/POWER KING/Desktop/sest/gym_database.db"
        if os.path.exists(db_path):
            shutil.copy(db_path, backup_folder)
        else:
            messagebox.showerror("خطأ في النسخ الاحتياطي", "لم يتم العثور على قاعدة البيانات.")

        # قم بإعداد رسالة تأكيد
        messagebox.showinfo("نجاح النسخ الاحتياطي", "تم إنشاء نسخة احتياطية بنجاح.")

    except Exception as e:
        # إذا حدث خطأ أثناء النسخ الاحتياطي
        messagebox.showerror("خطأ في النسخ الاحتياطي", f"حدث خطأ: {str(e)}")


    log_activity("نسخة احتياطية ", "نسخه احتياطية  .")

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
import os

def open_subscriptions_page():
    def search_subscriptions_by_period():
        start_date = start_date_cal.get_date()
        end_date = end_date_cal.get_date()

        # الاتصال بقاعدة البيانات SQLite
        conn = sqlite3.connect('gym_database.db')
        cursor = conn.cursor()

        # استعلام لاسترداد البيانات بناءً على تاريخ البداية وتاريخ النهاية
        cursor.execute("SELECT تاريخ_التسجيل, رقم_الاشتراك, الاسم, مدة_الاشتراك, حالة_الاشتراك, تاريخ_الدفع, المبلغ_المدفوع FROM main WHERE تاريخ_التسجيل >= ? AND تاريخ_التسجيل <= ?", (start_date.isoformat(), end_date.isoformat()))

        # استرداد البيانات
        data = cursor.fetchall()

        # إزالة البيانات الحالية من القائمة (إذا كانت موجودة)
        for item in tree.get_children():
            tree.delete(item)

        # إضافة البيانات المستردة من البحث إلى القائمة
        for row in data:
            tree.insert("", "end", values=row)

        # مجموع الاشتراكات
        total_subscriptions_label.config(text=f"عدد الاشتراكات: {len(data)}")

        # مجموع المبالغ المدفوعة
        total_payment = sum(row[6] for row in data)
        total_payment_label.config(text=f"إجمالي المبلغ المدفووع: {total_payment} ريال")

    # إنشاء نافذة جديدة لعرض الاشتراكات
    subscriptions_window = tk.Toplevel()
    subscriptions_window.title("قائمة الاشتراكات")
    subscriptions_window.geometry("1000x600")  # تكبير حجم النافذة

    # إضافة Calendar لتحديد تاريخ البداية
    start_date_label = tk.Label(subscriptions_window, text="تاريخ بداية الفترة:")
    start_date_label.pack()

    start_date_cal = DateEntry(subscriptions_window, date_pattern='dd/mm/yyyy', width=20)
    start_date_cal.pack()

    # إضافة Calendar لتحديد تاريخ النهاية
    end_date_label = tk.Label(subscriptions_window, text="تاريخ نهاية الفترة:")
    end_date_label.pack()

    end_date_cal = DateEntry(subscriptions_window, date_pattern='dd/mm/yyyy', width=20)
    end_date_cal.pack()

    # إضافة زر لتنفيذ عملية البحث
    search_button = tk.Button(subscriptions_window, text="بدء البحث", command=search_subscriptions_by_period)
    search_button.pack()

    # إنشاء قائمة (TreeView) لعرض البيانات في نافذة الاشتراكات
    tree = ttk.Treeview(subscriptions_window, columns=("تاريخ_التسجيل", "رقم_الاشتراك", "الاسم", "مدة_الاشتراك", "حالة_الاشتراك", "تاريخ_الدفع", "المبلغ_المدفوع"))

    # تحديد اسماء الأعمدة في القائمة
    tree.heading("#1", text="تاريخ_التسجيل")
    tree.heading("#2", text="رقم_الاشتراك")
    tree.heading("#3", text="الاسم")
    tree.heading("#4", text="مدة_الاشتراك")
    tree.heading("#5", text="حالة_الاشتراك")
    tree.heading("#6", text="تاريخ_الدفع")
    tree.heading("#7", text="المبلغ_المدفوع")

    # تحديد عرض الأعمدة
    tree.column("#1", width=100)
    tree.column("#2", width=100)
    tree.column("#3", width=150)
    tree.column("#4", width=100)
    tree.column("#5", width=100)
    tree.column("#6", width=100)
    tree.column("#7", width=100)

    # عرض القائمة في منتصف الصفحة
    tree.pack(expand=True, fill='both')

    # مجموع الاشتراكات
    total_subscriptions_label = tk.Label(subscriptions_window, text="عدد الاشتراكات: 0")
    total_subscriptions_label.pack()

    # مجموع المبالغ المدفوعة
    total_payment_label = tk.Label(subscriptions_window, text="إجمالي المبلغ المدفووع: 0 ريال")
    total_payment_label.pack()

    log_activity("الاشتراكات", "االاشتراكات .")



import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import time
log_text = None  # تعريف log_text في النطاق الرئيسي

log_file_path = "activity_log.txt"
log_text = None  # قم بتعريف log_text كمتغير عالمي

def log_activity(username, action, description=""):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S] ")
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{timestamp}{username}: {action}: {description}\n")

    # تحديث واجهة النصوص في نافذة السجل
    update_activity_log_text()


def show_activity_log_window():
    global log_text
    log_window = tk.Toplevel(root)
    log_window.title("سجل النشاط")
    log_window.geometry("800x600")  # زيادة حجم النافذة للتمرير

    log_text = tk.Text(log_window, wrap=tk.WORD, state=tk.DISABLED)
    log_text.pack(fill="both", expand=True)

    # إضافة مربعي نص للتمرير لأعلى ولأسفل
    scrollbar_y = ttk.Scrollbar(log_window, command=log_text.yview)
    scrollbar_y.pack(side="right", fill="y")

    log_text["yscrollcommand"] = scrollbar_y.set

    # إضافة مربعي نص للتمرير لليسار واليمين
    scrollbar_x = ttk.Scrollbar(log_window, command=log_text.xview, orient="horizontal")
    scrollbar_x.pack(side="bottom", fill="x")

    log_text["xscrollcommand"] = scrollbar_x.set

    # قم بتحديث واجهة النصوص في نافذة السجل عند فتحها
    update_activity_log_text()

    def on_activity_log_closing():
        log_window.destroy()

    log_window.protocol("WM_DELETE_WINDOW", on_activity_log_closing)

def update_activity_log_text():
    global log_text
    if log_text is not None:
        with open(log_file_path, "r") as log_file:
            log_content = log_file.read()
            log_text.config(state=tk.NORMAL)
            log_text.delete(1.0, tk.END)  # حذف النص الحالي
            log_text.insert(tk.END, log_content)
            log_text.config(state=tk.DISABLED)
            # حرك المؤشر لأسفل بعد تحديث النصوص
            log_text.yview_moveto(1.0)












import tkinter as tk
from tkinter import ttk, filedialog
import sqlite3
from datetime import datetime
import shutil
from PIL import Image, ImageTk

# اتصل بقاعدة البيانات
conn = sqlite3.connect('gym_database.db')
cursor = conn.cursor()

# قم بتنفيذ استعلام إنشاء الجدول
cursor.execute('''
    CREATE TABLE IF NOT EXISTS measurements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        الاسم TEXT,
        رقم_الاشتراك INTEGER,
        تاريخ_القياس TEXT,
        الوقت TEXT,
        مسار_الصورة TEXT
    );
''')

# ارتبط التغييرات
conn.commit()

# أغلق الاتصال
conn.close()

# تحديد tree كمتغير على مستوى النموذج
tree = None


def open_add_measurement_window(member_subscription_number=None):
    add_measurement_window = tk.Toplevel()
    add_measurement_window.title("إضافة قياس")
    add_measurement_window.geometry("800x600")

    # تخزين رقم الاشتراك لاستخدامه في إضافة القياس
    if member_subscription_number is not None:
        member_subscription_var = tk.StringVar(value=str(member_subscription_number))
    else:
        member_subscription_var = tk.StringVar()

    # خانة الاسم
    name_label = ttk.Label(add_measurement_window, text="الاسم:")
    name_label.grid(row=0, column=0, padx=10, pady=10)

    name_entry = ttk.Entry(add_measurement_window)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    # خانة رقم الاشتراك
    subscription_label = ttk.Label(add_measurement_window, text="رقم الاشتراك:")
    subscription_label.grid(row=1, column=0, padx=10, pady=10)

    subscription_entry = ttk.Entry(add_measurement_window)
    subscription_entry.grid(row=1, column=1, padx=10, pady=10)

    # تاريخ القياس (تلقائياً)
    date_label = ttk.Label(add_measurement_window, text="تاريخ القياس:")
    date_label.grid(row=2, column=0, padx=10, pady=10)

    date_entry = ttk.Entry(add_measurement_window)
    date_entry.grid(row=2, column=1, padx=10, pady=10)

    # تعيين قيمة تاريخ اليوم تلقائياً
    today_date = datetime.today().strftime('%Y-%m-%d')
    date_entry.insert(0, today_date)

    # الوقت (تلقائياً)
    time_label = ttk.Label(add_measurement_window, text="الوقت:")
    time_label.grid(row=3, column=0, padx=10, pady=10)

    time_entry = ttk.Entry(add_measurement_window)
    time_entry.grid(row=3, column=1, padx=10, pady=10)

    # تعيين قيمة الوقت الحالي تلقائياً
    current_time = datetime.now().strftime('%H:%M:%S')
    time_entry.insert(0, current_time)

    # صورة القياس
    image_path_label = ttk.Label(add_measurement_window, text="صورة القياس:")
    image_path_label.grid(row=4, column=0, padx=10, pady=10)

    image_path_entry = ttk.Entry(add_measurement_window, state="readonly")
    image_path_entry.grid(row=4, column=1, padx=10, pady=10)

    browse_button = ttk.Button(add_measurement_window, text="اختيار صورة", command=lambda: browse_image(image_path_entry))
    browse_button.grid(row=4, column=2, padx=10, pady=10)

    # حفظ القياس
    save_button = ttk.Button(add_measurement_window, text="حفظ القياس", command=lambda: save_measurement(
        name_entry.get(), subscription_entry.get(), date_entry.get(), time_entry.get(), image_path_entry.get()
    ))
    save_button.grid(row=5, column=1, pady=10)

    # زر البحث
    search_button = ttk.Button(add_measurement_window, text="البحث", command=open_measurement_search_window)
    search_button.grid(row=5, column=2, padx=10, pady=10)


def browse_image(entry_widget):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    entry_widget.configure(state="normal")
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)
    entry_widget.configure(state="readonly")


def save_measurement(name, subscription_number, date, time, image_path):
    conn = sqlite3.connect('gym_database.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO measurements (الاسم, رقم_الاشتراك, تاريخ_القياس, الوقت, مسار_الصورة)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, subscription_number, date, time, image_path))
        conn.commit()

        if image_path:
            destination_folder = "images_folder"
            shutil.copy(image_path, destination_folder)

    finally:
        conn.close()


def open_measurement_search_window():
    global tree  # قم بتعيين tree كمتغير على مستوى النموذج
    measurement_search_window = tk.Toplevel()
    measurement_search_window.title("البحث عن بيانات القياس")
    measurement_search_window.geometry("600x400")

    search_label = ttk.Label(measurement_search_window, text="رقم الاشتراك:")
    search_label.grid(row=0, column=0, padx=10, pady=10)

    search_entry = ttk.Entry(measurement_search_window)
    search_entry.grid(row=0, column=1, padx=10, pady=10)

    search_button = ttk.Button(measurement_search_window, text="بحث", command=lambda: search_measurement_data(search_entry.get()))
    search_button.grid(row=0, column=2, padx=10, pady=10)

    # تحديد tree في نطاق واجهة المستخدم
    columns = ("تاريخ القياس", "الوقت", "صورة القياس")  # تغيير اسم العمود
    tree = ttk.Treeview(measurement_search_window, columns=columns, show="headings")

    # تحديد عناوين الأعمدة
    for col in columns:
        tree.heading(col, text=col)

    tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)


def search_measurement_data(subscription_number):
    global tree  # قم بتعيين tree كمتغير على مستوى النموذج
    # قم بتنفيذ استعلام لاسترجاع بيانات القياس بناءً على رقم الاشتراك
    conn = sqlite3.connect('gym_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT تاريخ_القياس, الوقت, مسار_الصورة
        FROM measurements
        WHERE رقم_الاشتراك = ?
    ''', (subscription_number,))

    measurement_data = cursor.fetchall()

    conn.close()

    # عرض بيانات القياس في Treeview
    for index, row in enumerate(measurement_data, start=1):
        tree.insert("", "end", values=row)
        display_image_column(row[2], index)  # اعرض الصورة في العمود المخصص


def display_image_column(image_path, index):
    # عرض الصورة في العمود المخصص
    with Image(filename=image_path) as img:
        img.resize(width=50, height=50)
        img.save(filename="resized_image.png")

        image = ImageTk.PhotoImage(file="resized_image.png")
        tree.column("صورة القياس", width=100)  # تحديد عرض العمود
        tree.heading("صورة القياس", text="صورة القياس")  # تحديد عنوان العمود
        tree.set(tree.get_children()[index - 1], "صورة القياس", image)







def logout(root):
    # إضافة أي شيء إضافي تحتاجه لعملية تسجيل الخروج هنا
    # على سبيل المثال، يمكنك إغلاق النافذة الرئيسية وفتح نافذة تسجيل الدخول من جديد
    root.destroy()  # إغلاق النافذة الحالية
    open_login_page()  # قم بتعريف دالة open_login_window() لفتح نافذة تسجيل الدخول من جديد









import sqlite3

# Initialize SQLite database connection
conn = sqlite3.connect('gym_database.db')
cursor = conn.cursor()

# Check if the users table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
table_exists = cursor.fetchone()

# If the users table does not exist, create it
if not table_exists:
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    conn.commit()
    print("Table 'users' created.")
else:
    # Check if the 'role' column exists, and add it if not
    cursor.execute("PRAGMA table_info(users);")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]

    if 'role' not in column_names:
        cursor.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT '';")
        conn.commit()
        print("Column 'role' added to table 'users'.")
    else:
        print("Table 'users' already exists, and 'role' column is present.")


def authenticate_user(username, password):
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    result = conn.execute(query, (username, password)).fetchone()
    return result

def login_clicked(username_entry, password_entry, login_window):
    entered_username = username_entry.get()
    entered_password = password_entry.get()

    result = authenticate_user(entered_username, entered_password)

    print("Result from authenticate_user:", result)

    if result:
        role = result[3]
        log_activity(entered_username, "تسجيل الدخول", f"تم تسجيل الدخول بدور {role}")
        open_main_page(login_window, role)
    else:
        messagebox.showerror("خطأ", "فشل تسجيل الدخول. الرجاء التحقق من اسم المستخدم وكلمة المرور.")


class ScrollableFrame(tk.Frame):
    def __init__(self, container, width, height, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Variables to track dragging
        self.dragging = False
        self.start_x = 0
        self.start_y = 0

        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.canvas.bind("<B1-Motion>", self.on_drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_drag_release)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def on_drag_start(self, event):
        self.dragging = True
        self.start_x = event.x
        self.start_y = event.y

    def on_drag_motion(self, event):
        if self.dragging:
            delta_x = event.x - self.start_x
            delta_y = event.y - self.start_y
            self.canvas.move(self.scrollable_frame, delta_x, delta_y)
            self.start_x = event.x
            self.start_y = event.y

    def on_drag_release(self, event):
        self.dragging = False

def open_main_page(login_window, role):
    login_window.destroy()  # إغلاق نافذة تسجيل الدخول

    root = tk.Tk()
    root.title("تطبيق إدارة المشتركين مركز ملك القوة الرياضي")
    root.geometry("1920x1080")

    canvas = tk.Canvas(root, width=1920, height=1080)
    canvas.pack()

    image = Image.open("C:/Users/POWER KING/Desktop/sest/background.png")
    image = image.resize((1920, 1080), Image.ANTIALIAS if "ANTIALIAS" in Image.__dict__ else Image.BICUBIC)

    background_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=background_image, anchor=tk.NW)

    style = ttk.Style()
    style.theme_use('clam')

    style.configure("TButton",
                    foreground="black",
                    background="#2E8BC0",
                    padding=(10, 5),
                    font=("Helvetica", 16, "bold"))

    style.configure("Colored.TButton",
                    foreground="black",
                    background="#1E90FF",
                    padding=(10, 5),
                    font=("Helvetica", 16, "bold"))

    def update_time():
        current_time = time.strftime("%I:%M:%S %p")
        current_date = time.strftime("%d/%m/%Y")
        time_label.config(text=current_time)
        date_label.config(text=current_date)
        root.after(1000, update_time)

    def search():
        query = search_entry.get()
        for button in button_frame.scrollable_frame.winfo_children():
            if query.lower() in button.cget("text").lower():
                button.configure(style="Colored.TButton")
            else:
                button.configure(style="TButton")

    search_entry = ttk.Entry(root, font=("Helvetica", 16))
    search_entry.place(x=1030, y=10, width=230)
    search_entry.bind("<KeyRelease>", lambda event: search())

    button_frame = ScrollableFrame(root, width=230, height=900)
    button_frame.place(x=1030, y=50)

    time_frame = ttk.Frame(root, width=200, height=30)
    time_frame.place(x=100, y=20)

    time_label = ttk.Label(time_frame, text="", font=("Helvetica", 36, "bold"))
    time_label.pack(side="left", padx=5)

    date_frame = ttk.Frame(root, width=200, height=50)
    date_frame.place(x=100, y=100)

    date_label = ttk.Label(date_frame, text="", font=("Helvetica", 42, "bold"))
    date_label.pack(side="left", padx=5)



    # Adding buttons
    if role == "admin":
        buttons_info = [
            ("إدراج مشترك جديد", add_member),
            ("تجديد الاشتراك", lambda: open_renew_subscription_window(root)),
            ("ترقية الاشتراك", lambda: open_upgrade_subscription_window(root)),
            ("البحث والتعديل", open_search_window),
            ("إيقاف الاشتراك", stop_subscription_window),
            ("سلة المحذوفات", open_deleted_subscribers_window),
            ("القياسات", lambda: open_add_measurement_window(123)),
            ("صفحة الإيرادات", open_income_window),
            ("صفحة المصروفات", open_expense_window),
            ("إنشاء تقرير", open_report_window),
            ("بحث  qrcode", open_qr_search),
            ("بحث يدوي", open_manual_search),
            ("اشتراكات اوشك على الانتهاء", show_members_with_remaining_days),
            ("عرض الأخبار", lambda: show_news_ticker(root, time_frame)),  # إضافة زر لعرض الشريط الإخباري
            ("إجراء نسخة احتياطية", backup_data),
            ("الاشتراكات", open_subscriptions_page),
            ("إنشاء قائمة سعر", open_add_price_window),
            ("عرض قوائم الأسعار", update_price_list),
            ("الديون", display_debt_subscribers),
            ("سجل النشاط", show_activity_log_window),
            ("إعدادات", open_settings),
            ("صلاحيات المستخدمين", open_user_permissions_window),
            ("تسجيل الخروج", lambda: logout(root)),
        ]
    elif role == "employee":
        buttons_info = [
            ("إدراج مشترك جديد", add_member),
            ("تجديد الاشتراك", lambda: open_renew_subscription_window(root)),
            ("إيقاف الاشتراك", stop_subscription_window),
            ("صفحة الإيرادات", open_income_window),
            ("صفحة المصروفات", open_expense_window),
            ("بحث  qrcode", open_qr_search),
            ("بحث يدوي", open_manual_search),
            ("اشتراكات اوشك على الانتهاء", show_members_with_remaining_days),
            ("إجراء نسخة احتياطية", backup_data),
            ("الديون", display_debt_subscribers),
            ("تسجيل الخروج", lambda: logout(root)),
        ]
    elif role == "متابعه":
        buttons_info = [
            ("بحث  qrcode", open_qr_search),
            ("بحث يدوي", open_manual_search),
            ("تسجيل الخروج", lambda: logout(root)),
        ]
    else:
        buttons_info = [
            ("الديون", display_debt_subscribers),
            ("سجل النشاط", show_activity_log_window),
            ("تسجيل الخروج", lambda: logout(root)),
        ]

    # Organizing buttons
    last_category = None
    for button_text, command in buttons_info:
        if button_text.startswith('=='):
            label = ttk.Label(button_frame.scrollable_frame, text=button_text.strip('= '), font=("Helvetica", 12, "bold"))
            label.pack(fill="x", pady=5)
            last_category = label
        else:
            if last_category:
                ttk.Separator(button_frame.scrollable_frame, orient='horizontal').pack(fill="x", pady=5)
            button = ttk.Button(button_frame.scrollable_frame, text=button_text, command=command, style="TButton")
            button.pack(fill="x", pady=5)

    update_time()  # Start updating time
    root.mainloop()

def open_user_permissions_window():
    user_permissions_window = tk.Toplevel()
    user_permissions_window.title("صلاحيات المستخدمين")
    user_permissions_window.geometry("600x400")

    users_combobox_label = ttk.Label(user_permissions_window, text="اختر مستخدم:")
    users_combobox_label.grid(row=0, column=0, padx=10, pady=10, sticky="E")

    users = [user[0] for user in conn.execute("SELECT username FROM users").fetchall()]
    users_combobox = ttk.Combobox(user_permissions_window, values=users)
    users_combobox.grid(row=0, column=1, padx=10, pady=10)

    permissions_label = ttk.Label(user_permissions_window, text="صلاحيات المستخدم:")
    permissions_label.grid(row=1, column=0, padx=10, pady=10, sticky="E")

    permissions_var = tk.StringVar()
    permissions_combobox = ttk.Combobox(user_permissions_window, textvariable=permissions_var, values=["admin", "employee"])
    permissions_combobox.grid(row=1, column=1, padx=10, pady=10)

    save_permissions_button = ttk.Button(user_permissions_window, text="حفظ الصلاحيات", command=lambda: save_permissions(users_combobox.get(), permissions_var.get()))
    save_permissions_button.grid(row=2, column=0, columnspan=2, pady=20)

    cancel_button = ttk.Button(user_permissions_window, text="إلغاء", command=user_permissions_window.destroy)
    cancel_button.grid(row=3, column=0, columnspan=2, pady=20)

def save_permissions(username, role):
    if not username:
        messagebox.showwarning("تحذير", "الرجاء اختيار مستخدم.")
        return

    query = "UPDATE users SET role = ? WHERE username = ?"
    conn.execute(query, (role, username))
    conn.commit()

    messagebox.showinfo("نجاح", f"تم حفظ صلاحيات المستخدم {username} بنجاح.")

def add_user(new_username_entry, new_password_entry, new_role_combobox, new_user_window):
    new_username = new_username_entry.get()
    new_password = new_password_entry.get()
    new_role = new_role_combobox.get()

    if not new_username or not new_password:
        messagebox.showwarning("تحذير", "الرجاء إدخال اسم المستخدم وكلمة المرور.")
        return

    query = "INSERT INTO users (username, password, role) VALUES (?, ?, ?)"
    conn.execute(query, (new_username, new_password, new_role))
    conn.commit()

    messagebox.showinfo("نجاح", "تمت إضافة المستخدم بنجاح.")
    new_user_window.destroy()

def delete_user(users_combobox, delete_user_window):
    selected_user = users_combobox.get()

    if not selected_user:
        messagebox.showwarning("تحذير", "الرجاء اختيار مستخدم للحذف.")
        return

    query = "DELETE FROM users WHERE username = ?"
    conn.execute(query, (selected_user,))
    conn.commit()

    messagebox.showinfo("نجاح", f"تم حذف المستخدم {selected_user} بنجاح.")
    delete_user_window.destroy()

def open_settings():
    settings_window = tk.Toplevel()
    settings_window.title("إعدادات")
    settings_window.geometry("400x300")

    # إضافة حقول اسم المستخدم وكلمة المرور
    username_label = ttk.Label(settings_window, text="اسم المستخدم:")
    username_label.grid(row=0, column=0, padx=10, pady=10, sticky="E")

    username_entry = ttk.Entry(settings_window)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    password_label = ttk.Label(settings_window, text="كلمة المرور:")
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky="E")

    password_entry = ttk.Entry(settings_window, show="*")  # يخفي النص
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    # إضافة زر إضافة مستخدم جديد
    add_user_button = ttk.Button(settings_window, text="إضافة مستخدم جديد", command=lambda: add_user_clicked(settings_window))
    add_user_button.grid(row=3, column=0, columnspan=2, pady=20)

    # إضافة زر حذف مستخدم
    delete_user_button = ttk.Button(settings_window, text="حذف مستخدم", command=lambda: delete_user_clicked(settings_window))
    delete_user_button.grid(row=4, column=0, columnspan=2, pady=20)

def add_user_clicked(settings_window):
    new_user_window = tk.Toplevel(settings_window)
    new_user_window.title("إضافة مستخدم جديد")
    new_user_window.geometry("300x300")

    new_username_label = ttk.Label(new_user_window, text="اسم المستخدم:")
    new_username_label.grid(row=0, column=0, padx=10, pady=10, sticky="E")

    new_username_entry = ttk.Entry(new_user_window)
    new_username_entry.grid(row=0, column=1, padx=10, pady=10)

    new_password_label = ttk.Label(new_user_window, text="كلمة المرور:")
    new_password_label.grid(row=1, column=0, padx=10, pady=10, sticky="E")

    new_password_entry = ttk.Entry(new_user_window, show="*")  # يخفي النص
    new_password_entry.grid(row=1, column=1, padx=10, pady=10)

    new_role_label = ttk.Label(new_user_window, text="دور المستخدم:")
    new_role_label.grid(row=2, column=0, padx=10, pady=10, sticky="E")

    roles = ["admin", "employee", "متابعه"]
    new_role_combobox = ttk.Combobox(new_user_window, values=roles)
    new_role_combobox.grid(row=2, column=1, padx=10, pady=10)

    add_user_button = ttk.Button(new_user_window, text="إضافة مستخدم", command=lambda: add_user(new_username_entry, new_password_entry, new_role_combobox, new_user_window))
    add_user_button.grid(row=3, columnspan=2, pady=20)

def delete_user_clicked(settings_window):
    delete_user_window = tk.Toplevel(settings_window)
    delete_user_window.title("حذف مستخدم")
    delete_user_window.geometry("300x300")

    users_combobox_label = ttk.Label(delete_user_window, text="اختر مستخدم:")
    users_combobox_label.grid(row=0, column=0, padx=10, pady=10, sticky="E")

    users = [user[0] for user in conn.execute("SELECT username FROM users").fetchall()]
    users_combobox = ttk.Combobox(delete_user_window, values=users)
    users_combobox.grid(row=0, column=1, padx=10, pady=10)

    delete_user_button = ttk.Button(delete_user_window, text="حذف مستخدم", command=lambda: delete_user(users_combobox, delete_user_window))
    delete_user_button.grid(row=1, columnspan=2, pady=20)



def open_login_page():
    login_window = tk.Tk()
    login_window.title("تسجيل الدخول")
    login_window.geometry("700x400")

    image_path = "C:/Users/POWER KING/Desktop/sest/logo1.png"
    image = Image.open(image_path)
    image = image.resize((400, 400), Image.ANTIALIAS if "ANTIALIAS" in Image.__dict__ else Image.BICUBIC)

    if image.mode == 'RGB':
        image.putalpha(255)

    background_image = ImageTk.PhotoImage(image)
    background_label = tk.Label(login_window, image=background_image)
    background_label.image = background_image
    background_label.grid(row=0, column=0, rowspan=4, sticky="nsew")

    style = ttk.Style()
    style.theme_use('clam')

    style.configure('TEntry', font=('Helvetica', 14), padding=5, relief="solid")
    style.configure('TButton', font=('Helvetica', 14), padding=10, relief="raised", foreground="black", background="#2E8BC0")

    entry_frame = ttk.Frame(login_window, padding=10)
    entry_frame.grid(row=1, column=1, rowspan=2, columnspan=2, padx=10, pady=10, sticky="nsew")

    username_label = ttk.Label(entry_frame, text="اسم المستخدم:")
    username_label.grid(row=0, column=0, padx=10, pady=10, sticky="E")

    username_entry = ttk.Entry(entry_frame, style='TEntry')
    username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="W")

    password_label = ttk.Label(entry_frame, text="كلمة المرور:")
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky="E")

    password_entry = ttk.Entry(entry_frame, show="*", style='TEntry')
    password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="W")

    login_button = ttk.Button(login_window, text="تسجيل الدخول", command=lambda: login_clicked(username_entry, password_entry, login_window), style='TButton')
    login_button.grid(row=3, column=1, columnspan=2, pady=20)

    login_window.grid_rowconfigure(0, weight=1)
    login_window.grid_rowconfigure(1, weight=1)
    login_window.grid_rowconfigure(2, weight=1)
    login_window.grid_rowconfigure(3, weight=1)
    login_window.grid_columnconfigure(0, weight=1)
    login_window.grid_columnconfigure(1, weight=1)
    login_window.grid_columnconfigure(2, weight=1)

    login_window.mainloop()

# Run the program
open_login_page()
















