import http.client
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.options |= ssl.OP_LEGACY_SERVER_CONNECT
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE


def get_html(host, path):
    connection = http.client.HTTPSConnection(host, context=context)
    connection.request("GET", path)
    response = connection.getresponse()
    content = response.read().decode()
    connection.close()
    return content
