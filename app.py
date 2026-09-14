from flask import Flask, render_template_string, request
import json

app = Flask(__name__)

# Paleta de colores empresariales formales
COLORS = {
    'primary': '#1a3a52',      # Azul oscuro profesional
    'secondary': '#2c5aa0',    # Azul medio
    'accent': '#ff6b35',       # Naranja para acentos
    'light_bg': '#f5f7fa',     # Gris muy claro
    'dark_text': '#1a1a1a',    # Negro texto
    'light_text': '#6b7280',   # Gris texto
    'success': '#10b981',      # Verde
    'warning': '#f59e0b'       # Ámbar
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Oil & Gas Analytics - Dashboard Profesional</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary: """ + COLORS['primary'] + """;
            --secondary: """ + COLORS['secondary'] + """;
            --accent: """ + COLORS['accent'] + """;
            --light-bg: """ + COLORS['light_bg'] + """;
            --dark-text: """ + COLORS['dark_text'] + """;
            --light-text: """ + COLORS['light_text'] + """;
            --success: """ + COLORS['success'] + """;
            --warning: """ + COLORS['warning'] + """;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--light-bg) 0%, #ffffff 100%);
            color: var(--dark-text);
            line-height: 1.6;
        }

        /* ========== HEADER ========== */
        .navbar {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            padding: 1rem 2rem;
            box-shadow: 0 4px 20px rgba(26, 58, 82, 0.15);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .navbar-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .navbar-logo {
            font-size: 1.8rem;
            font-weight: 700;
            color: white;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .navbar-logo i {
            color: var(--accent);
            font-size: 2rem;
        }

        .navbar-menu {
            display: flex;
            gap: 2rem;
        }

        .navbar-link {
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            font-weight: 500;
            position: relative;
            transition: var(--transition);
        }

        .navbar-link::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 2px;
            background: var(--accent);
            transition: var(--transition);
        }

        .navbar-link:hover {
            color: white;
        }

        .navbar-link:hover::after {
            width: 100%;
        }

        /* ========== HERO SECTION ========== */
        .hero {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 50%, var(--primary) 100%);
            color: white;
            padding: 4rem 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            opacity: 0.1;
            animation: drift 20s infinite linear;
        }

        @keyframes drift {
            0%, 100% { transform: translateX(0); }
            50% { transform: translateX(50px); }
        }

        .hero-content {
            max-width: 800px;
            margin: 0 auto;
            position: relative;
            z-index: 2;
            animation: slideInDown 0.8s ease-out;
        }

        @keyframes slideInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .hero h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            font-weight: 800;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }

        .hero p {
            font-size: 1.25rem;
            margin-bottom: 2rem;
            opacity: 0.95;
        }

        /* ========== BUTTONS ========== */
        .btn {
            display: inline-block;
            padding: 0.875rem 2rem;
            border-radius: 0.5rem;
            text-decoration: none;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: var(--transition);
            position: relative;
            overflow: hidden;
            font-size: 1rem;
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }

        .btn:hover::before {
            width: 300px;
            height: 300px;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--accent) 0%, #ff8c42 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(255, 107, 53, 0.4);
        }

        .btn-secondary {
            background: var(--secondary);
            color: white;
            box-shadow: 0 4px 15px rgba(44, 90, 160, 0.3);
        }

        .btn-secondary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(44, 90, 160, 0.4);
        }

        .btn-outline {
            border: 2px solid white;
            background: transparent;
            color: white;
            margin-left: 1rem;
        }

        .btn-outline:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-2px);
        }

        /* ========== MAIN CONTAINER ========== */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        .section-title {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 2rem;
            color: var(--primary);
            position: relative;
            padding-bottom: 1rem;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 60px;
            height: 4px;
            background: linear-gradient(90deg, var(--accent) 0%, transparent 100%);
            border-radius: 2px;
        }

        /* ========== CARDS ========== */
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }

        .card {
            background: white;
            border-radius: 0.75rem;
            overflow: hidden;
            box-shadow: 0 2px 12px rgba(26, 58, 82, 0.08);
            transition: var(--transition);
            cursor: pointer;
            position: relative;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--accent), var(--secondary));
            transform: scaleX(0);
            transform-origin: left;
            transition: var(--transition);
            z-index: 2;
        }

        .card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 32px rgba(26, 58, 82, 0.15);
        }

        .card:hover::before {
            transform: scaleX(1);
        }

        .card-header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .card-header::after {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.1), transparent);
            border-radius: 50%;
        }

        .card-icon {
            font-size: 3rem;
            margin-bottom: 0.5rem;
            display: inline-block;
            position: relative;
            z-index: 1;
            transition: var(--transition);
        }

        .card:hover .card-icon {
            transform: scale(1.1) rotate(5deg);
            filter: drop-shadow(0 4px 8px rgba(255, 107, 53, 0.3));
        }

        .card-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            position: relative;
            z-index: 1;
        }

        .card-body {
            padding: 1.5rem;
        }

        .card-text {
            color: var(--light-text);
            margin-bottom: 1.5rem;
            line-height: 1.8;
        }

        .card-footer {
            padding: 0 1.5rem 1.5rem;
            display: flex;
            gap: 0.5rem;
        }

        .card-link {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--secondary);
            text-decoration: none;
            font-weight: 600;
            transition: var(--transition);
            padding: 0.5rem 1rem;
            border-radius: 0.3rem;
        }

        .card-link:hover {
            color: var(--accent);
            background: var(--light-bg);
            padding-left: 1.5rem;
        }

        /* ========== FEATURES SECTION ========== */
        .features {
            background: var(--light-bg);
            padding: 3rem 2rem;
            border-radius: 1rem;
            margin-bottom: 3rem;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
        }

        .feature {
            display: flex;
            gap: 1rem;
            padding: 1.5rem;
            background: white;
            border-radius: 0.5rem;
            transition: var(--transition);
        }

        .feature:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 15px rgba(26, 58, 82, 0.1);
        }

        .feature-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, var(--accent) 0%, #ff8c42 100%);
            border-radius: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5rem;
            flex-shrink: 0;
        }

        .feature-content h3 {
            margin-bottom: 0.5rem;
            color: var(--primary);
        }

        .feature-content p {
            color: var(--light-text);
            font-size: 0.95rem;
        }

        /* ========== STATS ========== */
        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }

        .stat-box {
            background: white;
            padding: 2rem;
            border-radius: 0.75rem;
            text-align: center;
            box-shadow: 0 2px 12px rgba(26, 58, 82, 0.08);
            transition: var(--transition);
            border-left: 4px solid transparent;
        }

        .stat-box:hover {
            border-left-color: var(--accent);
            transform: translateY(-4px);
        }

        .stat-number {
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--accent);
            margin-bottom: 0.5rem;
        }

        .stat-label {
            color: var(--light-text);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 1px;
        }

        /* ========== FOOTER ========== */
        footer {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: rgba(255, 255, 255, 0.9);
            padding: 3rem 2rem 1rem;
            text-align: center;
            margin-top: 4rem;
        }

        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }

        .footer-section h4 {
            margin-bottom: 1rem;
            color: white;
        }

        .footer-section p, .footer-section a {
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            transition: var(--transition);
            display: block;
            margin: 0.5rem 0;
        }

        .footer-section a:hover {
            color: var(--accent);
            padding-left: 0.5rem;
        }

        .footer-bottom {
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding-top: 2rem;
        }

        /* ========== RESPONSIVE ========== */
        @media (max-width: 768px) {
            .navbar-menu {
                flex-direction: column;
                gap: 1rem;
            }

            .hero h1 {
                font-size: 2rem;
            }

            .btn-outline {
                margin-left: 0;
                display: block;
                margin-top: 1rem;
            }

            .cards-grid {
                grid-template-columns: 1fr;
            }
        }

        /* ========== ANIMATIONS ========== */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .card {
            animation: fadeInUp 0.6s ease-out forwards;
        }

        .card:nth-child(1) { animation-delay: 0.1s; }
        .card:nth-child(2) { animation-delay: 0.2s; }
        .card:nth-child(3) { animation-delay: 0.3s; }
        .card:nth-child(4) { animation-delay: 0.4s; }
    </style>
