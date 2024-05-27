import io
import os
import json
import time
import re
import numpy as np
import pickle


# 将不包含 robots.txt 请求资源文件的 ua 进行去重存放在字典中，并返回这个字典
def robot_txt_label(dataset_path, out_robot_feature):
    with open(dataset_path, 'r') as fp:
        content = json.load(fp)
    ua_lable_dict = {}
    for i, line in enumerate(content):
        ip = content[line]['ip']
        resource = content[line]['resource'] if 'resource' in content[line] and '' != content[line]['resource'] else 'CHENRUI'
        useragent = content[line]['useragent'] if 'useragent' in content[line] and '' != content[line]['useragent'] else 'CHENRUI'

        if 'robots.txt' in resource:
            print(f'ip:{ip}, line:{line}, resource:{resource}')
            with open(out_robot_feature, 'a') as f:
                out_features_line = line + '\t' + ip + '\t' + resource + '\t' + useragent + '\t' + 'Bot/Crawler' + '\n'
                f.write(out_features_line)
        else:
            # write_content += line + '\t' + ip + '\t' + resource + '\t' + useragent + '\n'
            ua_lable_dict[useragent] = 0
            # with open(out_feature, 'a') as f:
            #     ua_lable_dict[useragent] = useragent
                # write_feature = line + '\t' + ip + '\t' + resource + '\t' + useragent + '\n'
                # f.write(write_feature)
    return ua_lable_dict
    # with open(out_feature, 'wb') as dump_file:
    #     pickle.dump(ua_lable_dict, dump_file)

re_list = ['bot','^Buck\/[0-9]','spider','crawl','^.?$','[^a]fish','^IDA$','^ruby$','^@ozilla\/\d','^脝脝陆芒潞贸碌脛$','^破解后的$','AddThis','A6-Indexer','ADmantX','alexa','Alexandria(\s|\+)prototype(\s|\+)project','AllenTrack','almaden','appie','API[\+\s]scraper','Arachni','Arachmo','architext','ArchiveTeam','aria2\/\d','arks','^Array$','asterias','atomz','axios\/\d','BDFetch','Betsie','baidu','biglotron','BingPreview','binlar','bjaaland','Blackboard[\+\s]Safeassign','blaiz-bee','bloglines','blogpulse','boitho\.com-dc','bookmark-manager','Brutus\/AET','BUbiNG','bwh3_user_agent','CakePHP','celestial','cfnetwork','checklink','checkprivacy','China\sLocal\sBrowse\s2\.6','Citoid','cloakDetect','coccoc\/1\.0','Code\sSample\sWeb\sClient','ColdFusion','collection@infegy.com','com\.plumanalytics','combine','contentmatch','ContentSmartz','convera','core','Cortana','CoverScout','crusty\/\d','curl\/','cursor','custo','DataCha0s\/2\.0','daum(oa)?','^\%?default\%?$','DeuSu\/','Dispatch\/\d','Docoloc','docomo','Download\+Master','Drupal','DSurf','DTS Agent','EasyBib[\+\s]AutoCite[\+\s]','easydl','EBSCO\sEJS\sContent\sServer','EcoSearch','ELinks\/','EmailSiphon','EmailWolf','Embedly','EThOS\+\(British\+Library\)','facebookexternalhit\/','favorg','Faveeo\/\d','FDM(\s|\+)\d','Feedbin','feedburner','FeedFetcher','feedreader','ferret','Fetch(\s|\+)API(\s|\+)Request','findlinks','findthatfile','^FileDown$','^Filter$','^firefox$','^FOCA','Fulltext','Funnelback','Genieo','GetRight','geturl','GigablastOpenSource','G-i-g-a-b-o-t','GLMSLinkAnalysis','Goldfire(\s|\+)Server','google','Grammarly','GroupHigh\/\d','grub','gulliver','gvfs\/','harvest','heritrix','holmes','htdig','htmlparser','HeadlessChrome','HttpComponents\/1.1','HTTPFetcher','http.?client','httpget','httpx','httrack','ia_archiver','ichiro','iktomi','ilse','Indy Library','^integrity\/\d','internetseer','intute','iSiloX','iskanie','^java\/\d{1,2}.\d','jeeves','Jersey\/\d','jobo','Koha','kyluka','larbin','libcurl','libhttp','libwww','lilina','^LinkAnalyser','link.?check','LinkLint-checkonly','^LinkParser\/','^LinkSaver\/','linkscan','LinkTiger','linkwalker','lipperhey','livejournal\.com','LOCKSS','LongURL.API','ltx71','lwp','lycos[_+]','MaCoCu','mail\.ru','MarcEdit','mediapartners-google','megite','MetaURI[\+\s]API\/\d\.\d','Microsoft(\s|\+)URL(\s|\+)Control','Microsoft Office Existence Discovery','Microsoft Office Protocol Discovery','Microsoft-WebDAV-MiniRedir','mimas','mnogosearch','moget','motor','^Mozilla$','^Mozilla.4\.0$','^Mozilla\/4\.0\+\(compatible;\)$','^Mozilla\/4\.0\+\(compatible;\+ICS\)$','^Mozilla\/4\.5\+\[en]\+\(Win98;\+I\)$','^Mozilla.5\.0$','^Mozilla\/5.0\+\(compatible;\+MSIE\+6\.0;\+Windows\+NT\+5\.0\)$','^Mozilla\/5\.0\+like\+Gecko$','^Mozilla\/5.0(\s|\+)Gecko\/20100115(\s|\+)Firefox\/3.6$','^MSIE','MuscatFerre','myweb','nagios','^NetAnts\/\d','netcraft','netluchs','newspaper\/\d','ng\/2\.','^Ning\/\d','no_user_agent','nomad','nutch','^oaDOI$','ocelli','Offline(\s|\+)Navigator','OgScrper','okhttp','onetszukaj','^Opera\/4$','OurBrowser','panscient','parsijoo','^Pattern\/\d','Pcore-HTTP','pear\.php\.net','perman','PHP\/','pidcheck','pioneer','playmusic\.com','playstarmusic\.com','^Postgenomic(\s|\+)v2','powermarks','proximic','PycURL','python','Qwantify','rambler','ReactorNetty\/\d','Readpaper','redalert','Riddler','robozilla','rss','scan4mail','scientificcommons','scirus','scooter','Scrapy\/\d','ScoutJet','^scrutiny\/\d','SearchBloxIntra','shoutcast','Site24x7','SkypeUriPreview','slurp','sogou','speedy','sqlmap','SrceDAMP','Strider','summify','sunrise','Sysomos','T\-H\-U\-N\-D\-E\-R\-S\-T\-O\-N\-E','tailrank','Teleport(\s|\+)Pro','Teoma','The[\+\s]Knowledge[\+\s]AI','titan','^Traackr\.com$','Trello','Trove','Turnitin','twiceler','Typhoeus','ucsd','ultraseek','^undefined$','^unknown$','Unpaywall','URL2File','urlaliasbuilder','urllib','^user.?agent$','^User-Agent','validator','virus.detector','voila','^voltron$','voyager\/','w3af\.org','Wanadoo','Web(\s|\+)Downloader','WebCloner','webcollage','WebCopier','Webinator','weblayers','Webmetrics','webmirror','webmon','weborama-fetcher','webreaper','WebStripper','WebZIP','Wget','WhatsApp','wordpress','worm','www\.gnip\.com','WWW-Mechanize','xenu','y!j','yacy','yahoo','yandex','Yeti\/\d','Zabbix','ZoteroTranslationServer','zeus','zyborg','7siters']

