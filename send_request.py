import socket

def realizar_request(ruta, token=None):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect(('localhost', 8080))
        
        request = f'GET {ruta} HTTP/1.1\r\n'
        request += 'Host: localhost\r\n'
        
        if token:
            request += f'Authorization: Bearer {token}\r\n'
        
        request += '\r\n'
        
        client_socket.send(request.encode())
        
        response = client_socket.recv(4096).decode()
        print(response)
        
        return response
        
    except ConnectionRefusedError:
        print("Error: No se pudo conectar al servidor. Asegúrate de que esté ejecutándose.")
    except Exception as e:
        print(f"Error en la petición: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    print("Acceso sin endpoint")
    realizar_request('/')
    
    print("\nAcceso con endpoint api_hora")
    realizar_request('/api_hora')
    
    print("\nAcceso con endpoint /admin sin token")
    realizar_request('/admin')
    
    print("\nAcceso con endpoint /admin con token incorrecto")
    realizar_request('/admin', token='9999')
    
    print("\nAcceso con endpoint /admin con token correcto")
    realizar_request('/admin', token='1234')
    
    print("\nEndpoint que no existe")
    realizar_request('/hola_mundo')