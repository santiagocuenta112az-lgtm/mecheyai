#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pca = Adafruit_PWMServoDriver(0x40);

// ===== PROTOTIPOS =====
void actualizarParpadeo();
void actualizarOjos();
void iniciarParpadeo();
void moverParpadoL(int pos);
void moverParpadoR(int pos);

// ===== CANALES =====
// párpados
int L_inv = 0;
int L_norm = 1;
int R_inv = 2;
int R_norm = 3;

// ojos (movimiento)
int eye_X_L = 4;
int eye_Y_L = 5;
int eye_X_R = 6;
int eye_Y_R = 7;

// ===== RANGOS =====
int abierto = 300;
int cerrado = 500;

int L_cerrado_inv = 430;
int R_cerrado_inv = 440;

// ojos
int eye_center = 370;
int eye_range = 80;

// ===== TIEMPO =====
unsigned long t_actual;

// parpadeo
bool parpadeando = false;
unsigned long t_parpadeo = 0;
unsigned long siguienteParpadeo = 0;
int fase = 0;
int pos_parpado = 300;

// ojos
unsigned long t_ojos = 0;
int targetX = 370;
int targetY = 370;

void setup() {
  Wire.begin();
  pca.begin();
  pca.setPWMFreq(50);

  randomSeed(analogRead(0));

  siguienteParpadeo = millis() + random(3000, 8000);
}

// ===============================
// LOOP PRINCIPAL
// ===============================
void loop() {

  t_actual = millis();

  actualizarParpadeo();
  actualizarOjos();
}

// ===============================
// PARPADEO NO CONSTANTE
// ===============================
void actualizarParpadeo() {

  if (!parpadeando && t_actual > siguienteParpadeo) {
    iniciarParpadeo();
  }

  if (!parpadeando) return;

  if (t_actual - t_parpadeo < 15) return;
  t_parpadeo = t_actual;

  if (fase == 0) { // cerrar
    pos_parpado += 12;
    if (pos_parpado >= cerrado) {
      pos_parpado = cerrado;
      fase = 1;
    }
  }
  else if (fase == 1) { // pausa
    fase = 2;
  }
  else if (fase == 2) { // abrir
    pos_parpado -= 6;
    if (pos_parpado <= abierto) {
      pos_parpado = abierto;
      parpadeando = false;

      // decidir siguiente parpadeo (NO constante)
      int tipo = random(0, 100);
      if (tipo < 60)
        siguienteParpadeo = t_actual + random(3000, 6000);
      else if (tipo < 85)
        siguienteParpadeo = t_actual + random(1000, 2500);
      else
        siguienteParpadeo = t_actual + random(7000, 12000);
    }
  }

  moverParpadoL(pos_parpado);
  moverParpadoR(pos_parpado);
}

void iniciarParpadeo() {
  parpadeando = true;
  fase = 0;
  pos_parpado = abierto;
}

// ===============================
// MOVIMIENTO DE OJOS (PRIORIDAD)
// ===============================
void actualizarOjos() {

  // actualizar cada 20 ms → mucho más activo que párpados
  if (t_actual - t_ojos < 20) return;
  t_ojos = t_actual;

  // cada cierto tiempo cambiar objetivo
  if (random(0, 100) < 5) {
    targetX = eye_center + random(-eye_range, eye_range);
    targetY = eye_center + random(-eye_range, eye_range);
  }

  // mover suavemente hacia el objetivo
  static int posX = eye_center;
  static int posY = eye_center;

  posX += (targetX - posX) * 0.1;
  posY += (targetY - posY) * 0.1;

  // aplicar a ambos ojos
  pca.setPWM(eye_X_L, 0, posX);
  pca.setPWM(eye_Y_L, 0, posY);

  pca.setPWM(eye_X_R, 0, posX);
  pca.setPWM(eye_Y_R, 0, posY);
}

// ===============================
// PÁRPADOS (IGUAL QUE ANTES)
// ===============================
void moverParpadoL(int pos_norm) {

  pca.setPWM(L_norm, 0, pos_norm);

  int norm_limit = constrain(pos_norm, abierto + 40, cerrado - 30);

  int pos_inv = map(norm_limit,
                    abierto + 40,
                    cerrado - 30,
                    L_cerrado_inv,
                    abierto + 60);

  pca.setPWM(L_inv, 0, pos_inv);
}

void moverParpadoR(int pos_norm) {

  pca.setPWM(R_norm, 0, pos_norm);

  int norm_limit = constrain(pos_norm, abierto + 30, cerrado - 20);

  int pos_inv = map(norm_limit,
                    abierto + 30,
                    cerrado - 20,
                    R_cerrado_inv,
                    abierto + 50);

  pca.setPWM(R_inv, 0, pos_inv);
}