import streamlit as st
import pyodbc

# وظيفة الاتصال بقاعدة البيانات
def get_conn():
   
    conn_str = (
        'DRIVER={SQL Server};'
        'SERVER=(local);'  SQL Management Studio
        'DATABASE=SchoolManagementDB;'
        'Trusted_Connection=yes;'
    )
    return pyodbc.connect(conn_str)

# إعدادات واجهة الموقع
st.set_page_config(page_title="نظام إدارة المدرسة", layout="wide")

st.title("🏫 لوحة تحكم إدارة المدرسة")

# القائمة الجانبية
menu = ["الرئيسية", "إضافة طالب جديد", "سجل المدفوعات", "التقارير"]
choice = st.sidebar.selectbox("القائمة", menu)

if choice == "الرئيسية":
    st.write("مرحباً بك في نظام إدارة المدرسة الأهلية. استخدم القائمة الجانبية للتنقل.")

elif choice == "إضافة طالب جديد":
    st.subheader("📝 تسجيل طالب جديد")
    with st.form("student_form"):
        name = st.text_input("اسم الطالب الرباعي")
        dob = st.date_input("تاريخ الميلاد")
        class_id = st.number_input("رقم الصف (ID)", min_value=1)
        fees = st.number_input("إجمالي الأقساط", min_value=0)
        phone = st.text_input("رقم هاتف ولي الأمر")
        
        submit = st.form_submit_button("حفظ الطالب")
        
        if submit:
            try:
                conn = get_conn()
                cursor = conn.cursor()
                cursor.execute("{CALL sp_AddStudent (?, ?, ?, ?, ?)}", (name, dob, class_id, fees, phone))
                conn.commit()
                st.success(f"تم تسجيل الطالب {name} بنجاح!")
            except Exception as e:
                st.error(f"خطأ في الاتصال بقاعدة البيانات: {e}")

elif choice == "التقارير":
    st.subheader("📊 كشف حساب الطالب")
    student_id = st.number_input("أدخل رقم الطالب", min_value=1)
    if st.button("عرض"):
        try:
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("{CALL sp_GetStudentBalance (?)}", (student_id))
            row = cursor.fetchone()
            if row:
                st.write(f"**الاسم:** {row[0]}")
                st.write(f"**المتبقي ماليًا:** {row[4]}")
            else:
                st.warning("الطالب غير موجود.")
        except Exception as e:
            st.error(f"حدث خطأ: {e}")


