#PY3#HPM#
# Master file for Rrosetta programme.

#=========================

import sys

import citation_json
import get_sentiment
import img_anal
import sent_mail
import text_sum
import txt_anal

#=========================


def run(_auth_code, _language='english', DEBUG=False):
    """
    Takes OAuth2 code, (String, Bool)
    Saves JSON file
    """
    sent_mail = set()
    if DEBUG:
        sent_mail = sent_mail.debug()
    else:
        sent_mail = sent_mail.main(_auth_code)
    print("sent: ", len(sent_mail))

    # perform recursive summerisation to find single sentence.
    sentence = [text_sum.main(sent_mail, _lang=_language)]
    print(sentence)

    # perform NLTK analysis to find noun
    noun_dict = get_sentiment.main(sentence)
    noun_list = []
    noun_list.append([nouns for sentiment in noun_dict for counter in noun_dict[sentiment]
                      for nouns in noun_dict[sentiment][counter] if counter >= 0 and nouns.isalpha()])
    print(noun_list)

    # perform citation scraping
    for nouns in noun_list:
        for noun in nouns:
            if noun.isalpha():
                citation_json.main(noun, "./citation_jsons/")

    print("done")
#-------------------------


#=========================
if __name__ == "__main__":
    import sys
    run(sys.argv[1])
