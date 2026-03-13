# ============================================
# CALLIOPE REAKTIONSSPIEL – SPIELER
# Klasse 10 Informatik
# MakeCode Python
# Dieses Programm ist identisch für alle Spieler.
# Die Spieler-ID wird per Tastendruck beim Start gewählt.
# ============================================

# --- Variablen ---
meine_id = 0
id_gesetzt = False
aufgabe = 0
habe_gesendet = False

# --- Initialisierung ---
radio.set_group(1)
# Spieler auffordern, ID zu wählen
basic.show_string("ID?")

# ============================================
# ID-AUSWAHL (vor dem Spielstart)
# A = Spieler 1 | B = Spieler 2
# A+B = Spieler 3 | nochmal A wenn ID=3 → Spieler 4
# ============================================

def on_button_a():
    global meine_id, id_gesetzt, habe_gesendet
    if not id_gesetzt:
        meine_id = 1
        id_gesetzt = True
        basic.show_number(1)
        basic.pause(1000)
        basic.clear_screen()
    elif meine_id == 3:
        # Upgrade: ID 3 → ID 4
        meine_id = 4
        basic.show_number(4)
        basic.pause(1000)
        basic.clear_screen()
    elif aufgabe > 0 and not habe_gesendet:
        # Im Spiel: Aktion 1 (Taste A gedrückt) senden
        habe_gesendet = True
        radio.send_number(meine_id * 10 + 1)
        basic.show_arrow(ArrowNames.NORTH)
        basic.pause(500)
        basic.clear_screen()
input.on_button_pressed(Button.A, on_button_a)


def on_button_b():
    global meine_id, id_gesetzt, habe_gesendet
    if not id_gesetzt:
        meine_id = 2
        id_gesetzt = True
        basic.show_number(2)
        basic.pause(1000)
        basic.clear_screen()
    elif aufgabe > 0 and not habe_gesendet:
        # Im Spiel: Aktion 2 (Taste B gedrückt) senden
        habe_gesendet = True
        radio.send_number(meine_id * 10 + 2)
        basic.show_arrow(ArrowNames.NORTH)
        basic.pause(500)
        basic.clear_screen()
input.on_button_pressed(Button.B, on_button_b)


def on_button_ab():
    global meine_id, id_gesetzt, habe_gesendet
    if not id_gesetzt:
        meine_id = 3
        id_gesetzt = True
        basic.show_number(3)
        basic.pause(1000)
        basic.clear_screen()
    elif aufgabe > 0 and not habe_gesendet:
        # Im Spiel: Aktion 3 (A+B gleichzeitig) senden
        habe_gesendet = True
        radio.send_number(meine_id * 10 + 3)
        basic.show_arrow(ArrowNames.NORTH)
        basic.pause(500)
        basic.clear_screen()
input.on_button_pressed(Button.AB, on_button_ab)

# ============================================
# NEIGUNGSAKTIONEN (Erweiterung aus Kapitel 5)
# Kommentiere diese Blöcke aus, wenn du die
# Basis-Version (nur Tasten) möchtest
# ============================================

def on_forever():
    global habe_gesendet
    if id_gesetzt and aufgabe > 0 and not habe_gesendet:
        x = input.acceleration(Dimension.X)
        if x < -400:
            # Links geneigt → Aktion 4
            habe_gesendet = True
            radio.send_number(meine_id * 10 + 4)
            basic.show_arrow(ArrowNames.WEST)
            basic.pause(500)
            basic.clear_screen()
        elif x > 400:
            # Rechts geneigt → Aktion 5
            habe_gesendet = True
            radio.send_number(meine_id * 10 + 5)
            basic.show_arrow(ArrowNames.EAST)
            basic.pause(500)
            basic.clear_screen()

basic.forever(on_forever)

# ============================================
# FUNK-EMPFANG: Signal vom Spielleiter (Zahl 1-5)
# ============================================

def on_received_number(received_number: int):
    global aufgabe, habe_gesendet
    if not id_gesetzt:
        return
    # Ist es ein gültiger Signal-Code (1-5)?
    if received_number >= 1 and received_number <= 5:
        aufgabe = received_number
        habe_gesendet = False
        signal_anzeigen()
