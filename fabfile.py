import os,sys,logging,time
from fabric.api import env,local,run,sudo,put,cd,lcd,puts,task,get,hide
from fabric.operations import local as lrun, run
from fabric.state import env
from settings import BUCKET_NAME
import data
from settings import USER,private_key,HOST
env.user = USER
env.key_filename = private_key
env.hosts = [HOST,]

SKIP = """
adrijana-dejanovic
agnes-buzala
agnes-sokolowska
agyness-deyn
ai-tominaga
alana-bunte
alessandra-albrecht
alexandra-agoston
alexandra-spencer
alexa-yudina
alice-rausch
alina-baikova
aline-weber
alison-nix
ali-stephens
alize-barange
alla-kostromichova
allyson-ally-ertel
amanda-ware
anais-mali
andressa-fontana
andzelika-buivydaite
aneta-pajak
anja-leuenberger
anna-arendshorst
anna-grostina
anna-jagodzinska
anna-piirainen
annemarije-rus
annemijn-dijs
astrid-holler
athena-wilson
auguste-abeliunaite
bambi-northwood--blyth
brenda-kranz
brynja-j%C3%B3nbjarnard%C3%B3ttir
caitlin-lomax
camille-rowe
candice-swanepoel
carolina-thaler
caroline-brasch-nielsen
chloe-norgaard
claire-granlund
clarine-de-jonge
constance-jablonski
crystal-noreiga
dafne-cejas
dalianah-arekion
daria-pilnitskaya
daria-werbowy
darla-baker
deimante-misiunaite
diana-dondoe
diana-gartner
diana-moldovan
drielly-oliveira
eleonore-toulin
elettra-rossellini-wiedemann
elianne-smit
elise-crombez
eliza-sys
ellen-danes
elsa-sylvan
elyse-saunders
emilia-nilsson
emma-maclaren
enly-tammela
ernesta-petkeviciute
fanny-francois
georgia-may-jagger
georgie-wass
grace-hartzel
hanna-verhees
hanne-gaby-odiele
hedvig-palm
heidi-mount
heidi-verster
helena-magone
henrietta-hellberg
ieva-birzina
ilze-bajare
ines-crnokrak
inga-eiriksdottir
ioanna-ntenti
isabeli-fontana
isabella-farrell
isabella-melo
iveta-bogdane
iza-olak
jada-joyce
jamilla-hoogenboom
jana-wieland
jeanne-cadieu
jeisa-chiminazzo
jemma-baines
jenny-sweeney
jessiann-gravel-beland
jiaye-wu
joan-smalls
johanna-wahlberg
jules-mordovets
julia-johansen
katarina-ivanovska
katarina-ivanovska/.DS_Store
kate-ellery
kate-king
kate-kosushkina
katerina-netolicka
katryn-kruger
kat-shandruk
katy-dron
kelie-santos
kelley-ash
kelly-mittendorf
kerstin-mannik
kim-noorda
kirstin-kragh-liljegren
kristina-tsirekidze
kristina-tsvetkova
kristine-zandmane
laima-andersone
lara-mullen
lara-stone_ii
laura-julie
lauren-rippingham
lia-pavlova
lien-vieira
liliana-dominguez
lily-zhi
linda-vojtova
lin-kjerulf
list.txt
lone-praesto
louise-pedersen
lucie-von-alten
mackenzie-drazan
maddie-kulicka
maddison-brown
madison-headrick
magda-laguinge
maggie-laine
maria-borges_iii
maria-bradley
mariacarla-boscono
maria-palm
marihenny-rivera
mariya-markina
marthe-van-stuijvenberg
megan-mcnierney
meghan-collison
melodie-monrose
michelle-van-bijnen
michelle-zwaal
mila-krasnoiarova
mila-mihaljcic
mimmi-soderstrom
monika-sawicka
montana-cox
naemi-schink
nastya-zhidkikh
natalia-semanova
noa-vermeer
noelle-roques
noreen-carmody
nova-malanova
nyasha-matonhodze
olga-maliouk
ophelie-rupp
patrycja-gardygajlo
paulina-heiler
querelle-jansen
ranya-mordanova
romee-strijd
romee-strijd/romee_strijd_8053510.jpg
romina-lanaro
romina-lanaro/3057948.jpg
roos-van-bosstraeten
rose-cordero
ros-georgiou
ruby-jean-wilson
sadie-newman
sanne-nijhof
sasha-antonowskaia
sasha-pivovarova
saskia-de-brauw
serafima-kobzeva
sonya-gorelova
sophie-srej
sophie-touchet
stella-tennant
stina-rapp-wastenson
sui-he
suzie-bird
taja-feistner
tania-balash%21
thairine-garcia
thaisa-liz
ubah-hassan
ugne-andrikonyte
vala-thorsteinsson
valentina-zelyaeva
valeriane-le-moi
vanessa-moody
veneda-budny
vita-sidorkina
waleska-gorczevski
xiao-wen-ju
yana-karpova
yana-van-ginneken
zuzanna-stankiewicz
"""

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='logs/fab.log',
                    filemode='a')


