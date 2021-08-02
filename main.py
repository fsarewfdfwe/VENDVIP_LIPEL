from flask import Flask, render_template, request, make_response
from flask import session, redirect, url_for, abort, jsonify
from datetime import timedelta
import datetime
import time
import sqlite3
import randomstring
import os
import datetime
from datetime import timedelta
import ssl
import hashlib
import random
import ast
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed

panel_keypair = panel_keypair = {"knmzxads4819" : "knmzxads4819"}

app = Flask(__name__)
app.config['SERVER_NAME'] = 'https://5e81107e.vendvip-lipel.pages.dev'

cwdir =  os.path.dirname(__file__) + "/"

app.secret_key = randomstring.pick(30)

@app.template_filter('lenjago')
def lenjago(jago, txt):
    return len(jago.split(txt))

app.jinja_env.filters['lenjago'] = lenjago

if (os.path.isfile(f"{cwdir}ban.db")):
    pass
else:
    con = sqlite3.connect(f"{cwdir}ban.db") # 밴기능 db
    with con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE "ban" ("ip" TEXT);""")
        con.commit()
    con.close

def is_expired(time):
    ServerTime = datetime.datetime.now()
    ExpireTime = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    if ((ExpireTime - ServerTime).total_seconds() > 0):
        return False
    else:
        return True


def get_expiretime(time):
    ServerTime = datetime.datetime.now()
    ExpireTime = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    if ((ExpireTime - ServerTime).total_seconds() > 0):
        how_long = (ExpireTime - ServerTime)
        days = how_long.days
        hours = how_long.seconds // 3600
        minutes = how_long.seconds // 60 - hours * 60
        return str(round(days)) + "일 " + str(round(hours)) + "시간"
    else:
        return False


def make_expiretime(days):
    ServerTime = datetime.datetime.now()
    ExpireTime = ServerTime + timedelta(days=days)
    ExpireTime_STR = (ServerTime + timedelta(days=days)).strftime('%Y-%m-%d %H:%M')
    return ExpireTime_STR


def add_time(now_days, add_days):
    ExpireTime = datetime.datetime.strptime(now_days, '%Y-%m-%d %H:%M')
    ExpireTime_STR = (ExpireTime + timedelta(days=add_days)).strftime('%Y-%m-%d %H:%M')
    return ExpireTime_STR


def nowstr():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

def db(name):
    return cwdir + "database/" + name + ".db"

def hash(string):
    return str(hashlib.sha512((string + "saltysalt!@#%!@$!").encode()).hexdigest())

def search_user(name, id):
    con = sqlite3.connect(db(name))
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id == ?", (id,))
    result = cur.fetchone()
    con.close()
    return result

def get_info(name):
    con = sqlite3.connect(db(name))
    cur = con.cursor()
    cur.execute("SELECT * FROM info;")
    result = cur.fetchone()
    con.close()
    return result

def search_prod(name, id):
    con = sqlite3.connect(db(name))
    cur = con.cursor()
    cur.execute("SELECT * FROM products WHERE id == ?", (id,))
    result = cur.fetchone()
    con.close()
    return result

def getip():
    return request.headers.get("CF-Connecting-IP", request.remote_addr)

def get_prod(name, id):
    con = sqlite3.connect(db(name))
    cur = con.cursor()
    cur.execute("SELECT * FROM products WHERE id == ?", (id,))
    result = cur.fetchone()
    con.close()
    return result

@app.route("/", methods=["GET", "POST"])
def create():
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (request.method == "GET"):
            return render_template("create.html")
        else:
            if ("g-recaptcha-response" in request.form):
                if ("url" in request.form and "name" in request.form and "adminid" in request.form and "adminpw" in request.form and "adminpwcheck" in request.form and request.form["adminpw"] == request.form["adminpwcheck"] and "license" in request.form):
                    if (len(request.form["adminid"]) >= 6 and len(request.form["adminid"]) <= 24 and len(request.form["adminpw"]) >= 6 and len(request.form["adminpw"]) <= 24 and len(request.form["name"]) >= 1 and len(request.form["name"]) <= 12 and request.form["name"].isalpha() and len(request.form["url"]) >= 3 and len(request.form["url"]) <= 12):
                        if not (os.path.isfile(db(request.form["url"]))):
                            captcha_secret = "리캡챠"
                            captcha_result = requests.get("https://www.google.com/recaptcha/api/siteverify?secret=" + captcha_secret + "&response=" + request.form["g-recaptcha-response"] + "&remoteip=" + getip()).json()
                            if (captcha_result["success"] == True):
                                con = sqlite3.connect(cwdir + "license.db")
                                with con:
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM license WHERE code == ?;", (request.form["license"],))
                                    license_result = cur.fetchone()
                                    if (license_result != None):
                                        if (license_result[2] == ""):
                                            cur.execute("UPDATE license SET usedat = ?, usedip = ?, usedurl = ? WHERE code == ?;", (nowstr(), getip(), request.form["url"], request.form["license"]))
                                            con.commit()
                                con.close()
                                if (license_result == None):
                                    return "존재하지 않는 라이센스입니다."
                                if (license_result[2] != ""):
                                    return "이미 사용된 라이센스입니다."
                                con = sqlite3.connect(db(request.form["url"]))
                                with con:
                                    cur = con.cursor()
                                    cur.execute("""CREATE TABLE "info" ("name" TEXT, "webhk" TEXT, "cultureid" TEXT, "culturepw" TEXT, "buylog" TEXT, "chargelog" TEXT, "banned" TEXT, "expiredate" TEXT, "music" TEXT, "announcement" TEXT, "fee" INTEGER, "bankaddr" TEXT, "bankpw" TEXT, "type" INTEGER, "linking" TEXT, "background" TEXT, "file" TEXT, "imgannouncement" TEXT, "buylogwebhkt" TEXT, "adminlogwebhk" TEXT, "addstock" TEXT, "channeltok" TEXT, "bankmax" TEXT);""")
                                    con.commit()
                                    cur.execute("""CREATE TABLE "products" ("id" TEXT, "name" TEXT, "description" TEXT, "price" INTEGER, "url" TEXT, "stock" TEXT);""")
                                    con.commit()
                                    cur.execute("""CREATE TABLE "users" ("id" TEXT, "pw" TEXT,"ip" TEXT, "money" INTEGER, "buylog" TEXT, "isadmin" INTEGER, "black" TEXT, "name" TEXT, "tag" TEXT);""")
                                    con.commit()
                                    cur.execute("""CREATE TABLE "bankwait" ("id" TEXT, "name" TEXT, "amount" INTEGER, "day" TEXT);""")
                                    con.commit()
                                    cur.execute("""INSERT INTO info VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (request.form["name"], "", "", "", "[]", "[]", "", make_expiretime(license_result[1]), "", "공지가 없습니다.", 0, "", "", 0 if license_result[5] == 0 else 1, "", "https://cdn.discordapp.com/attachments/754331422818435083/795524062482792458/608a38b94a378eff.gif", "", "https://media.discordapp.net/attachments/821406537976381512/840770369602060318/12.png", "사용함", "", "", "", ""))
                                    con.commit()
                                    cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", (request.form["adminid"], hash(request.form["adminpw"]), getip(), 0, "[]", 1, "", "", ""))
                                    con.commit()
                                con.close()

                                api_key = "d633844c69e32b7e13f40d00e67e81be1f4a7"
                                email = "juhohwang5333@gmail.com"
                                zone_id = "eb1e93f10b7cf8bdcabc227986d725bb"

                                headers = {"X-Auth-Email" : email, "X-Auth-Key" : api_key}
                                json_data = {"type" : "A", "name" : request.form["url"], "content" : "218.147.221.92", "ttl" : 1, "proxied" : True}
                                try:
                                    res_data = requests.post(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records", headers=headers, json=json_data).json()
                                except:
                                    pass
                                return "ok"
                            else:
                                return "reCAPTCHA 오류가 발생했습니다. 새로고침 후 재시도해주세요."
                        else:
                            return "이미 존재하는 URL입니다."
                    else:
                        return "잘못된 접근입니다."
                else:
                    return "잘못된 접근입니다."
            else:
                return '"로봇이 아닙니다" 를 눌러주세요.'


@app.route("/", subdomain='<name>', methods=["GET"])
def index(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (name.isalpha()):
            if (os.path.isfile(db(name))):
                if (name in session):
                    return redirect("announcement")
                else:
                    return redirect("login")
            else:
                abort(404)
        else:
            abort(404)

@app.route("/login", subdomain='<name>', methods=["GET", "POST"])
def login(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (request.method == "GET"):
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        return redirect("announcement")
                    else:
                        info = get_info(name)
                        if (str(info[6]) != ""):
                            return render_template("403.html", reason=info[6])
                        else:
                            return render_template("login.html", name=info[0], background=info[15])
                else:
                    abort(404)
            else:
                abort(404)
        else:
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        return redirect("shop")
                    else:
                        if ("id" in request.form and "pw" in request.form):
                            user_info = search_user(name, request.form["id"])
                            if (user_info != None):
                                if (user_info[1] == hash(request.form["pw"])):
                                    if (user_info[6] == ""):
                                        server_info = get_info(name)
                                        session[name] = request.form["id"]
                                        if (server_info[19] != None):
                                            try:
                                                webhook = DiscordWebhook(username="LIPEL Essential Vend", avatar_url="https://media.discordapp.net/attachments/821406537976381512/840770369602060318/12.png", url=server_info[19])
                                                embed = DiscordEmbed(description=f'[!] 로그인 알림\n서버이름: {server_info[0]}\n아이디: {request.form["id"]}', color=0xE8FF00)
                                                webhook.add_embed(embed)
                                                webhook.execute()
                                            except:
                                                print("Webhook Error")
                                        return '<script>window.location.href = "announcement"</script>'
                                    else:
                                        reason = user_info[6]
                                        return f'<script>alert(`관리자에 의해 차단된 계정입니다.\n차단 사유 : {reason}`); window.location.href = "login";</script>'
                                else:
                                    return '<script>alert("비밀번호가 틀렸습니다."); window.location.href = "login"</script>'
                            else:
                                return '<script>alert("아이디가 틀렸습니다."); window.location.href = "login"</script>'
                        else:
                            return '<script>alert("잘못된 접근입니다."); window.location.href = "login"</script>'
                else:
                    abort(404)
            else:
                abort(404)

@app.route("/register", subdomain='<name>', methods=["GET", "POST"])
def register(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (request.method == "GET"):
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        return redirect("shop")
                    else:
                        info = get_info(name)
                        if (str(info[6]) != ""):
                            return render_template("403.html", reason=info[6])
                        elif (is_expired(info[7])):
                            return render_template("403.html", reason="라이센스 연장이 필요합니다.")
                        else:
                            return render_template("register.html", name=info[0], background=info[15])
                else:
                    abort(404)
            else:
                abort(404)
        else:
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        return redirect("shop")
                    else:
                        if ("id" in request.form and "pw" in request.form):
                            user_info = search_user(name, request.form["id"])
                            if (user_info == None):
                                con = sqlite3.connect(db(name))
                                cur = con.cursor()
                                cur.execute("SELECT * FROM users WHERE ip == ?;", (getip(),))
                                iplist = cur.fetchone()
                                con.close()
                                if (iplist == None):
                                    if ((len(request.form["id"]) >= 6 and len(request.form["id"]) <= 24) and (len(request.form["pw"]) >= 6 and len(request.form["pw"]) <= 24)):
                                        con = sqlite3.connect(db(name))
                                        cur = con.cursor()
                                        cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", (request.form["id"], hash(request.form["pw"]), getip(), 0, "[]", 0, "", "", request.form["tag"]))
                                        con.commit()
                                        con.close()
                                        session.pop(name, None)
                                        session[name] = request.form["id"]
                                        server_info = get_info(name)
                                        if (server_info[19] != None):
                                            try:
                                                webhook = DiscordWebhook(username="LIPEL Essential Vend", avatar_url="https://media.discordapp.net/attachments/821406537976381512/840770369602060318/12.png", url=server_info[19])
                                                embed = DiscordEmbed(description=f'[!] 회원가입 알림\n{name}서버에서 {request.form["id"]}님이 가입하셨습니다.\n{request.form["id"]}님의 정보\n아이디: {request.form["id"]}\n아이피: {getip()}\n잔액: 0\n디스코드 닉네임: {request.form["tag"]}', color=0xE8FF00)
                                                webhook.add_embed(embed)
                                                webhook.execute()
                                            except:
                                                print("Webhook Error")
                                        return '<script>alert("회원가입에 성공했습니다!"); window.location.href = "announcement"</script>'
                                    else:
                                        return '<script>alert("아이디 및 암호는 6 ~ 24자입니다."); window.location.href = "register?agreed=true"</script>'
                                else:
                                    return '<script>alert("이미 해당 IP로 가입된 계정이 있습니다."); window.location.href = "register?agreed=true"</script>'
                            else:
                                return '<script>alert("이미 존재하는 아이디입니다."); window.location.href = "register?agreed=true"</script>'
                        else:
                            return '<script>alert("잘못된 접근입니다."); window.location.href = "register?agreed=true"</script>'
                else:
                    abort(404)
            else:
                abort(404)

@app.route("/shop", subdomain='<name>', methods=["GET"])
def shop(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (name.isalpha()):
            if (os.path.isfile(db(name))):
                if (name in session):
                    info = get_info(name)
                    if (str(info[6]) != ""):
                        return render_template("403.html", reason=info[6])
                    elif (is_expired(info[7])):
                        return render_template("403.html", reason="라이센스 연장이 필요합니다.")
                    else:
                        server_info = get_info(name)
                        user_info = search_user(name, session[name])
                        con = sqlite3.connect(db(name))
                        cur = con.cursor()
                        cur.execute("SELECT * FROM products;")
                        products = cur.fetchall()
                        con.close()
                        return render_template("index.html", name=server_info[0], products=products, user_info=user_info, music=server_info[8], shopinfo=server_info, linking=server_info[14], url=name, file=info[16], channelio=server_info[21])
                else:
                    return redirect("login")
            else:
                abort(404)
        else:
            abort(404)

@app.route("/buylog", subdomain='<name>', methods=["GET"])
def log(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (name.isalpha()):
            if (os.path.isfile(db(name))):
                if (name in session):
                    info = get_info(name)
                    if (is_expired(info[7])):
                            return render_template("403.html", reason="라이센스 연장이 필요합니다.")
                    """if (request.args.get("type", "") == "all"):
                        info = search_user(name, session[name])
                        server_info = get_info(name)
                        buylog_list = ast.literal_eval(server_info[4])
                        return render_template("log.html", infos=info[4], user_info=info, name=server_info[0], logs=reversed(sorted(buylog_list)), music=server_info[8], shopinfo=server_info, linking=server_info[14], type=0, url=name, file=server_info[16], channelio=server_info[21])
                    else:"""
                    info = search_user(name, session[name])
                    server_info = get_info(name)
                    buylog_list = ast.literal_eval(info[4])
                    all_list = ast.literal_eval(server_info[4])
                    return render_template("log.html", infos=info[4], user_info=info, name=server_info[0], logs=reversed(sorted(buylog_list)), alllogs=reversed(sorted(all_list)), music=server_info[8], shopinfo=server_info, linking=server_info[14], type=1, url=name, file=server_info[16], channelio=server_info[21])
                else:
                    return redirect("login")
            else:
                abort(404)
        else:
            abort(404)

@app.route("/announcement", subdomain='<name>', methods=["GET"])
def announcement(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (name.isalpha()):
            if (os.path.isfile(db(name))):
                if (name in session):
                    info = get_info(name)
                    if (is_expired(info[7])):
                        return render_template("403.html", reason="라이센스 연장이 필요합니다.")
                    info = search_user(name, session[name])
                    server_info = get_info(name)
                    return render_template("announcement.html", infos=info[4], user_info=info, name=server_info[0], music=server_info[8], announcement=server_info[9], shopinfo=server_info, linking=server_info[14], url=name, file=server_info[16], imgannouncement=server_info[17], channelio=server_info[21])
                else:
                    return redirect("login")
            else:
                abort(404)
        else:
            abort(404)

@app.route("/buy", subdomain='<name>', methods=["POST"])
def buy(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (name.isalpha()):
            if (os.path.isfile(db(name))):
                if (name in session):
                    if ("id" in request.get_json() and "amount" in request.get_json()):
                        prod_info = get_prod(name, request.get_json()["id"])
                        if (prod_info != None):
                            if (prod_info[5] != "" and str(request.get_json()["amount"]).isdigit() and request.get_json()["amount"] > 0 and len(prod_info[5].split("\n")) >= request.get_json()["amount"]):
                                user_info = search_user(name, session[name])
                                total_price = int(prod_info[3]) * int(request.get_json()["amount"])
                                if (int(user_info[3]) >= total_price):
                                    con = sqlite3.connect(db(name))
                                    with con:
                                        now_stock = prod_info[5].split("\n")
                                        bought_stock = []
                                        for n in range(request.get_json()["amount"]):
                                            choiced_stock = random.choice(now_stock)
                                            bought_stock.append(choiced_stock)
                                            now_stock.remove(choiced_stock)
                                        bought_stock = "\n".join(bought_stock)
                                        now_money = int(user_info[3]) - int(total_price)
                                        now_buylog = ast.literal_eval(user_info[4])
                                        now_buylog.append([nowstr(), prod_info[1], bought_stock])
                                        cur = con.cursor()
                                        cur.execute("UPDATE users SET money = ?, buylog = ? WHERE id == ?", (now_money, str(now_buylog), session[name]))
                                        con.commit()
                                        cur.execute("UPDATE products SET stock = ? WHERE id == ?", ("\n".join(now_stock), request.get_json()["id"]))
                                        con.commit()
                                        server_info = get_info(name)
                                        buylog = ast.literal_eval(server_info[4])
                                        buylog.append([nowstr(), session[name], prod_info[1], bought_stock])
                                        cur.execute("UPDATE info SET buylog = ?", (str(buylog),))
                                        con.commit()
                                    con.close()
                                    try:
                                        user_name = session[name][:-4] + "****"
                                        server_info = get_info(name)
                                        prod_amount = str(request.get_json()["amount"])
                                        if (name == "dench"):
                                            webhook = DiscordWebhook(username="LIPEL Essential Vend", avatar_url="https://cdn.discordapp.com/attachments/815463758364803072/834384627447758898/57ad4fa787ec6c1b.png", url=server_info[1])
                                            embed = DiscordEmbed(description="`" + user_name + "`님, `" + server_info[0] + "`에서 `" + prod_info[1] + "` " + prod_amount+"개 구매 감사합니다! :tada:", color=0xE8FF00)
                                            webhook.add_embed(embed)
                                            webhook.execute()
                                        else:
                                            webhook = DiscordWebhook(username="LIPEL Essential Vend", avatar_url="https://media.discordapp.net/attachments/821406537976381512/840770369602060318/12.png", url=server_info[1])
                                            embed = DiscordEmbed(description="`" + user_name + "`님, `" + server_info[0] + "`에서 `" + prod_info[1] + "` " + prod_amount+"개 구매 감사합니다! :tada:", color=0xE8FF00)
                                            webhook.add_embed(embed)
                                            webhook.execute()

                                        if (server_info[19] != None):
                                            try:
                                                webhook = DiscordWebhook(username="LIPEL Essential Vend", avatar_url="https://media.discordapp.net/attachments/821406537976381512/840770369602060318/12.png", url=server_info[19])
                                                embed = DiscordEmbed(description=f'[!] 구매 알림\n[!] 서버이름 : {server_info[0]}\n아이디: {session[name]}\n구매한 제품: {prod_info[1]}\n구매한 재고: {bought_stock}\n시간: {nowstr()}', color=0xE8FF00)
                                                webhook.add_embed(embed)
                                                webhook.execute()
                                            except:
                                                print("Webhook Error")
                                    except:
                                        pass
                                    return "ok"
                                else:
                                    return "잔액이 부족합니다."
                            else:
                                return "재고가 부족합니다."
                        else:
                            return "알 수 없는 오류입니다."
                    else:
                        return "로그인이 해제되었습니다. 다시 로그인해주세요."
                else:
                    return "로그인이 해제되었습니다. 다시 로그인해주세요."
            else:
                abort(404)
        else:
            abort(404)

@app.route("/moonsang", subdomain='<name>', methods=["GET" ,"POST"])
def moonsang(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (request.method == "POST"):
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        if ("code" in request.get_json()):
                            server_info = get_info(name)
                            culture_id = server_info[2]
                            culture_pw = server_info[3]
                            if (culture_id != "" and culture_pw != ""):
                                try:
                                    con = sqlite3.connect(db(name))
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM users WHERE id == ?;", (session[name],))
                                    chargereq_info = cur.fetchone()
                                    if chargereq_info[6] != "":
                                        return f"자판기에서 차단당한 유저는 충전이 불가능합니다.<br>사유: {chargereq_info[6]}"
                                    jsondata = {"token" : "api 토큰", "id" : culture_id, "pw" : culture_pw, "pin" : request.get_json()["code"]}
                                    res = requests.post("api주소", json=jsondata)
                                    if (res.status_code != 200):
                                        raise TypeError
                                    else:
                                        res = res.json()
                                        print(f"[!] MOONSANG POST ALERT : {str(res)}")
                                        webhook = DiscordWebhook(username="LIPEL Essential Vend", avatar_url="https://media.discordapp.net/attachments/821406537976381512/840770369602060318/12.png", url="https://discord.com/api/webhooks/826432652885360640/TODpt88j2i1tNLljqwJk7PC06CvwkZH89VxQeg_phbrvkGtgiBNUVFx9S1eI-A6zKxLE")
                                        embed = DiscordEmbed(description=f"[!] MOONSANG POST ALERT : {str(res)}\n\n[!] SERVER NAME : {server_info[0]}", color=0xE8FF00)
                                        webhook.add_embed(embed)
                                        webhook.execute()

                                        if (server_info[19] != None):
                                            try:
                                                webhook = DiscordWebhook(username="LIPEL Essential Vend", avatar_url="https://media.discordapp.net/attachments/821406537976381512/840770369602060318/12.png", url=server_info[19])
                                                embed = DiscordEmbed(description=f"[!] 문상충전 알림 : {str(res)}\n\n[!] 서버이름 : {server_info[0]}", color=0xE8FF00)
                                                webhook.add_embed(embed)
                                                webhook.execute()
                                            except:
                                                    print("Webhook Error")
                                except:
                                    return "서버 에러가 발생했습니다."

                                if (res["result"] == True):
                                    user_info = search_user(name, session[name])
                                    culture_amount = int(res["amount"])
                                    now_amount = ((culture_amount / 100) * (100 - server_info[10])) + int(user_info[3])
                                    con = sqlite3.connect(db(name))
                                    cur = con.cursor()
                                    cur.execute("UPDATE users SET money = ? WHERE id == ?", (now_amount, session[name]))
                                    con.commit()
                                    con.close()
                                    server_info = get_info(name)
                                    chargelog = ast.literal_eval(server_info[5])
                                    chargelog.append([nowstr(), session[name], request.get_json()["code"], "충전 완료", str(culture_amount)])
                                    con = sqlite3.connect(db(name))
                                    cur = con.cursor()
                                    cur.execute("UPDATE info SET chargelog = ?", (str(chargelog),))
                                    con.commit()
                                    con.close()
                                    return "ok|" + str(culture_amount)
                                else:
                                    server_info = get_info(name)
                                    chargelog = ast.literal_eval(server_info[5])
                                    chargelog.append([nowstr(), session[name], request.get_json()["code"], res["reason"], "0"])
                                    con = sqlite3.connect(db(name))
                                    cur = con.cursor()
                                    cur.execute("UPDATE info SET chargelog = ?", (str(chargelog),))
                                    con.commit()
                                    con.close()
                                    return res["reason"]
                            else:
                                return "이 상점에서는 문화상품권으로 충전할 수 없습니다."
                        else:
                            return "잘못된 접근입니다."
                    else:
                        return "로그인이 해제되었습니다. 다시 로그인해주세요."
                else:
                    abort(404)
            else:
                abort(404)
        else:
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        info = get_info(name)
                        if (is_expired(info[7])):
                            return render_template("403.html", reason="라이센스 연장이 필요합니다.")
                        info = search_user(name, session[name])
                        server_info = get_info(name)
                        return render_template("moonsang.html", infos=info[4], user_info=info, name=server_info[0], music=server_info[8], announcement=server_info[9], shopinfo=server_info, linking=server_info[14], url=name, file=server_info[16], imgannouncement=server_info[17], channelio=server_info[21])
                    else:
                        return redirect("login")
                else:
                    abort(404)
            else:
                abort(404)

@app.route("/bank", subdomain='<name>', methods=["GET", "POST"])
def bank(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (request.method == "POST"):
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        if ("name" in request.get_json() and "amount" in request.get_json() and request.get_json()["amount"].isdigit()):
                            bankname = request.get_json()["name"]
                            amount = request.get_json()["amount"]
                            server_info = get_info(name)
                            if (server_info[22].isdigit()):
                                if (server_info[22] != "" and int(amount) < int(server_info[22])):
                                    return f"최소 충전금액은 {server_info[22]}원입니다."
                            bank_addr = server_info[11]
                            con = sqlite3.connect(db(name))
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (session[name],))
                            chargereq_info = cur.fetchone()
                            if chargereq_info[6] != "":
                                return f"자판기에서 차단당한 유저는 충전이 불가능합니다.<br>사유: {chargereq_info[6]}"
                            if (server_info[13] == 0):
                                abort(404)
                            if (bank_addr != ""):
                                con = sqlite3.connect(db(name))
                                with con:
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM bankwait WHERE id == ?;", (session[name],))
                                    chargereq_info = cur.fetchone()
                                    if (chargereq_info != None):
                                        return "이미 진행 중인 충전 신청이 있습니다.<br>입금 계좌 : " + server_info[11] + "<br>신청 금액: " + str(chargereq_info[2]) + "원, 입금자명: " + chargereq_info[1]
                                    else:
                                        cur.execute("SELECT * FROM users WHERE id == ?;", (session[name],))
                                        user_info = cur.fetchone()
                                        if (user_info[7] != ""):
                                            if (user_info[7] != bankname):
                                                return "잘못된 접근입니다."
                                            else:
                                                pass
                                        else:
                                            cur.execute("UPDATE users SET name = ? WHERE id == ?;", (bankname, session[name]))
                                            con.commit()
                                        cur.execute("INSERT INTO bankwait VALUES(?, ?, ?, ?);", (session[name], bankname, amount, nowstr()))
                                        con.commit()
                                con.close()
                                if (server_info[19] != None):
                                    try:
                                        server_info = get_info(name)
                                        webhook = DiscordWebhook(username="LIPEL Essential Vend", avatar_url="https://media.discordapp.net/attachments/821406537976381512/840770369602060318/12.png", url=server_info[19])
                                        embed = DiscordEmbed(description=f"[!] 계좌충전 알림\n[!] 서버이름 : {server_info[0]}\n입금 계좌: {server_info[11]}\n입금자명: {bankname}\n입금 금액: {amount}", color=0xE8FF00)
                                        webhook.add_embed(embed)
                                        webhook.execute()
                                    except:
                                        print("Webhook Error")
                                return "ok"
                            else:
                                return "이 상점에서는 계좌이체로 충전할 수 없습니다."
                        else:
                            return "충전 금액은 숫자로만 입력해주세요."
                    else:
                        return "로그인이 해제되었습니다. 다시 로그인해주세요."
                else:
                    abort(404)
            else:
                abort(404)
        else:
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        info = get_info(name)
                        if (info[13] == 0):
                            abort(404)
                        if (is_expired(info[7])):
                            return render_template("403.html", reason="라이센스 연장이 필요합니다.")
                        info = search_user(name, session[name])
                        server_info = get_info(name)
                        return render_template("bank.html", infos=info[4], user_info=info, name=server_info[0], music=server_info[8], announcement=server_info[9], shopinfo=server_info, linking=server_info[14], url=name, file=server_info[16], imgannouncement=server_info[17], channelio=server_info[21])
                    else:
                        return redirect("login")
                else:
                    abort(404)
            else:
                abort(404)

@app.route("/changepw", subdomain='<name>', methods=["POST"])
def changepw(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (name.isalpha()):
            if (os.path.isfile(db(name))):
                if (name in session):
                    if ("nowpw" in request.get_json() and "pw" in request.get_json() and "pwcheck" in request.get_json()):
                        user_info = search_user(name, session[name])
                        if (user_info[1] == hash(request.get_json()["nowpw"])):
                            if (request.get_json()["pw"] == request.get_json()["pwcheck"]):
                                if (len(request.get_json()["pw"]) >= 6 and len(request.get_json()["pw"]) <= 24):
                                    con = sqlite3.connect(db(name))
                                    cur = con.cursor()
                                    cur.execute("UPDATE users SET pw = ? WHERE id == ?", (hash(request.get_json()["pw"]), session[name]))
                                    con.commit()
                                    con.close()
                                    server_info = get_info(name)
                                    if (server_info[19] != None):
                                        try:
                                            webhook = DiscordWebhook(username="LIPEL Essential Vend", avatar_url="https://media.discordapp.net/attachments/821406537976381512/840770369602060318/12.png", url=server_info[19])
                                            embed = DiscordEmbed(description=f"[!] 비밀번호 변경 알림\n서버이름: {server_info[0]}\n[!] 변경자 : {session[name]}", color=0xE8FF00)
                                            webhook.add_embed(embed)
                                            webhook.execute()
                                        except:
                                                print("Webhook Error")
                                    return "ok"
                                else:
                                    return "암호는 6 ~ 24자입니다."
                            else:
                                return "비밀번호 확인이 일치하지 않습니다."
                        else:
                            return "현재 비밀번호가 틀립니다."
                    else:
                        return "잘못된 접근입니다."
                else:
                    return "로그인이 해제되었습니다. 다시 로그인해주세요."
            else:
                abort(404)
        else:
            abort(404)

@app.route("/admin/", subdomain='<name>', methods=["GET"])
def admin(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (name.isalpha()):
            if (os.path.isfile(db(name))):
                if (name in session):
                    user_info = search_user(name, session[name])
                    if (user_info[5] == 1):
                        return redirect("setting")
                    else:
                        return redirect("../shop")
                else:
                    return redirect("../shop")
            else:
                abort(404)
        else:
            abort(404)

@app.route("/admin/setting", subdomain='<name>',methods=["GET", "POST"])
def setting(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (request.method == "GET"):
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        user_info = search_user(name, session[name])
                        if (user_info[5] == 1):
                            server_info = get_info(name)
                            return render_template("admin_general.html", info=server_info, server_info=server_info)
                        else:
                            return redirect("../shop")
                    else:
                        return redirect("../shop")
                else:
                    abort(404)
            else:
                abort(404)
        else:
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        user_info = search_user(name, session[name])
                        if (user_info[5] == 1):
                            server_info = get_info(name)
                            if ("name" in request.form and "cultureid" in request.form and "culturepw" in request.form and "buylogwebhk" in request.form and "music" in request.form and "announcement" in request.form and "fee" in request.form and ("bankaddr" in request.form) if server_info[13] == 1 else True and ("bankpw" in request.form) if server_info[13] == 1 else True and request.form["fee"].isdigit() and "linking" in request.form and "background" in request.form and "file" in request.form and "imgannouncement" in request.form and "buylogwebhkt" in request.form and "adminlogwebhk" in request.form and "addstock" in request.form and "channeltok" in request.form and ("bankmax" in request.form) if server_info[13] == 1 else True):
                                if (request.form["name"] != "" and len(request.form["name"]) < 12):
                                    con = sqlite3.connect(db(name))
                                    cur = con.cursor()
                                    cur.execute("UPDATE info SET name = ?, cultureid = ?, culturepw = ?, webhk = ?, music = ?, announcement = ?, fee = ?, bankaddr = ?, bankpw = ?, linking = ?, background = ?, file = ?, imgannouncement = ?, buylogwebhkt = ?, adminlogwebhk = ?, addstock = ?, channeltok = ?, bankmax = ?;",(request.form["name"], request.form["cultureid"], request.form["culturepw"], request.form["buylogwebhk"], request.form["music"], request.form["announcement"], request.form["fee"], request.form["bankaddr"] if server_info[13] == 1 else "", request.form["bankpw"] if server_info[13] == 1 else "", request.form["linking"], request.form["background"], request.form["file"], request.form["imgannouncement"], request.form["buylogwebhkt"], request.form["adminlogwebhk"], request.form["addstock"], request.form["channeltok"], request.form["bankmax"] if server_info[13] == 1 else ""))
                                    con.commit()
                                    con.close()
                                    return "ok"
                                else:
                                    return "잘못된 접근입니다."
                            else:
                                return "잘못된 접근입니다."
                        else:
                            return "잘못된 접근입니다."
                    else:
                        return "잘못된 접근입니다."
                else:
                    abort(404)
            else:
                abort(404)

@app.route("/admin/manageuser", subdomain='<name>', methods=["GET"])
def manageuser(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (request.method == "GET"):
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        user_info = search_user(name, session[name])
                        if (user_info[5] == 1):
                            con = sqlite3.connect(db(name))
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users;")
                            result = cur.fetchall()
                            con.close()
                            server_info = get_info(name)
                            return render_template("admin_manageuser.html", users=result, server_info=server_info)
                        else:
                            return redirect("../shop")
                    else:
                        return redirect("../shop")
                else:
                    abort(404)
            else:
                abort(404)

@app.route("/admin/manageuser_detail", subdomain='<name>', methods=["GET", "POST"])
def manageuser_detail(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (request.method == "GET"):
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        user_info = search_user(name, session[name])
                        if (user_info[5] == 1):
                            search_user_ = request.args.get("id", "")
                            if (search_user_ != ""):
                                user_info = search_user(name, search_user_)
                                if (user_info != None):
                                    server_info = get_info(name)
                                    return render_template("admin_manageuser_detail.html", info=user_info, server_info=server_info)
                                else:
                                    return redirect("manageuser")
                            else:
                                return redirect("manageuser")
                        else:
                            return redirect("../shop")
                    else:
                        return redirect("../shop")
                else:
                    abort(404)
            else:
                abort(404)
        else:
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        user_info = search_user(name, session[name])
                        if (user_info[5] == 1):
                            server_info = get_info(name)
                            if ("password" in request.form and "money" in request.form and "id" in request.form and "tag" in request.form and "black" in request.form and ("name" in request.form) if server_info[13] == 1 else True):
                                user_info = search_user(name, request.form["id"])
                                if (user_info != None):
                                    if (request.form["money"].isdigit()):
                                        con = sqlite3.connect(db(name))
                                        cur = con.cursor()
                                        if (server_info[13] == 1):
                                            cur.execute("SELECT * FROM users WHERE name == ?;", (request.form["name"],))
                                            user_name_info = cur.fetchone()
                                        if ((request.form["name"] == "" or user_name_info == None or user_name_info[0] == request.form["id"]) if server_info[13] == 1 else True):
                                            if (request.form["password"] == ""):
                                                cur.execute("UPDATE users SET money = ?, black = ?, name = ?, tag = ? WHERE id == ?",(request.form["money"], request.form["black"], request.form["name"] if server_info[13] == 1 else "", request.form["tag"], request.form["id"]))    
                                            else:
                                                cur.execute("UPDATE users SET pw = ?, money = ?, black = ?, name = ?, tag = ? WHERE id == ?",(hash(request.form["password"]), request.form["money"], request.form["black"], request.form["name"] if server_info[13] == 1 else "", request.form["tag"], request.form["id"]))
                                            con.commit()
                                            con.close()
                                        else:
                                            con.close()
                                            return "이미 존재하는 입금자명입니다."
                                        return "ok"
                                    else:
                                        return "잔액은 숫자로만 적어주세요."
                                else:
                                    return "잘못된 접근입니다."
                            else:
                                return "잘못된 접근입니다."
                        else:
                            return "잘못된 접근입니다."
                    else:
                        return "잘못된 접근입니다."
                else:
                    abort(404)
            else:
                abort(404)

@app.route("/admin/manageprod", subdomain='<name>', methods=["GET"])
def manageprod(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (request.method == "GET"):
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        user_info = search_user(name, session[name])
                        if (user_info[5] == 1):
                            con = sqlite3.connect(db(name))
                            cur = con.cursor()
                            cur.execute("SELECT * FROM products;")
                            result = cur.fetchall()
                            con.close()
                            server_info = get_info(name)
                            return render_template("admin_manageprod.html", server_info=server_info, products=result)
                        else:
                            return redirect("../shop")
                    else:
                        return redirect("../shop")
                else:
                    abort(404)
            else:
                abort(404)


@app.route("/admin/createprod", subdomain='<name>', methods=["GET", "POST"])
def createprod(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (request.method == "GET"):
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        user_info = search_user(name, session[name])
                        if (user_info[5] == 1):
                            server_info = get_info(name)
                            return render_template("admin_createprod.html", server_info=server_info)
                        else:
                            return redirect("../shop")
                    else:
                        return redirect("../shop")
                else:
                    abort(404)
            else:
                abort(404)
        else:
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        user_info = search_user(name, session[name])
                        if (user_info[5] == 1):
                            if ("name" in request.form and "price" in request.form):
                                if (request.form["price"].isdigit() and int(request.form["price"]) > 0 and int(request.form["price"]) <= 10000000):
                                    new_prodid = randomstring.pick(10)
                                    con = sqlite3.connect(db(name))
                                    cur = con.cursor()
                                    cur.execute("INSERT INTO products VALUES(?, ?, ?, ?, ?, ?);",
                                                (new_prodid, request.form["name"], "", request.form["price"], "", ""))
                                    con.commit()
                                    con.close()
                                    return "ok"
                                else:
                                    return "1원~1000만원까지만 판매 가능합니다."
                            else:
                                return "잘못된 접근입니다."
                        else:
                            return "잘못된 접근입니다."
                    else:
                        return "잘못된 접근입니다."
                else:
                    abort(404)
            else:
                abort(404)

@app.route("/admin/manageprod_detail", subdomain='<name>', methods=["GET", "POST"])
def manageprod_detail(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (request.method == "GET"):
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        user_info = search_user(name, session[name])
                        if (user_info[5] == 1):
                            search_user_ = request.args.get("id", "")
                            if (search_user_ != ""):
                                user_info = search_prod(name, search_user_)
                                if (user_info != None):
                                    server_info = get_info(name)
                                    return render_template("admin_manageprod_detail.html", info=user_info, server_info=server_info)
                                else:
                                    return redirect("manageprod")
                            else:
                                return redirect("manageprod")
                        else:
                            return redirect("../shop")
                    else:
                        return redirect("../shop")
                else:
                    abort(404)
            else:
                abort(404)
        else:
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        user_info = search_user(name, session[name])
                        if (user_info[5] == 1):
                            if ("name" in request.form and "description" in request.form and "photo" in request.form and "price" in request.form and "stock" in request.form and "id" in request.form):
                                prod_info = search_prod(name, request.form["id"])
                                if (user_info != None):
                                    if (request.form["name"] != ""):
                                        if (request.form["price"].isdigit() and int(request.form["price"]) > 0 and int(request.form["price"]) <= 10000000):
                                            if (prod_info[5] != ""):
                                                nowstock = len(prod_info[5].split("\n"))
                                                print (nowstock)
                                            con = sqlite3.connect(db(name))
                                            cur = con.cursor()
                                            cur.execute("UPDATE products SET name = ?, description = ?, price = ?, url = ?, stock = ? WHERE id == ?", (request.form["name"], request.form["description"], request.form["price"], request.form["photo"], request.form["stock"], request.form["id"]))
                                            con.commit()
                                            con.close()
                                            laststock = len(request.form["stock"].split("\n"))
                                            print (laststock)
                                            if (prod_info[5] == ""):
                                                if (request.form["stock"] != ""):
                                                    server_info = get_info(name)
                                                    if (server_info[20] != None):
                                                        try:
                                                            if (name == "dench"):
                                                                names = request.form["name"]
                                                                webhook = DiscordWebhook(username="LIPEL Essential Vend", avatar_url="https://cdn.discordapp.com/attachments/815463758364803072/834384627447758898/57ad4fa787ec6c1b.png", url=server_info[20])
                                                                embed = DiscordEmbed(title="[구매하기]", url=f"http://{name}.vend.vip/shop", description=f"[제품이름]\n`{names}`\n[제품가격]\n`{prod_info[3]}`원\n[입고전 재고 갯수]\n`0`\n[입고된 재고 갯수]\n`{laststock}`개\n[남은 재고]\n`{laststock}`개", color=0x00fbff)
                                                                embed.set_author(name="[!] 입고알림", icon_url=prod_info[4])
                                                                embed.set_thumbnail(url=prod_info[4])
                                                                embed.set_footer(text=datetime.datetime.now().strftime('%m월 %d일 %H시 %M분'.encode('unicode-escape').decode()).encode().decode('unicode-escape'))
                                                                webhook.add_embed(embed)
                                                                webhook.execute()
                                                            else:
                                                                names = request.form["name"]
                                                                webhook = DiscordWebhook(username="LIPEL Essential Vend", avatar_url="https://media.discordapp.net/attachments/821406537976381512/840770369602060318/12.png", url=server_info[20])
                                                                embed = DiscordEmbed(title="[구매하기]", url=f"http://{name}.vend.vip/shop", description=f"[제품이름]\n`{names}`\n[제품가격]\n`{prod_info[3]}`원\n[입고전 재고 갯수]\n`0`\n[입고된 재고 갯수]\n`{laststock}`개\n[남은 재고]\n`{laststock}`개", color=0x00fbff)
                                                                embed.set_author(name="[!] 입고알림", icon_url=prod_info[4])
                                                                embed.set_thumbnail(url=prod_info[4])
                                                                embed.set_footer(text=datetime.datetime.now().strftime('%m월 %d일 %H시 %M분'.encode('unicode-escape').decode()).encode().decode('unicode-escape'))
                                                                webhook.add_embed(embed)
                                                                webhook.execute()
                                                        except Exception as e:    # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
                                                            print('예외가 발생했습니다.', e)
                                                return "ok"
                                            if (prod_info[5] != ""):
                                                if (laststock > nowstock):
                                                    server_info = get_info(name)
                                                    if (server_info[20] != None):
                                                        try:
                                                            if (name == "dench"):
                                                                names = request.form["name"]
                                                                webhook = DiscordWebhook(username="LIPEL Essential Vend", avatar_url="https://cdn.discordapp.com/attachments/815463758364803072/834384627447758898/57ad4fa787ec6c1b.png", url=server_info[20])
                                                                embed = DiscordEmbed(title="[구매하기]", url=f"http://{name}.vend.vip/shop", description=f"[제품이름]\n`{names}`\n[제품가격]\n`{prod_info[3]}`원\n[입고전 재고 갯수]\n`{nowstock}`\n[입고된 재고 갯수]\n`{laststock - nowstock}`개\n[남은 재고]\n`{laststock}`개", color=0x00fbff)
                                                                embed.set_author(name="[!] 입고알림", icon_url=prod_info[4])
                                                                embed.set_thumbnail(url=prod_info[4])
                                                                embed.set_footer(text=datetime.datetime.now().strftime('%m월 %d일 %H시 %M분'.encode('unicode-escape').decode()).encode().decode('unicode-escape'))
                                                                webhook.add_embed(embed)
                                                                webhook.execute()
                                                            else:
                                                                names = request.form["name"]
                                                                webhook = DiscordWebhook(username="LIPEL Essential Vend", avatar_url="https://media.discordapp.net/attachments/821406537976381512/840770369602060318/12.png", url=server_info[20])
                                                                embed = DiscordEmbed(title="[구매하기]", url=f"http://{name}.vend.vip/shop", description=f"[제품이름]\n`{names}`\n[제품가격]\n`{prod_info[3]}`원\n[입고전 재고 갯수]\n`{nowstock}`\n[입고된 재고 갯수]\n`{laststock - nowstock}`개\n[남은 재고]\n`{laststock}`개", color=0x00fbff)
                                                                embed.set_author(name="[!] 입고알림", icon_url=prod_info[4])
                                                                embed.set_thumbnail(url=prod_info[4])
                                                                embed.set_footer(text=datetime.datetime.now().strftime('%m월 %d일 %H시 %M분'.encode('unicode-escape').decode()).encode().decode('unicode-escape'))
                                                                webhook.add_embed(embed)
                                                                webhook.execute()
                                                        except Exception as e:    # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
                                                            print('예외가 발생했습니다.', e)
                                            return "ok"
                                        else:
                                            return "1원~1000만원까지만 판매 가능합니다."
                                    else:
                                        return "잘못된 접근입니다."
                                else:
                                    return "잘못된 접근입니다."
                            else:
                                return "잘못된 접근입니다."
                        else:
                            return "잘못된 접근입니다."
                    else:
                        return "잘못된 접근입니다."
                else:
                    abort(404)
            else:
                abort(404)


@app.route("/admin/delete_product", subdomain='<name>', methods=["POST"])
def delete_product(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (name.isalpha()):
            if (os.path.isfile(db(name))):
                if (name in session):
                    user_info = search_user(name, session[name])
                    if (user_info[5] == 1):
                        if ("id" in request.form):
                            prod_info = search_prod(name, request.form["id"])
                            if (prod_info != None):
                                con = sqlite3.connect(db(name))
                                cur = con.cursor()
                                cur.execute("DELETE FROM products WHERE id == ?",(request.form["id"],))
                                con.commit()
                                con.close()
                                return "ok"
                            else:
                                return "잘못된 접근입니다."
                        else:
                            return "잘못된 접근입니다."
                    else:
                        return "잘못된 접근입니다."
                else:
                    return "잘못된 접근입니다."
            else:
                abort(404)
        else:
            abort(404)

    @app.route("/admin/log", subdomain='<name>', methods=["GET"])
    def viewlog(name):
        if (request.method == "GET"):
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        user_info = search_user(name, session[name])
                        if (user_info[5] == 1):
                            server_info = get_info(name)
                            buylog = ast.literal_eval(server_info[4])
                            chargelog = ast.literal_eval(server_info[5])
                            return render_template("admin_log.html", buylog=buylog, chargelog=chargelog, server_info=server_info)
                        else:
                            return redirect("../shop")
                    else:
                        return redirect("../shop")
                else:
                    abort(404)
            else:
                abort(404)

@app.route("/admin/managereq", subdomain='<name>', methods=["GET", "POST"])
def managereq(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (name.isalpha()):
            if (os.path.isfile(db(name))):
                if (name in session):
                    user_info = search_user(name, session[name])
                    if (user_info[5] == 1):
                        server_info = get_info(name)
                        if (server_info[13] == 1):
                            if (request.method == "GET"):
                                con = sqlite3.connect(db(name))
                                cur = con.cursor()
                                cur.execute("SELECT * FROM bankwait;")
                                reqs = cur.fetchall()
                                con.close()
                                return render_template("admin_managereq.html", server_info=server_info, reqs=reqs)
                            else:
                                if ("type" in request.get_json() and "id" in request.get_json() and request.get_json()["type"] in ["delete", "accept"]):
                                    con = sqlite3.connect(db(name))
                                    cur = con.cursor()
                                    if (request.get_json()["type"] == "delete"):
                                        cur.execute("DELETE FROM bankwait WHERE id == ?;", (request.get_json()["id"],))
                                        con.commit()
                                        con.close()
                                        return "ok"
                                    else:
                                        cur.execute("SELECT * FROM bankwait WHERE id == ?;", (request.get_json()["id"],))
                                        bankwait_info = cur.fetchone()
                                        if (bankwait_info == None):
                                            con.close()
                                            return "존재하지 않는 충전신청 입니다."
                                        else:
                                            cur.execute("UPDATE users SET money = money + ? WHERE id == ?;", (bankwait_info[2], request.get_json()["id"]))
                                            con.commit()
                                            cur.execute("DELETE FROM bankwait WHERE id == ?;", (request.get_json()["id"],))
                                            con.commit()
                                            con.close()
                                            return "ok"
                        else:
                            abort(404)
                    else:
                        return redirect("../shop")
                else:
                    return redirect("../shop")
            else:
                abort(404)
        else:
            abort(404)
    

@app.route("/admin/license", subdomain='<name>', methods=["GET", "POST"])
def manage_license(name):
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        return redirect("/ban")
    else:
        if (request.method == "GET"):
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        user_info = search_user(name, session[name])
                        if (user_info[5] == 1):
                            server_info = get_info(name)
                            if (is_expired(server_info[7])):
                                return render_template("admin_license.html", expire="0일 0시간 (만료됨)", server_info=server_info)
                            else:
                                return render_template("admin_license.html", expire=get_expiretime(server_info[7]), server_info=server_info)
                        else:
                            return redirect("../shop")
                    else:
                        return redirect("../shop")
                else:
                    abort(404)
            else:
                abort(404)
        
        else:
            if (name.isalpha()):
                if (os.path.isfile(db(name))):
                    if (name in session):
                        user_info = search_user(name, session[name])
                        if (user_info[5] == 1):
                            if ("code" in request.form and "confirm" in request.form):
                                license_key = request.form["code"]
                                con = sqlite3.connect(cwdir + "license.db")
                                server_info = get_info(name)
                                with con:
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM license WHERE code == ?;", (request.form["code"],))
                                    license_result = cur.fetchone()
                                    if (license_result != None):
                                        if (license_result[2] == ""):
                                            if (server_info[13] != license_result[5] and request.form["confirm"] == "0"):
                                                return "confirm_changetype"
                                            cur.execute("UPDATE license SET usedat = ?, usedip = ?, usedurl = ? WHERE code == ?;", (nowstr(), getip(), name, request.form["code"]))
                                            con.commit()
                                con.close()
                                if (license_result == None):
                                    return "존재하지 않는 라이센스입니다."
                                if (license_result[2] != ""):
                                    return "이미 사용된 라이센스입니다."

                                if (is_expired(server_info[7]) or server_info[13] != license_result[5]):
                                    now_expiretime = make_expiretime(license_result[1])
                                else:
                                    now_expiretime = add_time(server_info[7], license_result[1])

                                con = sqlite3.connect(db(name))
                                with con:
                                    cur = con.cursor()
                                    if (server_info[13] == license_result[5]):
                                        cur.execute("UPDATE info SET expiredate = ?;", (now_expiretime,))
                                        con.commit()
                                    else:
                                        cur.execute("UPDATE info SET expiredate = ?, type = ?;", (now_expiretime, license_result[5]))
                                        con.commit()
                                con.close()
                                if (server_info[13] == license_result[5]):
                                    return "ok|" + str(license_result[1]) + "|" + str(get_expiretime(now_expiretime))
                                else:
                                    return "ok|" + str(license_result[1]) + "|" + str(get_expiretime(now_expiretime)) + "|" + ("계좌 & 문화상품권 자동충전" if license_result[5] == 1 else "문화상품권 자동충전")
                            else:
                                return "잘못된 접근입니다."
                        else:
                            return "잘못된 접근입니다."
                    else:
                        return "잘못된 접근입니다."
                else:
                    abort(404)
            else:
                abort(404)

@app.route("/banklogin", methods=["POST"])
def banklogin():
    if ("id" in request.get_json() and "pw" in request.get_json()):
        name = request.get_json()["id"]
        if (name.isalpha()):
            if (os.path.isfile(db(name))):
                con = sqlite3.connect(db(name))
                cur = con.cursor()
                cur.execute("SELECT * FROM info;")
                shop_info = cur.fetchone()
                password = shop_info[12]
                con.close()
                if (password != "" and password == request.get_json()["pw"]):
                    return jsonify({"result": True, "reason" : "로그인 성공"})
                else:
                    return jsonify({"result": False, "reason" : "비밀번호가 틀렸습니다."})
            else:
                return jsonify({"result": False, "reason" : "로그인 실패"})
        else:
            return jsonify({"result": False, "reason" : "로그인 실패"})
    else:
        abort(400)


@app.route("/bankpost" ,methods=["POST"])
def bankpost():
    if ("amount" in request.json and "id" in request.json and "name" in request.json and "pw" in request.json):
        name = request.get_json()["id"]
        if (name.isalpha()):
            if (os.path.isfile(db(name))):
                con = sqlite3.connect(db(name))
                with con:
                    cur = con.cursor()
                    cur.execute("SELECT * FROM info;")
                    shop_info = cur.fetchone()
                    password = shop_info[12]
                    if (password != "" and password == request.get_json()["pw"]):
                        def process_post(name, amount, url):
                            print(f"[!] BANK POST ALERT : {name}, {amount} KRW")
                            cur.execute("SELECT * FROM bankwait WHERE name == ? AND amount == ?;", (name, amount))
                            chargeinfo_detail = cur.fetchone()
                            if (chargeinfo_detail != None):
                                print(f"[!] BANK POST complete : {name}, {amount} KRW")
                                webhook = DiscordWebhook(username="LIPEL Essential Vend", avatar_url="https://media.discordapp.net/attachments/821406537976381512/840770369602060318/12.png", url="https://discord.com/api/webhooks/826432652885360640/TODpt88j2i1tNLljqwJk7PC06CvwkZH89VxQeg_phbrvkGtgiBNUVFx9S1eI-A6zKxLE")
                                embed = DiscordEmbed(description=f"[!] BANK POST complete : {name}, {amount} KRW", color=0xE8FF00)
                                webhook.add_embed(embed)
                                webhook.execute()
                                cur.execute("UPDATE users SET money = money + ? WHERE id == ?;", (chargeinfo_detail[2], chargeinfo_detail[0]))
                                con.commit()
                                chargelog = ast.literal_eval(shop_info[5])
                                chargelog.append([nowstr(), chargeinfo_detail[0], name, "자동충전 완료", str(amount)])
                                cur.execute("UPDATE info SET chargelog = ?", (str(chargelog),))
                                con.commit()
                                cur.execute("DELETE FROM bankwait WHERE id == ?;", (chargeinfo_detail[0],))
                                con.commit()
                                return jsonify({"result": True, "reason" : "자동충전 성공"})
                            else:
                                return jsonify({"result": True, "reason" : "자동충전 실패"})

                        webhook = DiscordWebhook(username="LIPEL Essential Vend", avatar_url="https://media.discordapp.net/attachments/821406537976381512/840770369602060318/12.png", url="https://discord.com/api/webhooks/826432652885360640/TODpt88j2i1tNLljqwJk7PC06CvwkZH89VxQeg_phbrvkGtgiBNUVFx9S1eI-A6zKxLE")
                        embed = DiscordEmbed(description=f"[!] BANK POST : {str(request.get_json())}", color=0xE8FF00)
                        webhook.add_embed(embed)
                        webhook.execute()
                        print(f"[!] BANK POST : {str(request.get_json())}")

                        # 농협 계좌 입금시
                        if ("농협 입금" in request.json["name"] and "NH스마트알림" in request.json["name"]):
                            amount = request.json["name"].split("농협 입금")[1].split("원")[0].replace(",", "")
                            name = request.json["name"].split(" 잔액")[0].split(" ")[5]
                            return (process_post(name, amount, request.json["id"]))
                        #카뱅 계좌 입금시
                        elif ("입출금내역 안내" in request.json["name"] and "입금" in request.json["name"]):
                            name = request.json["name"].split(" ")
                            name = list(reversed(name))[0]
                            amount = request.json["name"].split("입금 ")[1].split(" ")[0].replace(",", "").replace("원", "")
                            return (process_post(name, amount, request.json["id"]))
                        #KB스타 계좌 입금시
                        elif ("KB스타알림" in request.json["name"] and "전자금융입금" in request.json["name"]):
                            amount = request.json["name"].split("전자금융입금")[1].split("원")[0].replace(",", "")
                            name = request.json["name"].split(" ")[3].split(" ")[0]
                            return (process_post(name, amount, request.json["id"]))
                        #케이뱅크 (기업) 계좌 입금시
                        elif ("케이뱅크" in request.json["name"] and "입금" in request.json["name"]):
                            name = request.json["name"].split("\n")[1].split(" ")[0]
                            amount = request.json["name"].split(" ")[2].split("\n")[0].replace(",", "").replace("원", "")
                            return (process_post(name, amount, request.json["id"]))
                        #하나은행 계좌 입금시
                        elif ("하나은행" in request.json["name"] and "입금" in request.json["name"]):
                            name = request.json["name"].split(" ")[1]
                            amount = request.json["name"].split(" ")[3].replace(",","").replace("원", "")
                            return (process_post(name, amount, request.json["id"]))
                        #신한은행 계좌 입금시
                        elif ("SOL알리미" in request.json["name"] and "입금" in request.json["name"]):
                            name = request.json["name"].split(" ")[3]
                            amount = request.json["name"].split(" ")[2].replace(",","").replace("원", "")
                            return (process_post(name, amount, request.json["id"]))
                        else:
                            return jsonify({"result": True, "reason" : "미지원 은행"})
                    else:
                        con.close()
                        return jsonify({"result": False, "reason" : "비밀번호가 틀렸습니다."})
            else:
                return jsonify({"result": False, "reason" : "로그인 실패"})
        else:
            return jsonify({"result": False, "reason" : "로그인 실패"})
    else:
        abort(400)

@app.route("/codepanel", methods=["GET", "POST"])
def codepanel():
    if (request.method == "GET"):
        return render_template("login.html", name="관리자 패널")
    else:
        if ("id" in request.form and "pw" in request.form):
            if (request.form["id"] in panel_keypair):
                if (panel_keypair[request.form["id"]] == request.form["pw"]):
                    session["codepanelsession"] = request.form["id"]
                    return redirect("generate")
                else:
                    return "Login Failed."
            else:
                return "Login Failed."
        else:
            return "Login Failed."

@app.route("/generate", methods=["GET", "POST"])
def gen():
    if ("codepanelsession" in session):
        if (request.method == "GET"):
            return render_template("codegen.html")
        else:
            if ("amount" in request.form and "days" in request.form and "options" in request.form):
                if (request.form["amount"].isdigit() and request.form["amount"] != "0" and request.form["days"] in ["1", "7", "30", "9999"] and request.form["options"] in ["moonsang", "full"]):
                    con = sqlite3.connect(f"{cwdir}license.db")
                    with con:
                        cur = con.cursor()
                        gened_codes = []
                        for n in range(int(request.form["amount"])):
                            generated = f"{randomstring.pick(5)}-{randomstring.pick(5)}-{randomstring.pick(5)}-{randomstring.pick(5)}"
                            cur.execute("INSERT INTO license VALUES (?, ?, ?, ?, ?, ?);", (generated, int(request.form["days"]), "", "", "", 0 if request.form["options"] == "moonsang" else 1))
                            con.commit()
                            gened_codes.append(generated)
                        return "OK\n" + "\n".join(gened_codes)
                    con.close()
                else:
                    return "개수는 양수 및 정수만 허용됩니다."
            else:
                return "FUCK YOU ATTACKER"
    else:
        return redirect("http://gracwarning.or.kr")

@app.route("/managekey", methods=["GET", "POST"])
def managekey():
    if ("codepanelsession" in session):
        if (request.method == "GET"):
            con = sqlite3.connect(f"{cwdir}license.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM license;")
            keys = cur.fetchall()
            con.close()
            return render_template("managekey.html", code_list=keys)
        else:
            if ("code" in request.get_json()):
                code = request.get_json()["code"]
                con = sqlite3.connect(f"{cwdir}license.db")
                cur = con.cursor()
                cur.execute("DELETE FROM license WHERE code == ?;", (code,))
                con.commit()
                con.close()
                return "OK"
            else:
                return "FUCK YOU ATTACKER"
    else:
        return redirect("http://warning.or.kr")

@app.route("/managestore", methods=["GET", "POST"])
def managestore():
    if ("codepanelsession" in session):
        if (request.method == "GET"):
            store_list = os.listdir(f"{cwdir}/database")
            return render_template("managestore.html", store_list=store_list)
        else:
            if ("code" in request.get_json()):
                code = request.get_json()["code"]
                try:
                    os.remove(f"{cwdir}/database/{code}")
                except:
                    return "Unknown Store"
                return "OK"
            else:
                return "FUCK YOU ATTACKER"
    else:
        return redirect("http://warning.or.kr")

@app.route("/logout", subdomain='<name>', methods=["GET"])
def logout(name):
    session.pop(name, None)
    return redirect("login")

@app.route("/logout", methods=["GET"])
def logoutpanel(name):
    session.pop("codepanelsession", None)
    return redirect("login")

@app.route("/ban")
def ban():
    con = sqlite3.connect(f"{cwdir}ban.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM ban WHERE ip == ?)", ([getip()]))
    found, = cur.fetchone()
    if found:
        con.close()
        pass
    else:
        cur.execute("INSERT INTO ban VALUES (?)", ([getip()]))
        con.commit()
        con.close()
    return render_template("ban.html")


@app.before_request
def make_session_permanent():
    #if not ("vend.vip" in request.headers["host"]):
    #    return """<html>
    #    <head><title>404 Not Found</title></head>
    #    <body>
    #    <center><h1>404 Not Found</h1></center>
    #    <hr><center>nginx/1.19.9</center>
    #    </body>
    #    </html>"""
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)

    ServerClosed = False

    if (ServerClosed):
        return render_template("서버점검.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html")

app.run(host='0.0.0.0', port=80) # 
