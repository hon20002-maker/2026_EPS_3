import streamlit as st
import pandas as pd

# 設定網頁標題與風格
st.set_page_config(page_title="全台股五等分價值估值工具", layout="centered")

st.title("📈 全台上市/上櫃股票五等分價值估值工具")
st.write("本網頁支援全台灣所有上市與上櫃股票！請至財經網站（如台灣股市資訊網、Goodinfo）查詢該股數據並填入下方，系統將秒速為您產出 2026 最新五等分估值表。")

st.markdown("---")

# 建立側邊欄或主介面的輸入區
st.subheader("📥 第一步：填入股票基本與財務數據")

col1, col2 = st.columns(2)
with col1:
    stock_name = st.text_input("股票名稱或代號：", "廣達 (2382)")
    rev_2025 = st.number_input("2025 年全年總營收 (億元)：", min_value=0.0, value=10856.0, step=10.0, help="請填入2025年全年的總營收")
    growth_rate = st.number_input("2026年前5個月累計營收年增率 (%)：", value=18.5, step=0.1, help="例如年增18.5%，請輸入 18.5")
    margin_rate = st.number_input("最新近四季平均稅後淨利率 (%)：", value=4.5, step=0.1, help="請將最新近四季的稅後淨利率相加除以4")

with col2:
    shares_out = st.number_input("目前發行總股數 (億股)：", min_value=0.01, value=38.6, step=0.1, help="可由實收資本額除以10元換算，例如資本額386億即為38.6億股")
    pe_high = st.number_input("近三年每年最高本益比之平均值：", min_value=0.1, value=19.5, step=0.1)
    pe_low = st.number_input("近三年每年最低本益比之平均值：", min_value=0.1, value=11.2, step=0.1)

st.markdown("---")

# 計算按鈕
if st.button("🚀 一鍵秒速精算合理股價", type="primary"):
    if pe_high <= pe_low:
        st.error("錯誤：『最高本益比平均值』必須大於『最低本益比平均值』，請重新檢查輸入。")
    else:
        st.success(f"⚡ 計算成功！【{stock_name}】2026年最新五等分估值報告已產出：")
        
        # 1. 預估 2026 全年營收
        est_rev = rev_2025 * (1 + (growth_rate / 100))
        # 2. 預估 2026 稅後淨利
        est_net_income = est_rev * (margin_rate / 100)
        # 3. 預估 2026 全年 EPS
        est_eps = est_net_income / shares_out
        
        # 顯示三大核心預估指標
        c1, c2, c3 = st.columns(3)
        c1.metric("預估 2026 全年營收", f"{est_rev:,.1f} 億元")
        c2.metric("預估 2026 稅後淨利", f"{est_net_income:,.1f} 億元")
        c3.metric("預估 2026 全年 EPS", f"{est_eps:.2f} 元")
        
        # 5. 五等分區間推導
        pe_range = pe_high - pe_low
        step = pe_range / 5
        pe_points = [pe_low + step * i for i in range(6)]
        
        intervals = []
        for i in range(5):
            low_pe = pe_points[i]
            high_pe = pe_points[i+1]
            low_price = low_pe * est_eps
            high_price = high_pe * est_eps
            
            if i == 0:
                tag = "便宜（下方位置）"
            elif i == 4:
                tag = "昂貴（上方位置）"
            else:
                tag = "合理（中間區域）"
                
            intervals.append({
                "區間位置": f"第 {i+1} 區間",
                "本益比範圍": f"{low_pe:.2f} 倍 ～ {high_pe:.2f} 倍",
                "2026 預估股價區間": f"{low_price:,.1f} 元 ～ {high_price:,.1f} 元",
                "評價等級": tag
            })
            
        df = pd.DataFrame(intervals)
        
        # 漂亮輸出結果表格
        st.subheader("📊 2026 年股票估值五等分區間表")
        st.table(df)
        
        # 貼心小警語
        st.caption("※ 註：本工具計算結果僅供參考，投資有風險，入市需謹慎。")
