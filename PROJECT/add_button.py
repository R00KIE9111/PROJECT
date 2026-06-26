import os

folder = r'c:\Users\rooki\Downloads\Proyecto\PROJECT\PROJECT\templates'
files = ['asignaciones.html', 'equipos.html', 'eventos.html', 'historial.html', 
         'mis_asignaciones.html', 'mis_equipos.html', 'mis_historiales.html', 
         'servicio.html', 'sucursales.html', 'usuarios.html']

link_html = '\n    <div style="margin: 10px 0;"><a href="{{ url_for(\'index\') }}" style="padding: 8px 15px; background: #007bff; color: white; text-decoration: none; border-radius: 4px;">&larr; Volver a Inicio</a></div>\n'

for f_name in files:
    path = os.path.join(folder, f_name)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<body>' in content and 'Volver a Inicio' not in content:
        content = content.replace('<body>', f'<body>{link_html}', 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

print('Done adding buttons')
