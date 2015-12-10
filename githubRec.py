# -*- coding: utf-8 -*-
'''
Created by ch yy, 10/12/2015
To recommended best match github user repository
'''
import requests
from getpass import getpass
import json
from github import Github
import networkx as nx
from operator import itemgetter
import sys
from collections import Counter
from networkx.readwrite import json_graph
import webbrowser

def start_test():
    client,repo,stargazers,user = getRespond()
    g = addTOGraph(repo,stargazers,user)
    classify()
    addEdge(stargazers,client,g)
    getPopular(g)
    savaGraph1(g)
    top10(g)
    additional(stargazers,client,g) # 不必须，耗时可不必执行
    saveGraph2(g)
    findOutgoingEdges(g) # 不必须，耗时可不必执行
    addProgramLanguage(g) # 不必须，耗时可不必执行
    stats(g) # 不必须，耗时可不必执行
    saveGraph3(g)
    displayGraph(g)
    webbrowser.open_new_tab("http://%s:%s/%s.html"%("localhost","9999", "display_githubRec"))

def simpleDisplay():
    '''
    利用每次处理后保存的图来进行恢复展示
    :return:
    '''
    g = nx.read_gpickle("/home/ch/github.gpickle.1")
    print nx.info(g)
    print

    mtsw_users = [n for n in g if g.node[n]['type'] == 'user']
    h = g.subgraph(mtsw_users)

    print nx.info(h)

    d = json_graph.node_link_data(h)
    json.dump(d, open('force.json', 'w'))
    webbrowser.open_new_tab("http://%s:%s/%s.html"%("localhost","9999", "display_githubRec"))

def getAuth():
    '''
    获取github API的通关令牌
    :return:
    '''
    username = ''
    password = ''

    url = 'https://api.github.com/authorizations'
    note = 'Mining the Social Web, 2nd E'
    post_data = {'scopes':['repo'],'note': note }

    response = requests.post(url,auth = (username, password),data = json.dumps(post_data),)

    print "API response:", response.text
    print
    print "Your OAuth token is", response.json()['token']

def getRespond():
    '''
    获取原始仓库或者用户的一切API请求
    :return: client,repo,stargazers,user
    '''
    url = "https://api.github.com/repos/edx/edx-analytics-pipeline/stargazers"
    response = requests.get(url)

    print json.dumps(response.json()[0], indent=1)
    print

    for (k,v) in response.headers.items():
        print k, "=>", v

    ACCESS_TOKEN = '9ebc1b3f8357b7b5a208daafd8a65a7ead7eba19'

    # 这里配置查找的用户以及公开仓库
    USER = 'edx'
    REPO = 'edx-analytics-pipeline'

    client = Github(ACCESS_TOKEN, per_page=100)
    user = client.get_user(USER)
    repo = user.get_repo(REPO)

    stargazers = [ s for s in repo.get_stargazers() ] #可以先对这些人数进行分类限制
    print "Number of stargazers", len(stargazers) #人数众多，速度太慢
    return client,repo,stargazers,user #在这里可以控制人数

def addTOGraph(repo,stargazers,user):
    '''
    添加用户节点和仓库边，构成自我图
    :param repo: 仓库
    :param stargazers: 添加star的用户
    :param user: 原始user
    :return:
    '''
    g = nx.DiGraph()
    g.add_node(repo.name + '(repo)', type='repo', lang=repo.language, owner=user.login)

    for sg in stargazers:
        g.add_node(sg.login + '(user)', type='user')
        g.add_edge(sg.login + '(user)', repo.name + '(repo)', type='gazes')
        print sg.login + '(user)'
    print nx.info(g)
    print
    print g.node['edx-analytics-pipeline(repo)']
    print g.node['edx(user)']
    print
    print g['edx(user)']['edx-analytics-pipeline(repo)']

    print
    print g['edx(user)']
    print g['edx-analytics-pipeline']
    print
    print g.in_edges(['edx(user)'])
    print g.out_edges(['edx(user)'])
    print
    print g.in_edges(['edx-analytics-pipeline(repo)'])
    print g.out_edges(['edx-analytics-pipeline(repo)'])
    return g

def classify():
    '''
    计算图的中心度度量
    '''
    kkg = nx.generators.small.krackhardt_kite_graph()

    print "点度中心度"
    print sorted(nx.degree_centrality(kkg).items(),
             key=itemgetter(1), reverse=True)
    print

    print "中介中心度"
    print sorted(nx.betweenness_centrality(kkg).items(),
             key=itemgetter(1), reverse=True)
    print

    print "接近中心度"
    print sorted(nx.closeness_centrality(kkg).items(),
             key=itemgetter(1), reverse=True)

def addEdge(stargazers,client,g):
    '''
    # 添加关注边，构建新区图谱，以获取最受欢迎的top10
    '''
    for i, sg in enumerate(stargazers):
        try:
            for follower in sg.get_followers():
                if follower.login + '(user)' in g:
                    g.add_edge(follower.login + '(user)', sg.login + '(user)', type='follows')
        except Exception, e:
            print >> sys.stderr, "Encountered an error fetching followers for",sg.login, "Skipping."
            print >> sys.stderr, e

        print "Processed", i+1, " stargazers. Num nodes/edges in graph", g.number_of_nodes(), "/", g.number_of_edges()
        print "Rate limit remaining", client.rate_limiting

