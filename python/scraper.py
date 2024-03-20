# scraper file

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os

# years = ['2017', '2018', '2019', '2020']
# years = ['2014', '2015', '2016']
years = ['2010', '2011', '2012', '2013']

wiki = "https://en.wikipedia.org"
dirname = os.path.dirname(__file__)

def scrapeDraft(aYear):

    # connecting to web page
    pageLink = "https://en.wikipedia.org/wiki/" + aYear + "_NFL_Draft"
    draft_df = pd.DataFrame(columns=['Round', 'Pick_No', 'Team', 'Player', 'Player_Link', 'Pos', 'College', 'Conf'])
    page = requests.get(pageLink, headers={'User-Agent': 'Mozilla/5.0'})
    content = BeautifulSoup(page.content, "html.parser")

    # get the table
    tables = content.find_all('table')
    my_table = tables[0]
    for table in tables:
        if "Rnd." in table.text:
            my_table = table
            break
    table_body = my_table.find('tbody')
    rows = table_body.find_all('tr')[1:]

    # testFile = open('results/test.txt', "w+")
    # for row in rows:
    #     testFile.write(row.prettify())
    # testFile.close()
 
    # iterate through table rows and add data to dataframe
    for row in rows:
        ths = row.find_all('th')
        tds = row.find_all('td')
        if len(ths) > 1:
            As = ths[1].find_all('a')
            if(len(As) > 0):
                draft_df.loc[len(draft_df)] = [cleanNum(ths[0].text), As[0].string, cleanString(tds[1].text), cleanString(tds[2].text), wiki + tds[2].find('a', href=True)['href'] + ' ', cleanString(tds[3].text), cleanString(tds[4].text), cleanString(tds[5].text)]
            else:
                if len(tds[2].find_all('a')) > 0:
                    draft_df.loc[len(draft_df)] = [cleanNum(ths[0].text), ths[1].find_all('b')[0].string, cleanString(tds[1].text), cleanString(tds[2].text), wiki + tds[2].find('a', href=True)['href'] + ' ', cleanString(tds[3].text), cleanString(tds[4].text), cleanString(tds[5].text)]
                else:
                    tds[2].find('span').replace_with('')
                    draft_df.loc[len(draft_df)] = [cleanNum(ths[0].text), ths[1].find_all('b')[0].string, cleanString(tds[1].text), cleanString(tds[2].text), '', cleanString(tds[3].text), cleanString(tds[4].text), cleanString(tds[5].text)]
        else:
            if(len(tds) >= 7):
                Bs = row.find_all('b')
                if len(tds[3].find_all('a')) > 0:
                    draft_df.loc[len(draft_df)] = [cleanNum(Bs[0].string), Bs[1].string, cleanString(tds[2].text), cleanString(tds[3].text), wiki + tds[3].find('a', href=True)['href'] + ' ', cleanString(tds[4].text), cleanString(tds[5].text), cleanString(tds[6].text)]
                else:
                    tds[3].find('span').replace_with('')
                    draft_df.loc[len(draft_df)] = [cleanNum(Bs[0].string), Bs[1].string, cleanString(tds[2].text), cleanString(tds[3].text), '', cleanString(tds[4].text), cleanString(tds[5].text), cleanString(tds[6].text)]

    # unique ids
    draft_df['ID'] = aYear + draft_df['Pick_No'].apply(makeID)

    # save current dataframe to file
    if not os.path.exists(dirname + "/results/" + aYear):
        os.makedirs(dirname + "/results/" + aYear) 
    draft_df.to_csv("results/" + aYear + "/draftdf_" + aYear + ".csv", index=False)

    return draft_df

