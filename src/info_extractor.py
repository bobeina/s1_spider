"""
info_extractor.py
"""
import asyncio
import re
import os
import time
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class S1PostsInfoExtractor:
    """
    下载s1的某个帖子的所有页
    __init__() 中 driver参数可选项：geckodriver/chromedriver
    """

    def __init__(self,
                 origin_url=None,
                 driver_path=None,
                 driver=None,
                 user_agent_str=None,
                 headless=True
                 ):
        self.origin_url = origin_url

        # chrome; 改用firefox
        # self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_argument(user_agent_str)
        # if headless:
        #     self.chrome_options.add_argument("--headless")
        # self.browser = webdriver.Chrome(executable_path=driver_path, options=self.chrome_options) #old version for chrome
        # self.browser = webdriver.Chrome(ChromeDriverManager().install())

        self.browser_options = webdriver.FirefoxOptions()
        # self.browser_options.add_argument(user_agent_str)
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent_str)
        if headless:
            self.browser_options.add_argument('--headless')
        full_driver_path = os.path.join(driver_path, driver)

        print('S1PostsInfoExtractor.__init__() full_driver_path=', full_driver_path)

        self.browser = webdriver.Firefox(profile, executable_path=full_driver_path, options=self.browser_options)

        self.score_tab = None
        self.main_tab = self.browser.current_window_handle
        self.cookies = None
        self.page_num = 0
        # 设cookie前要先读一个页面
        self.load_page('https://bbs.saraba1st.com/2b/')

        # 开一个新tab用于查找帖子加扣鹅情况
        self.main_tab = self.browser.current_window_handle
        print('crnt page(before): ', self.browser.current_window_handle)
        self.browser.execute_script("window.open('about:blank');")
        # time.sleep(1)
        print('crnt page(after): ', self.browser.current_window_handle)

        for tab in self.browser.window_handles:
            print(' tab handle --> ', tab)
            if tab != self.main_tab:
                self.score_tab = tab
        # self.score_tab = self.browser.window_handles[-1]
        if self.score_tab is None or self.score_tab == self.main_tab:
            raise ValueError("Initialize new tab failed. Exit.")

        print('main page: ', self.main_tab)
        print('sub  page: ', self.score_tab)
        print('crnt page: ', self.browser.current_window_handle)
        print('switching to main...')
        self.browser.switch_to.window(self.main_tab)
        time.sleep(1)

    def auto_login(self, usernm=None, pwd=None):
        if usernm is None or pwd is None:
            print('Sorry, usernm/pwd cannot be None with auto_login().')
            return
        # todo 网络不太稳定时偶尔会出错，待修
        usernm_dom = self.browser.find_element_by_id('ls_username')
        pwd_dom = self.browser.find_element_by_id('ls_password')
        send_dom = self.browser.find_element_by_xpath('//button[@class="pn vm"]')
        usernm_dom.send_keys(usernm)
        pwd_dom.send_keys(pwd)
        send_dom.click()
        time.sleep(1)

    def load_page(self, url, other_tab=None):
        self.origin_url = url
        if other_tab is None:
            if self.browser.current_window_handle != self.main_tab:
                self.browser.switch_to.window(self.main_tab)
        else:
            self.browser.switch_to.window(other_tab)
        self.browser.get(url)
        delay = 10  # seconds
        try:
            myElem = WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.ID, 'threadsortswait')))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")

    def load_page_with_cookie(self, url, current_tab=None) -> bool:
        print('Loading page <{url}>...'.format(url=url))
        if self.cookies is None:
            print('No cookie for current page.')
            return False
        for c in self.cookies:
            # 暂时保留
            # if 'expiry' in c:
            #     del c['expiry']
            # print(c)
            self.browser.add_cookie(c)
        if current_tab is None:
            self.browser.switch_to.window(self.main_tab)
        else:
            self.browser.switch_to.window(current_tab)

        time.sleep(3)

        # # 刷新页面
        bvalue = self.browser.get(url)
        return True

    def save_current_cookies(self, filepath='cookies', filename='saraba1st.com.json'):
        cookies = self.browser.get_cookies()
        parent_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        fullname = os.path.join(parent_dir, filepath, filename)
        with open(fullname, 'w') as fp:
            fp.write(json.dumps(cookies))

    def is_login(self):
        """
        判断是否登录
        :return: 返回已登录的用户名字符串，未登录则返回 None
        """
        user_name_container = self.browser.find_elements_by_class_name('vwmy')
        if len(user_name_container) == 0:
            return None
        return user_name_container[0]

    def login(self, usernm, pwd):
        """
        登录并保存cookie
        :param usernm:
        :param pwd:
        :return:
        """
        # TODO 未完
        print("WARNING: this method is not finished.")
        # self.cookies = self.browser.get_cookies()

    def load_cookies_from_file(self, cookie_file):
        with open(cookie_file, 'r') as fp:
            cookie = fp.read()
            self.cookies = json.loads(cookie)
            print('Load cookies from file <{file}> OK.'.format(
                file=cookie_file
            ))

    def get_page_index(self) -> bool:
        """
        获取页索引，将结果保存在 self.page_index list 中，若读取页面失败，置page_index为[]，若只有一页，置其为[page_url]
        :return: bool
        """
        try:
            if not self.is_login():
                return False
            text = self.browser.find_element_by_xpath('//div[@class="pg"]/label/span').text
            print('text: ', text)
        except Exception as e:
            self.page_num = 1
            return True
        pattern = re.compile(r'\d+')
        match_str = pattern.search(text)

        if match_str:
            total_page = match_str.group()
            # print('共 {tp} 页'.format(tp=total_page))
            self.page_num = int(total_page)
        else:
            self.page_num = 1
        return True

    #########################################################################################################
    # 以下诸模块负责解析页面元素、将页面按回复拆分；生成可塞到原始数据库中的数据，过后再作进一步的处理和解析，例如图像、引用等
    @staticmethod
    def extract_author(post):
        """
        :param post:
        :return: 发帖人ID、nick
        """
        try:
            raw_author_info = post.find_element_by_xpath('tbody/tr/td/div/div/div/a[@class="xw1"]')
        except Exception as e:
            print('---------------debug-info----------------->>>')
            print(e)
            print('.'*30)
            print(post.get_attribute('innerHTML'))
            print('<<<------------------------------------------')
            raise e

        if not raw_author_info:
            return None, None
        author_nick = raw_author_info.text
        raw_author_id = raw_author_info.get_attribute("href")
        pattern_aid = re.compile(r'space-uid-(\d+)', re.IGNORECASE)
        author_id = pattern_aid.search(raw_author_id)
        return author_id.group(1), author_nick

    def extract_thread_subject(self):
        """
        抽取帖子主题
        :return: 正常情况下返回字符串，若返回None时，页面获取大概出错了
        """
        thread_subject = self.browser.find_element_by_id('thread_subject')
        if thread_subject:
            return thread_subject.text
        return None

    @staticmethod
    def extract_post_title(post)->str:
        """
        帖子标题；注意，主楼标题需另作处理
        :param post:
        :return:
        """
        try:
            raw_title = post.find_element_by_xpath('tbody/tr//div[@class="pct"]/div[@class="pcb"]/h2')
            if raw_title:
                return raw_title.text
        except NoSuchElementException as e:
            return ''

    @staticmethod
    def extract_edited_info(post):
        """
        抽取出帖子编辑提示信息
        :param post:
        :return: edited by, edited datetime str
        """
        # <i class="pstatus"> 本帖最后由 XXXXXXXXX 于 2020-6-3 15:19 编辑 </i>
        try:
            raw_edited_hint = post.find_element_by_class_name('pstatus')
            if raw_edited_hint:
                pattern = re.compile(r' 本帖最后由 (.*) 于 (.*) 编辑', re.IGNORECASE)
                result = pattern.search(raw_edited_hint.text)
                if result is not None:
                    return str(result.group(1)), str(result.group(2))
        except NoSuchElementException as e:
            pass
        return None, None

    @staticmethod
    def extract_raw_content(post):
        """
        抽取回复内容
        :param post:
        :return: post_id, content,
        """
        # xpath_str = 'tbody//td[@class="t_f"]'
        # try:
        #     raw_content = post.find_element_by_xpath(xpath_str)
        #     if raw_content:
        #         return raw_content.get_attribute('innerHTML')
        # except NoSuchElementException as e:
        #     # tbody tr td.plc div.pct div.pcb div.locked
        #     banned_xpath_str = 'tbody//div[@class="locked"]'
        xpath_str = 'tbody//div[@class="pct"]/div[@class="pcb"]'
        raw_content = post.find_element_by_xpath(xpath_str)
        if raw_content:
            return raw_content.get_attribute('innerHTML')
        return None

    @staticmethod
    def extract_post_time(post):
        """
        抽取层数、回帖时间及楼层id
        :param post: 该层帖子 dom
        :return:
        """
        post_id = post.get_attribute('id')[3:]

        # print('-'*100)
        # print('thread_id: ', thread_id)
        # print('post_id: ', post_id)

        raw_floor = post.find_element_by_xpath("tbody/tr//div[@class='pi']/strong/a")
        if '楼主' in raw_floor.get_attribute('innerHTML'):
            floor = 1
        else:
            floor = int(raw_floor.text[:-1])
        try:
            xpath_str = 'tbody/tr/td[@class="plc"]/div[@class="pi"]/div[@class="pti"]/div[@class="authi"]/em'
            raw_post_time = post.find_element_by_xpath(xpath_str)
        except Exception as e:
            print('=' * 100)
            print('出错警告:')
            print(post.get_attribute('innerHTML'))
            print('<' * 100)
            raise e
        post_time_str = raw_post_time.text
        time_pattern = re.compile(r'发表于 (.*)', re.IGNORECASE)
        t_result = time_pattern.search(post_time_str)
        post_time = str(t_result.group(1))
        return floor, post_time, post_id

    @staticmethod
    def if_post_has_score(post):
        try:
            # score_signal = post.find_element_by_xpath("h3[@class='psth xs1']/span[@class='icon_ring vm'")

            xpath_str = "tbody//h3[@class='psth xs1']" #/span[@class='icon_ring vm']"
            score_signal_html = post.find_element_by_xpath(xpath_str).get_attribute('innerHTML')
            print('score_signal_html: ', score_signal_html)
            if '评分' in score_signal_html:
                return True
            else:
                print('评分 not found')
                return False
        except NoSuchElementException as e:
            return False

    def load_post_scores_page(self, tid, pid):
        """
        获取该帖子的全部评分列表
        :param tid:
        :param pid:
        :return:
        """
        score_url = 'https://bbs.saraba1st.com/2b/forum.php?mod=misc&action=viewratings&tid={tid}&pid={pid}'.format(
            tid=tid,
            pid=pid
        )
        self.load_page_with_cookie(score_url, current_tab=self.score_tab)
        #/div[@class='f_c']/div[@class='c floatwrap']/table/tr/td
        xpath_str = "//div[@class='f_c']/div[@class='c floatwrap']/table/tbody/tr"
        trs = self.browser.find_elements_by_xpath(xpath_str)
        result = []
        uid_pattern = re.compile(r'space-uid-(\d+)')
        for tr in trs:
            tds = tr.find_elements_by_xpath("td")
            if tds:
                td_data = []
                for i, td in enumerate(tds):
                    td_data.append(td.text)
                raw_url = tds[1].find_element_by_xpath('a').get_attribute('href')
                uid = uid_pattern.search(raw_url)
                td_data.append(int(uid.group(1)))
                result.append(tuple(td_data))
        time.sleep(1)
        handles = self.browser.window_handles
        self.browser.switch_to.window(handles[0])
        return result

    def extract_info_from_post(self, post, thread_id) -> dict:
        """
        初步划分数据库中的帖子信息结构：id thread_id post_id floor post_title raw_content author_id author post_time editor_nick modified_flag save_time
        :param post: 以 div[@class='plhin'] 为条件查询到的table列表中的一个
        :return: dict, 包括的 key 有：
         thread_id, post_id, floor, post_title, raw_content, author_id, author_nick, post_time, editor_nick, edited_time
        """

        # id thread_id post_id floor raw_content author_id author post_time modified_flag save_time
        # auto: id save_time
        # 未完：thread_id post_id author modified_flag
        author_id, author_nick = self.extract_author(post)
        editor_nick, edited_time = self.extract_edited_info(post)
        raw_content = self.extract_raw_content(post)
        floor, post_time, post_id = self.extract_post_time(post)
        post_title = self.extract_post_title(post)
        scores = []
        has_score = self.if_post_has_score(post)
        if has_score == True:
            scores = self.load_post_scores_page(thread_id, post_id)
        rvalue = {
            # 'thread_id': thread_id,
            'post_id': int(post_id),
            'floor': int(floor),
            'post_title': post_title,
            'raw_content': raw_content,
            'author_id': int(author_id),
            'author': author_nick,
            'post_time': post_time,
            'editor_nick': editor_nick,
            'edited_time': edited_time,
            'scores': scores
        }
        return rvalue

    def parse_page(self, thread_id, page_index, gt=None, lt=None):
        """
        解析页面元素、将页面按回复拆分；生成可塞到原始数据库中的数据
        :param gt: 只返回 post_id 大于 gt 指定的帖子
        :param lt: （理论上）只返回 post_id 小于 lt 指定的帖子，目前不用
        :return: list, list 中的元素为 extract_info_from_post() 返回的 dict，包含的key有：
                thread_id, post_id, floor, raw_content, author_id, author_nick, post_time, editor_nick, edited_time
        """
        url = "https://bbs.saraba1st.com/2b/thread-{tid}-{page_index}-1.html".format(
            tid=thread_id,
            page_index=page_index+1
        )
        time.sleep(1)
        print("Page {p}; Yielding {url}...".format(p=page_index, url=url))

        bvalue = self.load_page_with_cookie(url)

        posts = self.browser.find_elements_by_xpath('//div[@id="postlist"]/div/table[@class="plhin"]')

        # 帖子结构：id thread_id post_id raw_content author_id author post_time modified_flag save_time
        # 若帖子编辑过，则modified_flag = 1, 否则为0
        # return [self.extract_info_from_post(post) for post in posts]
        info_list = []
        for i, post in enumerate(posts):
            rvalue = self.extract_info_from_post(post, thread_id)
            if gt is not None:
                if rvalue['post_id'] <= gt:
                    continue
            rvalue['thread_id'] = thread_id
            info_list.append(rvalue)
        return info_list

    def parse_thread(self, thread_id):
        """

        :param url: thread 地址
        :return:
        """
        # 生成url
        print('parse_thread() start')

        url = "https://bbs.saraba1st.com/2b/thread-{tid}-1-1.html".format(tid=thread_id)
        self.origin_url = url
        self.load_page_with_cookie(url)
        time.sleep(3)

        # 获取总页数
        bvalue = self.get_page_index()
        if not bvalue:
            print('Get page index failed. Exit.')
            return None

        print('Total page: ', self.page_num)

        # 按页读取
        for page_index in range(self.page_num):

            # if page_index+1 < self.page_num:
            post_data = self.parse_page(thread_id, page_index)

            print('>'*100)
            print(post_data)
            print('<'*100)

            yield post_data

        # TODO 待分析如何判断帖子是否编辑过、是否与当前版本相同，是否需要重新抓取
        # <i class="pstatus"> 本帖最后由 XXXXXXXXX 于 2020-6-3 15:19 编辑 </i>

        # TODO 图片及影片的处理：此处先不管

        #

    def continue_thread(self, thread_id, last_post_id, page):
        """
        更新帖子（不更新在上次爬取之后编辑过的，只寻找新的回复）
        :param thread_id: thread 地址
        :param last_post_id: 从数据库中获取到的该帖最后一个回复的 post_id
        :param page: 根据数据库中该帖总回复数计算出的页数（S1可能在抽楼后会有bug，待验）
        :return:
        """
        # 生成url
        print('continue_thread() start')

        url = "https://bbs.saraba1st.com/2b/thread-{tid}-{page}-1.html".format(
            tid=thread_id,
            # page=page
            page=1
        )
        self.origin_url = url
        self.load_page_with_cookie(url)
        time.sleep(3)

        # 获取总页数
        bvalue = self.get_page_index()
        if not bvalue:
            print('Get page index failed. Exit.')
            return None
        # if self.page_num < page:
        #     return

        print('Total page: ', self.page_num)

        # 按页读取
        for page_index in range(page, self.page_num):
            post_data = self.parse_page(thread_id, page_index, gt=last_post_id)
            yield post_data