</head>
<body>
    <!-- NAVBAR -->
    <nav class="navbar">
        <div class="navbar-container">
            <div class="navbar-logo">
                <i class="fas fa-oil-can"></i>
                Oil & Gas Analytics
            </div>
            <div class="navbar-menu">
                <a href="#" class="navbar-link">Dashboard</a>
                <a href="#" class="navbar-link">Análisis</a>
                <a href="#" class="navbar-link">Reportes</a>
                <a href="#" class="navbar-link">Contacto</a>
            </div>
        </div>
    </nav>

    <!-- HERO SECTION -->
    <section class="hero">
        <div class="hero-content">
            <h1>Plataforma de Análisis Empresarial</h1>
            <p>Transformamos datos en decisiones estratégicas para la industria energética</p>
            <button class="btn btn-primary" onclick="handleClick('primary')">
                <i class="fas fa-chart-line"></i> Comenzar Análisis
            </button>
            <button class="btn btn-outline" onclick="handleClick('outline')">
                <i class="fas fa-info-circle"></i> Más Información
            </button>
        </div>
    </section>

    <!-- MAIN CONTENT -->
    <div class="container">
        <!-- STATS -->
        <h2 class="section-title">Métricas Clave</h2>
        <div class="stats-container">
            <div class="stat-box" onclick="animateStat(this)">
                <div class="stat-number">150+</div>
                <div class="stat-label">Campos Analizados</div>
            </div>
            <div class="stat-box" onclick="animateStat(this)">
                <div class="stat-number">85%</div>
                <div class="stat-label">Precisión de Datos</div>
            </div>
            <div class="stat-box" onclick="animateStat(this)">
                <div class="stat-number">2.4M</div>
                <div class="stat-label">Registros Procesados</div>
            </div>
            <div class="stat-box" onclick="animateStat(this)">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Monitoreo Continuo</div>
            </div>
        </div>

        <!-- FEATURES -->
        <h2 class="section-title">Características Principales</h2>
        <div class="features">
            <div class="features-grid">
                <div class="feature">
                    <div class="feature-icon">
                        <i class="fas fa-database"></i>
                    </div>
                    <div class="feature-content">
                        <h3>Base de Datos Robusta</h3>
                        <p>Almacenamiento seguro y escalable de todos tus datos</p>
                    </div>
                </div>
                <div class="feature">
                    <div class="feature-icon">
                        <i class="fas fa-brain"></i>
                    </div>
                    <div class="feature-content">
                        <h3>Análisis Inteligente</h3>
                        <p>Modelos predictivos con IA avanzada</p>
                    </div>
                </div>
                <div class="feature">
                    <div class="feature-icon">
                        <i class="fas fa-shield-alt"></i>
                    </div>
                    <div class="feature-content">
                        <h3>Seguridad Empresarial</h3>
                        <p>Cumplimiento de estándares internacionales</p>
                    </div>
                </div>
                <div class="feature">
                    <div class="feature-icon">
                        <i class="fas fa-chart-pie"></i>
                    </div>
                    <div class="feature-content">
                        <h3>Visualizaciones Avanzadas</h3>
                        <p>Gráficos interactivos y dashboards personalizados</p>
                    </div>
                </div>
                <div class="feature">
                    <div class="feature-icon">
                        <i class="fas fa-sync-alt"></i>
                    </div>
                    <div class="feature-content">
                        <h3>Actualización en Tiempo Real</h3>
                        <p>Sincronización automática de datos</p>
                    </div>
                </div>
                <div class="feature">
                    <div class="feature-icon">
                        <i class="fas fa-headset"></i>
                    </div>
                    <div class="feature-content">
                        <h3>Soporte Dedicado</h3>
                        <p>Equipo experto disponible siempre</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- CARDS SECTION -->
        <h2 class="section-title">Soluciones Especializadas</h2>
        <div class="cards-grid">
            <div class="card">
                <div class="card-header">
                    <i class="fas fa-chart-line card-icon"></i>
                    <h3 class="card-title">Análisis Predictivo</h3>
                </div>
                <div class="card-body">
                    <p class="card-text">Anticipate market trends with our advanced predictive models powered by machine learning algorithms.</p>
                </div>
                <div class="card-footer">
                    <a href="#" class="card-link" onclick="handleCardClick(event, 'predictivo')">
                        Explorar <i class="fas fa-arrow-right"></i>
                    </a>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <i class="fas fa-map card-icon"></i>
                    <h3 class="card-title">Mapeo Geográfico</h3>
                </div>
                <div class="card-body">
                    <p class="card-text">Visualize operational assets and production zones across geographic locations with interactive maps.</p>
                </div>
                <div class="card-footer">
                    <a href="#" class="card-link" onclick="handleCardClick(event, 'geografico')">
                        Explorar <i class="fas fa-arrow-right"></i>
                    </a>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <i class="fas fa-flask card-icon"></i>
                    <h3 class="card-title">Análisis Químico</h3>
                </div>
                <div class="card-body">
                    <p class="card-text">Comprehensive chemical composition analysis and quality control for extracted resources.</p>
                </div>
                <div class="card-footer">
                    <a href="#" class="card-link" onclick="handleCardClick(event, 'quimico')">
                        Explorar <i class="fas fa-arrow-right"></i>
                    </a>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <i class="fas fa-wrench card-icon"></i>
                    <h3 class="card-title">Mantenimiento Predictivo</h3>
                </div>
                <div class="card-body">
                    <p class="card-text">Reduce downtime with predictive maintenance schedules based on equipment performance data.</p>
                </div>
                <div class="card-footer">
                    <a href="#" class="card-link" onclick="handleCardClick(event, 'mantenimiento')">
                        Explorar <i class="fas fa-arrow-right"></i>
                    </a>
                </div>
            </div>
        </div>
    </div>

    <!-- FOOTER -->
    <footer>
        <div class="footer-content">
            <div class="footer-section">
                <h4>Empresa</h4>
                <a href="#">Sobre Nosotros</a>
                <a href="#">Carreras</a>
                <a href="#">Blog</a>
                <a href="#">Prensa</a>
            </div>
            <div class="footer-section">
                <h4>Soluciones</h4>
                <a href="#">Análisis de Datos</a>
                <a href="#">Monitoreo</a>
                <a href="#">Reportes</a>
                <a href="#">Consultoría</a>
            </div>
            <div class="footer-section">
                <h4>Legal</h4>
                <a href="#">Privacidad</a>
                <a href="#">Términos</a>
                <a href="#">Seguridad</a>
                <a href="#">Compliance</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 Oil & Gas Analytics. Todos los derechos reservados.</p>
        </div>
    </footer>

    <script>
        // Efecto ripple en botones
        function handleClick(type) {
            console.log('Botón ' + type + ' clickeado');
            showNotification(type === 'primary' ? 'Análisis iniciado' : 'Mostrando información');
        }

        // Efecto en tarjetas
        function handleCardClick(e, type) {
            e.preventDefault();
            showNotification('Abriendo módulo: ' + type);
        }

        // Animar estadísticas
        function animateStat(element) {
            element.style.transform = 'scale(1.05)';
            setTimeout(() => {
                element.style.transform = 'scale(1)';
            }, 300);
            showNotification('Estadística seleccionada');
        }

        // Notificación flotante
        function showNotification(message) {
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: linear-gradient(135deg, #1a3a52 0%, #2c5aa0 100%);
                color: white;
                padding: 1rem 1.5rem;
                border-radius: 0.5rem;
                box-shadow: 0 4px 15px rgba(26, 58, 82, 0.3);
                animation: slideInRight 0.3s ease-out;
                z-index: 1000;
                font-weight: 600;
            `;
            notification.textContent = message;
            document.body.appendChild(notification);

            setTimeout(() => {
                notification.style.animation = 'slideInRight 0.3s ease-out reverse';
                setTimeout(() => notification.remove(), 300);
            }, 3000);
        }

        // Agregar estilos de animación faltantes
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(100px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
        `;
        document.head.appendChild(style);

        // Efecto parallax en hero
        window.addEventListener('scroll', () => {
            const hero = document.querySelector('.hero');
            if (hero) {
                const scrolled = window.pageYOffset;
                hero.style.backgroundPosition = `0 ${scrolled * 0.5}px`;
            }
        });

        console.log('✨ Dashboard Oil & Gas cargado correctamente');
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stats')
def get_stats():
    return {
        'campos': 150,
        'precision': 85,
        'registros': 2400000,
        'monitoreo': '24/7'
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
