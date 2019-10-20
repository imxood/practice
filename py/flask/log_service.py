from flask import Flask, make_response, request, session, render_template, send_file, Response
from flask.views import MethodView
from datetime import datetime
import humanize
import os
import re
import stat
import json
import mimetypes
import sys
from pathlib2 import Path

app = Flask(__name__, static_url_path='/assets', static_folder='assets')
root = os.path.normpath("/tmp")
key = ""

datatypes = {'audio': 'm4a,mp3,oga,ogg,webma,wav', 'archive': '7z,zip,rar,gz,tar', 'image': 'gif,ico,jpe,jpeg,jpg,png,svg,webp', 'pdf': 'pdf', 'quicktime': '3g2,3gp,3gp2,3gpp,mov,qt', 'source': 'atom,bat,bash,c,cmd,coffee,css,hml,js,json,java,less,markdown,md,php,pl,py,rb,rss,sass,scpt,swift,scss,sh,xml,yml,plist', 'text': 'txt', 'video': 'mp4,m4v,ogv,webm', 'website': 'htm,html,mhtm,mhtml,xhtm,xhtml'}
icontypes = {'icon-jfi-file-text': 'txt,log'}


@app.template_filter('size_fmt')
def size_fmt(size):
    return humanize.naturalsize(size)


@app.template_filter('time_fmt')
def time_desc(timestamp):
    mdate = datetime.fromtimestamp(timestamp)
    str = mdate.strftime('%Y-%m-%d %H:%M:%S')
    return str


@app.template_filter('data_fmt')
def data_fmt(filename):
    t = 'unknown'
    for type, exts in datatypes.items():
        if filename.split('.')[-1] in exts:
            t = type
    return t


@app.template_filter('icon_fmt')
def icon_fmt(filename):
    i = 'icon-jfi-file-o'
    for icon, exts in icontypes.items():
        if filename.split('.')[-1] in exts:
            i = icon
    return i


@app.template_filter('humanize')
def time_humanize(timestamp):
    mdate = datetime.utcfromtimestamp(timestamp)
    return humanize.naturaltime(mdate)


def get_type(mode):
    if stat.S_ISDIR(mode) or stat.S_ISLNK(mode):
        type = 'dir'
    else:
        type = 'file'
    return type


class PathView(MethodView):

    def get(self, p=''):

        path = os.path.join(root, p)

        if os.path.isdir(path):

            contents = []
            total = {'size': 0, 'dir': 0, 'file': 0}

            for filename in os.listdir(path):

                filepath = os.path.join(path, filename)
                stat_res = os.stat(filepath)

                info = {}
                info['name'] = filename
                info['mtime'] = stat_res.st_mtime
                ft = get_type(stat_res.st_mode)
                info['type'] = ft
                sz = stat_res.st_size
                info['size'] = sz

                contents.append(info)

                total[ft] += 1
                total['size'] += sz

            page = render_template('index.html', path=p,
                                   total=total, contents=contents)
            res = make_response(page, 200)

        elif os.path.isfile(path):

            res = send_file(path)
            res.headers.add('Content-Disposition', 'attachment')

        return res


path_view = PathView.as_view('path_view')
app.add_url_rule('/', view_func=path_view)
app.add_url_rule('/<path:p>', view_func=path_view)


if __name__ == '__main__':
    app.run('127.0.0.1', '8000', threaded=True, debug=True)
