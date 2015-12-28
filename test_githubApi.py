# -*- coding: utf-8 -*-
import requests
import json
from github import Github
import networkx as nx
from operator import itemgetter
from collections import Counter
from networkx.readwrite import json_graph
import webbrowser
import os

def start(USER = 'edx', REPO = 'edx-documentation'):
    '''
    哪些用户关注了某个用户的某个仓库，这些follows关注的兴趣点
    :param USER:
    :param REPO:
    :return:
    '''
    ACCESS_TOKEN = '1161b718b9555cd76bf7ff9070c8f1ba300ea885'

    client = Github(ACCESS_TOKEN, per_page=100)
    user = client.get_user(USER)
    repo = user.get_repo(REPO)

    stargazers = [ s for s in repo.get_stargazers() ] #可以先对这些人数进行分类限制
    print "关注人的数目: %d \n" % len(stargazers) #如果人数很多，速度很慢
#-------------------------------------------------------------------------------------#
    g = nx.DiGraph()
    g.add_node(repo.name + '(r)', type='repo', lang=repo.language, owner=user.login)

    for sg in stargazers:
        g.add_node(sg.login + '(u)', type='user')
        g.add_edge(sg.login + '(u)', repo.name + '(r)', type='gazes')
        print sg.login + '(u)'

    for i, sg in enumerate(stargazers):
        try:
            for follower in sg.get_followers():
                if follower.login + '(u)' in g:
                    g.add_edge(follower.login + '(u)', sg.login + '(u)', type='follows')
        except Exception, e:
            print "获取追随者失败，跳过", sg.login, e

        print "正在处理第", i+1, " 个关注者。"
#-------------------------------------------------------------------------------------#
    c = Counter([e[1] for e in g.edges_iter(data=True) if e[2]['type'] == 'follows'])
    popular_users = [(u, f) for (u, f) in c.most_common() if f > 1]
    print "受欢迎的用户数目：", len(popular_users)
    print "最受欢迎的10个用户：", popular_users[:10]
#-------------------------------------------------------------------------------------#
    MAX_REPOS = 500

    for i, sg in enumerate(stargazers):
        print sg.login
        try:
            for starred in sg.get_starred()[:MAX_REPOS]: # Slice to avoid supernodes
                g.add_node(starred.name + '(r)', type='repo', lang=starred.language, owner=starred.owner.login)
                g.add_edge(sg.login + '(u)', starred.name + '(r)', type='gazes')
        except Exception, e: #ssl.SSLError:
            print "获取加星仓库失败　", sg.login, "跳过."

        print "正在处理", i+1, "加星的仓库"



#-------------------------------------------------------------------------------------#
    filename = "1.1"
    nx.write_gpickle(g, filename)

    d = json_graph.node_link_data(g)
    filename = "1.json"
    json.dump(d, open(filename, 'w'))

def analytics():
    g = nx.read_gpickle("1.1")
    data = {}
    for n in g.nodes_iter():
        if (g.node[n]['type'] == 'repo' and g.node[n]['lang'] not in data):
            data[ g.node[n]['lang']] = 0
        elif (g.node[n]['type'] == 'repo' and g.node[n]['lang'] in data) :
            data[ g.node[n]['lang']] = data[ g.node[n]['lang']]+ 1
        else:
            pass
    print data