# 使用counter进行正则匹配
def ua_re_check(ua_dict, save_folder):
    for ua_dict_key in ua_dict.keys():
        is_save = False
        for re_item in re_list:
            # 正则表达式的验证
            if check_string(re_item, ua_dict_key):
                is_save = True
                break
        if is_save:
            ua_dict[ua_dict_key] = 1

    for ua_item in ua_dict.keys():
        with open(save_folder, 'a') as save_file:
            save_file.writelines(ua_item + '\t' + str(ua_dict[ua_item]) + '\n')


# 功能：检查字符串str是否符合正则表达式re_exp
# re_exp:正则表达式
# str:待检查的字符串
def check_string(re_exp, str):
    res = re.search(re_exp, str)
    if res:
        return True
    else:
        return False


# 提取session的特征值然后匹配label
def session_lable(features_dataset):
    ip_features_dict = {}
    with open(features_dataset, 'r') as file:
        content = file.readlines()
    for line in content:
        ip_lables = line.replace('\n', '').split('\t')
        ip = ip_lables[1]
        labels = np.array(ip_lables[-2:])

        if ip_features_dict.__contains__(ip) and (not np.array_equal(ip_features_dict[ip], labels)):
            print(f'ip:{ip}, labels:{labels}, ip_features:{ip_features_dict[ip]}')

        ip_features_dict[ip] = labels

    # print(ip_features_dict)


# 1. 判断请求中是否/robots.txt文件，如果包含这个请求的流量，将该流量保存在out_robot_feature.txt文件中，不包含的保存在out.txt文件中
# 2. 调用ua_re_check，读取第一步的out.txt文件，根据counter project提供的正则表达式对ua进行匹配，判断是否是爬虫，
# 并将结果保存在out_counter_features.txt文件中
# 3. 打开Java代码，该代码读取第2步中保存的 ua_labels.txt 文件，使用browscap项目的工具进行ua匹配，然后将文件保存在 ua_counter_labels.txt 中

if __name__ == '__main__':
    dataset_path = '/home/chenrui/localworkspace/ml_dataset/ml_dataflow/public_v2.json'

    # out_robot_feature.txt
    # out.txt

    # 1. 判断请求中是否/robots.txt文件，如果包含这个请求的流量，将该流量保存在out_robot_feature.txt文件中，不包含的保存在out.txt文件中
    out_robot_feature = '/home/chenrui/localworkspace/ml_dataset/ml_dataflow/out_robot_feature.txt'
    ua_dict = robot_txt_label(dataset_path, out_robot_feature)

    # 2. 调用ua_re_check，读取第一步的out.txt文件，根据counter project提供的正则表达式对ua进行匹配，判断是否是爬虫，
    ua_dict_label_save_path = '/home/chenrui/localworkspace/ml_dataset/ml_dataflow/ua_labels.txt'
    ua_re_check(ua_dict, ua_dict_label_save_path)

    # 3. 打开Java代码，该代码读取第2步中保存的 ua_labels.txt 文件，使用browscap项目的工具进行ua匹配，然后将文件保存在 ua_counter_labels.txt 中
    # 这一步是在idea中运行

    # 4. 第四步调整到 group_features文件中执行，读取 ua_counter_labels.txt 的标注好的ua，与读取到session的流量中的ua 进行匹配，从而对流量进行标注

    # features_dataset = 'C:/Users/crdch/Downloads/out_features.txt'
    # features_dataset = 'C:/Users/crdch/Downloads/out_robot_feature.txt'
    # session_lable('C:/Users/crdch/Downloads/out_features.txt')


    # for re_item in re_list:
    #     # 正则表达式的验证
    #     if check_string(re_item, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'):
    #         is_save = True
    #         print(re_item)
    #         break
