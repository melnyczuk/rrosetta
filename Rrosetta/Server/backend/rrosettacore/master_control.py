import sys
from . import get_sentiment
from . import gmail_sent_folder
from . import text_sum
from . import citation_json as cj
from . import txt_anal
from . import img_anal

def run(_language='english', DEBUG=False):
    auth_code = ''
    sent_mail = set()
    if DEBUG:
        sent_mail = set(gmail_sent_folder.debug())
    else:
        sent_mail = set(gmail_sent_folder.main(auth_code))

    print("sent: ", len(sent_mail))

    full_corp = ''
    for mail in sent_mail:
        full_corp += str(mail).join(' ')

    print(len(full_corp))

    sentence = [text_sum.main(full_corp, _language=_language)]
    print(sentence)

    noun_dict = []# get_sentiment.main(sentence)
    noun_list = []
    noun_list.append([nouns for sentiment in noun_dict for counter in noun_dict[sentiment]
                    for nouns in noun_dict[sentiment][counter] if counter >= 5 and nouns.isalpha()])
    print(noun_list)
    for nouns in noun_list:
        for noun in nouns:
            if noun.isalpha():
                cj.main(noun, "./citation_jsons/")
                img_anal.analyse(noun)
                txt_anal.analyse(noun)
    print("done")