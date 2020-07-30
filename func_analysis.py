def authors_name(data):
    """
        It returns the name of participants in chat. 
    """
    authors = data.Author.unique().tolist()
    return [name for name in authors if name != None]


def extract_emojis(s):
    """
        This function is used to calculate emojis in text and return in a list.
    """
    return [c for c in s if c in emoji.UNICODE_EMOJI]


def stats(data):
    """
        This function takes input as data and return number of messages and total emojis used in chat.
    """
    total_messages = data.shape[0]
    media_messages = data[data['Message'] == '<Media omitted>'].shape[0]
    emojis = sum(data['emoji'].str.len())
    
    return "Total Messages 💬: {} \nMedia 🎬: {} \nEmoji's 😂: {}".format(total_messages, media_messages, emojis)


def popular_emoji(data):
    """
        This function returns the list of emoji's with it's frequency.
    """
    total_emojis_list = list([a for b in data.emoji for a in b])
    emoji_dict = dict(c.Counter(total_emojis_list))
    emoji_list = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
    return emoji_list


def visualize_emoji(data):
    """
        This function is used to make pie chart of popular emoji's.
    """
    emoji_df = pd.DataFrame(popular_emoji(data), columns=['emoji', 'count'])
    
    fig = px.pie(emoji_df, values='count', names='emoji')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.show()
    
    
def word_cloud(df):
    """
        This function is used to generate word cloud using dataframe.
    """
    
    df = df[df['Message'] != '<Media omitted>']
    df = df[df['Message'] != 'This message was deleted']
    words = ' '.join(df['Message'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    # To stop article, punctuations
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)
    
    plt.figure(figsize=(45,8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

