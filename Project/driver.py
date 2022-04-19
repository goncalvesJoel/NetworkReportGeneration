# ===== ===== ===== ===== import extra
import os
from re import A
import weasyprint
import json
from jinja2 import Environment, FileSystemLoader
from datetime import date, timedelta
from calendar import monthrange
import math

# ===== ===== ===== ===== import translator ===== 
from i18n import resource_loader
from i18n.translator import t
from i18n import translations
from i18n import config

# ===== ===== ===== ===== import graph =====
#from runPlotly.line_chart_during_month import *
import generateGraphics.lineGraphics as line
import generateGraphics.pieGraphics as pie
import generateGraphics.mapGraphics as maps


# ===== ===== ===== ===== folder path =====
# == ROOT = '/home/user/Desktop/weasyprintTest/'

ROOT =os.getcwd()+'/networkReportGeneration/'
ASSETS_DIR = os.path.join(ROOT, 'assets')

TEMPLAT_SRC = os.path.join(ROOT, 'templates')
CSS_SRC = os.path.join(ROOT, 'static/css')
DEST_DIR = os.path.join(ROOT, 'output')

TEMPLATE = 'templatecopy.html'
CSS = 'style.css'
OUTPUT_FILENAME = 'my-report4.pdf'

# === graphic colors
yellow = "rgb(252, 194, 25)"
grey ="rgb(134, 137, 140)"
lightGray = "rgb(173, 175, 179)"
lighterGray="rgb(214, 216, 217)"

#=== abbreviation for thousand OR million
thousandORmillion = ""

def writeTemplate(namefile,htmlContent):
    file=open(ROOT+"templates/"+namefile,'w+',encoding='utf-8')
    file.write(htmlContent)
    file.close()

