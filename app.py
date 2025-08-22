import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Mini Data Analytics Dashboard", page_icon="📊", layout="wide")

# Sidebar
st.sidebar.header("⚙️ Controls")

# Title
st.title("📊 Mini Data Analytics Dashboard")
st.markdown("A simple and interactive way to explore your data.")

# Upload CSV
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ File uploaded successfully!")

    # Tabs for better UX
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Raw Data", "📈 Summary Statistics", "📝 Columns", "📊 Charts"])

    with tab1:
        st.subheader("Raw Data")
        st.dataframe(df, use_container_width=True)

    with tab2:
        st.subheader("Summary Statistics")
        st.write(df.describe(include="all"))

    with tab3:
        st.subheader("Columns in Dataset")
        col_info = pd.DataFrame({
            "Column Name": df.columns,
            "Data Type": df.dtypes.values,
            "Missing Values": df.isnull().sum().values
        })
        st.table(col_info)

    with tab4:
        st.subheader("Interactive Charts")
        chart_type = st.radio("Select chart type", ["Bar Chart", "Line Chart", "Pie Chart"], horizontal=True)

        numeric_columns = df.select_dtypes(include='number').columns.tolist()
        categorical_columns = df.select_dtypes(include='object').columns.tolist()

        if chart_type in ["Bar Chart", "Line Chart"] and numeric_columns:
            x_col = st.selectbox("Select X-axis column", df.columns, key="xcol")
            y_col = st.selectbox("Select numeric Y-axis column", numeric_columns, key="ycol")

            if chart_type == "Bar Chart":
                fig = px.bar(df, x=x_col, y=y_col, color=x_col, title=f"{y_col} by {x_col}")
            else:
                fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} over {x_col}")

            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Pie Chart" and numeric_columns and categorical_columns:
            names_col = st.selectbox("Select column for categories", categorical_columns, key="namescol")
            values_col = st.selectbox("Select numeric column for values", numeric_columns, key="valscol")

            fig = px.pie(df, names=names_col, values=values_col, title=f"Distribution of {values_col} by {names_col}")
            st.plotly_chart(fig, use_container_width=True)

    # Download cleaned data
    st.sidebar.download_button(
        "⬇️ Download Processed Data",
        df.to_csv(index=False).encode(),
        "processed_data.csv",
        "text/csv"
    )

else:
    st.info("👆 Upload a CSV file from the sidebar to get started.")
