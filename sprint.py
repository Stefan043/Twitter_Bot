import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
from nltk.tokenize import word_tokenize
import re
import operator 
import json
from collections import Counter
from nltk.corpus import stopwords
import string
from nltk import bigrams
from collections import defaultdict
import vincent
import sys
 
consumer_key = '4VAEYOhZ9EYUpeclCt6s5ZFGs'
consumer_secret = 'a1mtI4z1DYcZ0YrLqdVZg4vnGUxX4aLvNltDUsyln02wON1n2g'
access_token = '1247080467268075520-40NbMCYKspO39l8ALPUmadggOFu8nx'
access_secret = 'ZIfDrLiWy7pURRLqMl8oaAn7Ynss4eaHAjSuJljIc7pER'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth, wait_on_rate_limit=True)
 
# class MyListener(StreamListener):
 
#     def on_data(self, data):
#         try:
#             with open('python.json', 'a') as f:
#                 f.write(data)
#                 return True
#         except BaseException as e:
#             print("Error on_data: %s" % str(e))
#         return True
 
#     def on_error(self, status):
#         print(status)
#         return True
 
# twitter_stream = Stream(auth, MyListener())
# twitter_stream.filter(track=['#programming'])

 
#with open('python.json', 'r') as f:
    # line = f.readline() # read only the first tweet/line
    # tweet = json.loads(line) # load it as Python dict
    # print(json.dumps(tweet, indent=4)) # pretty-print

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens
 
with open('python.json', 'r') as f:
    for line in f:
        try:
            tweet = json.loads(line)
            tokens = preprocess(tweet['text'])
            print(tokens)
        except:
            print("\n")

fname = 'python.json'
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        try:
            tweet = json.loads(line)
        except:
            print()
        # Create a list with all the terms
        terms_all = [term for term in preprocess(tweet['text'])]
        # Update the counter
        count_all.update(terms_all)
    # Print the first 5 most frequent words
    print(count_all.most_common(5))

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']
terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]

# Count terms only once, equivalent to Document Frequency
terms_single = set(terms_all)
# Count hashtags only
terms_hash = [term for term in preprocess(tweet['text']) 
              if term.startswith('#')]
# Count terms only (no hashtags, no mentions)
terms_only = [term for term in preprocess(tweet['text']) 
              if term not in stop and
              not term.startswith(('#', '@'))] 
              # mind the ((double brackets))
              # startswith() takes a tuple (not a list) if 
              # we pass a list of inputs

terms_bigram = bigrams(terms_stop)

com = defaultdict(lambda : defaultdict(int))
 
# f is the file pointer to the JSON data set

with open(fname, 'r') as f:
    for line in f: 
        try:
            tweet = json.loads(line)
        except:
            print()
        terms_only = [term for term in preprocess(tweet['text']) 
                    if term not in stop 
                    and not term.startswith(('#', '@'))]
 
        # Build co-occurrence matrix
        for i in range(len(terms_only)-1):            
            for j in range(i+1, len(terms_only)):
                w1, w2 = sorted([terms_only[i], terms_only[j]])                
                if w1 != w2:
                    com[w1][w2] += 1

com_max = []
# For each term, look for the most common co-occurrent terms
with open(fname, 'r') as f:
    for t1 in com:
        t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
        for t2, t2_count in t1_max_terms:
            com_max.append(((t1, t2), t2_count))
# Get the most frequent co-occurrences
    terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
    print(terms_max[:5])

search_word = sys.argv[1] # pass a term as a command-line argument
count_search = Counter()

with open(fname, 'r') as f:
    for line in f:
        try:
            tweet = json.loads(line)
        except:
            print()
        terms_only = [term for term in preprocess(tweet['text']) 
                    if term not in stop 
                    and not term.startswith(('#', '@'))]
        if search_word in terms_only:
            count_search.update(terms_only)
    print("Co-occurrence for %s:" % search_word)
    print(count_search.most_common(20))

word_freq = count_terms_only.most_common(20)
labels, freq = zip(*word_freq)
data = {'data': freq, 'x': labels}
bar = vincent.Bar(data, iter_idx='x')
bar.to_json('term_freq.json')