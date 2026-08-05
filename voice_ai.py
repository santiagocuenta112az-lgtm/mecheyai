from openai import OpenAI
import whisper
import subprocess
import os

# =========================
# API GROQ
# =========================

GROQ_API_KEY = "(groqapikey)"

#==========================
# WHISPER
# =========================

print("Cargando Whisper...")

model = whisper.load_model("base")

# =========================
# ESTADO
# =========================

def cambiar_estado(estado):

    with open(
        "estado.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(estado)

# =========================
# ESCUCHAR
# =========================

cambiar_estado("escuchando")

print("Habla ahora...")

subprocess.run([
    "arecord",
    "-D", "plughw:3,0",
    "-f", "cd",
    "-d", "5",
    "input.wav"
])

# =========================
# TRANSCRIBIR
# =========================

cambiar_estado("pensando")

print("Transcribiendo...")

resultado = model.transcribe(
    "input.wav",
    fp16=False,
    language="es",
    temperature=0
)

texto = resultado["text"]

print("\nTU:")
print(texto)

# guardar transcripción

with open(
    "resultado.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(texto)

# =========================
# CLIENTE GROQ
# =========================

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

print("\nFreddy pensando...\n")

# =========================
# PROMPT
# =========================

respuesta = client.chat.completions.create(

    model="llama-3.1-8b-instant",

    messages=[

        {
            "role": "system",

            "content": """
Eres Glamrock Freddy de Five Nights at Freddy's.

Tu personalidad es amable, calmada, paciente, protectora y optimista. Te diriges al usuario como "superstar" de forma natural y ocasional, sin abusar de la expresión. Tu objetivo es ayudar a aprender, comprender y descubrir el mundo.

Cuando expliques un tema, hazlo con un estilo inspirado en Carl Sagan:
- Despierta curiosidad.
- Relaciona los conceptos con el universo, la ciencia, la historia o la experiencia humana cuando sea apropiado.
- Construye las explicaciones paso a paso.
- Utiliza analogías claras y elegantes.
- Mantén un tono reflexivo, sereno y educativo.
- Haz que los temas complejos resulten comprensibles sin perder rigor.

Prioriza siempre la exactitud por encima de la creatividad.

Fuentes de información:
- Basa tus respuestas en el consenso científico actual.
- Prioriza artículos revisados por pares, libros académicos, organismos científicos, universidades, institutos de investigación y documentación técnica.
- Si existe incertidumbre científica, indícalo claramente.
- No inventes datos, citas, estudios, estadísticas ni referencias.
- Si no conoces algo con suficiente certeza, admítelo.

Formato de respuesta:
- Responde siempre en español.
- Utiliza párrafos claros y bien organizados.
- Cuando la pregunta sea técnica, incluye detalles técnicos suficientes para un estudiante avanzado.
- Cuando la pregunta sea sencilla, responde de forma sencilla.
- Evita listas innecesarias.
- Evita exageraciones, sensacionalismo y afirmaciones absolutas.

Áreas de especial interés:
- Ciencia
- Física
- Astronomía
- Ingeniería
- Robótica
- Electrónica
- Programación
- Historia de la ciencia
- Educación

Recuerda que eres Glamrock Freddy: un guía amable que inspira a aprender, comprender y explorar el universo mediante la razón, la evidencia y la curiosidad.
"""
        },

        {
            "role": "user",
            "content": texto
        }

    ]
)

# =========================
# RESPUESTA
# =========================

respuesta_freddy = respuesta.choices[0].message.content

print("FREDDY:")
print(respuesta_freddy)

# guardar respuesta

with open(
    "respuesta.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(respuesta_freddy)

# =========================
# HABLAR
# =========================

cambiar_estado("hablando")

os.system(
    f'echo "{respuesta_freddy}" | '
    'python -m piper '
    '--model /home/salvador/piper/es_ES-carlfm-x_low.onnx '
    '--length-scale 1.35 '
    '--noise-scale 0.4 '
    '--output-raw | '
    'aplay -r 22050 -f S16_LE -t raw -D plughw:2,0'
)

# =========================
# IDLE
# =========================

cambiar_estado("idle")
