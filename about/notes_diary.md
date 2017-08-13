## ONGOING PROJECT DIARY
+ 2017-06-22:  
  + Built a script to catalog all links on a webpage into a csv file. This may be used to generate content from, ie, a wikipedia page: allowing quick access to referenced sites & articles etc. Also contains all image srcs.
---
+ 2017-06-23:
  + Read the Gmail API terms of service: all seems fine, project seems legit; exception: 5e1-"Prohibitions on Content":"Scrape, build databases, or otherwise create permanent copies of such content, or keep cached copies longer than permitted by the cache header" may be problematic? 
    [LINK](https://console.developers.google.com/tos?id=universal)  
  + If gmail used, a plus would be the level of invasion: folks may feel shocked that the work would use their email; also, could use mailing lists and spam subscriptions to get a quick insight into user interests.
---
+ 2017-07-03:  
  + Lots of debate about the ethical/practical implications of my project. Can't help but see this as further proof this is a ripe topic.  
  + Created 8Q survey: results interesting, especially after posting to the forum.  
  + I should be sure to include a link to the place where you revoke access at the same time the email goes out saying "yr zine is ready in the lobby".  
---
+ 2017-07-04:  
  + Successfully accessed the content of my email messages.  
  + Orange also making zines markup project!  
  + Didn't quite translate my gmail emails that got pulled.  
---
+ 2017-07-10:  
  + Initiated Twitter App to scrape tweets to use as training data.  
  + [LINK](https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/)  
  + saved tweets to json with key=username values=tweets  
  + built crawler to maximise tweets for teaching-set  
---
+ 2017-07-28:  
  + Got sentiment analysis to work.  
  + Works by using words surrounding nouns to judge rough opinion of noun > add these together for all instances of noun  
---
+ 2017-08-01:  
  + Planned Zine markdown algorithm.
  + Stores details about all scraped items in JSON and builds from that.
---
+ 2017-08-06:  
  + Proof of concept:  
            - Reading Gmail sent emails - but not all and not enough  
            - Getting nouns from emails - small number of emails reducing the accuracy - need to link semantics  
            - Creating JSON/s from wiki - needs to be more robust!  
---
+ 2017-08-07:  
  + Getting a lot more sent emails (160 / 1300)  
  + Sentiment Analysis is not working - super inaccurate - fuck.  
---
+ 2017-08-08:  
  + Charlotte kindly showed me how to setup a Node.js server environment. 
  + Began writing JS to format scraped content into a visual form.  
    - At this stage, this just consists of a list of images and text. Still interesting.  
---
+ 2017-08-09:  
  + Sharped up decision tree for JS  
---
+ 2017-08-10:  
  + Improved JSON retention of scraped information.  
---
+ 2017-08-12:  
  + Implemented what I hope is the correct approach for Gmail OAuth2  
    - Unable to check as I think I need the frontend. Not sure.  
  + Research better methodologies for analysing emails. Will implement later in the week.  
    - Would be great thematically if I could find a dump of leaked emails to use as training data.  
---
+ 2017-08-13:  
  + Researched and implemented Django python server. AMAZING.  
  + Made citation_json.py script run just using a url as an input.  
  + Reorganised project folders in light of this breakthrough.  
---