@task
def notebook_server():
    """
    Run IPython notebook on an AWS server
    run("openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.key -out mycert.pem")
    c = get_config()
    c.NotebookApp.open_browser = False
    c.NotebookApp.ip = '0.0.0.0'
    c.NotebookApp.port = 8888
    c.NotebookApp.certfile = u'/home/ubuntu/mycert.pem'
    c.NotebookApp.enable_mathjax = False
    c.NotebookApp.password = u'{}'
    :return:
    """
    from IPython.lib.security import passwd
    sudo("/home/ubuntu/anaconda/bin/ipython notebook --ip=0.0.0.0  --NotebookApp.password={} --no-browser".format(passwd())) #--certfile=mycert.pem


@task
def notebook():
    """
    deactivate
    pip freeze > requirements.txt
    local("sudo port select --set python python27")
    local("sudo port select --set ipython ipython27")
    local("sudo port select --set pip pip27")
    local("sudo port select --set virtualenv virtualenv27")
    :return:
    """
    local("ipython-2.7 notebook")


@task
def setup():
    """
        install Tensorflow
        /Users/aub3/.ssh/cs5356
    """
    run("/home/ubuntu/anaconda/bin/pip install https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.6.0-cp27-none-linux_x86_64.whl")
    run("/home/ubuntu/anaconda/bin/pip install --upgrade fabric")
    run("/home/ubuntu/anaconda/bin/pip install --upgrade boto3")
    run("/home/ubuntu/anaconda/bin/pip install --upgrade dlib")
    run("/home/ubuntu/torch/install/bin/luarocks install dpnn")
    run("/home/ubuntu/torch/install/bin/luarocks install nn")
    run("/home/ubuntu/torch/install/bin/luarocks install image")
    run("/home/ubuntu/torch/install/bin/luarocks install torch")
    sudo("apt-get update")
    sudo("apt-get install -y awscli")
    upload()


@task
def download():
    get("/home/ubuntu/crfasrnn/","crfasrnn")

@task
def freeze():
    local("source ~/portenv/bin/activate;pip freeze >> requirements.txt")


@task
def connect():
    """
    Creates connect.sh for the current host
    :return:
    """
    fh = open("connect.sh",'w')
    fh.write("#!/bin/bash\n"+"ssh -i "+env.key_filename+" "+"ubuntu"+"@"+HOST+"\n")
    fh.close()

@task
def backup():
    get("/tmp/*.png",".")

@task
def upload():
    try:
        sudo("rm -rf workspace")
        run("mkdir workspace")
    except:
        pass
    put("*.py","workspace/")
    put("*.md","workspace/")
    put("*.ipynb","workspace/")
    put("*.sh","workspace/")
    for d in filter(os.path.isdir, os.listdir('.')):
        if not d.startswith('.'):
            put("{}".format(d),"workspace/")


@task
def preprocess():
    # sudo("apt-get install -y parallel")
    # run("mkdir images")
    # with cd("images"):
    #     for line in SKIP.split("\n"):
    #         if line.strip():
    #             run("mkdir {}".format(line.strip()))
    dataset = data.Dataset()
    for count,name in dataset.sorted():
        skip = False
        logging.info("starting {} {}".format(name,count))
        with cd("images"):
            try:
                run("mkdir {}".format(name))
            except:
                skip = True
                logging.info("skipping {}".format(name))
            if not skip:
                with cd("{}".format(name)):
                    logging.info("downloading {}".format(name))
                    with hide('output'):
                        run("aws s3 cp s3://aub3data/models/{} . --recursive --region \"us-east-1\"".format(name))
                    logging.info("renaming {}".format(name))
                    run('for f in * ; do mv "$f" "{}_$f" ; done'.format(name.replace('-','_')))
                    logging.info("resizing {}".format(name))
                    try:
                        with hide('output'):
                            run('find -iname "*.jpg" -type f -print0 | parallel --progress -0 -j +0 "mogrify -resize \'500x500\'"')
                        logging.info("finished {}".format(name))
                    except:
                        logging.info("Error while resizing {}".format(name))
                        pass
                    logging.info("Uploading started {}".format(name))
                    with hide('output'):
                        run('aws s3 mv ../{} s3://aub3data/dataset/ --recursive --region "us-east-1"'.format(name)) # run("find . -iname '*.jpg' -exec mv --target-directory ../dataset/ {} +")
                    logging.info("Uploading finished {}".format(name))

