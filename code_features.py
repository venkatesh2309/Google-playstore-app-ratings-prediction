import json

Category={'VIDEO_PLAYERS': 0,
 'BOOKS_AND_REFERENCE': 1,
 'DATING': 2,
 'TRAVEL_AND_LOCAL': 3,
 'SHOPPING': 4,
 'NEWS_AND_MAGAZINES': 5,
 'SOCIAL': 6,
 'PHOTOGRAPHY': 7,
 'HEALTH_AND_FITNESS': 8,
 'FINANCE': 9,
 'LIFESTYLE': 10,
 'SPORTS': 11,
 'COMMUNICATION': 12,
 'PERSONALIZATION': 13,
 'PRODUCTIVITY': 14,
 'BUSINESS': 15,
 'MEDICAL': 16,
 'TOOLS': 17,
 'GAME': 18,
 'Others': 19,
 'FAMILY': 20}
Type={'Paid': 0, 'Free': 1}
CRating={'Everyone 10+': 0, 'Adults': 1, 'Teen': 2, 'Everyone': 3}
LUpdated_year={'2010': 0,'2011': 1,'2012': 2,'2013': 3,'2014': 4,'2015': 5,'2016': 6,'2017': 7,'2018': 8}
Ins_Label={'Morethan 10Million': 3,'Morethan 1Million - 10Million': 2,'Zero - Thousand': 0,'Morethan Thousand - 1Million': 1}
Price_L={'101$ or above': 0, '1$ to 100$': 1, 'Free': 2}
Size_L={'0 to 1MB': 0,'Varies to device': 1,'1 to 10MB': 2,'More then 10MB': 3}


Json_obj={"Category_L": Category,
          "Type": Type,
          "ContentRating": CRating,
          "LastUpdated_year":LUpdated_year,
          "Install_Labels": Ins_Label,
          "Price_Label": Price_L,
          "Size_Label": Size_L
          }

    
## Dump json
with open('factors_codes.json','w') as file:
    json.dump(Json_obj,file)
    
## for reading the dunped file 
with open('factors_codes.json') as file:
    factors_codes=json.load(file)

