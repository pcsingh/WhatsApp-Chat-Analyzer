# Libraries Imported
import streamlit as st
import time
import io
import csv
import sys
import os

from custom_modules import func_use_extract_data as func
from custom_modules import func_analysis as analysis

# to disable warning by file_uploader going to convert into io.TextIOWrapper
st.set_option('deprecation.showfileUploaderEncoding', False)

# ------------------------------------------------

# Sidebar and main screen text and title.
st.title("WhatsApp Chat Analyzer 😃")
st.markdown(
    "This app is use to analyze your WhatsApp Chat using the exported text file 📁.")
st.sidebar.image("./assets/images/banner.jpeg",use_column_width=True)
st.sidebar.title("Analyze:")
st.sidebar.markdown(
    "This app is use to analyze your WhatsApp Chat using the exported text file 📁.")

st.sidebar.markdown('<b>Prem Chandra Singh</b>\
                <a href = "https://github.com/pcsingh/WhatsApp-Chat-Analyzer/" ><img src = "https://img.shields.io/badge/Author-@pcsingh-gray.svg?colorA=gray&colorB=dodgerblue&logo=github"/>\
                <a/>', unsafe_allow_html=True)

st.sidebar.markdown('**How to export chat text file?**')
st.sidebar.text('Follow the steps 👇:')
st.sidebar.text('1) Open the individual or group chat.')
st.sidebar.text('2) Tap options > More > Export chat.')
st.sidebar.text('3) Choose export without media.')

st.sidebar.markdown('*You are all set to go 😃*.')
# -------------------------------------------------

# Upload feature for txt file and drop-down menu for date format selection{Way 1}
st.sidebar.markdown('**Upload your chat text file:**')
date_format = st.sidebar.selectbox('Please select the date format of your file:',
                                   ('mm/dd/yyyy', 'mm/dd/yy',
                                    'dd/mm/yyyy', 'dd/mm/yy',
                                    'yyyy/mm/dd', 'yy/mm/dd'), key='0')
filename = st.sidebar.file_uploader("", type=["txt"])
st.sidebar.markdown("**Don't worry your data is not stored!**")
st.sidebar.markdown("**feel free to use 😊.**")

# =========================================================

# Select feature for txt file {Way 2}

# def file_selector(folder_path='.'):
#     filenames = os.listdir(folder_path)
#     selected_filename = st.sidebar.selectbox('Select a file', filenames)
#     return os.path.join(folder_path, selected_filename)

# filename = file_selector()
# st.sidebar.markdown('You selected {}'.format(filename))

# Check file format
# if not filename.endswith('.txt'):
#     st.error("Please upload only text file!")
#     st.sidebar.error("Please upload only text file!")
# else:

