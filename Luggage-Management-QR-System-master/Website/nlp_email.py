import nltk
import pandas as pd
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords,twitter_samples
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import re, string, random
import smtplib
from email.message import EmailMessage

import mongo_api

mongo_api.main()

# data = {
#     'email': email,
#     'msg': msg,
#     'type': type
# }

nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('punkt')

#sample is helpdesk's messages
#df is training dataset
df = pd.read_csv('csv\\helpdesk.csv')
sample=pd.read_csv('csv\\messages.csv')
dfsc=df[df['category']=='Staff Complaint']
dflu=df[df['category']=='Luggage Complaint']
dfsp=df[df['category']=='Spam']
#stopwords contains list of most common english words in a sentence
stop_words=stopwords.words()

#removes special characters and splits the query string into useful words
def remove_noise(tweet_tokens, stop_words = ()):
    cleaned_tokens = []
    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

#cleaning the data and converting verbs into their basic forms 
def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)
        

dfsc_tweets=list(dfsc['Message'])
dflu_tweets=list(dflu['Message'])
dfspam_tweets=list(dfsp['Message'])

spam_tokens=[]
for k in dfspam_tweets:
    l=str(k).split()
    spam_tokens.append(l)
sc_tokens=[]
for k in dfsc_tweets:
    l=str(k).split()
    sc_tokens.append(l)
lug_tokens=[]
for k in dflu_tweets:
    l=str(k).split()
    lug_tokens.append(l)

    
clean_sc=[]
clean_lug=[]
clean_spam=[]
for tokens in sc_tokens:
    clean_sc.append(remove_noise(tokens, stop_words))
for tokens in spam_tokens:
    clean_spam.append(remove_noise(tokens, stop_words))
    
for tokens in lug_tokens:
    clean_lug.append(remove_noise(tokens, stop_words))
    
complaint_tokens_for_model = get_tweets_for_model(clean_sc)
luggage_tokens_for_model = get_tweets_for_model(clean_lug)
spam_tokens_for_model = get_tweets_for_model(clean_spam)

complaint_dataset = [(tweet_dict, "Staff Complaints")
                     for tweet_dict in complaint_tokens_for_model]
spam_dataset= [(tweet_dict1,'Spam')
               for tweet_dict1 in spam_tokens_for_model]
luggage_dataset = [(tweet_dict2, "Luggage Complaint")
                     for tweet_dict2 in luggage_tokens_for_model]
#now you have useful list of words for every query and you can train the model
#this is final dataset for training
dataset = luggage_dataset+complaint_dataset+spam_dataset
#training the data
classifier = NaiveBayesClassifier.train(dataset)
d=[]
segre=[]
samplep=sample.iloc[:,2]
for text in samplep:
    custom_tokens = remove_noise(word_tokenize(text))
    d= [text,classifier.classify(dict([token, True] for token in custom_tokens))]
    segre.append(d[1])
#splitting input csv file into 2 files , luggage_complaints and staff_complaints
sample['Category']=segre
sample_lugg=sample[sample['Category']=='Luggage Complaint']
sample_sc=sample[sample['Category']=='Staff Complaints']
sample_lugg.to_csv('csv\\luggage_complaints.csv')
sample_sc.to_csv('csv\\staff_complaints.csv')


##email script

#loading 2 datasets
staff_complaints=pd.read_csv('csv\\staff_complaints.csv')
sc_emails=staff_complaints.iloc[0:len(staff_complaints),1]
sc_flight=staff_complaints.iloc[0:len(staff_complaints),2]
sc_message=staff_complaints.iloc[0:len(staff_complaints),3]
luggage_complaints=pd.read_csv('csv\\luggage_complaints.csv')
lc_emails=luggage_complaints.iloc[0:len(luggage_complaints),1]
lc_flight=luggage_complaints.iloc[0:len(luggage_complaints),2]
lc_message=luggage_complaints.iloc[0:len(luggage_complaints),3]

#login credentials of sender's email
qremail='qrluggage@gmail.com'
qrpass='autoemailsend'
typeofemail=''

while typeofemail!='stop':
    print('Enter "luggage complaint" or "staff complaint"')
    typeofemail=str(input())
    if typeofemail=='luggage complaint':
        sent_lugg=1

    if typeofemail=='staff complaint':
        sent_staff=1

    msg = EmailMessage()
    msg['Subject'] = 'Regarding ' + typeofemail + '.'
    msg['From'] = qremail
    
    msg.add_header('Content-Type', 'text/html')
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(qremail,qrpass)
        c=0
        if typeofemail=='staff complaint':
            for k in range(len(sc_emails)):
                msg['To'] = sc_emails[k]
                mongo_api.Complaint.find_one_and_update(
                    {
                        'email': sc_emails[k],
                        'flight': sc_flight[k],
                        'msg': sc_message[k],
                    },
                    {
                        '$set': {
                            'type': 'staff complaint'
                        }
                    }
                )

                c+=1
                mail = sc_emails[k][:list(sc_emails[k]).index('@')]
                msg.set_payload('<h1>Dear '+str(mail)+',</h1>\n<p style="font-size: 20px">We are really sorry for inconvenience caused to you.<br> We will look into the matter and get back to you soon with an update on your ' + typeofemail + '.</p>')
                smtp.send_message(msg)
                print('Email sent to: '+sc_emails[k])

                # filename = "csv\\staff_complaints.csv"
                # f = open(filename, "w+")
                # f.close()

        if typeofemail=='luggage complaint':
            for k in range(len(lc_emails)):
                msg['To'] = lc_emails[k]
                mongo_api.Complaint.find_one_and_update(
                    {
                        'email': lc_emails[k],
                        'flight': lc_flight[k],
                        'msg': lc_message[k],
                    },
                    {
                        '$set': {
                            'type': 'luggage complaint'
                        }
                    },
                    upsert=True
                )

                c+=1
                mail = lc_emails[k][:list(lc_emails[k]).index('@')]
                msg.set_payload('<h1>Dear '+str(mail)+',</h1>\n<p style="font-size: 20px">We are really sorry for inconvenience caused to you.<br> We will look into the matter and get back to you soon with an update on your ' + typeofemail + '.</p>')
                smtp.send_message(msg)
                print('Email sent to: '+lc_emails[k])

                # filename = "csv\\luggage_complaints.csv"
                # f = open(filename, "w+")
                # f.close()

# filename = "csv\\messages.csv"
# f = open(filename, "w+")
# f.close()