def scrapePlayers(a_df, aYear):

    player_df = pd.DataFrame(columns=['Player', 'ID', 'MVP', 'SB_MVP', 'SB_WIN', 'OPOY', 'DPOY', 'OROY', 'DROY', 'First_AP', 'Second_AP', 'Pro_Bowl'])

    # iterate back through dataframe and get player info from player links
    for index, row in a_df.iterrows():

        playerName = row['Player']
        playerID = row['ID']
        mvp = 0
        sb_mvp = 0
        sb_winner = 0
        opoy = 0
        dpoy = 0
        oroy = 0
        droy = 0
        first_ap = 0
        second_ap = 0
        pro_bowl = 0

        if row['Player_Link'] != '':

            # connect to player web page
            curLink = row['Player_Link']
            curPage = requests.get(curLink, headers={'User-Agent': 'Mozilla/5.0'})
            curContent = BeautifulSoup(curPage.content, "html.parser")
            tbody = curContent.find('tbody')

            trs = tbody.find_all('tr')
            ix = -1

            for i in range(len(trs)):
                tr = trs[i]
                ths = tr.find_all(string=re.compile(".*Career highlights and awards.*"))
                if(len(ths) > 0):
                    ix = i+1
                    break

            if(ix > -1):
                career_tr = trs[ix]
                lis = career_tr.find_all('li')
                for li in lis:
                    award = li.text

                    if "NFL Most Valuable Player" in award:
                        tot = cleanCount(award[:3])
                        if not tot == "":
                            mvp = mvp + int(tot)
                        else:
                            mvp = mvp + 1

                    elif "Super Bowl MVP" in award:
                        tot = cleanCount(award[:3])
                        if not tot == "":
                            sb_mvp = sb_mvp + int(tot)
                        else:
                            sb_mvp = sb_mvp + 1
                    
                    elif "Super Bowl champion" in award:
                        tot = cleanCount(award[:3])
                        if not tot == "":
                            sb_winner = sb_winner + int(tot)
                        else:
                            sb_winner = sb_winner + 1

                    elif "NFL Offensive Player of the Year" in award:
                        tot = cleanCount(award[:3])
                        if not tot == "":
                            opoy = opoy + int(tot)
                        else:
                            opoy = opoy + 1

                    elif "NFL Defensive Player of the Year" in award:
                        tot = cleanCount(award[:3])
                        if not tot == "":
                            dpoy = dpoy + int(tot)
                        else:
                            dpoy = dpoy + 1

                    elif "NFL Offensive Rookie of the Year" in award:
                        tot = cleanCount(award[:3])
                        if not tot == "":
                            oroy = oroy + int(tot)
                        else:
                            oroy = oroy + 1

                    elif "NFL Defensive Rookie of the Year" in award:
                        tot = cleanCount(award[:3])
                        if not tot == "":
                            droy = droy + int(tot)
                        else:
                            droy = droy + 1

                    elif "First-team All-Pro" in award:
                        tot = cleanCount(award[:3])
                        if not tot == "":
                            first_ap = first_ap + int(tot)
                        else:
                            first_ap = first_ap + 1

                    elif "Second-team All-Pro" in award:
                        tot = cleanCount(award[:3])
                        if not tot == "":
                            second_ap = second_ap + int(tot)
                        else:
                            second_ap = second_ap + 1

                    elif "Pro Bowl" in award:
                        tot = cleanCount(award[:3])
                        if not tot == "":
                            pro_bowl = pro_bowl + int(tot)
                        else:
                            pro_bowl = pro_bowl + 1

        # end of if with player connection

        player_df.loc[len(player_df)] = [playerName, playerID, mvp, sb_mvp, sb_winner, opoy, dpoy, oroy, droy, first_ap, second_ap, pro_bowl]


    player_df.to_csv("results/" + aYear + "/playerdf_" + aYear + ".csv", index=False)
    return player_df

    # testFile = open('results/test.txt', "w+", encoding="utf-8")
    # testFile.write(tbody.prettify())
    # testFile.close()
    # break


def makeID(aPick):
    pick_str = aPick.zfill(3)
    return pick_str

def cleanNum(aString):
    return ''.join(s for s in aString if s.isalnum())

def cleanCount(aString):
    return ''.join(s for s in aString if s.isnumeric())

def cleanString(aString):
    return ''.join(s for s in aString if (s.isalnum() or s == ' '))

for y in years:
    cur_df = scrapeDraft(y)
    scrapePlayers(cur_df, y)

