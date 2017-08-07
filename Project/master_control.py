import get_sentiment
import gmailsentfolder
import citation_json

sent_mail = set(gmailsentfolder.main())
print("sent: ", len(sent_mail))
noun_dict = get_sentiment.main(sent_mail)
noun_list = []
noun_list.append([nouns for sentiment in noun_dict for counter in noun_dict[sentiment] for nouns in noun_dict[sentiment][counter] if counter >= 5 and nouns.isalpha()])
print(noun_list)
for nouns in noun_list:
    for noun in nouns:
        if noun.isalpha():
            citation_json.main(noun, "./citation_jsons/")