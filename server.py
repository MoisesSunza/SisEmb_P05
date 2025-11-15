import socket
from datetime import datetime
from http_parser import parse_http_request, send_http_response

def start_server():
    token_admin="1234"
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    host = '0.0.0.0'
    port = 8080
    
    socket_server.bind((host, port))
    socket_server.listen(5)
    
    def extraer_token(headers):
        header_auth = headers.get('Authorization', '')
        if header_auth.startswith('Bearer '):
            return header_auth[7:]
        return None
    
    def handler_path(path, headers):
        if path == "/":
            return send_http_response(200, "Hola mundo desde handler")
        
        elif path == "/api_hora":
            hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return send_http_response(200, f"Hora actual: {hora_actual}")
        
        elif path == "/admin":
            token = extraer_token(headers)
            
            if token is None:
                return send_http_response(401, "No autorizado por token requerido")
            
            if token == token_admin:
                return send_http_response(200, "Acceso autorizado al panel de administración")
            else:
                return send_http_response(403, "Acceso denegado por token inválido")
            
        return send_http_response(404, "path no encontrada")
    
    try:
        print(f"Servidor iniciado en {host}:{port}")
        while True:
            client_socket, client_address = socket_server.accept()
            print(f"Conexión exitosa con: {client_address}")
            
            request_data = client_socket.recv(1024).decode('utf-8')
            
            parsed = parse_http_request(request_data)
            
            print(parsed)
            print(f"path de la petición: {parsed.get('path')}")
            
            response = handler_path(parsed.get('path'), parsed.get('headers', {}))
            
            client_socket.send(response.encode('utf-8'))
            client_socket.close()
    
    except KeyboardInterrupt:
        print("\nApagando servidor")
    finally:
        socket_server.close()

if __name__ == "__main__":
    import os
    token = "1234"
    start_server(token_admin=token)