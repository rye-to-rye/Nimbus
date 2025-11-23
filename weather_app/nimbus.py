import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from OpenWeatherApi import WeatherInfo
import sip  # required for sip.isdeleted()
from geoCode import GeoInfo

# -------------------------------------------------------------
# Worker thread for background data fetching
# -------------------------------------------------------------
class WeatherWorker(QThread):
    result_ready = pyqtSignal(object)

    def __init__(self, city):
        super().__init__()
        self.city = city

    def run(self):
        try:
            weather = WeatherInfo(self.city)
            self.result_ready.emit(weather)
        except Exception as e:
            print(f"Worker error: {e}")
            self.result_ready.emit(None)


# -------------------------------------------------------------
# Main Window Class
# -------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nimbus")
        self.resize(1000, 950)

        self.create_widgets()
        self.setup_layouts()
        self.set_styles()

    # ---------------------------------------------------------
    # UI Setup
    # ---------------------------------------------------------
    def create_widgets(self):
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setFixedHeight(150)

        # Weather info
        self.temp = QLabel("—°")
        self.humidity = QLabel("Humidity")
        self.description = QLabel("Description")
        self.feels_like = QLabel("Feels like")
        self.wind_speed = QLabel("Wind speed")
        self.weather_header = QLabel("Weather today in city, state, country")

        # Geo info
        self.city = QLabel("City")
        self.state = QLabel("State")
        self.country = QLabel("Country")

        # Search bar + button
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Enter a city...")
        self.submit_button = QPushButton("Search")
        self.submit_button.clicked.connect(self.submit)

        # Make labels centered and adaptive
        for label in [
            self.temp, self.humidity, self.description, self.feels_like,
            self.wind_speed, self.weather_header, self.city, self.state, self.country
        ]:
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            label.setAlignment(Qt.AlignCenter)

    def setup_layouts(self):
        # Top bar
        top_bar = QWidget()
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(0, 30, 0, 30)
        top_layout.setSpacing(15)
        top_layout.addStretch()
        top_layout.addWidget(self.search_box)
        top_layout.addWidget(self.submit_button)
        top_layout.addStretch()

        # Sections
        geo_section = self.make_section([self.city, self.state, self.country])
        temp_section = self.make_section([self.icon_label, self.temp, self.description])
        summary_section = self.make_section([self.weather_header, self.feels_like])
        extra_section = self.make_section([self.wind_speed, self.humidity], horizontal=True)

        # Weather card
        self.weather_card = QWidget()
        self.weather_card.setObjectName("weather_card")
        card_layout = QVBoxLayout(self.weather_card)
        card_layout.setAlignment(Qt.AlignTop)
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(30, 30, 30, 30)
        for s in [geo_section, temp_section, summary_section, extra_section]:
            card_layout.addWidget(s)

        # Central layout
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(40, 20, 40, 40)
        main_layout.setSpacing(25)
        main_layout.addWidget(top_bar)
        main_layout.addWidget(self.weather_card, alignment=Qt.AlignHCenter)
        main_layout.addStretch()

    def make_section(self, widgets, horizontal=False):
        section = QWidget()
        section.setObjectName("section")
        layout = QHBoxLayout(section) if horizontal else QVBoxLayout(section)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        for w in widgets:
            layout.addWidget(w)
        return section

    # ---------------------------------------------------------
    # Styles
    # ---------------------------------------------------------
    def set_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a1c4fd, stop:1 #c2e9fb);
                font-family: 'Segoe UI';
            }

            QLineEdit {
                font-size: 26px;
                padding: 12px 20px;
                border: 2px solid #d0d0d0;
                border-radius: 25px;
                background-color: white;
                color: #333;
                min-width: 400px;
            }

            QLineEdit:focus {
                border: 2px solid #03adfc;
                background-color: #f9f9f9;
            }

            QPushButton {
                font-size: 26px;
                border-radius: 25px;
                border: none;
                color: white;
                background-color: #03adfc;
                padding: 10px 25px;
            }

            QPushButton:hover { background-color: #02c4f8; }
            QPushButton:pressed { background-color: #0288d1; }

            QWidget#weather_card {
                background-color: rgba(255, 255, 255, 200);
                border-radius: 30px;
            }

            QWidget#section {
                background-color: rgba(255, 255, 255, 220);
                border: 1.5px solid #d0e3fa;
                border-radius: 20px;
                padding: 20px;
            }

            QLabel {
                color: #333;
            }
        """)

        self.submit_button.setCursor(QCursor(Qt.PointingHandCursor))

        self.temp.setStyleSheet("font-size: 90px; font-weight: bold; color: #0277bd;")
        self.description.setStyleSheet("font-size: 38px; font-style: italic; color: #555;")
        self.weather_header.setStyleSheet("font-size: 28px;")
        self.feels_like.setStyleSheet("font-size: 28px;")
        self.humidity.setStyleSheet("font-size: 28px;")
        self.wind_speed.setStyleSheet("font-size: 28px;")
        self.city.setStyleSheet("font-size: 32px;")
        self.state.setStyleSheet("font-size: 32px;")
        self.country.setStyleSheet("font-size: 32px;")

    # ---------------------------------------------------------
    # Fetch Weather + Loading Animation
    # ---------------------------------------------------------
    def submit(self):
        
        city_text = self.search_box.text().strip()
        geo = GeoInfo(city_text)
        if not city_text:
            self.show_error("Please enter a city name.")
            return

        self.show_loading(f"Fetching weather for {geo.fetch_city()}...")

        # Threaded API call
        self.worker = WeatherWorker(city_text)
        self.worker.result_ready.connect(self.handle_result)
        self.worker.start()

    def handle_result(self, weather):
        self.hide_loading()

        if not weather or weather.error_message or not weather.weather_json:
            self.show_error(weather.error_message or "Unable to fetch weather data.")
            return

        self.temp.setText(f"{weather.get_temp()}°")
        self.humidity.setText(f"Humidity: {weather.get_humidity()}%")
        self.description.setText(weather.get_description().capitalize())
        self.feels_like.setText(f"Feels like: {weather.get_feels_like()}°")
        self.wind_speed.setText(f"Wind speed: {weather.get_wind_speed()} mph")
        self.weather_header.setText(
            f"Weather today in {weather.city}, {weather.state}, {weather.country}"
        )
        self.city.setText(f"{weather.city},")
        self.state.setText(f"{weather.state},")
        self.country.setText(f"{weather.country}")

        self.icon_label.setText(self.get_weather_icon(weather.get_description()))

    # ---------------------------------------------------------
    # Loading Overlay (with Fade In/Out)
    # ---------------------------------------------------------
    def show_loading(self, message="Loading..."):
        """Display a centered semi-transparent loading overlay safely."""
        # Delete existing overlay if it’s still valid
        try:
            if hasattr(self, "loading_overlay") and self.loading_overlay and not sip.isdeleted(self.loading_overlay):
                self.loading_overlay.deleteLater()
        except Exception:
            pass  # Ignore any stale QWidget errors

        self.loading_overlay = QWidget(self)
        self.loading_overlay.setGeometry(self.rect())
        self.loading_overlay.setStyleSheet("""
            background-color: rgba(255, 255, 255, 200);
            border-radius: 20px;
        """)

        layout = QVBoxLayout(self.loading_overlay)
        layout.setAlignment(Qt.AlignCenter)

        # Create spinner (built-in Qt GIF)
        spinner_label = QLabel()
        spinner_movie = QMovie(":/qt-project.org/styles/commonstyle/images/working.gif")
        spinner_label.setMovie(spinner_movie)
        spinner_movie.start()

        text_label = QLabel(message)
        text_label.setStyleSheet("font-size: 28px; color: #333; font-weight: bold;")

        layout.addWidget(spinner_label)
        layout.addWidget(text_label)

        # Apply fade-in
        self.loading_overlay.setGraphicsEffect(QGraphicsOpacityEffect(self.loading_overlay))
        self.loading_overlay.show()
        self.fade_animation(self.loading_overlay, 0, 1, duration=400)

        self.search_box.setEnabled(False)
        self.submit_button.setEnabled(False)


    def hide_loading(self):
        if hasattr(self, "loading_overlay"):
            self.fade_animation(self.loading_overlay, 1, 0, duration=400, delete=True)
        self.search_box.setEnabled(True)
        self.submit_button.setEnabled(True)
        
    def resizeEvent(self, event):
      super().resizeEvent(event)
      # scale icon size relative to window height
      new_size = max(100, int(self.height() * 0.12))
      self.icon_label.setStyleSheet(f"font-size: {new_size}px; margin: 10px;")


    def fade_animation(self, widget, start, end, duration=300, delete=False):
        """Generic fade animation for widgets"""
        effect = widget.graphicsEffect() or QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity", widget)
        animation.setDuration(duration)
        animation.setStartValue(start)
        animation.setEndValue(end)
        animation.setEasingCurve(QEasingCurve.InOutQuad)

        if delete:
            animation.finished.connect(widget.deleteLater)
        animation.start(QAbstractAnimation.DeleteWhenStopped)

    # ---------------------------------------------------------
    # Error Display
    # ---------------------------------------------------------
    def show_error(self, message):
        self.icon_label.setText("⚠️")
        self.temp.setText("Error")
        self.description.setText(message)
        self.humidity.setText("")
        self.feels_like.setText("")
        self.wind_speed.setText("")
        self.weather_header.setText("")
        self.city.setText("")
        self.state.setText("")
        self.country.setText("")

    # ---------------------------------------------------------
    # Helper
    # ---------------------------------------------------------
    def get_weather_icon(self, desc):
        desc = (desc or "").lower()
        if "clear" in desc or "sun" in desc:
            return "☀️"
        elif "cloud" in desc:
            return "🌤️"
        elif "rain" in desc or "drizzle" in desc:
            return "🌧️"
        elif "thunder" in desc:
            return "⛈️"
        elif "snow" in desc:
            return "❄️"
        elif "mist" in desc or "fog" in desc or "haze" in desc:
            return "🌫️"
        return "🌦️"



def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()




