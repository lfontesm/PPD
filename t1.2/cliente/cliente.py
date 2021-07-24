import xmlrpc.client

connection_ = xmlrpc.client.ServerProxy('http://localhost:8000')
print(f'Recebi do servidor: {connection_.oi_meu_bom()}')