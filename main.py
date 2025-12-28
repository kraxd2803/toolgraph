import streamlit as st
import numpy as np
import plotly.graph_objects as go

#1title
st.set_page_config(page_title="📊TOOL VẼ ĐỒ THỊ", layout="wide")
st.caption("made by DangKhoa🔰 - beta version")
st.title("Công cụ vẽ đồ thị tương tác")

hd = "huongdan.png"

if st.toggle("📄 Hiển thị Hướng dẫn sử dụng"):
    try:
        st.image(hd, caption="bật bảng setting ở đây",width="stretch")
    except FileNotFoundError:
        st.warning(f"⚠️ KHÔNG TÌM THẤY ẢNH: Vui lòng đảm bảo file ảnh '{hd}' đã được đặt cùng thư mục với main.py")

#2inp
st.sidebar.header("Setting")
loai_ham = st.sidebar.selectbox(
    "Chọn loại hàm số:",
    ("Hàm bậc nhất (y = ax + b)", "Hàm Parabol cơ bản (y = ax²)", "Hàm bậc hai đầy đủ (y = ax² + bx + c)")
)

#3setting
st.sidebar.subheader("Điều chỉnh tham số")
a = st.sidebar.slider("Hệ số a", -10.0, 10.0, 1.0, 0.1)
b = st.sidebar.slider("Hệ số b", -10.0, 10.0, 0.0, 0.1)

#4cal
if loai_ham == "Hàm Parabol cơ bản (y = ax²)":
    congthuc = f"y = {a}x^2"
    x = np.linspace(-10, 10, 1000)
    y = a * x**2
    # Tọa độ đỉnh
    dinh_x, dinh_y = 0.0, 0.0
    
elif "Hàm bậc hai đầy đủ" in loai_ham:
    c=st.sidebar.slider("Hệ số c", -10.0,10.0,0.0,0.1)
    congthuc = f"y = {a}x^2 + {b}x + {c}"
    x = np.linspace(-10,10,1000)
    y = a*x**2 + b*x + c
    if a != 0:
        dinh_x = -b / (2 * a)
        dinh_y = a * dinh_x**2 + b * dinh_x + c
    else:
        dinh_x, dinh_y = None, None 

else:
    congthuc = f"y = {a}x + {b}"
    x= np.linspace(-10,10,100)
    y=a*x +b


st.sidebar.subheader("Đạo hàm & Tiếp tuyến")
x0 = st.sidebar.slider("Chọn điểm x₀", -10.0, 10.0, 2.0, 0.1)

if loai_ham == "Hàm bậc nhất (y = ax + b)":
    dao_ham = a              # Đạo hàm của ax + b luôn là a
    y0 = a * x0 + b          # Tọa độ y tại điểm x0

elif loai_ham == "Hàm Parabol cơ bản (y = ax²)":
    dao_ham = 2 * a * x0     # Công thức đạo hàm: y' = 2ax
    y0 = a * x0**2

else:
    dao_ham = 2 * a * x0 + b # Công thức đạo hàm: y' = 2ax + b
    y0 = a * x0**2 + b * x0 + c

    

#5 hien thi & tao do thi
st.latex(congthuc)
fig = go.Figure()

#ve ham chinh
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Đồ thị', line=dict(color='#00FFCC', width=3)))

#vẽ điểm tiếp xúc (x0, y0)
fig.add_trace(go.Scatter(x=[x0], y=[y0], mode='markers', 
                         marker=dict(color='yellow', size=10), 
                         name=f'Điểm đang xét (x₀={x0})'))

#vẽ đường tiếp tuyến
x_tangent = np.linspace(x0 - 2, x0 + 2, 10)
y_tangent = dao_ham * (x_tangent - x0) + y0
fig.add_trace(go.Scatter(x=x_tangent, y=y_tangent, mode='lines', 
                         line=dict(color='yellow', dash='dot'), 
                         name=f'Tiếp tuyến (k={dao_ham:.2f})'))

# đánh dấu đỉnh Parabol (nếu là hàm bậc hai)
if "Hàm" in loai_ham and "bậc hai" in loai_ham or "Parabol" in loai_ham:
    if a != 0:
        fig.add_trace(go.Scatter(x=[dinh_x], y=[dinh_y], mode='markers',
                                 marker=dict(color='red', size=12, symbol='x'),
                                 name='Đỉnh Parabol (I)'))

#truc ox,oy
fig.add_hline(y=0,line_dash="dash", line_color="gray", opacity=0.5)
fig.add_vline(x=0,line_dash="dash", line_color="gray", opacity=0.5)
             
#ui
fig.update_layout(
    xaxis=dict(range=[-10, 10], zeroline=True),
    yaxis=dict(range=[-10, 10], zeroline=True),
    height=600,
    template="plotly_dark",
    margin=dict(l=20, r=80, t=40, b=80)
)

st.plotly_chart(fig, use_container_width=True)
st.write(f"👉 Tại $x = {x0}$, độ dốc (đạo hàm) là **{dao_ham:.2f}**")

#6 Phân tích
with st.expander("Xem chi tiết thông số"):
    if "Hàm" in loai_ham and "bậc hai" in loai_ham and a != 0:
        st.write(f"Tọa độ đỉnh I: $({dinh_x:.2f}, {dinh_y:.2f})$")
        delta = b**2 - 4*a*c if loai_ham == "Hàm bậc hai đầy đủ (y = ax² + bx + c)" else 0
        st.write(f"Biệt thức $\Delta$: {delta:.2f}")





