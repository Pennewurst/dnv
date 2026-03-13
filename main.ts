/**
 * ============================================
 */
/**
 * CALLIOPE REAKTIONSSPIEL – SPIELER
 */
/**
 * Klasse 10 Informatik
 */
/**
 * MakeCode Python
 */
/**
 * Dieses Programm ist identisch für alle Spieler.
 */
/**
 * Die Spieler-ID wird per Tastendruck beim Start gewählt.
 */
/**
 * ============================================
 */
/**
 * --- Variablen ---
 */
// ============================================
// FUNK-EMPFANG: Signal vom Spielleiter (Zahl 1-5)
// ============================================
radio.onReceivedNumber(function (received_number) {
    if (!(id_gesetzt)) {
        return
    }
    // Ist es ein gültiger Signal-Code (1-5)?
    if (received_number >= 1 && received_number <= 5) {
        aufgabe = received_number
        habe_gesendet = false
        signal_anzeigen()
    }
})
// ============================================
// ID-AUSWAHL (vor dem Spielstart)
// A = Spieler 1 | B = Spieler 2
// A+B = Spieler 3 | nochmal A wenn ID=3 → Spieler 4
// ============================================
input.onButtonPressed(Button.A, function () {
    if (!(id_gesetzt)) {
        meine_id = 1
        id_gesetzt = true
        basic.showNumber(1)
        basic.pause(1000)
        basic.clearScreen()
    } else if (meine_id == 3) {
        // Upgrade: ID 3 → ID 4
        meine_id = 4
        basic.showNumber(4)
        basic.pause(1000)
        basic.clearScreen()
    } else if (aufgabe > 0 && !(habe_gesendet)) {
        // Im Spiel: Aktion 1 (Taste A gedrückt) senden
        habe_gesendet = true
        radio.sendNumber(meine_id * 10 + 1)
        basic.showArrow(ArrowNames.North)
        basic.pause(500)
        basic.clearScreen()
    }
})
input.onButtonPressed(Button.AB, function () {
    if (!(id_gesetzt)) {
        meine_id = 3
        id_gesetzt = true
        basic.showNumber(3)
        basic.pause(1000)
        basic.clearScreen()
    } else if (aufgabe > 0 && !(habe_gesendet)) {
        // Im Spiel: Aktion 3 (A+B gleichzeitig) senden
        habe_gesendet = true
        radio.sendNumber(meine_id * 10 + 3)
        basic.showArrow(ArrowNames.North)
        basic.pause(500)
        basic.clearScreen()
    }
})
input.onButtonPressed(Button.B, function () {
    if (!(id_gesetzt)) {
        meine_id = 2
        id_gesetzt = true
        basic.showNumber(2)
        basic.pause(1000)
        basic.clearScreen()
    } else if (aufgabe > 0 && !(habe_gesendet)) {
        // Im Spiel: Aktion 2 (Taste B gedrückt) senden
        habe_gesendet = true
        radio.sendNumber(meine_id * 10 + 2)
        basic.showArrow(ArrowNames.North)
        basic.pause(500)
        basic.clearScreen()
    }
})
// ============================================
// FUNK-EMPFANG: Feedback vom Spielleiter (Name+Wert)
// ============================================
radio.onReceivedValue(function (name, value) {
    if (!(id_gesetzt)) {
        return
    }
    if (name == "gewinner") {
        if (value == meine_id) {
            // Ich habe gewonnen!
            basic.setLedColor(basic.rgb(0, 255, 0))
            basic.showIcon(IconNames.Yes)
            music.playTone(880, music.beat(BeatFraction.Double))
            basic.pause(2000)
        } else {
            // Jemand anderes hat gewonnen
            basic.setLedColor(basic.rgb(0, 0, 0))
            basic.showString("S" + ("" + value))
            basic.pause(2000)
        }
        aufgabe = 0
        basic.setLedColor(basic.rgb(0, 0, 0))
        basic.clearScreen()
    } else if (name == "falsch") {
        if (value == meine_id) {
            // Ich war falsch!
            basic.setLedColor(basic.rgb(255, 0, 0))
            basic.showIcon(IconNames.No)
            music.playTone(220, music.beat(BeatFraction.Whole))
            basic.pause(1500)
            basic.setLedColor(basic.rgb(0, 0, 0))
            basic.clearScreen()
        }
    } else if (name == "ende") {
        // Spielende
        basic.showString("ENDE!")
        basic.pause(1000)
        if (value == meine_id) {
            // Ich habe das Gesamtspiel gewonnen!
            basic.setLedColor(basic.rgb(255, 200, 0))
            basic.showString("WIN!")
            music.beginMelody(music.builtInMelody(Melodies.PowerUp), MelodyOptions.Once)
        } else {
            basic.setLedColor(basic.rgb(0, 0, 0))
            basic.showString("S" + ("" + value) + " WIN!")
        }
        basic.pause(3000)
        // Zurücksetzen
        basic.setLedColor(basic.rgb(0, 0, 0))
        basic.clearScreen()
        aufgabe = 0
        habe_gesendet = false
        // ID muss neu gewählt werden
        // (optional: ID beibehalten → id_gesetzt = True lassen)
        basic.showString("ID?")
    }
})
// ============================================
// SIGNALANZEIGE (übereinstimmend mit Spielleiter!)
// ============================================
function signal_anzeigen () {
    if (aufgabe == 1) {
        // Grünes Licht + hoher Ton → Taste A
        basic.setLedColor(basic.rgb(0, 255, 0))
        basic.showLeds(`
            . . # . .
            . # . # .
            . # # # .
            . # . # .
            . . . . .
            `)
        music.playTone(880, music.beat(BeatFraction.Half))
    } else if (aufgabe == 2) {
        // Rotes Licht + tiefer Ton → Taste B
        basic.setLedColor(basic.rgb(255, 0, 0))
        basic.showLeds(`
            # # # . .
            # . . # .
            # # # . .
            # . . # .
            # # # . .
            `)
        music.playTone(220, music.beat(BeatFraction.Half))
    } else if (aufgabe == 3) {
        // Blaues Licht + mittlerer Ton → A+B drücken
        basic.setLedColor(basic.rgb(0, 0, 255))
        basic.showIcon(IconNames.Heart)
        music.playTone(440, music.beat(BeatFraction.Half))
    } else if (aufgabe == 4) {
        // Gelbes Licht + tiefer Ton → links neigen
        basic.setLedColor(basic.rgb(255, 200, 0))
        basic.showArrow(ArrowNames.West)
        music.playTone(220, music.beat(BeatFraction.Half))
    } else if (aufgabe == 5) {
        // Orange Licht + hoher Ton → rechts neigen
        basic.setLedColor(basic.rgb(255, 100, 0))
        basic.showArrow(ArrowNames.East)
        music.playTone(988, music.beat(BeatFraction.Half))
    }
}
let meine_id = 0
let habe_gesendet = false
let aufgabe = 0
let id_gesetzt = false
// --- Initialisierung ---
radio.setGroup(1)
// Spieler auffordern, ID zu wählen
basic.showString("ID?")
// ============================================
// NEIGUNGSAKTIONEN (Erweiterung aus Kapitel 5)
// Kommentiere diese Blöcke aus, wenn du die
// Basis-Version (nur Tasten) möchtest
// ============================================
basic.forever(function () {
    let x: number;
if (id_gesetzt && aufgabe > 0 && !(habe_gesendet)) {
        x = input.acceleration(Dimension.X)
        if (x < -400) {
            // Links geneigt → Aktion 4
            habe_gesendet = true
            radio.sendNumber(meine_id * 10 + 4)
            basic.showArrow(ArrowNames.West)
            basic.pause(500)
            basic.clearScreen()
        } else if (x > 400) {
            // Rechts geneigt → Aktion 5
            habe_gesendet = true
            radio.sendNumber(meine_id * 10 + 5)
            basic.showArrow(ArrowNames.East)
            basic.pause(500)
            basic.clearScreen()
        }
    }
})
