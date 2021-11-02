import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st 
import seaborn as sns 
import numpy as np 
from wordcloud import WordCloud 

#function to skip line and have better visualization 
def skip_line(i):
    for j in range(i):
        st.write(" ")
    


st.title("Informations about my Snap and Spotify data")
st.write("Select a checkbox on the left side")


st.title("Informations about me")

col1, col2 = st.columns(2)

with col1 :
    st.write("Auban NDAMKOU NJAKAM")
    st.write("DS1 group Data Engineering")
    st.image("photo_identité.jpg")

with col2:
    st.write("Click below to my LinkedIn account")
    st.markdown("<h2>🔗 <a href='https://www.linkedin.com/in/aubain-ndamkou-njakam-ba7927182/'>Go to my linkedin</a></h2>", unsafe_allow_html=True)
    st.image("frame.png")

df = pd.read_csv('mydata/location.csv')

if st.sidebar.checkbox("Snap data"):
    st.subheader("Snap Data")
    st.image("https://upload.wikimedia.org/wikipedia/fr/a/ad/Logo-Snapchat.png", width=200)
    st.subheader("Snap map Data")
    st.write(df)

    skip_line(5)
    st.subheader("Formatting latitude and logitude in other dataframe")
    df1=df['Time']
    df2 = df['Latitude, Longitude'].str.split(',', expand=True).rename({0: 'lat', 1: 'lon'}, axis=1)
    st.write(df2)
    for col in df2.columns:
        df2[col] = df2[col].map(lambda x: float(x.split("±")[0]))
    
    #formatting time 
    df1 = pd.DataFrame({"Time" : pd.to_datetime(df1)})
    #concat data
    df = pd.concat([df1, df2], axis=1)
    

    skip_line(5)
    st.subheader("Visualizing all my location on the map")
    st.map(df2)
    st.write("I went to Africa for the Holiday in Cameroun my native country, We can also see that i travelled for Barcelona in spain, Before comming to Paris i was in the south of France")


    #share story on Snap chat 
    skip_line(5)
    st.subheader("shared story frequency by the last 30 days")
    df=pd.read_csv('mydata/shared_story.csv')
    #disable warning 
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.hist(df["Spotlight History/Story Date"],bins = 30, rwidth=0.8, range=(1,10))
    plt.xticks(rotation=85)
    plt.title('Frequency')
    st.pyplot()
    st.write("I didn't share enought on september but too much the 11/10/2021")
    skip_line(3)
    st.write("No enought data on snap,Let move to the spotify data")

    

