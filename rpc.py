"""Shared functions for client-server rpc"""
import pickle


# which functions are available for rpc
functions = {
}

# marshalling of dat: text -> function calls, and result -> text
def pack_procedure(name, *args):
    """Convert a procedure call to bytes"""
    package = {
        'name': name,
        'args': args
    }
    return pickle.dumps(package)

def unpack_procedure(data):
    """Unpack the bytes into a function name and list of args"""
    package = pickle.loads(data)
    return package['name'], package['args']

def  pack_result(value):
    """Convert a result value into bytes"""
    package = {
        'result': value
    }
    return pickle.dumps(package)

def unpack_result(data):
    """Convert bytes into a result"""
    package = pickle.loads(data)
    return package['result']

# evaluate procedure
def evaluate_procedure(name, args):
    if name in functions:
        func = functions[name]
        result = func(*args)
        return result
    
    else:
        return "Error: Unknown function" + name 
    
# Transport Layer
def send_msg(sock, data: bytes):
    """Send length-prefixed bytes over a socket"""
    length = len(data)
    sock.sendall(length.to_bytes(4, 'big') + data)
 
def recv_msg(sock) -> bytes:
    """Receive length-prefixed bytes from a socket"""
    raw_len = _recv_exact(sock, 4)
    length = int.from_bytes(raw_len, 'big')
    return _recv_exact(sock, length)
 
def _recv_exact(sock, n) -> bytes:
    """Read exactly n bytes from socket"""
    buf = b''
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError('Socket closed')
        buf += chunk
    return buf