radio.on_received_number(on_received_number)

# ============================================
# FUNK-EMPFANG: Feedback vom Spielleiter (Name+Wert)
# ============================================

def on_received_value(name: str, value: int):
    global aufgabe, habe_gesendet, id_gesetzt
    if not id_gesetzt:
        return

    if name == "gewinner":
        if value == meine_id:
            # Ich habe gewonnen!
            basic.set_led_color(basic.rgb(0, 255, 0))
            basic.show_icon(IconNames.YES)
            music.play_tone(Note.A5, music.beat(BeatFraction.DOUBLE))
            basic.pause(2000)
        else:
            # Jemand anderes hat gewonnen
            basic.set_led_color(basic.rgb(0, 0, 0))
            basic.show_string("S" + str(value))
            basic.pause(2000)
        aufgabe = 0
        basic.set_led_color(basic.rgb(0, 0, 0))
        basic.clear_screen()

    elif name == "falsch":
        if value == meine_id:
            # Ich war falsch!
            basic.set_led_color(basic.rgb(255, 0, 0))
            basic.show_icon(IconNames.NO)
            music.play_tone(Note.A3, music.beat(BeatFraction.WHOLE))
            basic.pause(1500)
            basic.set_led_color(basic.rgb(0, 0, 0))
            basic.clear_screen()

    elif name == "ende":
        # Spielende
        basic.show_string("ENDE!")
        basic.pause(1000)
        if value == meine_id:
            # Ich habe das Gesamtspiel gewonnen!
            basic.set_led_color(basic.rgb(255, 200, 0))
            basic.show_string("WIN!")
            music.begin_melody(music.built_in_melody(Melodies.POWER_UP), MelodyOptions.ONCE)
        else:
            basic.set_led_color(basic.rgb(0, 0, 0))
            basic.show_string("S" + str(value) + " WIN!")
        basic.pause(3000)
        # Zurücksetzen
        basic.set_led_color(basic.rgb(0, 0, 0))
        basic.clear_screen()
        aufgabe = 0
        habe_gesendet = False
        # ID muss neu gewählt werden
        # (optional: ID beibehalten → id_gesetzt = True lassen)
        basic.show_string("ID?")
radio.on_received_value(on_received_value)

# ============================================
# SIGNALANZEIGE (übereinstimmend mit Spielleiter!)
# ============================================

def signal_anzeigen():
    if aufgabe == 1:
        # Grünes Licht + hoher Ton → Taste A
        basic.set_led_color(basic.rgb(0, 255, 0))
        basic.show_leds("""
            # . . . #
            # . . . #
            # # # # #
            # . . . #
            # . . . #
            """)
        music.play_tone(Note.A5, music.beat(BeatFraction.HALF))
    elif aufgabe == 2:
        # Rotes Licht + tiefer Ton → Taste B
        basic.set_led_color(basic.rgb(255, 0, 0))
        basic.show_leds("""
            # # # . .
            # . . # .
            # # # . .
            # . . # .
            # # # . .
            """)
        music.play_tone(Note.A3, music.beat(BeatFraction.HALF))
    elif aufgabe == 3:
        # Blaues Licht + mittlerer Ton → A+B drücken
        basic.set_led_color(basic.rgb(0, 0, 255))
        basic.show_icon(IconNames.HEART)
        music.play_tone(Note.A4, music.beat(BeatFraction.HALF))
    elif aufgabe == 4:
        # Gelbes Licht + tiefer Ton → links neigen
        basic.set_led_color(basic.rgb(255, 200, 0))
        basic.show_arrow(ArrowNames.WEST)
        music.play_tone(Note.A3, music.beat(BeatFraction.HALF))
    elif aufgabe == 5:
        # Orange Licht + hoher Ton → rechts neigen
        basic.set_led_color(basic.rgb(255, 100, 0))
        basic.show_arrow(ArrowNames.EAST)
        music.play_tone(Note.B5, music.beat(BeatFraction.HALF))