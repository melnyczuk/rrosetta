import sys
import gmail_sent_folder, get_sentiment, text_sum, citation_json, txt_anal, img_anal


def authorise():
    from oauth2client import client
    flow = client.flow_from_clientsecrets()
    auth_uri = flow.step1_get_authorize_url()

def run(_auth_code, _language='english', DEBUG=False):
    sent_mail = set()
    if DEBUG:
        sent_mail = set(gmail_sent_folder.debug())
    else:
        sent_mail = set(gmail_sent_folder.main(_auth_code))

    print("sent: ", len(sent_mail))

    full_corp = ''
    for mail in sent_mail:
        full_corp += str(mail).join(' ')

    print(len(full_corp))

    sentence = [text_sum.main(full_corp, _lang=_language)]
    print(sentence)

    noun_dict = []# get_sentiment.main(sentence)
    noun_list = []
    noun_list.append([nouns for sentiment in noun_dict for counter in noun_dict[sentiment]
                    for nouns in noun_dict[sentiment][counter] if counter >= 5 and nouns.isalpha()])
    print(noun_list)
    for nouns in noun_list:
        for noun in nouns:
            if noun.isalpha():
                citation_json.main(noun, "./citation_jsons/")
                img_anal.analyse(noun)
                txt_anal.analyse(noun)
    print("done")

if __name__ == "__main__":
    import sys
    run('hi')