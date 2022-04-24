import socket
from enum import Enum
import urwid


class Place(Enum):
    ANTARCTICA = "Antártica"
    DEATHVALLEY = "Vale da Morte"
    SAARADESERT = "Deserto do Saara"


PLACES = ["Antártica", "Vale da Morte", "Deserto do Saara"]

HOST = "127.0.0.1"
PORT = 65432


def request_station(choice):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Conectando ao servidor", file =  open('client_log.txt','a'))
        s.connect((HOST, PORT))
        print(f"Enviando requisição da temperatura de {choice} para o servidor", file =  open('client_log.txt','a'))
        s.sendall(Place(choice).name.encode())
        data = s.recv(1024)
        item_chosen(choice, data.decode())


def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', loading, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def loading(button, choice):
    print("------------------------------------------------------------------------", file =  open('client_log.txt','a'))
    message = urwid.Text([u'Loading...'])
    main.original_widget = urwid.Filler(message)
    request_station(choice)


def item_chosen(place, temperature):
    print(f"Temperatura recebida do servidor para {place}: {temperature}ºC", file =  open('client_log.txt','a'))
    response = urwid.Text([u'A temperatura em ', place, u' é: ', temperature, u'ºC\n'])
    done = urwid.Button(u"Ok")
    urwid.connect_signal(done, 'click', restart_menu)
    main.original_widget = urwid.Filler(urwid.Pile([response,
                                                    urwid.AttrMap(done, None, focus_map='reversed')]))


def restart_menu(button):
    main_menu = urwid.Padding(menu(u'Selecione a Estação desejada', PLACES), left=2, right=2)
    main.original_widget = main_menu


main = urwid.Padding(menu(u'Selecione a Estação desejada', PLACES), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                    align='center', width=('relative', 60),
                    valign='middle', height=('relative', 60),
                    min_width=20, min_height=9)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
