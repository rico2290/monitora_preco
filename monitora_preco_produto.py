import smtplib, requests, sys
from bs4 import BeautifulSoup
from smtplib import SMTPException
import schedule, time

url = 'https://www.amazon.com.br/dp/B07KQWZTVG/ref=asc_df_B07KQWZTVG1561503600000/\
    ?creative=380333&creativeASIN=B07KQWZTVG&linkCode=asn&tag=zoom1p-20'
cabecalho = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) \
            Gecko/20100101 Firefox/67.0'}
user = 'rico220990@gmail.com'
password = 'zecipeskllmocqwc'

def verifica_preco_produto():
    try:
        print('Tentativa de conexão...')
        pagina = requests.get(url, headers=cabecalho)
        soup = BeautifulSoup(pagina.content, 'html.parser')
        titulo = (soup.find(id='productTitle').get_text()).strip()
        preco_produto = (soup.find(id='priceblock_ourprice').get_text().strip())
        parte_float = float(soup.find(id='priceblock_ourprice').get_text().strip()[2:7])
        
        if (parte_float > 2.000):
            print('Preço baixou!!!')
            print(' {0} ==> {1} '.format(titulo,preco_produto))
            enviar_email()
           

    except requests.exceptions.HTTPError as  err:
        print(err)
        sys.exit()
    except requests.exceptions.Timeout:
        print('Esgotado tempo de requisição')
    # print(soup.prettify().encode('utf-8')) 
 

def enviar_email():
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(user, password=password)
        subject = 'Corre!!! o preço baixou 😱 ' # 
        body = 'Acesse 👉 {url} '#.format(url)
        message = f'Subject: {subject}\n\n{body}'

        server.sendmail(
            from_addr = 'rico220990@gmail.com',
            to_addrs = 'ricorjl85@hotmail.com',
            msg=message
        )
        print('Email enviado com sucesso!!!')
    
    except SMTPException as e:
        print('Erro: Não foi possível enviar email: {}'.format(e))
    server.quit()

verifica_preco_produto()
#Executar a cada 2 minuto
# schedule.every(2).minutes.do(verifica_preco_produto).tag('pesquisa-na-amazon')
