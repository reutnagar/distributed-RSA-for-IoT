import socket
#import dbus

# def show_message(title, message):
#     bus = dbus.SessionBus()
#     object = bus.get_object("org.gnome.Tomboy", "/org/gnome/Tomboy/RemoteControl")
#     tomboy = dbus.Interface(object, "org.gnome.Tomboy.RemoteControl")

#     note = tomboy.CreateNamedNote(title)
#     tomboy.SetNoteContents(note , message)
#     tomboy.AddTagToNote(note,title)
#     tomboy.DisplayNote(note)

def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    my_socket.bind(('',8881))

    print 'start service ...'

    while True :
        message , address = my_socket.recvfrom(8192)
        print 'message %s from : %s' % ( str(message), address[0])
        #show_message('message from :'+ str(address[0]) , message)

if __name__ == "__main__" :
    main()
