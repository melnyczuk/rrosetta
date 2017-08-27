## ONGOING PROJECT DIARY
---
+ 2017-06-22:  
  + Built a script to catalog all links on a webpage into a csv file. This may be used to generate content from, ie, a wikipedia page: allowing quick access to referenced sites & articles etc. Also contains all image srcs.
---
+ 2017-06-23:
  + Read the Gmail API terms of service: all seems fine, project seems legit; exception: 5e1-"Prohibitions on Content":"Scrape, build databases, or otherwise create permanent copies of such content, or keep cached copies longer than permitted by the cache header" may be problematic? 
    [link](https://console.developers.google.com/tos?id=universal)  
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
  + Initiated Twitter App to scrape tweets to use as training data.  [link](https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/)  
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
    + [This youtube playlist was great.](https://www.youtube.com/playlist?list=PL6gx4Cwl9DGBlmzzFcLgDhKTTfNLfX1IK) 
  + Made citation_json.py script run just using a url as an input.  
  + Reorganised project folders in light of this breakthrough.  
  + Bought [Rrosetta.uk](http://Rrosetta.uk) to host site.
  + Download the Podesta emails from Wikileaks dump. Can use for training?
---
+ 2017-08-14:
  + Hit major hurdle: OAuth2 is not making any sense.
---
+ 2017-08-15:
  + Still no luck
  + May have to switch to Twitter data, which will suck!
  + Zero help from the department.
---
+ 2017-08-17:
  + Skyped with Fabio Natali from CCS and he talked me through using Django to make OAuth2 work! GLORIOUS VICTORY.
  + Implementing recursive Text Sumarisation using Sumy module.
    + This returns a sentence rather than a single word. Will use NLTK to pull out object noun.
---
+ 2017-08-18:
  + Found the perfect chair!
  + Ran programme on my emails and returned a very personal sentence. It works!
  + Tested on my mum's emails.
---
+ 2017-08-21:
  + Trying to get the object noun out of the sentence with NLTK is very inaccurate. 
  + So decided to swap out wikipedia for google searching instead.
    + Found the PWS module, which does a great job or formulating the Google search.
    + Carefully cut out Google tracking bits from url as these kept recognising I'm a bot and blocking me.
  + Results are a lot better, returned a page of Charlotte's Tumblr themes from a search of her sentence.
---
+ 2017-08-22:
  + Tightening up search, bit hit and miss.
  + Decided to start search four sentences rather than one to make it more robust. Works a lot better.
  + PWS decided to break, so I had to go into the module code and fix it myself. Saved my working patch as the googl module.
---
+ 2017-08-23:
  + Decided not to use JS to layout and export PDFs.
  + Instead I am going to use Reportlab for python, which looks like a great module.
    + [Watched this video.](https://www.youtube.com/watch?v=Ei0fL6j8DtI)
---
+ 2017-08-24:
  + Strengthened image analysis, adding PIL functionality to record dimensions and filetype and colour mode of images.
    + Now removes images that aren't actually there, and 1x1 pixel images that are used to track clicks for advertisers.
    + Added a flag in the image is square: probably a thumnail or logo.
    + Added a flag that assumes the image is a photo if it is bigger than certain dimensions.
---
+ 2017-08-25:
  + Strengthened JSON creation
    + Now passes the user email, the sentences used in Google search, and the list of urls that were scraped - this will form the credits page of the zine.
---
+ 2017-08-26:
  + Successfully ran programme all the way to saving the first page of pdf!
  + Thought about ML implementations:
    + To sort pulled text, and remove header/footer/junk content
    + To determine photos correctly.
  + Tried on James' emails from work Gmail - failed:
    + All sent emails have attachments (signature logo), so are 'multipart'
    + Should implement a check for multipart emails by seeing if body.size == 0
---
+ 2017-08-27:
  + Drastically improved email pulls:
    + Works with attachment emails
    + Correctly decodes everything.
  + Got super accurate results on my own emails.
  + Todo: 
    1.. make pdfmaker into class
    2.. make pdf page borders
    3.. make credit spread
    4.. do other spreads
---