def thousandORmillions(value):
    if value in range(1000, 999999):
        return str(value // 1000 % 1000)+"/thousand"
    elif value > 999999:
        return str( math.trunc(value // 1000000))+"/millions"
    return str(value)+"/ "

def splitString(typeString):
    return typeString.split("/")
       

# ===== ===== ===== ===== generate PDF =====
def translateReport(langCode):
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'translations')
    resource_loader.init_loaders()
    #reload(config)
    config.set('load_path', [filename])
    config.set('filename_format', '{locale}.{format}')
    config.set('file_format', 'json')
    config.set('locale', langCode)
    config.set('skip_locale_root_data', True)
    data = t('STATISTI')


# ===== ===== ===== ===== translations PDF =====
def startGeneratePDF(json_data_report):
    
    print('start generate report...')
    env = Environment(loader=FileSystemLoader(TEMPLAT_SRC))
    template = env.get_template(TEMPLATE)
    css = os.path.join(CSS_SRC, CSS)
    
    #===== json data teste
    #print(json_data_report["total_stats"]["languages"]["PT"])

    langCode=json_data_report["language"]
 
    #===== translate report
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'translations')
    resource_loader.init_loaders()
    #reload(config)
    config.set('load_path', [filename])
    config.set('filename_format', '{locale}.{format}')
    config.set('file_format', 'json')
    config.set('locale', langCode)
    config.set('skip_locale_root_data', True)
    #data = t('STATISTI')

    arrayColorsPie=["rgb(214, 216, 217)","rgb(173, 175, 179)","rgb(134, 137, 140)","rgb(252, 194, 25)"]
    arrayGreys=['cor-grey1','cor-grey2','cor-grey3','cor-yellow']

    #== Values (user_actions, photos_gifs_sent, number_views)
    #==== know if it's a thousand or a million

    total_stats_user_actions = thousandORmillions(json_data_report["total_stats"]["user_actions"])
    total_stats_photos_gifs_sent = thousandORmillions(json_data_report["total_stats"]["photos_gifs_sent"])
    total_stats_number_views = thousandORmillions(json_data_report["total_stats"]["number_views"])
    
    #==== separate the value and thousand or million
    separate_total_stats_user_actions = splitString(total_stats_user_actions)
    if separate_total_stats_user_actions[1] == "thousand":
        unity_user_actions = t('REPORT_Thousand')
    elif separate_total_stats_user_actions[1] == "millions":
        unity_user_actions = t('REPORT_Million')
    else:
         unity_user_actions = ""
    
    separate_total_stats_photos_gifs_sent=splitString(total_stats_photos_gifs_sent)
    if separate_total_stats_photos_gifs_sent[1] == "thousand":
        unity_photos_gifs_sent = t('REPORT_Thousand')
    elif separate_total_stats_photos_gifs_sent[1]  == "millions":
        unity_photos_gifs_sent = t('REPORT_Million')
    else:
        unity_photos_gifs_sent = ""
        
    
    separate_total_stats_number_views=splitString(total_stats_number_views)
    if separate_total_stats_number_views[1] == "thousand":
        unity_number_views = t('REPORT_Thousand')
    elif separate_total_stats_number_views[1] == "millions":
        unity_number_views = t('REPORT_Million')
    else:
        unity_number_views = ""



    #==pie chart features
    #====Modules
     # Events: , Transports: ,  Search: ,  News: ,
        
    ValueAuxModules=[{"icon": "", "text": t('REPORT_NEWS'), "value":json_data_report["modules"]["news"]["percent"]}, 
                     {"icon": "", "text": t('REPORT_EVENTS'), "value":json_data_report["modules"]["events"]["percent"]}, 
                     {"icon": "", "text": t('REPORT_SEARCH'), "value":json_data_report["modules"]["search"]["percent"]}, 
                     {"icon": "", "text": t('REPORT_TRANSPORTS'), "value":json_data_report["modules"]["transport"]["percent"]}]
    
    ValueAuxModules.sort(key=lambda x: x["value"], reverse=True)

    ValueModules=[]
    lblValueModules=[]
    TextModules=[]
    for i in range(len(ValueAuxModules)):
        ValueModules.append(ValueAuxModules[i]["value"])
        lblValueModules.append(ValueAuxModules[i]["icon"])
        TextModules.append(ValueAuxModules[i]["text"])


    
    TextModulesColorGraphic=['']*len(ValueModules)
    TextModulesColor=['']*len(ValueModules)
    TextModulesBold =['']*len(ValueModules)

    #ValueModules.sort(reverse=True)

    biggestModules = ValueModules.index(max(ValueModules))
    smallerModules = ValueModules.index(min(ValueModules))

    TextModulesBold [biggestModules] = "text_bold"

    TextModulesColor[biggestModules] = arrayGreys[3]
    TextModulesColor[smallerModules] = arrayGreys[0]
    TextModulesColorGraphic[biggestModules] = arrayColorsPie[3]
    TextModulesColorGraphic[smallerModules] = arrayColorsPie[0]
 
    indexColors = 1
    for i in range(0,len(TextModulesColor)):
        if TextModulesColor[i] == '':
            TextModulesColorGraphic[i] = arrayColorsPie[indexColors]
            TextModulesColor[i] = arrayGreys[indexColors]
            indexColors +=1
    
     

    #====Actions
    ValueActions=[]# order -> 50,10,30,10
    LangActions=[]
    
    indexArrayValue = 0
    for key, value in json_data_report["total_stats"]["languages"].items():
        if indexArrayValue <=3:
            ValueActions.append(value)
            LangActions.append(key)
        indexArrayValue +=1
        

    ValueActions.sort(reverse=True)
        
    
    TextActionsColorGraphic=['']*len(ValueActions)
    TextActionsColor=['']*len(ValueActions)
    TextActionsBold=['']*len(ValueActions)

    biggestActions = ValueActions.index(max(ValueActions))
    smallerActions = ValueActions.index(min(ValueActions))

    TextActionsBold[biggestActions] = "text_bold"

    if biggestActions == smallerActions:
        if len(ValueActions)>1:
           smallerActions=len(ValueActions)-1


    TextActionsColor[smallerActions] = arrayGreys[0]
    TextActionsColorGraphic[smallerActions] = arrayColorsPie[0]
    TextActionsColor[biggestActions] = arrayGreys[3]
    TextActionsColorGraphic[biggestActions] = arrayColorsPie[3]

    indexColors = 1
    for i in range(len(TextActionsColor)):
        if TextActionsColor[i] == '':
            TextActionsColorGraphic[i] = arrayColorsPie[indexColors]
            TextActionsColor[i] = arrayGreys[indexColors]
            indexColors +=1


    #==Table Categories
    new_categories = json_data_report["modules"]["news"]["top_categories"]
    events_categories =  json_data_report["modules"]["events"]["top_categories"]
    search_categories = json_data_report["modules"]["search"]["top_categories"]
    transport_categories = json_data_report["modules"]["transport"]["top_categories"]

    #itemsTable = list(zip(new_categories,events_categories,search_categories,transport_categories))
    cssColorTable = ["cor-one","cor-two","cor-tres"]
    itemsTable = []
    for i in range(len(new_categories)):
        itemsTable.append({"color":cssColorTable[i],
                           "columns": [
                               new_categories[i],
                               events_categories[i],
                               search_categories[i], 
                               transport_categories[i]
                           ],
                            })
    

    #==line graph features
    #====two lines with different scales
    #====During
    valuesDuring_X_months = [t('REPORT_MONTH_JAN'),
                            t('REPORT_MONTH_FEB'),
                            t('REPORT_MONTH_MAR'),
                            t('REPORT_MONTH_ABR'),
                            t('REPORT_MONTH_MAY'),
                            t('REPORT_MONTH_JUN'),
                            t('REPORT_MONTH_JUL'),
                            t('REPORT_MONTH_AUG'),
                            t('REPORT_MONTH_SEP'),
                            t('REPORT_MONTH_OCT'),
                            t('REPORT_MONTH_NOV'),
                            t('REPORT_MONTH_DEC'),]


    #====date range
    #start_date, end_date = '01-08-2021','31-08-2021' #12-08-2021','12-09-2021
    start_date = json_data_report["start_date"]
    end_date = json_data_report["end_date"] #' #12-08-2021','12-09-2021
    
    #====split date
    day, month, year = start_date.split('-')
    fullDate = date(int(year), int(month), int(day))
    MonthName = valuesDuring_X_months[(fullDate.month - 1)]  # nome do mes
    #====Monthly
    valuesDuring_Y1 = json_data_report["monthly"]["stats"]["user_actions"]
    valuesDuring_Y2 = json_data_report["monthly"]["stats"]["pedestrians"]
    text_During = json_data_report["monthly"]["description"]
    
    #====Weekly
    valuesWeek_X=[t('REPORT_WEEK_MON'),t('REPORT_WEEK_TUE'),t('REPORT_WEEK_WED'),t('REPORT_WEEK_THU'),t('REPORT_WEEK_FRI'),t('REPORT_WEEK_SAT'),t('REPORT_WEEK_SUN')]
    valuesWeek_Y1 = json_data_report["weekly"]["stats"]["user_actions"]
    valuesWeek_Y2 = json_data_report["weekly"]["stats"]["pedestrians"]
    text_Week = json_data_report["weekly"]["description"]
    
    #====Daily
    valuesDaily_X = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18','19','20', '21', '22', '23']
    valuesDaily_Y1 = json_data_report["daily"]["stats"]["user_actions"]
    valuesDaily_Y2 = json_data_report["daily"]["stats"]["pedestrians"]
    text_Daily = json_data_report["daily"]["description"]
    
    #== heatMap text
    heatMap_title = "DATA ANALISYS"
    heatMap_description = json_data_report["heatmap"]["description"]
    heatMap_comments = "User Actions*: Values indicate the number of touches made on TOMI. Content Display*: Values show the number of each content exhibited on lists, selections and search. Pedestrians*: This data is completely anonymous and privacy is respected."

    #====Execution of the construction of the graphics
    pie.modules(ASSETS_DIR, ValueModules, lblValueModules, TextModulesColorGraphic)
    pie.actions(ASSETS_DIR, ValueActions, TextActionsColorGraphic, t('REPORT_ACTIONS_BY_TOURIST_AND_LOCALS'))
    line.duringMonth(ASSETS_DIR, start_date, end_date,valuesDuring_X_months,valuesDuring_Y1,valuesDuring_Y2) #'06-08-2021','06-09-2021'
    line.weeklyTrend(ASSETS_DIR, valuesWeek_X,valuesWeek_Y1,valuesWeek_Y2)
    line.dailyTrend(ASSETS_DIR, valuesDaily_X, valuesDaily_Y1,valuesDaily_Y2)
    #maps.heatMap()

     

    #===== variables links
    template_vars = {
        #===== banner images
        'LINK_BANNER1': json_data_report["first_banner"]["img_banner1"],
        'LINK_BANNER2': json_data_report["second_banner"]["img_banner2"],

        #===== values_dates
        'DATES1': start_date,
        'DATES2': end_date,
        'MONTH_NAME': MonthName,
        'CITY': json_data_report["city"],
         
         #===== links
        'assets_dir': "file://" + ASSETS_DIR,

        #===== texts
        #== page header text
        'HEADER_TITLE_ONE':  json_data_report["header_title_one"],#"NEWS & DATE",
        'HEADER_TITLE_TWO': json_data_report["header_title"],#"COVID-19 PREVENTION",

         #== first_banner text
        'FIRST_BANNER_TITLE': json_data_report["first_banner"]["title"],#"New feature to detect mask usage"
        'FIRST_BANNER_CONTENT': json_data_report["first_banner"]["content"],

       
        #== second_banner text
        'SECOND_BANNER': json_data_report["second_banner"]["content"],

        'TEXT_DURING': text_During,
        'TEXT_WEEK': text_Week,
        'TEXT_DAILY': text_Daily,

        'HEATMAP_TITLE': heatMap_title,
        'HEATMAP_DESCRIPTION': heatMap_description,
        'HEATMAP_COMMENTS': heatMap_comments,
        
        'PODIUM_ACTIONS_LOCATION': json_data_report["podium"]["actions"]["location"],
        'PODIUM_ACTIONS_VALUE': json_data_report["podium"]["actions"]["number"],
        'PODIUM_SELFIES_LOCATION': json_data_report["podium"]["selfies"]["location"],
        'PODIUM_SELFIES_VALUE': json_data_report["podium"]["selfies"]["number"],

        #=====items Table
        'ITEMS_TABLE': itemsTable,
       
        #===== IMGs tomi smart media
        'SMART_SIZE':len(json_data_report["final_banner"]["img_media"]),
        'SMART_IMGS': json_data_report["final_banner"]["img_media"],
        'SMART_MEDIA_TITLE': json_data_report["final_banner"]["title"],
        'SMART_DESCRIPTION': json_data_report["final_banner"]["content"],
        
        #==== total_stats 
        'unity_user_actions':unity_user_actions,
        'unity_photos_gifs_sent':unity_photos_gifs_sent,
        'unity_number_views':unity_number_views,
        
        #== values_total_stats 
        'value_user_actions':separate_total_stats_user_actions[0],
        'value_photos_gifs_sent':separate_total_stats_photos_gifs_sent[0],
        'value_number_views':separate_total_stats_number_views[0],
                
        #===== values_MODULES
        'MODULES_VALUE': ValueModules,
        'MODULES_WORD': TextModules,
        'MODULES_TEXT_COLOR': TextModulesColor,
        'MODULES_TEXT_BOLD': TextModulesBold,
        'SIZE_MODULES': len(ValueModules),

        #===== values_Actions
        'ACTIONS_VALUE': ValueActions,
        'ACTIONS_LANG': LangActions,
        'ACTIONS_TEXT_COLOR': TextActionsColor,
        'ACTIONS_TEXT_BOLD': TextActionsBold,
        'SIZE_ACTIONS': len(ValueActions),

       
        #===== translations
        'REPORT_USER': t('REPORT_USER'),
        'REPORT_ACTIONS': t('REPORT_ACTIONS'),
        'REPORT_PHOTOGIFs': t('REPORT_PHOTOGIFs'),
        'REPORT_SENT': t('REPORT_SENT'),
        'REPORT_CONTENT': t('REPORT_CONTENT'),
        'REPORT_DISPLAY': t('REPORT_DISPLAY'),
        #'REPORT_Thousand': t('REPORT_Thousand'),
        #'REPORT_Million': t('REPORT_Million'),
        'REPORT_MODULES': t('REPORT_MODULES'),
        'REPORT_NEWS': t('REPORT_NEWS'),
        'REPORT_EVENTS': t('REPORT_EVENTS'),
        'REPORT_SEARCH': t('REPORT_SEARCH'),
        'REPORT_TRANSPORTS': t('REPORT_TRANSPORTS'),
        'REPORT_CHAMPION': t('REPORT_CHAMPION'),
        'REPORT_SELFIE_WINNER': t('REPORT_SELFIE_WINNER'),
        'REPORT_ACTIONS_BY_TOURIST_AND_LOCALS': t('REPORT_ACTIONS_BY_TOURIST_AND_LOCALS'),
        'REPORT_TOP_CONTENT_CATEGORIES': t('REPORT_TOP_CONTENT_CATEGORIES'),
        'REPORT_DURING_THE_MONTH': t('REPORT_DURING_THE_MONTH'),
        'REPORT_WEEKLY_TREND': t('REPORT_WEEKLY_TREND'),
        'REPORT_DAILY_TREND': t('REPORT_DAILY_TREND'),
        'REPORT_THE_PODIUM': t('REPORT_THE_PODIUM'),
        'REPORT_HEATMAP': t('REPORT_HEATMAP'),
        'REPORT_USER_ACTIONS': t('REPORT_USER_ACTIONS'),
        'REPORT_Main_categories_Module': t('REPORT_Main_categories_Module'),
        'REPORT_Monthly_User_Actions_Evolution': t('REPORT_Monthly_User_Actions_Evolution'),
        'REPORT_Weekly_Evolution_User_Actions': t('REPORT_Weekly_Evolution_User_Actions'),
        'REPORT_Average_User_Actions_Count_Week_Day': t('REPORT_Average_User_Actions_Count_Week_Day'),
        'REPORT_TOMI_With_Most_User_Actions': t('REPORT_TOMI_With_Most_User_Actions'),
        'REPORT_PEDESTRIANS': t('REPORT_PEDESTRIANS'),
        'REPORT_Monthly_Pedestrians_Evolution': t('REPORT_Monthly_Pedestrians_Evolution'),
        'REPORT_Weekly_Pedestrian_Evolution': t('REPORT_Weekly_Pedestrian_Evolution'),
        'REPORT_Average_Pedestrians_Count_Week_Day': t('REPORT_Average_Pedestrians_Count_Week_Day'),
        'REPORT_Average_Pedestrians_Counted_TOMI': t('REPORT_Average_Pedestrians_Counted_TOMI'),
        'REPORT_PHOTOS_GIFS_SENT': t('REPORT_PHOTOS_GIFS_SENT'),
        'REPORT_TOMI_With_Most_Selfie_GIFs_Sent': t('REPORT_TOMI_With_Most_Selfie_GIFs_Sent'),
        'REPORT_SUBSCRIBE_NEWSLETTER': t('REPORT_SUBSCRIBE_NEWSLETTER'),
        
    }


    #===== rendering css+html string
    rendered_string = template.render(template_vars)
    writeTemplate("templateGenerate.html",rendered_string)
    html = weasyprint.HTML(string=rendered_string)
    report = os.path.join(DEST_DIR, OUTPUT_FILENAME)
    test = html.render(stylesheets=[css])
    test.pages[0].height = test.pages[0]._page_box.children[0].height
    test.pages[0].width = test.pages[0]._page_box.children[0].width
    test.write_pdf(report)

    #html.write_pdf(report, stylesheets=[css])
    #print('file is generated successfully and under {}', DEST_DIR)
    print('height: ', test.pages[0].height, 'px auto')
    print('width: ', test.pages[0].width, 'px 21cm')

    return template_vars #OUTPUT_FILENAME
  


if __name__ == '__main__':
    startGeneratePDF()
