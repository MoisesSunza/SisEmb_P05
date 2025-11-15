def parse_http_request(request):
    lines = request.split('\r\n')
    
    request_line = lines[0]
    method, path, version = request_line.split(' ')
    
    headers = {}
    i = 1
    while i < len(lines) and lines[i] != '':
        if ':' in lines[i]:
            key, value = lines[i].split(':', 1)
            headers[key.strip()] = value.strip()
        i += 1
    
    body = ''
    if i + 1 < len(lines):
        body = '\r\n'.join(lines[i + 1:])
    
    return {
        'method': method,
        'path': path,
        'version': version,
        'headers': headers,
        'body': body
    }


def send_http_response(status_code, content, content_type='text/plain'):
    status_messages = {
        200: 'OK',
        201: 'Created',
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        500: 'Internal Server Error'
    }
    
    content_bytes = content.encode('utf-8')
    content_length = len(content_bytes)
    
    response = f"HTTP/1.1 {status_code} {status_messages.get(status_code, 'Unknown')}\r\n"
    response += f"Content-Type: {content_type}\r\n"
    response += f"Content-Length: {content_length}\r\n"
    response += "\r\n"
    response += content
    
    return response