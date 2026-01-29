import http.server
import socketserver
import os

# Port du serveur
PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # On récupère le chemin du fichier sur ton Mac
        path = self.translate_path(self.path)
        
        # 1. SI LE FICHIER N'EXISTE PAS (Les trous)
        # On renvoie "Vide" (204) pour que la carte ne plante pas
        if self.path.endswith('.pbf') and not os.path.exists(path):
            self.send_response(204)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            return

        # 2. SI LE FICHIER EXISTE (La soupe bleue)
        # On l'envoie en disant qu'il est ZIPPÉ (GZIP)
        if self.path.endswith('.pbf') and os.path.exists(path):
            self.send_response(200)
            self.send_header('Content-type', 'application/x-protobuf')
            self.send_header('Access-Control-Allow-Origin', '*')
            
            # --- C'EST CETTE LIGNE QUI REGLE LE PROBLEME ---
            self.send_header('Content-Encoding', 'gzip') 
            # -----------------------------------------------
            
            self.end_headers()
            with open(path, 'rb') as f:
                self.wfile.write(f.read())
            return
        
        # Pour les fichiers normaux (HTML, CSS)
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

print(f"Serveur GZIP lancé sur http://localhost:{PORT}")
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()