
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Hotel Reservations Deployment 🛎🏨🛌", page_icon="🏨")

st.header("Hotel Reservation Analysis Deployment")

st.image("pexels-pixabay-261102.jpg", caption="Hotel Reservation Deployment")

df = pd.read_csv("cleaned_hotel_reservations.csv")
st.dataframe(df.head())

page = st.sidebar.radio('Pages', ['Univariate Analysis', "Bivariate Analysis", "Multivariate Analysis"])

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']



if page == "Univariate Analysis":
    type = st.selectbox("Select Chart Type", ["Histogram","Pie"])

    if type == "Histogram":
        st.plotly_chart(px.histogram(data_frame=df.groupby("no_of_week_nights")["no_of_adults"].sum().sort_values(ascending=False).reset_index(),
        x='no_of_week_nights', y='no_of_adults', title='Spent Week Day Nights'))

        st.plotly_chart(px.histogram(data_frame=df.groupby("month_name")["no_of_adults"].sum().reset_index().sort_values(by="no_of_adults",
        ascending=False)
        , x='month_name', 
        y='no_of_adults', title='Most month preferred to customers'))

        st.plotly_chart(px.histogram(data_frame= df.groupby("room_type_reserved")["no_of_adults"].sum().reset_index(),
        y='no_of_adults', x='room_type_reserved', title='Preferred Room to Adults'))

    else:
        st.plotly_chart(px.pie(data_frame=df.groupby("type_of_meal_plan")["no_of_adults"].sum().sort_values(ascending=False).reset_index(),
        names="type_of_meal_plan", values="no_of_adults", title="Preferred Meal by Adults"))

        st.plotly_chart(px.pie(data_frame= df.groupby("booking_status")["total_guests"].sum().reset_index(),
        names="booking_status", values="total_guests", title="Cancellation of Reservations"))

        st.plotly_chart(px.pie(data_frame= df.groupby("market_segment_type")["avg_price_per_room"].mean().round(2).reset_index(), 
        names='market_segment_type', values='avg_price_per_room', title='Hotel Rooms AVG Prices by Market Segments'))

elif page == "Bivariate Analysis":
    type = st.selectbox("Select Chart Type", ["Bar","Line"])

    if type == "Bar":

        st.plotly_chart(px.bar(data_frame=df.groupby("type_of_meal_plan")[["no_of_adults", "no_of_children"]].sum().sort_values(by="type_of_meal_plan" 
        ,ascending=False).reset_index(), x="type_of_meal_plan", 
        y=["no_of_adults", "no_of_children"], title="Preferred Meal by Both Adults and Children"))

        st.plotly_chart(px.bar(data_frame= df.groupby("room_type_reserved")["avg_price_per_room"].mean().sort_values(ascending=False).reset_index().round(2), 
        y='avg_price_per_room', x='room_type_reserved', title='Room Type Price AVG'))

        st.plotly_chart(px.bar(data_frame= df.groupby("room_type_reserved")["total_guests"].sum().sort_values(ascending=False).reset_index(), 
        y= 'room_type_reserved', x='total_guests', color='total_guests', title='Preferred Room to Families'))

    elif type == "Line":
        st.plotly_chart(px.line(data_frame=df.groupby("day_name")["no_of_adults"].sum().reset_index().sort_values(by="day_name"), 
        x="day_name", y="no_of_adults", title="Most Day preferred to customers", category_orders= day_order))



elif page == "Multivariate Analysis":
    type = st.selectbox("Select Chart Type", ["Scatter Plot", "Heatmap"])

    if type == "Scatter Plot":
        st.plotly_chart(px.scatter(data_frame=df,
           x='no_of_special_requests', y='lead_time', color='repeated_guest', title='Special Requests vs. Lead Time(min)'))

        st.plotly_chart(px.scatter(data_frame= df.groupby(["no_of_children"])["avg_price_per_room"].mean().reset_index().round(2), 
        x='avg_price_per_room', y='no_of_children', 
        size='avg_price_per_room', title='AVG Price to Guests who own children'))

        st.plotly_chart(px.scatter(data_frame=df, x='no_of_week_nights',
        y='no_of_weekend_nights', size='no_of_adults', color='market_segment_type',
        title="Week Nights vs. Weekend Nights (Size by number of guests)"))

    elif type == "Heatmap":
        st.plotly_chart(px.imshow(df.corr(numeric_only=True).round(2), height=1200, width=2400, text_auto=True, title="Correlation between Numeric Columns"))
