import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. CHUẨN BỊ DỮ LIỆU 10 SINH VIÊN ---
data = {
'Họ tên': ['An', 'Bình', 'Chi', 'Dũng', 'Hà', 'Lan', 'Minh', 'Nam', 'Phúc', 'Trang'],
'Chuyên cần': [9.0, 8.5, 7.0, 9.5, 8.0, 6.0, 9.0, 7.5, 8.0, 9.5],
'Giữa kỳ': [7.0, 8.0, 6.0, 8.5, 7.0, 5.0, 8.0, 6.5, 7.0, 9.0],
'Cuối kỳ': [7.5, 7.5, 6.5, 9.0, 6.5, 5.5, 8.5, 7.0, 7.5, 9.0]
}

df = pd.DataFrame(data)

# Tính Điểm tổng kết (Ví dụ: Chuyên cần * 10% + Giữa kỳ * 30% + Cuối kỳ * 60%)
df['Tổng kết'] = round(df['Chuyên cần']*0.1 + df['Giữa kỳ']*0.3 + df['Cuối kỳ']*0.6, 2)

# Hàm xếp loại
def xep_loai(diem):
      if diem >= 8.5: return 'Giỏi'
      elif diem >= 7.0: return 'Khá'
      elif diem >= 5.0: return 'Trung bình'
      else: return 'Yếu'

df['Xếp loại'] = df['Tổng kết'].apply(xep_loai)


# --- 2. GIAO DIỆN STREAMLIT ---

# Hiển thị tiêu đề
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# Hiển thị bảng điểm 10 sinh viên
st.subheader("1. Bảng điểm chi tiết của sinh viên")
st.dataframe(df, use_container_width=True)

# Thống kê thông tin chung
st.subheader("2. Thống kê chung")
col1, col2, col3 = st.columns(3)

with col1:
diem_tb_lop = round(df['Tổng kết'].mean(), 2)
st.metric(label="Điểm trung bình của lớp", value=diem_tb_lop)

with col2:
so_sv_dat = len(df[df['Tổng kết'] >= 5.0])
st.metric(label="Số sinh viên đạt (>= 5.0)", value=so_sv_dat)

with col3:
st.metric(label="Tổng số sinh viên", value=len(df))

# Sinh viên cao nhất và thấp nhất
sv_cao_nhat = df.loc[df['Tổng kết'].idxmax()]
sv_thap_nhat = df.loc[df['Tổng kết'].idxmin()]

st.info(f"🏆 **Sinh viên có điểm tổng kết cao nhất:** {sv_cao_nhat['Họ tên']} ({sv_cao_nhat['Tổng kết']} điểm)")
st.warning(f"⚠️ **Sinh viên có điểm tổng kết thấp nhất:** {sv_thap_nhat['Họ tên']} ({sv_thap_nhat['Tổng kết']} điểm)")


# --- 3. XỔ XUỐNG CHỌN SINH VIÊN ---
st.subheader("3. Tra cứu thông tin từng sinh viên")
ten_chon = st.selectbox("Chọn tên sinh viên để xem chi tiết:", df['Họ tên'].tolist())

# Lọc dữ liệu sinh viên được chọn
sv_info = df[df['Họ tên'] == ten_chon].iloc[0]

st.write(f"Chi tiết điểm của **{ten_chon}**:")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Chuyên cần", sv_info['Chuyên cần'])
c2.metric("Giữa kỳ", sv_info['Giữa kỳ'])
c3.metric("Cuối kỳ", sv_info['Cuối kỳ'])
c4.metric("Tổng kết", sv_info['Tổng kết'])
c5.metric("Xếp loại", sv_info['Xếp loại'])


# --- 4. BIỂU ĐỒ CỘT NGANG ĐIỂM TỔNG KẾT ---
st.subheader("4. Biểu đồ điểm tổng kết của 10 sinh viên")

fig, ax = plt.subplots(figsize=(8, 5))
# Sắp xếp lại để hiển thị đẹp trên biểu đồ ngang
df_sorted = df.sort_values(by='Tổng kết', ascending=True)

bars = ax.barh(df_sorted['Họ tên'], df_sorted['Tổng kết'], color='#2171C1', height=0.6)
ax.set_xlim(0, 10)
ax.set_xlabel("Điểm tổng kết")
ax.set_ylabel("Sinh viên")

# Xóa bớt khung thừa
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='y', which='both', length=0)

st.pyplot(fig)


# --- 5. THÔNG TIN NGƯỜI TẠO Ở CUỐI TRANG ---
st.markdown("---")
st.markdown(
"<p style='text-align: center; color: gray; font-size: 12px;'>"
"Ứng dụng được tạo bởi: Nguyễn Văn A — MSSV: 12345678"
"</p>",
unsafe_allow_html=True

