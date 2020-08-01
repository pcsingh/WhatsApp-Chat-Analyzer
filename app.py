# Libraries Imported
import streamlit as st
import os
import io
import csv
import sys

from custom_modules import func_use_extract_data as func
from custom_modules import func_analysis as analysis

# to disable warning by file_uploader going to convert into io.TextIOWrapper
# st.set_option('deprecation.showfileUploaderEncoding', False)

# ------------------------------------------------

# Sidebar and main screen text and title.
st.title("WhatsApp Chat Analyzer 😃")
st.markdown("This app is use to analyze your WhatsApp Chat using the exported text file 📁.")

st.sidebar.title("Analyze:")
st.sidebar.markdown("This app is use to analyze your WhatsApp Chat using the exported text file 📁.")

st.sidebar.markdown('[![Premchandra Singh]\
                    (https://img.shields.io/badge/Author-@pcsingh-gray.svg?colorA=gray&colorB=dodgerblue&logo=github)]\
                    (https://github.com/pcsingh/WhatsApp-Chat-Analyzer/)')

st.sidebar.markdown('**How to export chat text file?**')
st.sidebar.text('Follow the steps 👇:')
st.sidebar.text('1) Open the individual or group chat.')
st.sidebar.text('2) Tap options > More > Export chat.')
st.sidebar.text('3) Choose export without media.')

st.sidebar.markdown('*You are all set to go 😃*.')
# -------------------------------------------------

# Upload feature for txt file {Way 1}
st.sidebar.markdown('**Upload your chat text file:**')
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
#     st.markdown("<style>h2{color:red;}</style><b><h2>Please upload only text file!</h2></b>", unsafe_allow_html=True)
#     st.sidebar.markdown("<style>b{color:red;}</style><b>Please upload only text file!</b>", unsafe_allow_html=True)  
# else:

# ===========================================================
if filename is not None:

    # Loading files into data as a DataFrame
    # filename = ("./Chat.txt")
    
    @st.cache(persist=True, allow_output_mutation=True)
    def load_data():
        reader = csv.reader(filename, delimiter='\n')
        file_contents = []
        
        for each in reader:
            if len(each) > 0:
                file_contents.append(each[0])
            else:
                file_contents.append('')

        return func.read_data(file_contents)
    try:
        data = load_data()
        
        if data.empty:
            st.error("Please upload the WhatsApp chat dataset!")
            
        if st.sidebar.checkbox("Show raw data", False):
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
                    st.markdown("### Analyze {} members together:".format(member))
                    st.markdown(analysis.stats(data), unsafe_allow_html=True)
                    
                    st.write("**Top 10 frequent use emoji:**")
                    emoji = analysis.popular_emoji(data)
                    for e in emoji[:10]:
                        st.markdown('**{}** : {}'.format(e[0], e[1]))
                    
                    st.write('**Visualize emoji distribution in pie chart:**')
                    st.plotly_chart(analysis.visualize_emoji(data))
                    
                    st.write('**Most active date:**')
                    analysis.active_date(data)
                    st.pyplot()
                    
                    st.write('**Most active time for chat:**')
                    analysis.active_time(data)
                    st.pyplot()
                    
                    st.write('**Day wise distribution of messages for {}:**'.format(member))
                    st.plotly_chart(analysis.day_wise_count(data))
                    
                    st.write('**Number of messages as times move on**')
                    st.plotly_chart(analysis.num_messages(data))
                    
                    st.write('**Chatter:**')
                    st.plotly_chart(analysis.chatter(data))
                    
                    st.markdown('**Word Cloud:**')
                    analysis.word_cloud(data)
                    st.pyplot()
                    
                else:
                    member_data = data[data['Author'] == member]
                    st.markdown("### Analyze {} chat:".format(member))
                    st.markdown(analysis.stats(member_data), unsafe_allow_html=False)
                    
                    st.write("**Top 10 Popular emoji:**")
                    emoji = analysis.popular_emoji(member_data)
                    for e in emoji[:10]:
                        st.markdown('**{}** : {}'.format(e[0], e[1]))
                        
                    st.write('**Visualize emoji distribution in pie chart:**')
                    st.plotly_chart(analysis.visualize_emoji(member_data))
                    
                    st.write('**Most active date of {} on WhatsApp:**'.format(member))
                    analysis.active_date(member_data)
                    st.pyplot()
                    
                    st.write('**When {} is active for chat:**'.format(member))
                    analysis.active_time(member_data)
                    st.pyplot()
                    
                    st.write('**Day wise distribution of messages for {}:**'.format(member))
                    st.plotly_chart(analysis.day_wise_count(member_data))
                    
                    st.write('**Number of messages as times move on**')
                    st.plotly_chart(analysis.num_messages(member_data))
                    
                    st.markdown('**Word Cloud:**')
                    analysis.word_cloud(member_data)
                    st.pyplot()
            except:
                e = sys.exc_info()[0]
                st.error("It seems that something is wrong! Try Again. Error Type: {}".format(e.__name__))
                
        # --------------------------------------------------

    except:
        e = sys.exc_info()[0]
        st.error("Something is wrong in loading the data! Try again. Error Type: {}".format(e.__name__))


st.sidebar.markdown("[![built with love](https://forthebadge.com/images/badges/built-with-love.svg)](https://www.linkedin.com/in/premchandra-singh/)")
st.sidebar.markdown("[![smile please](https://forthebadge.com/images/badges/makes-people-smile.svg)](https://www.linkedin.com/in/premchandra-singh/)")

