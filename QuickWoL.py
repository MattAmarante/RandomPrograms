import sys
import socket
import re

def get_local_ip():
    """
    Restituisce l'indirizzo IP locale della macchina.
    Se non è possibile determinarlo, restituisce "127.0.0.1".
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1)) # Connessione a un IP non raggiungibile per ottenere il proprio indirizzo locale
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    finally:
        s.close()

    return local_ip

def validate_mac_address(mac: str) -> str:
    """
    Controlla se la stringa 'mac' rappresenta un MAC address valido.
    Se il MAC non è valido o è "FF:FF:FF:FF:FF:FF" (indirizzo broadcast),
    la funzione restituisce una stringa vuota.
    Altrimenti ritorna il MAC address in formato maiuscolo.
    """

    mac_upper = mac.upper()
    # Verifica se è l'indirizzo broadcast
    if mac_upper == "FF:FF:FF:FF:FF:FF":
        return ""
    
    # Verifica che il MAC segua il formato tipico: XX:XX:XX:XX:XX:XX
    pattern = r"^(?:[0-9A-F]{2}:){5}[0-9A-F]{2}$"
    if re.fullmatch(pattern, mac_upper):
        return mac_upper
    
    return ""

def create_magic_packet(mac: str, dest_ip: str) -> bytes:
    """
    Crea un magic packet per il Wake-on-LAN destinato all'indirizzo IP specificato.
    
    Parametri:
      mac      -> MAC address di destinazione (formato "XX:XX:XX:XX:XX:XX")
      dest_ip  -> indirizzo IP al quale il pacchetto verrà inviato (tipicamente l'indirizzo di broadcast)
    
    Ritorna:
      Il magic packet come sequenza di byte. Se il MAC non è valido, ritorna una sequenza vuota.
    
    Il magic packet è composto da 6 byte 0xFF seguiti da 16 ripetizioni del MAC address in byte.
    """

    valid_mac = validate_mac_address(mac)
    if not valid_mac:
        return b""
    
    # Rimuove i due punti e converte il MAC in bytes
    mac_bytes = bytes.fromhex(valid_mac.replace(":", ""))
    # Crea il magic packet: 6 byte di 0xFF seguiti da 16 ripetizioni del MAC address
    packet = b'\xff' * 6 + mac_bytes * 16
    return packet

def main():
    default_mac = "10:7C:61:61:84:8F"
    if len(sys.argv) == 1:
        mac_arg = default_mac
        print(f"Nessun MAC address fornito, uso default: {default_mac}")
    elif len(sys.argv) == 2:
        mac_arg = sys.argv[1]
    else:
        sys.stderr.write("Usage: {} [MAC_ADDRESS]\n".format(sys.argv[0]))
        sys.exit(1)
    
    packet = create_magic_packet(mac_arg, "192.168.1.255")
    if not packet:
        sys.stderr.write("MAC address non valido.\n")
        sys.exit(1)
    
    # Creazione della socket UDP in modalità broadcast
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Invio del magic packet alla porta 9 sull'indirizzo di broadcast
        sock.sendto(packet, ("192.168.1.255", 9))
        print("Magic packet inviato a 192.168.1.255:9")
    except Exception as e:
        sys.stderr.write("Errore durante l'invio del magic packet: {}\n".format(e))
        sys.exit(1)
    finally:
        sock.close()

if __name__ == "__main__":
    main()