from bs4 import BeautifulSoup
import requests
import urllib
from urllib.parse import quote
import re

url = "http://baixarquadrinhos.com/Hq-Quadrinho/ler-online-quadrinho-thanos-18-donny-cates-ou-baixar-em-cbr-e-pdf/"
def get_link_downloads(url):
    page = requests.get(url)
    page_soup = BeautifulSoup(page.content, 'html.parser')
    value = page_soup.find(attrs={'class': 'links-download'})
    links = []
    for val in value:
        if val.name != None and val['href'][0] == 'h':
            links.append(val['href'])
    return links


def lista():
    url = 'http://baixarquadrinhos.com/'
    tag = 'menu-item-object-custom'
    page = requests.get(url)
    page_soup = BeautifulSoup(page.content, 'html.parser')
    value = page_soup.find_all("ul", class_="menu")[1]
    value = value.find_all('a')
    links = []
    for link in value:
        links.append(link['href'])
    print(links)
    return links


def downloads_collection(url):
    page = requests.get(url)
    page_soup = BeautifulSoup(page.content, 'html.parser')
    # = page_soup.find(attrs={'class': 'menu'})
    links = []
    value = page_soup.find_all("h2", class_="su-post-title")
    for link in value:
        links.append(link.a['href'])

    links = sorted(links)
    for indexI in range(0,len(links)):
        print(indexI, '>', links[indexI])
    return links

def show_disp(lista):
    names_uni = []
    for indexI in range(0,len(lista)):
        name = lista[indexI].replace('http://baixarquadrinhos.com/', '').replace('-', ' ')
        name = name.upper().replace('QUADRINHO', '').replace('HQ','').replace('LER', '')
        name = name.replace(' EM ','').replace(' OU ', '').replace(' E ', '')
        name = name.replace('ONLINE', '').replace('MANGA', '').replace('EM CBR E PDF', '')
        name = name.replace('BAIXAR', '').replace('CBR','')
        name = name.replace('PDF','').replace('/', '')
        print('> ', indexI, '---', name)
        names_uni.append(name)
    return names_uni

def download_cbr(url, file_name):
    print(url)
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    url = quote(url.replace("http://", ""))
    url = f"http://{url}"
    urllib.request.urlretrieve(url,'downloads/'+file_name.strip().replace(" ", "")+'.cbr')
    print('downloads/'+file_name+'.cbr')


def show_content(lista):
    pattern = re.compile(r'(http:\/\/baixarquadrinhos.com\/)((ler)(-hq|-manga|-online|-onlline)(-quadrinho|-online))')
    names = []
    for indexI in range(0,len(lista)):
        value = re.search(pattern,lista[indexI])
        if value == None:
            name = lista[indexI].replace('http://baixarquadrinhos.com/', '').upper().replace('CATEGORIAS', '').replace(' ', '-').replace('/', '')
            print('> ', indexI, '---', name)
            names.append(name)
        else:
            regex_remove= str(value.group())
            name = lista[indexI].replace(regex_remove, '').replace('-', ' ').upper().replace('EM CBR E PDF', '').replace('BAIXAR', '').replace('/', '').replace(' OU ', '').replace(' ', '-')
            print('> ', indexI, '---', name)
            names.append(name)
        
    return names


        #print('> ', indexI, '---', lista[indexI])

def main():
    repositories = lista()
    names = show_content(repositories)
    print('Digite o numero referente para Download')
    print('USO:')
    value_input = int(input())
    print(repositories[value_input])
    conteudos_disp = downloads_collection(repositories[value_input])
    names = show_disp(conteudos_disp)

    
    print('DESEJA BAIXAR TUDO: Y/n')
    value_input = str(input())
    if(value_input.upper() == 'Y'):
        for indexI in range(0, len(conteudos_disp)):
            download_cbr(get_link_downloads(conteudos_disp[indexI])[0], names[indexI])
    else:    
        value_input = int(input('Digite o numero referente para Baixar'))
        print(conteudos_disp[value_input])
        print(names[value_input])
    


def help_use():
    print('----------------------------------')
    print('')
main()