def getPopular(g):
    print nx.info(g)
    print

    print len([e for e in g.edges_iter(data=True) if e[2]['type'] == 'follows'])
    print

    print len([e
           for e in g.edges_iter(data=True)
               if e[2]['type'] == 'follows' and e[1] == 'edx(user)'])
    print

    print sorted([n for n in g.degree_iter()], key=itemgetter(1), reverse=True)[:10]
    print

    print len(g.out_edges('edx(user)'))
    print len(g.in_edges('edx(user)'))
    print

    c = Counter([e[1] for e in g.edges_iter(data=True) if e[2]['type'] == 'follows'])
    popular_users = [ (u, f) for (u, f) in c.most_common() if f > 1 ]
    print "Number of popular users", len(popular_users)
    print "Top 10 popular users:", popular_users[:10]

def savaGraph1(g):
    '''
    暂存图节点边的各种信息，因为对于有的star比较多的仓库计算一次不容易
    '''
    nx.write_gpickle(g, "github.1")
    # 如果恢复图的信息可以这么使用，g = nx.read_gpickle("github.1")

def top10(g):
    '''
    计算每种度量的top10
    '''
    h = g.copy()
    h.remove_node('edx-analytics-pipeline(repo)')
    dc = sorted(nx.degree_centrality(h).items(), key=itemgetter(1), reverse=True)

    print "点度中心度"
    print dc[:10]
    print

    bc = sorted(nx.betweenness_centrality(h).items(), key=itemgetter(1), reverse=True)

    print "中介中心度"
    print bc[:10]
    print

    print "接近中心度"
    cc = sorted(nx.closeness_centrality(h).items(), key=itemgetter(1), reverse=True)
    print cc[:10]

def additional(stargazers,client,g):
    '''
    向图中加入带star的仓库
    '''
    MAX_REPOS = 500

    for i, sg in enumerate(stargazers):
        print sg.login
        try:
            for starred in sg.get_starred()[:MAX_REPOS]: # Slice to avoid supernodes
                g.add_node(starred.name + '(repo)', type='repo', lang=starred.language, owner=starred.owner.login)
                g.add_edge(sg.login + '(user)', starred.name + '(repo)', type='gazes')
        except Exception, e: #ssl.SSLError:
            print "Encountered an error fetching starred repos for", sg.login, "Skipping."

        print "Processed", i+1, "stargazers' starred repos"
        print "Num nodes/edges in graph", g.number_of_nodes(), "/", g.number_of_edges()
        print "Rate limit", client.rate_limiting

def saveGraph2(g):
    nx.write_gpickle(g, "github.2")

def findOutgoingEdges(g):
    '''
    承接additional
    '''
    print nx.info(g)
    print

    repos = [n for n in g.nodes_iter() if g.node[n]['type'] == 'repo']

    print "Popular repositories"
    print sorted([(n,d)
              for (n,d) in g.in_degree_iter() if g.node[n]['type'] == 'repo'], key=itemgetter(1), reverse=True)[:10]
    print

    print "Respositories that edx has bookmarked"
    print [(n,g.node[n]['lang'])
           for n in g['edx(user)'] if g['edx(user)'][n]['type'] == 'gazes']
    print

    print "Programming languages edx is interested in"
    print list(set([g.node[n]['lang']
                for n in g['edx(user)'] if g['edx(user)'][n]['type'] == 'gazes']))
    print

    print "Supernode candidates"
    print sorted([(n, len(g.out_edges(n)))
              for n in g.nodes_iter() if g.node[n]['type'] == 'user' and len(g.out_edges(n)) > 500],key=itemgetter(1), reverse=True)

def addProgramLanguage(g):
    '''
    给图增加编程语言节点
    '''
    repos = [n for n in g.nodes_iter() if g.node[n]['type'] == 'repo']

    for repo in repos:
        lang = (g.node[repo]['lang'] or "") + "(lang)"

        stargazers = [u for (u, r, d) in g.in_edges_iter(repo, data=True) if d['type'] == 'gazes']

        for sg in stargazers:
            g.add_node(lang, type='lang')
            g.add_edge(sg, lang, type='programs')
            g.add_edge(lang, repo, type='implements')

def stats(g):
    '''
    到目前位置一些调试输出信息
    '''
    print nx.info(g)
    print

    print [n for n in g.nodes_iter() if g.node[n]['type'] == 'lang']
    print

    print [n for n in g['edx(user)'] if g['edx(user)'][n]['type'] == 'programs']

    print "Most popular languages"
    print sorted([(n, g.in_degree(n)) for n in g.nodes_iter() if g.node[n]['type'] == 'lang'], key=itemgetter(1), reverse=True)[:10]
    print

    python_programmers = [u for (u, l) in g.in_edges_iter('Python(lang)') if g.node[u]['type'] == 'user']
    print "Number of Python programmers:", len(python_programmers)
    print

    javascript_programmers = [u for (u, l) in g.in_edges_iter('JavaScript(lang)') if g.node[u]['type'] == 'user']
    print "Number of JavaScript programmers:", len(javascript_programmers)
    print

    print "Number of programmers who use JavaScript and Python"
    print len(set(python_programmers).intersection(set(javascript_programmers)))

    print "Number of programmers who use JavaScript but not Python"
    print len(set(javascript_programmers).difference(set(python_programmers)))

def saveGraph3(g):
    nx.write_gpickle(g, "github.3")

def displayGraph(g):
    print "Stats on the full graph"
    print nx.info(g)
    print

    mtsw_users = [n for n in g if g.node[n]['type'] == 'user']
    h = g.subgraph(mtsw_users)

    print "Stats on the extracted subgraph"
    print nx.info(h)

    d = json_graph.node_link_data(h)
    json.dump(d, open('force.json', 'w'))

