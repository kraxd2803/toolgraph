import streamlit as st
import numpy as np
import plotly.graph_objects as go

#1title
st.set_page_config(page_title="📊TOOL VẼ ĐỒ THỊ", layout="wide",page_icon= "⚡️")
st.caption("made by DangKhoa🔰 - beta version")
st.title("Công cụ vẽ đồ thị tương tác")

hd = "huongdan.png"

if st.toggle("📄 Hiển thị Hướng dẫn sử dụng"):
    try:
        st.image(hd, caption="Bật bảng Settings ở góc trái màn hình", width="stretch")
    except Exception:
        # Dùng Exception chung để bắt mọi lỗi liên quan đến file hoặc định dạng
        st.warning(f"⚠️ KHÔNG TÌM THẤY ẢNH: Hãy đảm bảo file '{hd}' đã được upload lên GitHub cùng thư mục với main.py")
#2type
st.sidebar.header("Setting")
loai_ham = st.sidebar.selectbox(
    "Chọn loại hàm số:",
    ("Hàm bậc nhất (y = ax + b)", "Hàm Parabol cơ bản (y = ax²)", "Hàm bậc hai đầy đủ (y = ax² + bx + c)")
)

#3setting
st.sidebar.subheader("Điều chỉnh tham số")
a = st.sidebar.slider("Hệ số a", -10.0, 10.0, 1.0, 0.1)
b = st.sidebar.slider("Hệ số b", -10.0, 10.0, 0.0, 0.1)
c = st.sidebar.slider("Hệ số c", -10.0, 10.0, 0.0, 0.1)

st.sidebar.subheader("Đạo hàm & Tiếp tuyến")
x0 = st.sidebar.slider("Chọn điểm x₀", -10.0, 10.0, 2.0, 0.1)

st.sidebar.markdown("---")
st.sidebar.subheader("Giao điểm với đường thẳng (d)")
show_d = st.sidebar.checkbox("Bật đường thẳng (d): y = mx + n")
if show_d:

    m = st.sidebar.slider("Hệ số m", -10.0, 10.0, 1.0, 0.1)

    n = st.sidebar.slider("Hệ số n", -10.0, 10.0, -2.0, 0.1)

#4cal
dinh_x, dinh_y = 0.0, 0.0

if loai_ham == "Hàm bậc nhất (y = ax + b)":
    congthuc = f"y = {a}x + {b}"
    x = np.linspace(-10, 10, 1000)
    y = a*x + b
    dao_ham = a
    y0 = a*x0 + b

elif loai_ham == "Hàm Parabol cơ bản (y = ax²)":
    congthuc = f"y = {a}x^2"
    x = np.linspace(-10, 10, 1000)
    y = a*x**2
    dao_ham = 2*a*x0
    y0 = a*x0**2

else:  # Hàm bậc hai đầy đủ
    congthuc = f"y = {a}x^2 + {b}x + {c}"
    x = np.linspace(-10, 10, 1000)
    y = a*x**2 + b*x + c
    dao_ham = 2*a*x0 + b
    y0 = a*x0**2 + b*x0 + c
    

#5 hien thi & tao do thi
st.latex(congthuc)
fig = go.Figure()

if show_d:
    # 1. Vẽ đường thẳng (d)
    y_d = m * x + n
    fig.add_trace(go.Scatter(x=x, y=y_d, mode='lines', name=f'(d): y={m}x+{n}', 
                             line=dict(color='white', dash='dash')))

    # 2. Giải phương trình hoành độ giao điểm
    # ax^2 + (b-m)x + (c-n) = 0
    A = a if "bậc hai" in loai_ham or "Parabol" in loai_ham else 0
    B = (b - m) if "bậc hai" in loai_ham or "Parabol" in loai_ham else (a - m)
    C = (c - n) if "bậc hai" in loai_ham or "Parabol" in loai_ham else (b - n)

    if A != 0:
        # Giải bậc 2 bằng Delta
        delta_g = B**2 - 4*A*C
        if delta_g >= 0:
            x_roots = [(-B + np.sqrt(delta_g))/(2*A), (-B - np.sqrt(delta_g))/(2*A)]
            for xr in set(x_roots):
                yr = m * xr + n
                fig.add_trace(go.Scatter(x=[xr], y=[yr], mode='markers',
                                         marker=dict(color='orange', size=12, symbol='star'),
                                         name="Giao điểm"))
    elif B != 0:
        # Giải bậc 1: Bx + C = 0 -> x = -C/B
        xr = -C / B
        yr = m * xr + n
        fig.add_trace(go.Scatter(x=[xr], y=[yr], mode='markers',
                                 marker=dict(color='orange', size=12, symbol='star'),
                                 name="Giao điểm"))

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
if show_d and "Hàm bậc hai" in loai_ham:
    with st.expander("Phân tích giao điểm (P) và (d)"):
        st.write(f"Xét phương trình hoành độ giao điểm: ${a}x^2 + ({b}-{m})x + ({c}-{n}) = 0$")
        if delta_g > 0:
            st.success(f"$\Delta' = {delta_g:.2f} > 0$: (d) cắt (P) tại 2 điểm phân biệt.")
        elif delta_g == 0:
            st.warning(f"$\Delta' = 0$: (d) tiếp xúc với (P).")
        else:
            st.error(f"$\Delta' = {delta_g:.2f} < 0$: (d) và (P) không có điểm chung.")






