# ===========================================================
if filename is not None:

    # Loading files into data as a DataFrame
    # filename = ("./Chat.txt")
    # @st.cache(persist=True, allow_output_mutation=True) # https://docs.streamlit.io/library/advanced-features/caching#:~:text=st.cache_data%C2%A0is%20the%20recommended%20way%20to%20cache%20computations%20that%20return%20data%3A%20loading%20a%20DataFrame%20from%20CSV%2C
    @st.cache_data
    def load_data(date_format=date_format):

        file_contents = []

        if filename is not None:
            content = filename.read().decode('utf-8')

            # Use StringIO object to create a file-like object
            with io.StringIO(content) as f:
                reader = csv.reader(f, delimiter='\n')
                for each in reader:
                    if len(each) > 0:
                        file_contents.append(each[0])
                    else:
                        file_contents.append('')
        else:
            st.error("Please upload the WhatsApp chat dataset!")

        return func.read_data(file_contents, date_format)

    try:
        data = load_data()

        if data.empty:
            st.error("Please upload the WhatsApp chat dataset!")

        if st.sidebar.checkbox("Show raw data", True):
            st.write(data)
        # ------------------------------------------------

        # Members name involve in Chart
        st.sidebar.markdown("### To Analyze select")
        names = analysis.authors_name(data)
        names.append('All')
        member = st.sidebar.selectbox("Member Name", names, key='1')

        if not st.sidebar.checkbox("Hide", True):
            try:
                if member == "All":
                    st.markdown(
                        "### Analyze {} members together:".format(member))
                    st.markdown(analysis.stats(data), unsafe_allow_html=True)

                    st.write("**Top 10 frequent use emoji:**")
                    emoji = analysis.popular_emoji(data)
                    for e in emoji[:10]:
                        st.markdown('**{}** : {}'.format(e[0], e[1]))

                    st.write('**Visualize emoji distribution in pie chart:**')
                    st.plotly_chart(analysis.visualize_emoji(data))

                    st.markdown('**Word Cloud:**')
                    st.text(
                        "This will show the cloud of words which you use, larger the word size most often you use.")
                    st.pyplot(analysis.word_cloud(data))
                    # st.pyplot()

                    time.sleep(0.2)

                    st.write('**Most active date:**')
                    st.pyplot(analysis.active_date(data))
                    # st.pyplot()

                    time.sleep(0.2)

                    st.write('**Most active time for chat:**')
                    st.pyplot(analysis.active_time(data))
                    # st.pyplot()

                    st.write(
                        '**Day wise distribution of messages for {}:**'.format(member))
                    st.plotly_chart(analysis.day_wise_count(data))

                    st.write('**Number of messages as times move on**')
                    st.plotly_chart(analysis.num_messages(data))

                    st.write('**Chatter:**')
                    st.plotly_chart(analysis.chatter(data))

                else:
                    member_data = data[data['Author'] == member]
                    st.markdown("### Analyze {} chat:".format(member))
                    st.markdown(analysis.stats(member_data),
                                unsafe_allow_html=False)

                    st.write("**Top 10 Popular emoji:**")
                    emoji = analysis.popular_emoji(member_data)
                    for e in emoji[:10]:
                        st.markdown('**{}** : {}'.format(e[0], e[1]))

                    st.write('**Visualize emoji distribution in pie chart:**')
                    st.plotly_chart(analysis.visualize_emoji(member_data))

                    st.markdown('**Word Cloud:**')
                    st.text(
                        "This will show the cloud of words which you use, larger the word size most often you use.")
                    st.pyplot(analysis.word_cloud(member_data))

                    time.sleep(0.2)

                    st.write(
                        '**Most active date of {} on WhatsApp:**'.format(member))
                    st.pyplot(analysis.active_date(member_data))
                    # st.pyplot()

                    time.sleep(0.2)

                    st.write('**When {} is active for chat:**'.format(member))
                    st.pyplot(analysis.active_time(member_data))
                    # st.pyplot()

                    st.write(
                        '**Day wise distribution of messages for {}:**'.format(member))
                    st.plotly_chart(analysis.day_wise_count(member_data))

                    st.write('**Number of messages as times move on**')
                    st.plotly_chart(analysis.num_messages(member_data))

            except:
                e = sys.exc_info()[0]
                st.error("It seems that something is wrong! Try Again. Error Type: {}".format(
                    e.__name__))

        # --------------------------------------------------

    except:
        e = sys.exc_info()
        st.error("Something is wrong in loading the data! Please select the correct date format or Try again. Error Type: {}.\n \n **For Detail Error Info: {}**".format(e[0].__name__, e[1]))
        # Debugging
        # e = sys.exc_info()
        # st.error("Something is wrong! Try Again. Error Type: {}".format(e))


st.sidebar.markdown(
    "[![built with love](https://forthebadge.com/images/badges/built-with-love.svg)](https://www.linkedin.com/in/premchandra-singh/)")
st.sidebar.markdown(
    "[![smile please](https://forthebadge.com/images/badges/makes-people-smile.svg)](https://www.linkedin.com/in/premchandra-singh/)")
