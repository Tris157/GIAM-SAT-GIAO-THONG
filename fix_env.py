import os

env_path = 'Backend/.env'
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if 'RTSP_URL=' in line and 'Quangnam$ioc2020' in line and 'Quangnam\\$ioc2020' not in line:
            line = line.replace('Quangnam$ioc2020', 'Quangnam\\$ioc2020')
            print(f"Fixed RTSP_URL in .env")
        new_lines.append(line)
        
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
else:
    print(f"Error: {env_path} not found")
