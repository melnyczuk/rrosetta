import get_sentiment
import gmail_sent_folder
import citation_json
import txt_anal
import img_anal

sent_mail = set(gmail_sent_folder.main())
print("sent: ", len(sent_mail))
noun_dict = get_sentiment.main(sent_mail)
noun_list = []
noun_list.append([nouns for sentiment in noun_dict for counter in noun_dict[sentiment] for nouns in noun_dict[sentiment][counter] if counter >= 5 and nouns.isalpha()])
print(noun_list)
for nouns in noun_list:
    for noun in nouns:
        if noun.isalpha():
            citation_json.main(noun, "./citation_jsons/")
            img_anal.analyse(noun)
            txt_anal.analyse(noun)