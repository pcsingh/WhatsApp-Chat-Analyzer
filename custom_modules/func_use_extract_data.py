import pandas as pd
import re

import custom_modules.func_analysis as analysis


def startsWithDateTime(s):
    pattern = '^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4})(,)? ([0-9])|([0-9]):([0-9][0-9]) '
    result = re.match(pattern, s)
    if result:
        return True
    return False



def startsWithAuthor(s):
    """
        This function is used to verify the string(s) contains 'Author' or not with the help of regular expressions.
        
        Parameters:
            s: String
        
        Returns:
            True if it contains author name otherwise False
    """
    
    pattern = '^([\w()\[\]-]+):|([\w]+[\s]+([\w()\[\]-]+)):'
    result = re.match(pattern, s)
    if result:
        return True
    return False



def getDataPoint(line):
    """
        Use to extract the date, time, author and message from line.
        
        Parameters: 
            line (from txt file)
        
        Returns:
            date, time, author, message        
    """
    splitLine = line.split(' - ') # splitLine = ['18/06/17, 22:47', 'Loki: Why do you have 2 numbers, Banner?']
    
    dateTime = splitLine[0] # dateTime = '18/06/17, 22:47'

    if ',' not in dateTime:
        dateTime = dateTime.replace(' ', ', ', 1)

    date, time = dateTime.split(', ')  # date = '18/06/17'; time = '22:47'
    
    if "am" in time:
        time = time.replace("am", "") # time = '11:00 am' becomes time = '11:00 '
    elif "pm" in time:
        time = time.replace("pm", "") # time = '11:00 pm' becomes time = '11:00 '
        time = time.split(':') # time = ['11', '00 ']
        time[0] = str(int(time[0]) + 12) # time = ['23', '00 ']
        time = ':'.join(time) # time = '23:00 '

    message = ' '.join(splitLine[1:]) # message = 'Loki: Why do you have 2 numbers, Banner?'
    
    if startsWithAuthor(message): # True
        splitMessage = message.split(': ') # splitMessage = ['Loki', 'Why do you have 2 numbers, Banner?']
        author = splitMessage[0] # author = 'Loki'
        message = ' '.join(splitMessage[1:]) # message = 'Why do you have 2 numbers, Banner?'
    else:
        author = None
    return date, time, author, message


def read_data(file_contents, date_format):
    """
        This function is use to return the extracted data from txt file.
        
        Parameters:
            file_contents -> line by line contents from txt chat file
            
        Returns:
            data -> list of list having elements as date, time, author and message by the user.
    """
    # Dictionary to assign each date format to the corresponding strftime format
    date_formats_dict = {'mm/dd/yyyy': '%m/%d/%Y', 'mm/dd/yy': '%m/%d/%y',
                         'dd/mm/yyyy': '%d/%m/%Y', 'dd/mm/yy': '%d/%m/%y',
                         'yyyy/mm/dd': '%Y/%m/%d', 'yy/mm/dd': '%y/%m/%d'}

    data = [] # List to keep track of data so it can be used by a Pandas dataframe

    messageData = [] # to capture intermediate output for multi-line messages
    date, time, author = None, None, None # Intermediate variables to keep track of the current message being processed
    
    for line in file_contents:
        line = line.strip() # Guarding against erroneous leading and trailing whitespaces
        if startsWithDateTime(line): # If a line starts with a Date Time pattern, then this indicates the beginning of a new message
            if len(messageData) > 0: # Check if the message buffer contains characters from previous iterations
                data.append([date, time, author, ' '.join(messageData)]) # Save the tokens from the previous message in data
            messageData.clear() # Clear the messageData so that it can be used for the next message
            date, time, author, message = getDataPoint(line) # Identify and extract tokens from the line
            messageData.append(message) # Append message
        else:
            messageData.append(line) # If a line doesn't start with a Date Time pattern, then it is part of a multi-line message. So, just append to messageData
    
    df = pd.DataFrame(data, columns=['Date', 'Time', 'Author', 'Message'])
    df["Date"] = pd.to_datetime(df["Date"], format=date_formats_dict[date_format])
    df['emoji'] = df["Message"].apply(analysis.extract_emojis)
    
    return df