if st.sidebar.checkbox("Spotify Data"):
    
    st.subheader("Spotify Data")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Spotify_logo_with_text.svg/1118px-Spotify_logo_with_text.svg.png", width=200)

    dfs1 = pd.read_json("StreamingHistory0.json") # Load the JSON File into a dataframe
    dfs2 = pd.read_json("StreamingHistory1.json")
    dfs3 = pd.read_json("StreamingHistory2.json")
    #merging the data 
    spotify_stream_df = pd.concat([dfs1,dfs2,dfs3], ignore_index=True)
    skip_line(5)

    st.subheader("spotify streaming history")
    st.write(spotify_stream_df)

    #cleaning and formatting data 
    #Here we used the DatetimeIndex module to obatin the several unique information.
    spotify_stream_df["Play-Time"]= pd.to_datetime(spotify_stream_df["endTime"]) # To create a additional column
    spotify_stream_df['year'] = pd.DatetimeIndex(spotify_stream_df["Play-Time"]).year
    spotify_stream_df['month'] = pd.DatetimeIndex(spotify_stream_df["Play-Time"]).month
    spotify_stream_df['day'] = pd.DatetimeIndex(spotify_stream_df["Play-Time"]).day
    spotify_stream_df['weekday'] = pd.DatetimeIndex(spotify_stream_df["Play-Time"]).weekday
    spotify_stream_df['time'] = pd.DatetimeIndex(spotify_stream_df["Play-Time"]).time
    spotify_stream_df['hours'] = pd.DatetimeIndex(spotify_stream_df["Play-Time"]).hour
    spotify_stream_df['day-name'] = spotify_stream_df["Play-Time"].apply(lambda x: x.day_name())
    spotify_stream_df['Count'] = 1
    

    #Here we used the to_timedelta module to obatin the information regarding the time frame of the song played in milli-seconds.
    spotify_stream_df["Time-Played (hh-mm-ss)"] = pd.to_timedelta(spotify_stream_df["msPlayed"], unit='ms')

    def hours(td):
        '''To get the hour information'''
        return td.seconds/3600

    def minutes(td):
        '''To get the minutes information'''
        return (td.seconds/60)%60

    spotify_stream_df["Listening Time(Hours)"] = spotify_stream_df["Time-Played (hh-mm-ss)"].apply(hours).round(3)
    spotify_stream_df["Listening Time(Minutes)"] = spotify_stream_df["Time-Played (hh-mm-ss)"].apply(minutes).round(3)
    
    skip_line(5)
    st.subheader("Piechart of unique and no unique artist")
    
    unique_artists = spotify_stream_df["artistName"].nunique() # Count number of unique artist in dataset
    total_artists = spotify_stream_df["artistName"].count() # Count total artist in dataset
    unique_artist_percentage = unique_artists/total_artists*100 # Get the percentage of the unique

    unique_artist_list = np.array([unique_artists, total_artists-unique_artists]) # Make an array out of the results
    unique_artist_list_labels = [" Unique Artists", "Non Unique Artists"] # Make a lable for them

    fig, ax = plt.subplots(figsize=(12,6))
    ax.pie(unique_artist_list, labels= unique_artist_list_labels, autopct='%1.1f%%',explode=[0.05,0.05] ,startangle=180, shadow = True);
    plt.title("Unique Artist Percentage");
    st.pyplot(fig)
    st.write("The unique artist percentage comes around 4%")
    skip_line(5)

    
    st.subheader("Top 10 based on hours")
    top_10_artist_time_df = spotify_stream_df.groupby(["artistName"])[["Listening Time(Hours)","Listening Time(Minutes)","Count"]].sum().sort_values(by="Listening Time(Minutes)",ascending=False)
    st.write(top_10_artist_time_df.head(10))

    skip_line(5)
    st.write("Here we made a bar chart to show the same list in a better visualisation")
    fig,ax = plt.subplots(figsize=(12,8))
    ax.bar(top_10_artist_time_df.head(10).index,top_10_artist_time_df["Listening Time(Hours)"].head(10),color='red')
    ax.set(title="My Top 10 Favourite Artist (based on Hours)",xlabel="Artists",ylabel="No. of Hours Songs Played");
    plt.xticks(rotation=75);
    st.pyplot(fig)

    skip_line(5)
    st.subheader("Top 10 based on number of count")
    top_10_artist_count_df = spotify_stream_df.groupby(["artistName"])[["Listening Time(Hours)","Listening Time(Minutes)","Count"]].sum().sort_values(by="Count",ascending=False)
    st.write(top_10_artist_count_df.head(10))

    skip_line(5)
    st.write("Bar chart for better visualization")
    fig,ax = plt.subplots(figsize=(12,8))
    ax.bar(top_10_artist_count_df.head(10).index,top_10_artist_count_df["Count"].head(10),color='pink')
    ax.set(title="My Top 10 Favourite Artist (based on Counts)",xlabel="Artists",ylabel="No. of Times Songs Played");
    plt.xticks(rotation=75);
    st.pyplot(fig)

    skip_line(5)
    st.subheader("Pie Chart")
    st.write("This pie chart is to see the percentage usage of spotify over a week")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.pie(spotify_stream_df["day-name"].value_counts(), labels=spotify_stream_df["day-name"].value_counts().index, autopct='%1.1f%%', startangle=180, shadow = True);
    ax.set(title="Day wise % of Spotify Streaming");
    st.pyplot(fig)
    st.write("I listen more music on Friday followed by sunday")

    skip_line(5)
    st.subheader("Average Usage In a year")
    fig, ax = plt.subplots(figsize=(12,6))
    ax = sns.countplot(y=spotify_stream_df["month"], ax=ax)
    ax.set(title="Average Spotify Usage over Years", xlabel="Songs Played in Counts", ylabel="Months (1-12)");
    st.pyplot(fig)
    st.write("I was listened more music on May and April")

    skip_line(5)
    st.subheader("My top 50 song on spotify")
    fav_artist = spotify_stream_df.groupby(["artistName"])["Count"].count()
    st.write(fav_artist)
    st.subheader("WordCloud of my top 50 song i listened on spotify")
    fig, ax = plt.subplots(figsize=(20,15))
    wordcloud = WordCloud(width=1000,height=600, max_words=100,relative_scaling=1,normalize_plurals=False).generate_from_frequencies(fav_artist)
    ax.imshow(wordcloud, interpolation='bilinear')
    plt.axis(False)
    st.pyplot(fig)

    skip_line(5)
    st.subheader("Most listening day/usage with them occurences")
    active_usage = spotify_stream_df.groupby(['hours', 'day-name'])['artistName'].size().reset_index()
    active_usage_pivot = active_usage.pivot("hours", 'day-name', 'artistName')
    st.write(active_usage_pivot)

    skip_line(5)
    st.subheader("Heatmap of spotify Usage for better visualization")
    days = ["Monday", 'Tuesday', "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    fig, ax = plt.subplots(figsize=(15,12))
    ax = sns.heatmap(active_usage_pivot[days].fillna(0), robust=True, cmap="Blues", ax = ax);
    ax.set(title="Heat Map of Spotify Usage", xlabel="Days of the Week",ylabel="Time(in 24 hrs format)")
    st.pyplot(fig)

if st.button("🎉"):
    st.balloons()













